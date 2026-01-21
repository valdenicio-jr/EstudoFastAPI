from fastapi import APIRouter
from src.api import alunos
from src.api import professores
from src.api import turma
from src.api import turmas_professores

routers = APIRouter()

routers.include_router(alunos.router, prefix='/Alunos', tags=['FUNÇÕES ALUNOS'])
routers.include_router(professores.router, prefix='/Professores', tags=['FUNÇÕES PROFESSORES'])
routers.include_router(turma.router, prefix='/Turmas', tags=['FUNÇÕES TURMAS'])
routers.include_router(turmas_professores.router, prefix='/Rotas_Gerais', tags=['FUNÇÕES GERAIS'])
