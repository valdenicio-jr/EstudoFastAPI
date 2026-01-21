import sqlite3
import os
from src.schemas.alunos import SchemaAlunos
from passlib.context import CryptContext
from src.config.config import Settings
import uuid

class BancoConexao:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash_senha(cls, senha:str) -> str:
        return cls.pwd_context.hash(senha)

    @classmethod
    def conexao_bd(cls):
        cls.conexao = sqlite3.connect(Settings.URL_DB)
        cls.cursor = cls.conexao.cursor()

    @classmethod
    def verificador_cpf(cls, cpf:str):
        BancoConexao.conexao_bd()
        query = "SELECT cpf FROM Alunos WHERE cpf=?"
        cpfs_aluno = BancoConexao.cursor.execute(query, (cpf,)).fetchall()

        query = "SELECT cpf FROM Professores WHERE cpf=?"
        cpfs_professor = BancoConexao.cursor.execute(query, (cpf,)).fetchall()
        if cpfs_aluno or cpfs_professor:
            return False
        return True

    @classmethod
    def verificador_serie(cls, uuid_turma:str):
        BancoConexao.conexao_bd()
        query = "SELECT uuid FROM Turmas WHERE uuid=?"
        serie = BancoConexao.cursor.execute(query, (uuid_turma,)).fetchall()
        print(serie)
        return serie
        
    def Create_Table_Alunos():
        BancoConexao.conexao_bd()
        query = """
        CREATE TABLE IF NOT EXISTS Alunos (
            id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            uuid_turma VARCHAR(250) NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            senha VARCHAR(250) NOT NULL,
            uuid VARCHAR(250) NOT NULL);
         """
        BancoConexao.cursor.execute(query)
        BancoConexao.conexao.close()

    async def get_alunos():
        BancoConexao.conexao_bd()
        try:
            query = "SELECT uuid, nome, endereco, telefone, cpf, uuid_turma FROM alunos"
            alunos = BancoConexao.cursor.execute(query).fetchall()
            print(alunos)
            return True, {"Alunos": alunos}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def Insert_aluno(aluno: SchemaAlunos):
        BancoConexao.conexao_bd()
        try:
            if BancoConexao.verificador_cpf(aluno.Cpf) and BancoConexao.verificador_serie(aluno.uuid_turma):
                uuid_aluno = str(uuid.uuid4())

                query = "INSERT INTO alunos(nome, endereco, uuid_turma, telefone, cpf, senha, uuid) values(?, ?, ?, ?, ?, ?, ?)"
                BancoConexao.cursor.execute(query, (aluno.Nome, aluno.Endereco, aluno.uuid_turma, aluno.Telefone, aluno.Cpf, BancoConexao.hash_senha(aluno.Senha), uuid_aluno))
                print("Aluno inserido")
                
                BancoConexao.conexao.commit()

                return "Aluno inserido"
            else:
                if not BancoConexao.verificador_cpf(aluno.Cpf):
                    return "Esse uuid_turma não existe"
                return "Já existe esse CPF"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Update_aluno(aluno: SchemaAlunos):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_cpf(aluno.Cpf) and BancoConexao.verificador_serie(aluno.uuid_turma):
                query = "UPDATE alunos SET nome=?, endereco=?, uuid_turma=?, telefone=?, senha=? WHERE uuid=?"
                BancoConexao.cursor.execute(query, (aluno.Nome, aluno.Endereco, aluno.uuid_turma, aluno.Telefone, BancoConexao.hash_senha(aluno.Senha), aluno.uuid))
                print("Aluno editado")
                
                BancoConexao.conexao.commit()

                return "Aluno editado"
            else:
                if not BancoConexao.verificador_cpf(aluno.Cpf):
                    return "Esse id_turma não existe"
                return "Já existe aluno com esse CPF"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()
    
    async def Delete_aluno(uuid:str):
        BancoConexao.conexao_bd()
        try:
            query = "DELETE FROM alunos WHERE uuid = ?"
            BancoConexao.cursor.execute(query, (uuid,))
            print("Aluno deletado")
            
            BancoConexao.conexao.commit()
            BancoConexao.conexao.close()

            return "Aluno deletado"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()
        