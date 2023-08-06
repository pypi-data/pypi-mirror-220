# nsj-sql-utils-lib
Biblioteca de utilitários Python para facilitar a implementação de sistemas com acesso a banco de dados.

## Principais utilitários:

* **dao_util:** Módulo com utilitátios para implementação de classes DAO (exemplo: facilitar a criação da lista de fileds de um select, ou fields e values de um insert).
* **dbadapter3:** Classe adapter para utilizar conexões de banco de dados (útil para conexões psycopg2).
* **dbconection_psycopg2:** Classe para abertura de conexão com postgres, utilizando o drive psycopg2 (sem pool de conexões, nem uso do SQL Alchemy).
