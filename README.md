# Projeto C216

## Descrição
Este é o projeto C216, desenvolvido para o trabalho final do laboratório.
É uma lista de tarefas simples, com uma API com CRUD completo e uma interface Web para interagir com ela.

## Alunos
- Gustavo Figueiredo Luz - 57 GES
    - Email: gustavo.figueiredo@ges.inatel.br
- Rafael Felipe Rodrigues Moreira - 81 GES
    - Email: rafael.felipe@ges.inatel.br

## Estrutura do Projeto
- **/backend**: Código da API
    - /database: Script de inicialização do banco de dados
    - /test: Testes no POSTMAN
- **/frontend**: Código da interface Web
    - /templates: Templates HTML

## Pré-requisitos
- Docker

## Execução via Docker
1. Clone o repositório:
    ```sh
    git clone https://github.com/GustavoFLuz/Projeto-C216.git
    ```
2. Entre na pasta do projeto:
    ```sh
    cd Projeto-C216
    ```
3. Execute o comando:
    ```sh
    docker-compose up --build
    ```
4. Acesse a interface Web em [http://localhost:3000](http://localhost:3000) e a API em [http://localhost:8000](http://localhost:8000)
