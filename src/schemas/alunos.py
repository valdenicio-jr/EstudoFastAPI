from pydantic import BaseModel
#from typing import Optional

class SchemaAlunos(BaseModel):
        uuid: str #Optional[int] = None
        Nome: str
        Endereco: str
        uuid_turma: str
        Telefone: str
        Cpf: str
        Senha: str