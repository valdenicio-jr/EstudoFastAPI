from fastapi import APIRouter, Depends, HTTPException, status, Security
from typing import Union
from src.services.turmas_professores import BancoConexao
from src.schemas.turmas_professores import SchemaTurma_Professor
from src.auth.auth import verificador_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
oauth2_scheme = HTTPBearer()

BancoConexao.Create_Table_Turma_Professor()

@router.get("/Exibir")
async def Exibir_Turmas_Professores(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_turma_professor()
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.post("/insert")
async def Insert_Turmas(turma_professor:SchemaTurma_Professor, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":   
        msg = await BancoConexao.Insert_turma_professor(turma_professor)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.put("/update")
async def Update_Turmas(turma_professor: SchemaTurma_Professor, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Update_turma_professor(turma_professor)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.delete("/delete")
async def Delete_Turmas(uuid_turmas_professores: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        msg = await BancoConexao.Delete_turma_professor(uuid_turmas_professores)
        return msg 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.get("/Exibir_AlunosTurma")
async def Exibir_AlunosTurma(uuid_turma: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_alunos_turma(uuid_turma)
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.get("/Exibir_AlunosProfessor")
async def get_Alunos_Professor(uuid_professor: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_alunos_professor(uuid_professor)
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.get("/Exibir_ProfessoresTurma")
async def get_ProfessoresTurma(uuid_turma: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_professores_turma(uuid_turma)
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

@router.get("/Exibir_TurmasProfessor")
async def get_Turmas_Professor(uuid_professor: str, credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    dados_token =  verificador_token(credentials.credentials)
    if dados_token["tipo"] == "professor":
        result, dados = await BancoConexao.get_turmas_professor(uuid_professor)
        if result:
            return {"Dados": dados}
        return dados 
    elif not dados_token["tipo"] == "professor":
        return "Alunos não tem acesso a esse campo"
    return "Esse uuid é inválido"

