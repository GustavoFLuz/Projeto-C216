from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
from datetime import date
import asyncpg
import os

async def start_database():
    DATABASE_URL = os.environ.get("PGURL","postgres://postgres:postgres@database:5432/todo-db")
    return await asyncpg.connect(DATABASE_URL)

app = FastAPI()

class Tarefa(BaseModel):
    id: Optional[int] = None
    usuario: str
    nome: str
    data: date
    descricao: str
    completado: Optional[bool] = False

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

@app.get("/api/v1/tarefas/{usuario}")
async def queryTarefaUsuario(usuario: str):
    connection = await start_database()
    try:
        query = "SELECT * FROM tarefas WHERE usuario = $1"
        result = await connection.fetch(query, usuario)
        tarefas = [dict(tarefa) for tarefa in result]
        return tarefas
    finally:
        await connection.close()

@app.post("/api/v1/tarefas", status_code=201)
async def novaTarefa(novaTarefa: Tarefa):
    connection = await start_database()
    try:
        query = "INSERT INTO tarefas (usuario, nome, data, descricao) VALUES ($1, $2, $3, $4)"
        async with connection.transaction():
            result = await connection.execute(query, novaTarefa.usuario, novaTarefa.nome, novaTarefa.data, novaTarefa.descricao)
            return {"message": "Tarefa registrada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Não foi possível registrar a nova tarefa {str(e)}")
    finally:
        await connection.close()

@app.put("/api/v1/tarefas/completar/{usuario}/{id}")
async def completarTarefa(usuario:str, id:int):
    connection = await start_database()
    try:
        query = "SELECT * FROM tarefas WHERE id = $1 AND usuario = $2"
        tarefa = await connection.fetchrow(query, id, usuario)
        if tarefa is None:
            raise HTTPException(status_code=404, datail="Tarefa não encontrada!")
        
        update_query = "UPDATE tarefas SET completado = TRUE WHERE id = $1 AND usuario = $2"
        
        await connection.execute(update_query, id, usuario)

        return {"message": "Tarefa marcada com completado!"}
    finally:
        await connection.close()

@app.delete("/api/v1/tarefas/{usuario}/{id}")
async def deletarTarefa(usuario: str, id:int):
    connection = await start_database()
    try:
        query = "SELECT * FROM tarefas WHERE id = $1 AND usuario = $2"
        tarefa = await connection.fetchrow(query, id, usuario)
        if tarefa is None:
            raise HTTPException(status_code=404, datail="Tarefa não encontrada!")
        delete_query = "DELETE FROM tarefas WHERE id = $1 AND usuario = $2"
        await connection.execute(delete_query, id, usuario)
        return {"message":"Tarefa deletada com sucesso!"}
    finally:
        await connection.close()

@app.delete("/api/v1/tarefas/reset/")
async def resetarDB():
    init_sql = os.getenv('INIT_SQL', 'database/db.sql')
    connection = await start_database()
    try:
        with open(init_sql,'r') as file:
            sql_commands = file.read()
        await connection.execute(sql_commands)
        return {"message": "DB Resetado!"}
    finally:
        await connection.close()
        
resetarDB()