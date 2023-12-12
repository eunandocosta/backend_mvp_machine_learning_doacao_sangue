import os
import sqlite3
from logger import logger

from insertions import *

def db_create():
    try:
        db_path = './database'

        # Cria se o diretorio não existir
        os.makedirs(db_path, exist_ok=True)

        #Cria e direciona a base de dados para a pasta desejada
        db_path_join = os.path.join(db_path, 'blood_donations.db')
        
        #Conecta a base de dados
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        
        #Cria a tabela na base de dados
        cursor.execute("""CREATE TABLE IF NOT EXISTS doadores(
                        cpf STR NOT NULL UNIQUE,
                        recency INT NOT NULL,
                        frequency INT NOT NULL,
                        monetary INT NOT NULL,
                        time INT NOT NULL,
                        outcome INT
        )""")
        
        conexao.commit()
        conexao.close()

        return True
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        return str(e) if e is not None else "Erro desconhecido"
    
def donator_insert(self):
  try:
    with sqlite3.connect('./database/blood_donations.db') as conn:
      cursor = conn.cursor()
      cursor.execute("""
        INSERT INTO doadores(
          cpf, recency, frequency, monetary, time, outcome
        ) VALUES (
          ?,?,?,?,?,?
        )
      """, (self.cpf, self.recency, self.frequency, self.monetary, self.time, self.outcome))
      conn.commit()
    return True
  except sqlite3.Error as e:
    logger.error(f"Erro ao inserir doador: {e}")
    return False
  except Exception as e:
    # Capturar exceções inesperadas
    logger.exception(f"Erro inesperado ao inserir doador: {e}")
    print(e)
    return (f"Erro ao inserir doador: {e}")
    
def donator_show():
    try:
        db_path_join = os.path.join('./database', 'blood_donations.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        # Execute uma consulta para obter os nomes das colunas
        cursor.execute("PRAGMA table_info(doadores)")
        nomes_colunas = [coluna[1] for coluna in cursor.fetchall()]
        # Selecione os dados que você precisa
        cursor.execute("SELECT * FROM doadores")
        dados = cursor.fetchall()
        resultado = [dict(zip(nomes_colunas, linha)) for linha in dados]
        conexao.close()
        return resultado
    except Exception as e:
        return 'Erro: ' + str(e)
    
def donator_delete(cpf):
    try:
        db_path_join = os.path.join('./database', 'blood_donations.db')
        conexao = sqlite3.connect(db_path_join)
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM doadores WHERE cpf = ?", (cpf,))
        conexao.commit()
        conexao.close()
        
        return True # Indica que a exclusão foi bem-sucedida
    except Exception as e:
        return False  # Indica que ocorreu um erro durante a exclusão
    
def __str__(self):
    return f"cpf: {self.cpf}, Recency: {self.recency}, Frequency: {self.frequency}, Monetary: {self.monetary}, Time: {self.time}, Outcome: {self.outcome}"
    
db_create()
donator_show()