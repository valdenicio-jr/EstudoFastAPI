from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union
from src.services.turma import BancoConexao
from src.services.login import BancoConexaoLogin
from src.schemas.turma import SchemaTurma
from src.auth.auth import verificador_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
oauth2_scheme = HTTPBearer()

BancoConexao.Create_Table_Turma()

@router.get("/Exibir")
async def Exibir_Turmas(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_turma()
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.post("/insert")
async def Insert_Turmas(turma: SchemaTurma, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Insert_turma(turma)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.put("/update")
async def Update_Turmas(turma: SchemaTurma, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Update_turma(turma)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.delete("/delete")
async def Delete_Turmas(uuid_turma: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Delete_turma(uuid_turma)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"
