from pydantic import BaseModel

class SchemaLogin(BaseModel):
        Cpf: str
        Senha: str
