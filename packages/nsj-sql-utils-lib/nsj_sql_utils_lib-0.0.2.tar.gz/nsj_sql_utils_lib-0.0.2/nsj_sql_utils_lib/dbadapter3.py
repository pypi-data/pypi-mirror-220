class DBAdapter3:
    """
    Adaptador de banco de dados para uso com o Psycopg2.

    Obs.: Esse adapter é simplificado, com relação ao DBAdapter2 e o DBAdapter, mas,
    contém função para execução de instruções SQL multivaloradas.
    """

    def __init__(self, conn):
        self.conn = conn
        self._transaction = None

    def begin(self):
        if self._transaction is None:
            self.execute("begin")
            self._transaction = True

    def commit(self):
        if self._transaction is not None:
            self.execute("commit")
            self._transaction = None

    def rollback(self):
        if self._transaction is not None:
            self.execute("rollback")
            self._transaction = None

    def in_transaction(self):
        return self._transaction is not None

    def _handle_result(self, cur) -> tuple[list[dict[str, any]], int]:
        """
        Trata os resultados contidos no cursor, os convertendo para uma
        tupla cm uma lista de dicionários, e o total de linhas no cursor.
        """

        if cur.description is not None:
            lista = []
            item = cur.fetchone()
            while item is not None:
                obj = {}
                for i in range(len(cur.description)):
                    column = cur.description[i]
                    obj[column.name] = item[i]

                lista.append(obj)
                item = cur.fetchone()

            return (lista, cur.rowcount)
        else:
            return ([], cur.rowcount)

    def execute(self, sql, **kwargs) -> tuple[list[dict[str, any]], int]:
        """
        Executa uma query (parâmetro sql), que pode ser tanto select, quanto update ou delete,
        retornando uma tupla, onde o primeiro elemento é uma lista de dicionários,
        e a chave de cada dicionário corresponde às colunas da query (se for select),
        e o segundo elemento repesenta o total de linhas no retorno (se for um update
        ou insert, representa o total de linhas impactadas).

        Os parâmetros do comando sql devem ser passados com a sintaxe %(nome)s, no SQL,
        e seus valores devem ser passados como kwargs.
        """

        with self.conn.cursor() as cur:
            cur.execute(sql, kwargs)

            return self._handle_result(cur)

    def execute_many(
        self, sql, data: list[dict[str, any]]
    ) -> tuple[list[dict[str, any]], int]:
        """
        Executa uma query N vezes, de acordo com a lista de valores, em dicionários,
        recebidos no parâmetro "data"

        A query normalmente deve ser um insert, update ou delete, e
        retornan uma tupla, onde o primeiro elemento é uma lista de dicionários,
        e a chave de cada dicionário corresponde às colunas da query (se for select),
        e o segundo elemento repesenta o total de linhas no retorno (se for um update
        ou insert, representa o total de linhas impactadas).

        Os parâmetros do comando sql devem ser passados com a sintaxe %(nome)s, no SQL,
        e seus valores devem ser passados nos dicionários contidos na lista data.
        """

        with self.conn.cursor() as cur:
            cur.executemany(sql, data)

            return self._handle_result(cur)
