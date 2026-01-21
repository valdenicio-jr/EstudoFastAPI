import sqlite3
from src.schemas.turma import SchemaTurma
from src.config.config import Settings
import uuid

class BancoConexao:
    @classmethod
    def conexao_bd(cls):
        cls.conexao = sqlite3.connect(Settings.URL_DB)
        cls.cursor = cls.conexao.cursor()

    @classmethod
    def verificador_turma(cls, turma:str):
        BancoConexao.conexao_bd()
        query = "SELECT nome FROM Turmas WHERE nome=?"
        turma = BancoConexao.cursor.execute(query, (turma,)).fetchall()
        return turma

    @classmethod
    def verificador_uuid(cls, uuid:str):
        BancoConexao.conexao_bd()
        query = "SELECT uuid FROM Turmas WHERE uuid=?"
        turma = BancoConexao.cursor.execute(query, (uuid,)).fetchall()
        return turma
        
    def Create_Table_Turma():
        BancoConexao.conexao_bd()
        query = """
        CREATE TABLE IF NOT EXISTS Turmas(
            id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, 
            uuid VARCHAR(250) NOT NULL);
         """
        BancoConexao.cursor.execute(query)
        BancoConexao.conexao.close()

    async def get_turma():
        BancoConexao.conexao_bd()
        try:
            query = "SELECT nome, uuid FROM Turmas"

            turmas = BancoConexao.cursor.execute(query).fetchall()

            return True, {"Turmas": turmas}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def Insert_turma(turma: SchemaTurma):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_turma(turma.Nome):
                uuid_turma = str(uuid.uuid4())
                query = "INSERT INTO Turmas(nome, uuid) values(?, ?)"
                BancoConexao.cursor.execute(query, (turma.Nome, uuid_turma))
                print("Turma inserido")
                BancoConexao.conexao.commit()
                
                return "Turma inserido"
            else:
                return "Essa turma ja existe"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Update_turma(turma: SchemaTurma):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_turma(turma.Nome):
                query = "SELECT uuid FROM Turmas WHERE uuid=?"
                uuids = BancoConexao.cursor.execute(query, (turma.uuid,)).fetchall()

                if not uuids:
                    raise Exception("Esse uuid não existe")

                query = "UPDATE Turmas SET nome=? WHERE uuid=?"
                BancoConexao.cursor.execute(query, (turma.Nome, turma.uuid))
                print("Nome da turma editado")
                
                BancoConexao.conexao.commit()

                return "Nome da turma editado"
            else:
                return "Essa turma ja existe"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Delete_turma(uuid:str):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_uuid(uuid):
                raise Exception("Não existe turma com esse uuid")

            query = "DELETE FROM Turmas WHERE uuid=?"
            BancoConexao.cursor.execute(query, (uuid,))
            print("Turma deletado")

            BancoConexao.conexao.commit()

            return "Turma deletado"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()