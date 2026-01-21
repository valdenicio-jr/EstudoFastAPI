from pydantic import BaseModel

class SchemaTurma_Professor(BaseModel):
        uuid: str
        uuid_turma: str
        uuid_professor: str

