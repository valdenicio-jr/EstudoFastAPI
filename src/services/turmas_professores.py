import sqlite3
from src.schemas.turmas_professores import SchemaTurma_Professor
from src.config.config import Settings
import uuid

class BancoConexao:
    @classmethod
    def conexao_bd(cls):
        cls.conexao = sqlite3.connect(Settings.URL_DB)
        cls.cursor = cls.conexao.cursor()

    @classmethod
    def fazer_lista(cls, listas):
        lista_unica =[]
        for i in listas:
            for j in i:
                lista_unica.append(j)
        return lista_unica

    @classmethod
    def verificador_uuid(cls, uuid:str):
        BancoConexao.conexao_bd()
        query = "SELECT uuid FROM Turmas_Professores WHERE uuid=?"
        turma_professor = BancoConexao.cursor.execute(query, (uuid,)).fetchall()
        return turma_professor

    @classmethod
    async def verificador_uuid_turma_professor(cls, uuid_professor:str, uuid_turma:str):
        BancoConexao.conexao_bd()
        try:
            query = "SELECT id_professor FROM Professores WHERE uuid=?"
            professor = BancoConexao.cursor.execute(query, (uuid_professor,)).fetchone()
            print(professor[0])
            query = "SELECT id_turma FROM Turmas WHERE uuid=?"
            turma = BancoConexao.cursor.execute(query, (uuid_turma,)).fetchone()
            return professor[0], turma[0]
        except Exception as e:
            print(str(e))
            return False, False
    
    @classmethod
    async def verificador_turma_professor(cls, turma_professor: SchemaTurma_Professor):
        BancoConexao.conexao_bd()
        query = "SELECT id_turma FROM Turmas WHERE uuid=?"
        turma = BancoConexao.cursor.execute(query, (turma_professor.uuid_turma,)).fetchall()

        query = "SELECT id_professor FROM Professores WHERE uuid=?"
        professor = BancoConexao.cursor.execute(query, (turma_professor.uuid_professor,)).fetchall()
        
        query = "SELECT uuid_professor FROM Turmas_Professores WHERE uuid_turma=?"
        turmas_professores = BancoConexao.cursor.execute(query, (turma_professor.uuid_turma,)).fetchall()

        valor = True
        for i in turmas_professores:
            for j in i:
                if j == turma_professor.uuid_professor:
                    valor = False       

        if turma and professor and valor:
            return True
        return False
        
    def Create_Table_Turma_Professor():
        BancoConexao.conexao_bd()
        query = """
        CREATE TABLE IF NOT EXISTS Turmas_Professores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INTEGER NOT NULL,
            id_professor INTEGER NOT NULL, 
            uuid VARCHAR(250) NOT NULL,
            uuid_turma VARCHAR(250) NOT NULL,
            uuid_professor VARCHAR(250) NOT NULL); 
         """
        BancoConexao.cursor.execute(query)
        BancoConexao.conexao.close()

    async def get_turma_professor():
        BancoConexao.conexao_bd()
        try:
            query = "SELECT uuid, uuid_turma, uuid_professor FROM Turmas_Professores"

            turmas_professores = BancoConexao.cursor.execute(query).fetchall()

            return True, {"Turmas/Professores": turmas_professores}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def Insert_turma_professor(turma_professor: SchemaTurma_Professor):
        BancoConexao.conexao_bd()
        try:
            professor, turma = await BancoConexao.verificador_uuid_turma_professor(turma_professor.uuid_professor, turma_professor.uuid_turma)
            if professor <= 0 and turma <=0:
                raise Exception("Você passou uuids inválidos")

            if await BancoConexao.verificador_turma_professor(turma_professor):
                print("rlxxxxxxxx")
                uuid_turmas_professores = str(uuid.uuid4())
                query = "INSERT INTO Turmas_Professores(id_turma, id_professor, uuid, uuid_professor, uuid_turma) values(?, ?, ?, ?, ?)"
                BancoConexao.cursor.execute(query, (turma, professor, uuid_turmas_professores, turma_professor.uuid_professor, turma_professor.uuid_turma))
                print("Turma/Professor inserido")
                
                BancoConexao.conexao.commit()

                return "Turma/Professor inserido"
            else:
                return "Passe ids que sejam válidos"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Update_turma_professor(turma_professor: SchemaTurma_Professor):
        BancoConexao.conexao_bd()
        try:
            query = "UPDATE Turmas_Professores SET uuid_turma=?, uuid_professor=? WHERE uuid=?"
            BancoConexao.cursor.execute(query, (turma_professor.uuid_turma, turma_professor.uuid_professor, turma_professor.uuid))
            
            BancoConexao.conexao.commit()

            return "Turma/professor editada"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()

    async def Delete_turma_professor(uuid:str):
        BancoConexao.conexao_bd()
        try:
            if not BancoConexao.verificador_uuid(uuid):
                raise Exception("Não existe turma/professires com esse uuid")

            query = "DELETE FROM Turmas_professores WHERE uuid=?"
            BancoConexao.cursor.execute(query, (uuid,))
            print("Turma deletado")

            BancoConexao.conexao.commit()

            return "Turma deletado"
        except Exception as e:
            return str(e)
        finally:
            BancoConexao.conexao.close()      

    async def get_alunos_turma(idturma: str):
        BancoConexao.conexao_bd()
        try:
            query = """
            SELECT a.nome FROM Turmas_Professores tp
            INNER JOIN Turmas t ON tp.uuid_turma = t.uuid
            INNER JOIN Alunos a ON t.uuid = a.uuid_turma
            WHERE t.uuid = ?
            GROUP BY a.id_aluno
            """
            alunos = BancoConexao.cursor.execute(query,(idturma,)).fetchall()
            print(alunos)
            #print(BancoConexao.fazer_lista(alunos))
            return True, {"Alunos de tal turma": BancoConexao.fazer_lista(alunos)}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def get_alunos_professor(idprofessor: str):
        BancoConexao.conexao_bd()
        try:
            query = """
            SELECT a.nome FROM Professores p
            INNER JOIN Turmas_Professores tp ON p.uuid = tp.uuid_professor
            INNER JOIN Turmas t ON tp.uuid_turma = t.uuid
            INNER JOIN Alunos a ON t.uuid = a.uuid_turma
            WHERE p.uuid = ?
            """
            alunos = BancoConexao.cursor.execute(query, (idprofessor,)).fetchall()

            return True, {"Alunos com tais professores": BancoConexao.fazer_lista(alunos)}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()        

    async def get_professores_turma(idturma: str):
        BancoConexao.conexao_bd()
        try:
            query = """
            SELECT p.nome FROM Turmas_Professores tp
            INNER JOIN Professores p ON tp.uuid_professor = p.uuid
            INNER JOIN Turmas t ON tp.uuid_turma = t.uuid
            WHERE t.uuid = ?
            """
            professores = BancoConexao.cursor.execute(query,(idturma,)).fetchall()

            return True, {"Professores de tal turma": BancoConexao.fazer_lista(professores)}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()

    async def get_turmas_professor(idprofessor: str):
        BancoConexao.conexao_bd()
        try:
            query = """
            SELECT t.nome FROM Turmas_Professores tp
            INNER JOIN Professores p ON tp.id_professor = p.id_professor
            INNER JOIN Turmas t ON tp.id_turma = t.id_turma
            WHERE p.uuid = ?
            """
            professores = BancoConexao.cursor.execute(query,(idprofessor,)).fetchall()

            return True, {"Turmas que tal professor leciona": BancoConexao.fazer_lista(professores)}
        except Exception as e:
            return False, str(e)
        finally:
            BancoConexao.conexao.close()
        