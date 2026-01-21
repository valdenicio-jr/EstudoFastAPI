import uvicorn
import multiprocessing
from typing import Annotated
from fastapi import FastAPI, Depends
from src.rotas import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(routers)

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:5173",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

if __name__ == '__main__':
    multiprocessing.freeze_support()
    uvicorn.run("main:app", host="localhost", port=9004, log_level='info', reload=False, workers=1)