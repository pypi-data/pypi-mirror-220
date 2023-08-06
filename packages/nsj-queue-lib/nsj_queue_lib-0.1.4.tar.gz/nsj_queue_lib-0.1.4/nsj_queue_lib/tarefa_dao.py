import datetime
import hashlib

from nsj_sql_utils_lib import dao_util

from nsj_sql_utils_lib.dbadapter3 import DBAdapter3
from nsj_queue_lib.exception import NotFoundException


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
        "payload_hash",
    ]
    COLUNAS_STR = "tarefa." + ", tarefa.".join(COLUNAS)

    def __init__(self, db: DBAdapter3, queue_table: str):
        self.db = db
        self.queue_table = queue_table

    def get(self, id: int):
        """
        Recupera uma tarefa, por meio de seu ID
        """
        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR},
                coalesce(tarefa.payload, inicial.payload) as payload
            from
                {self.queue_table} as tarefa
                left join {self.queue_table} as inicial
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
    #             {self.queue_table}
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
                {self.queue_table} as tarefa
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
                {self.queue_table} as tarefa
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
                {self.queue_table} as tarefa
            where
                status = 'agendada'
                and data_hora <= clock_timestamp()
            order by data_hora
        """
        return self.db.execute(sql)

    def insert(self, tarefa: dict[str, any]):
        # Calculando o hash do payload
        if (
            "payload" in tarefa
            and tarefa["payload"] is not None
            and tarefa["payload"] != ""
        ):
            payload_hash = hashlib.sha256(tarefa["payload"].encode()).hexdigest()
            tarefa["payload_hash"] = payload_hash

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
            insert into {self.queue_table} (
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
            update {self.queue_table} set
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
            update {self.queue_table} set estouro_tentativas = True, status = %(status)s, mensagem=%(msg)s where id=%(id)s
        """
        self.db.execute(sql, id=tarefa_id, status=status, msg=msg)

    def purge(self, max_age: int, purge_limit: int):
        sql = f"""
            DELETE FROM {self.queue_table}
            WHERE ctid IN (
                SELECT ctid
                FROM {self.queue_table}
                WHERE
                    data_hora > clock_timestamp() - interval '{max_age} days'
                ORDER BY data_hora
                LIMIT {purge_limit}
            )        
        """
        self.db.execute(sql)

    def update_status(self, tarefa_id: int, status: str):
        sql = f"""
            update {self.queue_table} set status = %(status)s where id=%(id)s
        """
        self.db.execute(sql, id=tarefa_id, status=status)

    def notify(self, nome_fila: str):
        sql = f"""
            notify {nome_fila}, ''
        """
        self.db.execute(sql)

    def list_equivalent(self, chave_externa: str, payload: str, status: list[str]):
        """
        Lista as tarefas com mesma chave externa, payload e em algum dos status passados.
        """

        # Calculando o hash do payload
        payload_hash = None
        if payload is not None and payload != "":
            payload_hash = hashlib.sha256(payload.encode()).hexdigest()

        sql = f"""
            select
                {TarefaDAO.COLUNAS_STR}
            from
                {self.queue_table} as tarefa
            where
                tarefa.payload_hash = %(payload_hash)s
                and chave_externa = %(chave_externa)s
                and tarefa.status in %(status)s
        """

        result, _ = self.db.execute(
            sql,
            payload_hash=payload_hash,
            chave_externa=chave_externa,
            status=tuple(status),
        )

        return result
