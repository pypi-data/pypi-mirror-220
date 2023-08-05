from abc import ABC
from concurrent.futures import Executor as FutureExecutor, Future
from queue import Queue

from pympipool.external_interfaces.thread import RaisingThread
from pympipool.shared_functions.external_interfaces import (
    execute_parallel_tasks,
    execute_serial_tasks,
    cloudpickle_register,
    cancel_items_in_queue,
)


class ExecutorBase(FutureExecutor, ABC):
    """
    Base class for the Executor and PoolExecutor class defined below. The ExecutorBase class is not intended to be used
    alone. Rather it implements the submit(), shutdown() and __len__() function shared between the derived classes.
    """

    def __init__(self):
        self._future_queue = Queue()
        self._process = None
        cloudpickle_register(ind=3)

    def submit(self, fn, *args, **kwargs):
        """Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and returns
        a Future instance representing the execution of the callable.

        Returns:
            A Future representing the given call.
        """
        f = Future()
        self._future_queue.put({"fn": fn, "args": args, "kwargs": kwargs, "future": f})
        return f

    def shutdown(self, wait=True, *, cancel_futures=False):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by the
                parallel_executors have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        """
        if cancel_futures:
            cancel_items_in_queue(que=self._future_queue)
        self._future_queue.put({"shutdown": True, "wait": wait})
        self._process.join()

    def __len__(self):
        return self._future_queue.qsize()


class Executor(ExecutorBase):
    """
    The pympipool.Executor behaves like the concurrent.futures.Executor but it uses mpi4py to execute parallel tasks.
    In contrast to the mpi4py.futures.MPIPoolExecutor the pympipool.Executor can be executed in a serial python process
    and does not require the python script to be executed with MPI. Still internally the pympipool.Executor uses the
    mpi4py.futures.MPIPoolExecutor, consequently it is primarily an abstraction of its functionality to improve the
    usability in particular when used in combination with Jupyter notebooks.

    Args:
        cores (int): defines the number of MPI ranks to use for each function call
        oversubscribe (bool): adds the `--oversubscribe` command line flag (OpenMPI only) - default False
        enable_flux_backend (bool): use the flux-framework as backend rather than just calling mpiexec
        enable_slurm_backend (bool): enable the SLURM queueing system as backend - defaults to False
        init_function (None): optional function to preset arguments for functions which are submitted later
        cwd (str/None): current working directory where the parallel python task is executed
        queue_adapter (pysqa.queueadapter.QueueAdapter): generalized interface to various queuing systems
        queue_adapter_kwargs (dict/None): keyword arguments for the submit_job() function of the queue adapter

    Simple example:
        ```
        import numpy as np
        from pympipool import Executor

        def calc(i, j, k):
            from mpi4py import MPI
            size = MPI.COMM_WORLD.Get_size()
            rank = MPI.COMM_WORLD.Get_rank()
            return np.array([i, j, k]), size, rank

        def init_k():
            return {"k": 3}

        with Executor(cores=2, init_function=init_k) as p:
            fs = p.submit(calc, 2, j=4)
            print(fs.result())

        >>> [(array([2, 4, 3]), 2, 0), (array([2, 4, 3]), 2, 1)]
        ```
    """

    def __init__(
        self,
        cores,
        oversubscribe=False,
        enable_flux_backend=False,
        enable_slurm_backend=False,
        init_function=None,
        cwd=None,
        queue_adapter=None,
        queue_adapter_kwargs=None,
    ):
        super().__init__()
        self._process = RaisingThread(
            target=execute_parallel_tasks,
            kwargs={
                "future_queue": self._future_queue,
                "cores": cores,
                "oversubscribe": oversubscribe,
                "enable_flux_backend": enable_flux_backend,
                "enable_slurm_backend": enable_slurm_backend,
                "cwd": cwd,
                "queue_adapter": queue_adapter,
                "queue_adapter_kwargs": queue_adapter_kwargs,
            },
        )
        self._process.start()
        if init_function is not None:
            self._future_queue.put(
                {"init": True, "fn": init_function, "args": (), "kwargs": {}}
            )


class PoolExecutor(ExecutorBase):
    """
    To combine the functionality of the pympipool.Pool and the pympipool.Executor the pympipool.PoolExecutor again
    connects to the mpi4py.futures.MPIPoolExecutor. Still in contrast to the pympipool.Pool it does not implement the
    map() and starmap() functions but rather the submit() function based on the concurrent.futures.Executor interface.
    In this case the load balancing happens internally and the maximum number of workers max_workers defines the maximum
    number of parallel tasks. But only serial python tasks can be executed in contrast to the pympipool.Executor which
    can also execute MPI parallel python tasks.

    Args:
        max_workers (int): defines the total number of MPI ranks to use
        oversubscribe (bool): adds the `--oversubscribe` command line flag (OpenMPI only) - default False
        enable_flux_backend (bool): use the flux-framework as backend rather than just calling mpiexec
        enable_slurm_backend (bool): enable the SLURM queueing system as backend - defaults to False
        cwd (str/None): current working directory where the parallel python task is executed
        sleep_interval (float):
        queue_adapter (pysqa.queueadapter.QueueAdapter): generalized interface to various queuing systems
        queue_adapter_kwargs (dict/None): keyword arguments for the submit_job() function of the queue adapter

    Simple example:
        ```
        from pympipool import PoolExecutor

        def calc(i, j):
            return i + j

        with PoolExecutor(max_workers=2) as p:
            fs1 = p.submit(calc, 1, 2)
            fs2 = p.submit(calc, 3, 4)
            fs3 = p.submit(calc, 5, 6)
            fs4 = p.submit(calc, 7, 8)
            print(fs1.result(), fs2.result(), fs3.result(), fs4.result()
        ```
    """

    def __init__(
        self,
        max_workers=1,
        oversubscribe=False,
        enable_flux_backend=False,
        enable_slurm_backend=False,
        cwd=None,
        sleep_interval=0.1,
        queue_adapter=None,
        queue_adapter_kwargs=None,
    ):
        super().__init__()
        self._process = RaisingThread(
            target=execute_serial_tasks,
            kwargs={
                "future_queue": self._future_queue,
                "cores": max_workers,
                "oversubscribe": oversubscribe,
                "enable_flux_backend": enable_flux_backend,
                "enable_slurm_backend": enable_slurm_backend,
                "cwd": cwd,
                "sleep_interval": sleep_interval,
                "queue_adapter": queue_adapter,
                "queue_adapter_kwargs": queue_adapter_kwargs,
            },
        )
        self._process.start()
