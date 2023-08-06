import abc

from nsj_queue_lib.main_thread import MainThread
from nsj_queue_lib.retry_thread import RetryThread
from nsj_queue_lib.purge_thread import PurgeThread
from nsj_queue_lib.notify_thread import NotifyThread

from nsj_queue_lib.settings import logger


class WorkerBase(abc.ABC):
    def run(self):
        logger.info("Iniciando worker...")

        # Iniciando thread de retry
        retry_thread = RetryThread()
        retry_thread.start()

        # Iniciando thread de purge
        purge_thread = PurgeThread()
        purge_thread.start()

        # Iniciando thread de notify
        notify_thread = NotifyThread()
        notify_thread.start()

        # Iniciando thread principal
        main_thread = MainThread(self)
        main_thread.run()

    @abc.abstractmethod
    def execute(self, tarefa: dict[str, any], bd_conn):
        pass
