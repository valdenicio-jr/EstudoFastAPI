import sqlite3
from src.schemas.professores import SchemaProfessores
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
    def verificador_cpf(cls, cpf):
        BancoConexao.conexao_bd()
        query = "SELECT cpf FROM Alunos WHERE cpf=?"
        cpfs_aluno = BancoConexao.cursor.execute(query, (cpf,)).fetchall()

        query = "SELECT cpf FROM Professores WHERE cpf=?"
        cpfs_professor = BancoConexao.cursor.execute(query, (cpf,)).fetchall()
        if cpfs_aluno or cpfs_professor:
            return False
        return True

        return cpfs
        
    def Create_Table_Professores():
        BancoConexao.conexao_bd()
        query = """
        CREATE TABLE IF NOT EXISTS Professores(
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            telefone TEXT NOT NULL,
            especializacao TEXT NOT NULL,
            cpf TEXT NOT NULL,
            senha VARCHAR(250) NOT NULL,
            uuid VARCHAR(250) NOT NULL);
         """
        BancoConexao.cursor.execute(query)
        BancoConexao.conexao.close()

    async def get_professor():
        BancoConexao.conexao_bd()
        try:
            query = "SELECT nome, endereco, telefone, especializacao, cpf, uuid FROM Professores"
            professores = BancoConexao.cursor.execute(query).fetchall()
            print(professores)
            return True, {"Professores": professores}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def Insert_professor(professor: SchemaProfessores):
        BancoConexao.conexao_bd()
        try: 
            if BancoConexao.verificador_cpf(professor.Cpf):
                uuid_professor = str(uuid.uuid4())
                query = "INSERT INTO Professores(nome, endereco, telefone, especializacao, cpf, senha, uuid) values(?, ?, ?, ?, ?, ?, ?)"
                BancoConexao.cursor.execute(query, (professor.Nome, professor.Endereco, professor.Telefone, professor.Especializacao, professor.Cpf, BancoConexao.hash_senha(professor.Senha), uuid_professor))
                print("Professor inserido")
                
                BancoConexao.conexao.commit()
                return "Professor inserido"
            else:
                return "Já existe esse cpf"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Update_professor(professor: SchemaProfessores):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_cpf(professor.Cpf):
                query = "UPDATE Professores SET nome=?, endereco=?, telefone=?, especializacao=?, cpf=?, senha=? WHERE uuid=?"
                BancoConexao.cursor.execute(query, (professor.Nome, professor.Endereco, professor.Telefone, professor.Especializacao, professor.Cpf, BancoConexao.hash_senha(professor.Senha), professor.uuid))
                print("Professor editado")
                
                BancoConexao.conexao.commit()

                return "Professor editado"
            else:
                return "Já existe professor com esse cpf"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()
    
    async def Delete_professor(uuid:str):
        BancoConexao.conexao_bd()
        try:
            query = "DELETE FROM Professores WHERE uuid=?"
            BancoConexao.cursor.execute(query, (uuid,))
            print("Professor deletado")
            
            BancoConexao.conexao.commit()

            return "Professor deletado"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()