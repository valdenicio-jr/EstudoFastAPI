from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union
from src.services.alunos import BancoConexao
from src.services.login import BancoConexaoLogin
from src.schemas.alunos import SchemaAlunos
from src.schemas.login import SchemaLogin
from src.auth.auth import criar_token, verificador_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
oauth2_scheme = HTTPBearer()

BancoConexao.Create_Table_Alunos()

@router.post("/Login")
async def Login_Alunos(login: SchemaLogin, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    try:
        if not(login.Cpf and login.Senha):
            print(login.Cpf, login.Senha)
            raise HTTPException(status_code=400, detail="Digite credencias válidas")

        result, aluno = await BancoConexaoLogin.get_login_aluno(login)
        if result:
            if len(aluno) <= 1:
                raise HTTPException(status_code=401, detail="Você digitou credenciais que não existe")

            token_dados = {"uuid": aluno[0], "tipo": "aluno"}
            token = criar_token(token_dados)

            return {
                "access_token":token,
                "token_type": "bearer",
                "user": aluno,
            }
        else:
            return aluno
    except HTTPException as he:
        return str(he)


@router.get("/Exibir")
async def Exibir_Alunos(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_alunos()
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.post("/insert")
async def Insert_Alunos(aluno: SchemaAlunos, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Insert_aluno(aluno)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.put("/update")
async def Update_Alunos(aluno: SchemaAlunos, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Update_aluno(aluno)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"


@router.delete("/delete")
async def Delete_Alunos(uuid_aluno: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Delete_aluno(uuid_aluno)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"
