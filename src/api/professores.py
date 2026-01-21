from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union
from src.schemas.professores import SchemaProfessores
from src.schemas.login import SchemaLogin
from src.services.professores import BancoConexao
from src.services.login import BancoConexaoLogin
from src.auth.auth import criar_token
from src.auth.auth import verificador_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()

oauth2_scheme = HTTPBearer()

BancoConexao.Create_Table_Professores()

@router.post("/Login")
async def Login_Professores(login: SchemaLogin):
    try:
        if not(login.Cpf and login.Senha):
            print(login.Cpf, login.Senha)
            raise HTTPException(status_code=400, detail="Digite credencias válidas")

        result, professor = await BancoConexaoLogin.get_login_professor(login)
        if result:
            if len(professor) <= 1:
                raise HTTPException(status_code=401, detail="Você digitou credenciais que não existe")

            token_dados = {"uuid": professor[0], "tipo": "professor"}
            token = criar_token(token_dados)

            return {
                "access_token":token,
                "token_type": "bearer",
                "user": professor,
            }
        else:
            return aluno
    except HTTPException as he:
        return str(he)

@router.get("/Exibir")
async def Exibir_Professores(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_professor()
        if result:
            return {"Dados": dados}
        else:
            return dados
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.post("/insert")
async def Insert_Professores(professor: SchemaProfessores):
    msg = await BancoConexao.Insert_professor(professor)
    return msg 

@router.put("/update")
async def Update_Professores(professor: SchemaProfessores, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["uuid"] == professor.uuid and dados_token["tipo"] == "professor":
        msg = await BancoConexao.Update_professor(professor)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.delete("/delete")
async def Delete_Professores(uuid_professor: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["uuid"] == uuid_professor and dados_token["tipo"] == "professor":
        msg = await BancoConexao.Delete_professor(uuid_professor)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"
