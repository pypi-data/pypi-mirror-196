import asyncio
import importlib
import logging
import os
import subprocess
import sys
import tempfile
import typing
import zipfile
from contextlib import AbstractContextManager
from pathlib import Path
from types import TracebackType, ModuleType
from typing import Type

import botocore.exceptions
import dask
import dask_cloudprovider.aws.ecs
import dask_cloudprovider.aws.ecs as ecs
import git
import requests
from dask.distributed import Client
from dask.distributed import PipInstall
from dask_cloudprovider.aws import FargateCluster
from dask_cloudprovider.aws.helper import (
    dict_to_aws,
)
from distributed.core import Status
from git import Repo


class DistRunner(AbstractContextManager):
    """
    Context manager for running distributed tasks.
    """

    GIT_FILE = (
        "https://gitlab.com/crossref/labs/distrunner/-/"
        "raw/main/binary/git?inline=false"
    )
    GIT_CORE = (
        "https://gitlab.com/crossref/labs/distrunner/-/"
        "raw/main/binary/git-core.zip?inline=false"
    )

    def __exit__(
        self,
        __exc_type: Type[BaseException] | None,
        __exc_value: BaseException | None,
        __traceback: TracebackType | None,
    ) -> bool | None:
        """
        Closes the dask cluster and client
        :param __exc_type: an exception type
        :param __exc_value: an exception value
        :param __traceback: the traceback
        :return: Bool if successful or None
        """
        self._temp_dir.cleanup()

        if self._dask_cluster:
            self._dask_cluster.close()

        if __exc_value:
            logging.error(__exc_value)
            logging.error(__traceback)
            raise __exc_value

        return True

    def __init__(
        self,
        workers: int = 3,
        python_version: str = "3.10",
        requirements_file: str = "requirements.txt",
        repo: str = "",
        entry_module: str = "",
        entry_point: str = "",
        local: bool = True,
        retries: int = 3,
        worker_memory: int = 16384,  # memory in MB
        worker_cpus: int = 4096,  # CPU in milli-cpu (1/1024)
        verbose_workers: bool = False,
        git_binary: str | None = None,
        git_exec_path: str | None = None,
    ):
        """
        Initialize a Dask cluster with the specified number of workers.
        :param workers: the number of workers required
        :param python_version: the python version to use
        :param requirements_file: a requirements.txt file to install
        :param repo: the git repository to use for bootstrapping
        :param entry_point: the entry point to use for bootstrapping
        :param entry_module: the entry module to use for bootstrapping
        :param local: whether to run the cluster locally or on AWS Fargate
        :param retries: the number of times to retry bootstrapping the cluster
        :param worker_memory: the memory in MB to use for workers
        :param worker_cpus: the CPU in milli-cpu (1/1024) to use for workers
        :param verbose_workers: whether to log to the console
        :param git_binary: the path to the git binary or None to use the default
        :param git_exec_path: the path to the git executable or None to use the default
        """
        super().__init__()
        self._workers = workers
        self._python_version = python_version
        self._requirements_file = requirements_file
        self._repo = repo
        self._entry_point = entry_point
        self._entry_module = entry_module
        self._dask_cluster = None
        self._dask_client = None
        self._local = local
        self._retries = retries
        self._worker_memory = worker_memory
        self._worker_cpus = worker_cpus
        self._verbose_workers = verbose_workers
        self._git_binary = git_binary
        self._git_exec_path = git_exec_path

        # horrible monkey patching for Dask AWS 2022.10.0
        # these overrides fix Dask's horrible Weakref finalizer bugs
        # silencing command-line errors while still gracefully shutting down
        ecs.ECSCluster._create_worker_task_definition_arn = (
            PatchECS._create_worker_task_definition_arn
        )
        ecs.ECSCluster._delete_scheduler_task_definition_arn = (
            PatchECS._delete_scheduler_task_definition_arn
        )
        ecs.ECSCluster._delete_role = PatchECS._delete_role
        ecs.ECSCluster._delete_cluster = PatchECS._delete_cluster
        ecs.Task.close = PatchTask.close

        # create the temporary storage directory
        self._temp_dir = tempfile.TemporaryDirectory()

    @staticmethod
    def bootstrap_git_to_aws(
        git_file: str,
        git_core_file: str,
        working_directory: Path,
        reset_git: bool = False,
    ) -> str:
        """
        Bootstrap an AWS environment with git. Useful for MWAA
        :param git_file: URL of a precompiled git binary
        :param git_core_file: URL of precompiled and zipped git core binaries
        :param working_directory: pathlib.Path of the working directory
        :param reset_git: whether to set GitPython to use the new binary
        :return: the absolute path to the git binary
        """
        logging.info(f"Bootstrapping git...")
        git_path = str((working_directory / "git").absolute())
        git_core_path = str((working_directory / "git-core.zip").absolute())

        # get the Git binary compiled for Amazon
        # Linux-4.14.301-224.520.amzn2.x86_64-x86_64-with-glibc2.26
        DistRunner._download_file(git_file, git_path)

        logging.info(f"Applying execute permissions to git")
        os.chmod(git_path, 0o755)

        logging.info(f"Downloading git-core")
        DistRunner._download_file(git_core_file, git_core_path)

        logging.info(f"Decompressing git-core")
        DistRunner._decompress_zip(git_core_path, str(working_directory))

        if reset_git:
            logging.info("Reloading GitPython configuration")
            git.refresh(path=git_path)
            os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = git_path

        return git_path

    @staticmethod
    def _decompress_zip(zip_file: str, path: str) -> None:
        """
        Decompress a zip file to path
        :param zip_file: the zip file to decompress
        :param path: the output path
        :return: None
        """
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(path)

    @staticmethod
    def _download_file(url: str, path: str) -> None:
        """
        Download a file and save it in path
        :param url: the URL
        :param path: the output path
        :return: None
        """
        logging.info(f"Downloading {url} to {path}")

        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, "wb") as f:
                for chunk in r:
                    f.write(chunk)

    def start_cluster(self) -> None:
        """
        Start the Dask cluster
        :return: None
        """
        # initialize a dask cluster
        # NB: there is a bug with the AWS EC2 Provider that blocks us from
        # using it. See: https://github.com/dask/dask-cloudprovider/issues/249
        # so we use the FargateCluster instead
        if not self._local:
            logging.info("Starting remote cluster")
            self._dask_cluster = FargateCluster(
                **{
                    "n_workers": self._workers,
                    "image": f"daskdev/dask:latest-py{self._python_version}",
                    "worker_mem": self._worker_memory,
                    "worker_cpu": self._worker_cpus,
                }
            )

            # scale to the appropriate number of workers
            self._dask_cluster.scale(self._workers)
        else:
            logging.info("Starting local cluster")
            self._dask_cluster = dask.distributed.LocalCluster(
                n_workers=self._workers
            )

        # register the client
        logging.info("Starting client")
        self._dask_client = Client(self._dask_cluster)

    @staticmethod
    def _setup_system_path(path: tuple[Path | str]) -> list[str]:
        """
        Append a path to the system path
        :param path: a tuple of Path or str
        :return: the current system path
        """
        sys.path.append(str(path[0]))
        return sys.path

    @staticmethod
    def _import_lib(library: tuple) -> ModuleType | None:
        """
        Import a library by name
        :param library: a tuple containing the name of the library to import
        and a boolean indicating whether to return the imported module
        :return: the imported module
        """
        i = importlib.import_module(library[0])

        # note: we check here that the call requests a return because a module
        # can't be serialized in a distributed context
        if library[1]:
            return i

    def bootstrap_repo(self) -> ModuleType:
        """
        Bootstrap the environments
        :return: the imported entry module
        """

        temporary_directory = self._temp_dir.name

        logging.info("Bootstrapping environments")

        # install Git Python on all workers
        logging.info(
            "Installing distrunner and GitPython requirement on workers"
        )
        self._install_requirements(
            client=self._dask_client, requirements=["distrunner", "GitPython"]
        )
        self.process_worker_logs(verbose=self._verbose_workers)

        # we use the same location on every worker because if it's a local
        # set of workers, they can pool it
        logging.info("Pulling repository to workers")
        self._process_worker_retries(
            func=self._pull_git, arguments=(self._repo, temporary_directory)
        )
        self.process_worker_logs(verbose=self._verbose_workers)

        final_path = Path(temporary_directory) / "repo"
        logging.info(f"Using {final_path} as clone destination")

        # use the user-provided git binary if needed
        if self._git_binary:
            logging.info(f"Setting git binary to {self._git_binary}")
            os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = str(
                Path(self._git_binary).absolute()
            )
            git.refresh(path=str(Path(self._git_binary).absolute()))

        if self._git_exec_path:
            os.environ["GIT_EXEC_PATH"] = str(self._git_exec_path)
            sys.path.append(str(self._git_exec_path))

        # install dependencies to all workers
        # involves pulling down the repo to the Airflow task launcher
        # reading the requirements.txt and installing the dependencies
        logging.info("Gathering requirements for workers")
        requirements_list = self._gather_requirements(
            repo=self._repo,
            temporary_directory=temporary_directory,
            requirements_file=self._requirements_file,
        )

        logging.info("Installing requirements into workers")
        self._install_requirements(
            client=self.client, requirements=requirements_list
        )
        self.process_worker_logs(verbose=self._verbose_workers)

        # install the requirements into the Airflow environment
        logging.info("Installing requirements into Airflow")
        repo_path = Path(temporary_directory / Path("repo"))

        self._install_requirements_local(
            requirements_file=Path(repo_path / Path(self._requirements_file))
        )

        # import the entry point in the Airflow scheduler
        # this has to be done before we do it on the workers
        # because otherwise we can't deserialize the result
        logging.info("Importing entry module into Airflow")
        self._setup_system_path((repo_path,))
        i = self._import_lib((self._entry_module, True))

        # set up the environment on the workers
        logging.info("Setting up system path on workers")
        self._process_worker_retries(self._setup_system_path, (final_path,))
        self.process_worker_logs(verbose=self._verbose_workers)

        logging.info("Importing entry module into workers")
        self._process_worker_retries(
            self._import_lib, (self._entry_module, False)
        )
        self.process_worker_logs(verbose=self._verbose_workers)

        logging.info("Finishing bootstrap")
        return i

    @property
    def client(self) -> Client:
        """
        The dask client object.
        :return: a dask Client
        """
        return self._dask_client

    @staticmethod
    def _pull_git(repo_and_path: tuple[str, str]) -> str:
        """
        Pull a git repository to the local environment
        :param repo_and_path: a 2-tuple containing the git repository and the
        path to the directory
        :return: the temporary directory
        """
        temp_dir = repo_and_path[1]

        repo_path = Path(temp_dir) / Path("repo")

        if not repo_path.exists():
            Path.mkdir(repo_path, parents=True)
            Repo.clone_from(repo_and_path[0], repo_path)

        return temp_dir

    @staticmethod
    def _gather_requirements(
        repo,
        temporary_directory: str,
        requirements_file: str,
    ) -> list[str]:
        """
        Read a requirements.txt file and install it on the Dask cluster.
        :param repo: the remote repository
        :param temporary_directory: the temporary directory to use
        :return: None
        """
        # Clone into temporary dir
        repo_path = Path(temporary_directory) / "repo"

        if not repo_path.exists():
            Repo.clone_from(repo, repo_path, depth=1)

        return DistRunner._read_file_lines(repo_path / requirements_file)

    @staticmethod
    def _install_requirements_local(requirements_file) -> None:
        """
        Install requirements in the Airflow environment.
        :param requirements_file: the requirements.txt file to install
        :return: None
        """
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-input",
                "-r",
                str(requirements_file),
            ]
        )

    @staticmethod
    def _install_requirements(client: Client, requirements: list[str]) -> None:
        """
        Install requirements on the Dask cluster workers and scheduler
        :param client: the client
        :param requirements: a list of requirements to install
        :return: None
        """
        plugin = PipInstall(packages=requirements, pip_options=["--upgrade"])
        client.register_worker_plugin(plugin)

    @staticmethod
    def _read_file_lines(fn: Path) -> list[str]:
        """
        Read a file and return a list of lines.
        :param fn: the filename to read
        :return: a list of lines
        """
        with fn.open("r") as f:
            return f.readlines()

    def handover(self, imported_module: ModuleType) -> bool | None:
        """
        Hand over execution to the entry point
        :param imported_module: the imported entry module
        :return: None
        """
        logging.info("Locating entry point")
        entry_point = getattr(imported_module, self._entry_point)
        logging.info(f"Handing over to {entry_point} in {self._entry_module}")
        return entry_point(self)

    def process_worker_logs(self, verbose: bool = False) -> dict:
        """
        Process the logs from the workers
        :param verbose: a boolean indicating whether to print the logs
        :return: None
        """
        logging.info("Processing logs from workers")
        logs = self.client.get_worker_logs()

        if verbose:
            for key, val in logs.items():
                for log_entry in val:
                    logging.info(f"[Worker {key}]: {log_entry}")

        return logs

    def run(self) -> None:
        """
        Start the cluster, boostrap the environment, and hand over execution
        :return: None
        """
        # start the Dask cluster
        self.start_cluster()

        # bootstrap the environments and pull down the Git repo
        imported_module = self.bootstrap_repo()

        # hand over execution to the entry point
        self.handover(imported_module)

    def _process_worker_retries(
        self, func: typing.Callable, arguments: tuple, attempt: int = 0
    ) -> dict:
        """
        Run a function on the Dask cluster and retry if it fails
        :param func: the function to run
        :param arguments: the tuple of arguments to pass to the function
        :param attempt: the current attempt number
        :return: the results of the function
        """
        arguments = arguments + (attempt,)
        results = self._dask_client.run(func, arguments, on_error="return")

        for worker, item in results.items():
            if isinstance(item, Exception):
                if attempt >= self._retries:
                    logging.error("Failed to bootstrap the environment")
                    raise item
                else:
                    attempt += 1
                    logging.warning(
                        f"Failed to bootstrap the environment, "
                        f"retrying (attempt {attempt})"
                    )
                    return self._process_worker_retries(
                        func, arguments, attempt
                    )

        return results


"""
These classes re-implement some of the code from Dask AWS 2022.10.0
We then monkey patch them to the main classes to suppress errors in the Weakref
finalizers. For this reason, we need to stay on Dask 2022.10.0 unless they fix
this bug upstream.
"""


class PatchECS(dask_cloudprovider.aws.FargateCluster):
    async def _delete_cluster(self):
        try:
            async with self._client("ecs") as ecs:
                async for page in ecs.get_paginator("list_tasks").paginate(
                    cluster=self.cluster_arn, desiredStatus="RUNNING"
                ):
                    for task in page["taskArns"]:
                        await ecs.stop_task(cluster=self.cluster_arn, task=task)
                await ecs.delete_cluster(cluster=self.cluster_arn)
        except botocore.exceptions.HTTPClientError:
            pass

    async def _delete_role(self, role):
        try:
            async with self._client("iam") as iam:
                attached_policies = (
                    await iam.list_attached_role_policies(RoleName=role)
                )["AttachedPolicies"]
                for policy in attached_policies:
                    await iam.detach_role_policy(
                        RoleName=role, PolicyArn=policy["PolicyArn"]
                    )
                await iam.delete_role(RoleName=role)
        except botocore.exceptions.HTTPClientError:
            pass

    async def _delete_scheduler_task_definition_arn(self):
        if not self._scheduler_task_definition_arn_provided:
            async with self._client("ecs") as ecs:
                try:
                    await ecs.deregister_task_definition(
                        taskDefinition=self.scheduler_task_definition_arn
                    )
                except botocore.exceptions.HTTPClientError:
                    pass

    async def _create_worker_task_definition_arn(self):
        resource_requirements = []
        if self._worker_gpu:
            resource_requirements.append(
                {"type": "GPU", "value": str(self._worker_gpu)}
            )
        async with self._client("ecs") as ecs:
            response = await ecs.register_task_definition(
                family="{}-{}".format(self.cluster_name, "worker"),
                taskRoleArn=self._task_role_arn,
                executionRoleArn=self._execution_role_arn,
                networkMode="awsvpc",
                containerDefinitions=[
                    {
                        "name": "dask-worker",
                        "image": self.image,
                        "cpu": self._worker_cpu,
                        "memory": self._worker_mem,
                        "memoryReservation": self._worker_mem,
                        "resourceRequirements": resource_requirements,
                        "essential": True,
                        "command": [
                            "dask-cuda-worker"
                            if self._worker_gpu
                            else "dask-worker",
                            "--nthreads",
                            "{}".format(
                                max(int(self._worker_cpu / 1024), 1)
                                if self._worker_nthreads is None
                                else self._worker_nthreads
                            ),
                            "--memory-limit",
                            "{}MB".format(int(self._worker_mem)),
                            "--death-timeout",
                            "60",
                        ]
                        + (
                            list()
                            if not self._worker_extra_args
                            else self._worker_extra_args
                        ),
                        "ulimits": [
                            {
                                "name": "nofile",
                                "softLimit": 65535,
                                "hardLimit": 65535,
                            },
                        ],
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-region": ecs.meta.region_name,
                                "awslogs-group": self.cloudwatch_logs_group,
                                "awslogs-stream-prefix": self._cloudwatch_logs_stream_prefix,
                                "awslogs-create-group": "true",
                            },
                        },
                        "mountPoints": self._mount_points
                        if self._mount_points
                        else [],
                    }
                ],
                volumes=self._volumes if self._volumes else [],
                requiresCompatibilities=["FARGATE"]
                if self._fargate_workers
                else [],
                cpu=str(self._worker_cpu),
                memory=str(self._worker_mem),
                tags=dict_to_aws(self.tags),
            )
        return response["taskDefinition"]["taskDefinitionArn"]


class PatchTask(dask_cloudprovider.aws.ecs.Task):
    async def close(self, **kwargs):
        if self.task and self.status != Status.closed:
            try:
                async with self._client("ecs") as ecs:
                    await ecs.stop_task(
                        cluster=self.cluster_arn, task=self.task_arn
                    )
                await self._update_task()
                while self.task["lastStatus"] in ["RUNNING"]:
                    await asyncio.sleep(1)
                    await self._update_task()
            except botocore.exceptions.HTTPClientError:
                pass
        self.status = Status.closed
