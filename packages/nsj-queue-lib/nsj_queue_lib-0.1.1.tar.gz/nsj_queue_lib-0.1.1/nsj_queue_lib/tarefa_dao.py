import datetime

from nsj_sql_utils_lib import dao_util

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_queue_lib.exception import NotFoundException
from nsj_queue_lib.settings import QUEUE_TABLE


class TarefaDAO:
    COLUNAS = [
        "id",
        "id_inicial",
        "data_hora_inicial",
        "data_hora",
        "origem",
        "destino",
        "processo",
        "chave_externa",
        "proxima_tentativa",
        "tentativa",
        "status",
        "mensagem",
        "id_anterior",
        "data_hora_anterior",
        "status_anterior",
        "mensagem_anterior",
        "tenant",
        "grupo_empresarial",
    ]
    COLUNAS_STR = "tarefa." + ", tarefa.".join(COLUNAS)

    def __init__(self, db: DBAdapter3):
        self.db = db

    def get(self, id: int):
        """
        Recupera uma tarefa, por meio de seu ID
        """
        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR},
                coalesce(tarefa.payload, inicial.payload) as payload
            from
                {QUEUE_TABLE} as tarefa
                left join {QUEUE_TABLE} as inicial
                on (tarefa.id_inicial = inicial.id)
            where
                tarefa.id = %(id)s
        """
        result, count = self.db.execute(sql, id=id)

        if count != 1:
            raise NotFoundException("Não encontrada tarefa com ID {id}")

        return result[0]

    # def get_recuperacao_falhas(self, max_retries: int):
    #     """
    #     Lista as tarefas que tiveram falha, mas ainda passíveis de novo tratamento.
    #     """
    #     sql = f"""
    #         select
    #             {TarefaDAO.COLUNAS}
    #         from
    #             {QUEUE_TABLE}
    #         where
    #             status = 'falha'
    #             and tentativa <= %(max_tentativas)s
    #             and not reenfileirado
    #     """
    #     return self.db.execute(sql, max_tentativas=max_retries)

    def list_recuperacao_processando(self):
        """
        Lista as tarefas que estão em processando.
        """
        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR}
            from
                {QUEUE_TABLE} as tarefa
            where
                status = 'processando'
        """
        return self.db.execute(sql)

    def list_pendentes(self, max_tentativas: int):
        """
        Lista as tarefas que estiverem disponíveis para execução.
        """
        # TODO Adicionar join para ordenação com prioridades (tabela de configuração das prioridades)
        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR}
            from
                {QUEUE_TABLE} as tarefa
            where
                status = 'pendente'
                and tentativa <= %(max_tentativas)s
                and data_hora <= clock_timestamp()
            order by data_hora
        """
        return self.db.execute(sql, max_tentativas=max_tentativas)

    def list_agendadas_para_notificacao(self):
        """
        Lista as tarefas que estiverem agendadas e já passíveis de execução.
        """
        # TODO Adicionar join para ordenação com prioridades (tabela de configuração das prioridades)
        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR}
            from
                {QUEUE_TABLE} as tarefa
            where
                status = 'agendada'
                and data_hora <= clock_timestamp()
            order by data_hora
        """
        return self.db.execute(sql)

    def insert(self, tarefa: dict[str, any]):
        # Verificando os fields recebidos
        fields = []
        for col in TarefaDAO.COLUNAS:
            if col in tarefa:
                fields.append(col)

        # Criando a partes de fields e values do insert
        sql_fields, sql_values = dao_util.make_sql_insert_fields_values(
            fields, psycopg2=True
        )

        # Criando a query em si
        sql = f"""
            insert into {QUEUE_TABLE} (
                {sql_fields}
            ) values (
                {sql_values}
            )
        """

        # Executando o insert
        self.db.execute(sql, **tarefa)

    def update_flag_reenfileiramento_falha(
        self,
        tarefa_id: int,
        status: str,
        msg: str,
        proxima_tentativa: datetime.datetime,
    ):
        sql = f"""
            update {QUEUE_TABLE} set
                reenfileirado = True,
                status = %(status)s,
                mensagem=%(msg)s,
                proxima_tentativa=%(proxima_tentativa)s
            where id=%(id)s
        """
        self.db.execute(
            sql,
            id=tarefa_id,
            status=status,
            msg=msg,
            proxima_tentativa=proxima_tentativa,
        )

    def update_falha_max_retries(self, tarefa_id: int, status: str, msg: str):
        sql = f"""
            update {QUEUE_TABLE} set estouro_tentativas = True, status = %(status)s, mensagem=%(msg)s where id=%(id)s
        """
        self.db.execute(sql, id=tarefa_id, status=status, msg=msg)

    def purge(self, max_age: int, purge_limit: int):
        sql = f"""
            DELETE FROM {QUEUE_TABLE}
            WHERE ctid IN (
                SELECT ctid
                FROM {QUEUE_TABLE}
                WHERE
                    data_hora > clock_timestamp() - interval '{max_age} days'
                ORDER BY data_hora
                LIMIT {purge_limit}
            )        
        """
        self.db.execute(sql)

    def update_status(self, tarefa_id: int, status: str):
        sql = f"""
            update {QUEUE_TABLE} set status = %(status)s where id=%(id)s
        """
        self.db.execute(sql, id=tarefa_id, status=status)

    def notify(self, nome_fila: str):
        sql = f"""
            notify {nome_fila}, ''
        """
        self.db.execute(sql)
