import streamlit as st
from datetime import date
import sqlite3

# conexao Banco de dados

con = sqlite3.connect("motorista.db")
cur = con.cursor()

cur.execute("""
        CREATE TABLE IF NOT EXISTS motorista (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transportadora TEXT NOT NULL,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            cnh TEXT NOT NULL UNIQUE,
            validade_cnh TEXT NOT NULL,
            cetpp INTEGER NOT NULL DEFAULT 0,
            placa TEXT NOT NULL,
            renavam TEXT NOT NULL UNIQUE
        )
""")

con.commit()

transportadora = "Dallogs Express"
nome = "Edson da Silva"
cpf = "123.456.789-00"
cnh = "123456789"
validade_cnh = str(date(2028, 8, 15))  # Converte a data para texto 'YYYY-MM-DD'
cetpp = 1  # 1 para Sim, 0 para Não
placa = "UDX-5A45"
renavam = "00123456789"

try:
    cur.execute('''
        INSERT INTO motorista (
            transportadora, nome, cpf, cnh, validade_cnh, cetpp, placa, renavam
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (transportadora, nome, cpf, cnh, validade_cnh, cetpp, placa, renavam))
    
    con.commit()
    print("Motorista cadastrado com sucesso!")

except sqlite3.IntegrityError:
    print("Erro: CPF, CNH ou RENAVAM já cadastrado no sistema.")

finally:
    con.close()


