import sqlite3

# Abrir banco de Dados
def abrir_conexao():
    conexao = sqlite3.connect("base.db")
    return conexao

# Fechar Banco de Dados
def fechar_conexao(conexao):
    conexao.close()

# Criar Tabela Motorista
def criar_tabela_motorista():
    conexao = abrir_conexao()
    cur = conexao.cursor()

    tabela = """
            CREATE TABLE IF NOT EXISTS motorista(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transportadora TEXT NOT NULL,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                cnh TEXT NOT NULL UNIQUE,
                validade_cnh TEXT NOT NULL,
                cetpp INTEGER NOT NULL DEFAULT 0,
                placa TEXT NOT NULL,
                renavam TEXT NOT NULL
            )
        """
    cur.execute(tabela)
    conexao.commit()
    fechar_conexao(conexao)

criar_tabela_motorista()