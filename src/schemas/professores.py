from pydantic import BaseModel

class SchemaProfessores(BaseModel):
        uuid: str 
        Nome: str
        Endereco: str
        Telefone: str
        Especializacao: str
        Cpf: str
        Senha: str
