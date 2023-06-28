from flask import Flask, render_template, jsonify

import dados
from dados import obter_dados

app = Flask(__name__, static_folder='templates/assets/static', template_folder='templates')


@app.route('/')
def index():
    #dados = obter_dados()
    dados = {
        'em_aberto': [0, 0, 0, 0, ['red', 'red', 'red', 'red']],
        'finalizados': [0, 0, 0, 0],
        'sem_acesso': [0, 0, 0]
    }
    return render_template('index.html', em_aberto_total=dados['em_aberto'][0], vencidos=dados['em_aberto'][1], assumidos=dados['em_aberto'][2], criticos=dados['em_aberto'][3], cor_critico=dados['em_aberto'][4][0], cor_vencido=dados['em_aberto'][4][1], cor_assumido=dados['em_aberto'][4][2], finalizados_total=dados['finalizados'][0], sem_acesso_kdm=dados['sem_acesso'][0], sem_acesso_tele=dados['sem_acesso'][1])


@app.route('/atualizar_dados')
def atualizar_dados():
    dados = obter_dados()
    dados = {
        'em_aberto': [0, 0, 0, 0, ['red', 'red', 'red', 'red']],
        'finalizados': [0, 0, 0, 0],
        'sem_acesso': [0, 0, 0]
    }
    return jsonify(dados)


if __name__ == '__main__':
    app.run()

