from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Definindo as variáveis de ambiente
API_BASE_URL = "http://backend:8000"

tarefas_g = [
        {"id": 1, "completado":False, "nome": "Estudar Python", "data": "2021-09-01", "descricao": "Estudar Python para aprimorar os conhecimentos", "usuario": "gustavo"},
    ]

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro
@app.route('/tarefas/<username>', methods=['GET'])
def lista_de_tarefas(username):
    try:
        response = requests.get(f'{API_BASE_URL}/api/v1/tarefas/{username}')
        tarefas = response.json()
    except:
        tarefas = tarefas_g
    return render_template('tasks.html', tarefas=tarefas, usuario=username)

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_tarefa():
    print("Inserir")
    nome = request.form['nome']
    data = request.form['date']
    descricao = request.form['desc']
    usuario = request.form['usuario']
    
    payload = {
        'nome': nome,
        'data': data,
        'descricao' : descricao,
        'usuario': usuario
    }
    print("payload")
    print(payload)
    tarefas_g.append({
        "id": len(tarefas_g) + 1,
        "completado": False,
        "nome": nome,
        "data": data,
        "descricao": descricao,
        "usuario": usuario
    })
    try:
        #response = requests.post(f'{API_BASE_URL}/api/v1/tarefas/', json=payload)
        #if response.status_code == 201:
        return redirect(f"/tarefas/{usuario}")
        #else:
        #    return "Erro ao inserir tarefa", 500
    except:
        return "Erro ao inserir tarefa", 500

# Rota para completar uma tarefa
@app.route('/completar/<usuario>/<int:tarefa_id>', methods=['GET'])
def completar_tarefa(usuario, tarefa_id):
    payload = {
        'usuario': usuario,
        'tarefa_id': tarefa_id
    }
    print(payload)
    try:
        response = requests.put(f"{API_BASE_URL}/api/v1/tarefas/completar", json=payload)
        if response.status_code == 200:
            return redirect(f"/tarefas/{usuario}")
        else:
            return "Erro ao completar tarefa", 500
    except:
        return "Erro ao completar tarefa", 500

# Rota para excluir uma tarefa
@app.route('/excluir/<usuario>/<int:tarefa_id>', methods=['POST'])
def excluir_tarefa(usuario, tarefa_id):
    payload = {
        'usuario': usuario,
        'tarefa_id': tarefa_id
    }
    try:
        response = requests.delete(f"{API_BASE_URL}/api/v1/tarefas/", json=payload)
    
        if response.status_code == 200  :
            return redirect(f"/tarefas/{usuario}")
        else:
            return "Erro ao excluir tarefa", 500
    except:
        return "Erro ao excluir tarefa", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')