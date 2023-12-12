from model import *

from flask import request, jsonify, redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS

from model.__init__ import *

from schemas.donator_schema import Donator

from app import *
from model.__init__ import *
from model.__init__ import *
from schemas.error import *

from schemas.donator_schema import *

from insertions import *

import logging

from pydantic import ValidationError

logging.basicConfig(level=logging.DEBUG) 
logger = logging.getLogger(__name__)

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

#Configuração do banco de dados
database = '../database/blood_donations.db'

CORS(app, origins=['*'], methods=['GET', 'POST', 'DELETE'])

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
donator_tag = Tag(name="Doador", description="Adição, visualização e remoção de doadores à base")

def carga_inicial():
    print("Inicializando carga inicial...")
    dados_carga = [
        {"cpf": "11111111111", "recency": 1, "frequency": 2, "monetary": 1000, "time": 10},
        {"cpf": "22222222222", "recency": 2, "frequency": 3, "monetary": 1500, "time": 20},
        {"cpf": "33333333333", "recency": 3, "frequency": 4, "monetary": 2000, "time": 30},
        {"cpf": "44444444444", "recency": 4, "frequency": 5, "monetary": 2500, "time": 40},
        {"cpf": "55555555555", "recency": 5, "frequency": 6, "monetary": 3000, "time": 50},
        {"cpf": "66666666666", "recency": 6, "frequency": 7, "monetary": 3500, "time": 60},
        {"cpf": "77777777777", "recency": 7, "frequency": 8, "monetary": 4000, "time": 70},
        {"cpf": "88888888888", "recency": 8, "frequency": 9, "monetary": 4500, "time": 80},
        {"cpf": "99999999999", "recency": 9, "frequency": 10, "monetary": 5000, "time": 90},
        {"cpf": "10101010101", "recency": 10, "frequency": 11, "monetary": 5500, "time": 100},
        {"cpf": "12121212121", "recency": 11, "frequency": 12, "monetary": 6000, "time": 110},
        {"cpf": "13131313131", "recency": 12, "frequency": 13, "monetary": 6500, "time": 120}
    ]

    try:
        model_path = './predict_model/transfusion_frequency.pkl'
        modelo = ModelSchema.carrega_modelo(model_path)
    except Exception as e:
        print('Error ', e)
        return e

    for dados in dados_carga:
        novo_doador = Donator(
            cpf=dados['cpf'],
            recency=dados['recency'],
            frequency=dados['frequency'],
            monetary=dados['monetary'],
            time=dados['time'],
            outcome=ModelSchema.predicao(modelo, dados)
        )
        donator_insert(novo_doador)


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/swagger/novodoador', tags=[donator_tag])
def insert(form: DonatorSchema):
    """Insere um doador"""

    doadores = donator_show()

    form_dict = form.__dict__

    form_dict.pop('outcome', None)

    lista = []

    for i in doadores:
        lista.append(i['cpf'])
        

    try:
        model_path = './predict_model/transfusion_frequency.pkl'
        modelo = ModelSchema.carrega_modelo(model_path)
    except Exception as e:
        print("Error: ", e)
        return e

    try:
        doador = Donator(
            cpf=form.cpf,
            recency=form.recency,
            frequency=form.frequency,
            monetary=form.monetary,
            time=form.time,
            outcome=ModelSchema.predicao(modelo, form_dict)
        ) 

        cpf_doador = doador.cpf
        logger.debug(f"Adicionando doador de cpf: '{cpf_doador}'")
        
        if cpf_doador not in lista:
            result = donator_insert(doador)
            if result:
                return {"message": "Sucesso em inserir doador no banco de dados"}, 200
            else:
                return {"message": "Erro ao inserir doador"}, 500
        else:
            return {"message": "Doador duplicado"}, 421
    except Exception as e:
        # Capturar exceções inesperadas
        logger.exception(f"Erro inesperado ao inserir doador: {e}")
        return {"message": e}, 501
    
    
@app.delete('/swagger/deletedoador', tags=[donator_tag])
def delete(query: DonatorBuscaSchema):
    """Deleta um doador a partir do cpf de doador informado
    Retorna uma mensagem de confirmação da remoção.
    """

    doadores = []

    doadores.append(donator_show())

    lista = []

    for i in doadores:
        for j in i:
            doador = j['cpf']
            lista.append(doador)

    try:

        if query.cpf in lista:
            donator_delete(query.cpf)
            return {"message": "Doador removido", "cpf": query.cpf}
    except Exception as e:
        # se o doador não foi encontrado
        error_msg = "doador não encontrado na base :/"
        logger.warning(f"Erro ao deletar doador #'{query.cpf}', {e}")
        return {"message": error_msg}, 404
    
    
@app.get('/swagger/buscadoador', tags=[donator_tag])
def getter(query: DonatorBuscaSchema):
    """Encontra um doador a partir do cpf de doador informado
    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Coletando doador ")
    doadores = []
    doadores.append(donator_show())
   

    try:
        lista = []
        for i in doadores:
            for doador in i:
                doador_cpf = doador['cpf']
                lista.append(doador_cpf)
        if query.cpf in lista:
            return {"message": "doador encontrado", "cpf": query.cpf}
    except Exception as e:
        # se o doador não foi encontrado
        error_msg = " Doador não encontrado na base."
        logger.warning(f"Erro ao encontrar doador '{query.cpf}', {error_msg}")
        return {"message": error_msg}, 408

# Insere itens na tabela doador
@app.route('/doador/inserir', methods=['POST'])
def inserir_doador():
    """Insere itens na tabela doador"""

    doadores = donator_show()

    print(len(doadores) > 0)

    if len(doadores) < 1:
        carga_inicial()


    try:
        model_path = './predict_model/transfusion_frequency.pkl'
        modelo = ModelSchema.carrega_modelo(model_path)
    except Exception as e:
        print("Error: ", e)
        return e

    try:
        data = request.get_json()
        print(data)
        # Recebe os dados do front-end
        novo_doador = Donator(data['cpf'], 
                                data['recency'], 
                                data['frequency'], 
                                data['monetary'], 
                                data['time'], 
                                ModelSchema.predicao(modelo, data))
        resultado = donator_insert(novo_doador)
        if resultado:
            logger.debug(f"Inserindo doador {novo_doador.cpf}")
            return jsonify({'status': 200, 'message': 'Sucesso em inserir dados'})
        else:
            logger.error(f'Doador duplicado na base de dados: {novo_doador.cpf}')
            return jsonify({'error': f'Duplicidade em CPF'}), 409
    except Exception as e:
        logger.error(f"Erro ao inserir dados: {str(e)}")
        return jsonify({'error': f'Erro ao inserir dados: {str(e)}'}), 500

#Exibe os itens da tabela doador
@app.route('/doador/exibir', methods=['GET'])
def exibir_doador():
    """Exibe os itens da tabela doador"""
    try:
        dados = donator_show()
        return jsonify({'dados': dados}), 202
    except Exception as e:
        return jsonify({'error': 'Erro ao mostrar dados: ' + str(e)}), 500

# Deleta itens da tabela doador
@app.route('/doador/deletar/<cpf>', methods=['DELETE'])
def deletar_doador(cpf):
    """Deleta itens da tabela doador"""
    try:
        app.logger.info(f"Tentando excluir doador {cpf}")
        if donator_delete(cpf) == True:
            app.logger.info(f"doador {cpf} excluído com sucesso")
            return jsonify({"message": f'doador {cpf} deletado com sucesso'}), 200
        else:
            return jsonify({"error": f"doador {cpf} não encontrado"}), 404
    except Exception as e:
        app.logger.error(f"Erro ao excluir doador {cpf}: {str(e)}")
        return jsonify({"error": f"Erro ao excluir doador {cpf}: {str(e)}"}), 500
    
if __name__ == '__main__':
    # Inicia o servidor Flask
    app.run(port=5000, debug=True)
