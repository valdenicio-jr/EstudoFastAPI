import sqlite3
import os
from src.schemas.login import SchemaLogin
from passlib.context import CryptContext
from src.config.config import Settings

class BancoConexaoLogin:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_senha(cls, senha:str) -> str:
        return cls.pwd_context.hash(senha)
    
    @classmethod
    def conexao_bd(cls):
        cls.conexao = sqlite3.connect(Settings.URL_DB)
        cls.cursor = cls.conexao.cursor()

    # async def professor_senha(id:it) -> bool:
    #     BancoConexaoLogin.conexao_bd()
    #     query = "SELECT id FROM Professores WHERE id_professor=?"
    #     id_professor = BancoConexaoLogin.cursor.execute(query, (id,)).fetchall()
    #     print(id_professor)
    #     BancoConexaoLogin.conexao.close()
    #     if id_professor:
    #         return True
    #     return False

    async def get_login_aluno(login: SchemaLogin):
        BancoConexaoLogin.conexao_bd()
        try:
            query = "SELECT uuid, cpf, senha FROM alunos WHERE cpf=?"
            aluno = BancoConexaoLogin.cursor.execute(query, (login.Cpf,)).fetchall()
            if not aluno:
                return True, lista_tratada

            lista_tratada = []
            for i in aluno:
                for j in i:
                    lista_tratada.append(j)

            if not BancoConexaoLogin.pwd_context.verify(login.Senha, lista_tratada[2]):
                lista_tratada = []

            return True, lista_tratada
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexaoLogin.conexao.close()

    async def get_login_professor(login: SchemaLogin):
        BancoConexaoLogin.conexao_bd()
        try:
            query = "SELECT uuid, cpf, senha FROM professores WHERE cpf=?"
            professor = BancoConexaoLogin.cursor.execute(query, (login.Cpf,)).fetchall()

            lista_tratada = []
            for i in professor:
                for j in i:
                    lista_tratada.append(j)

            if not professor:
                return True, lista_tratada

            if not BancoConexaoLogin.pwd_context.verify(login.Senha, lista_tratada[2]):
                lista_tratada = []

            return True, lista_tratada
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexaoLogin.conexao.close()