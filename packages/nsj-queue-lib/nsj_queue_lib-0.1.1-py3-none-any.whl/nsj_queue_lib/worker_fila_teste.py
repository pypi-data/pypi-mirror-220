from nsj_queue_lib.worker_base import WorkerBase

# from settings import logger


class WorkerFilaTeste(WorkerBase):
    def execute(self, tarefa: dict[str, any], bd_conn):
        print(tarefa)


if __name__ == "__main__":
    WorkerFilaTeste().run()
