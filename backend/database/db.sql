DROP DATABASE IF EXISTS "todo-db";

CREATE DATABASE "todo-db";

USE "todo-db";

CREATE TABLE "tarefas" (
    "id" SERIAL,
    "usuario" VARCHAR(255) NOT NULL,
    "nome" VARCHAR(255) NOT NULL,
    "data" DATE NOT NULL,
    "descricao" TEXT NOT NULL,
    "completado" BOOLEAN DEFAULT FALSE NOT NULL,
    PRIMARY KEY ("id","usuario");
)