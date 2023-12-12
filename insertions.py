from schemas.donator_schema import Donator

from typing import List

from schemas.donator_schema import Donator
from typing import List

from schemas.donator_schema import *
from predict_model import *

from model.__init__ import donator_insert

from schemas.donator_schema import *

def apresenta_doador(doador: Donator):
    """ Retorna uma representação do produto seguindo o schema definido em
        DonatorSchema.
    """
    return {
        "cpf": doador.cpf,
        "autor": doador.autor,
        "descricao": doador.descricao,
        "valor": doador.valor,
        "estoque": doador.estoque
    }

def apresenta_doadores(doador: List[Donator]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for doadores in doador:
        result.append({
            "cpf": doadores.cpf,
            "autor": doadores.autor,
            "descricao": doadores.descricao,
            "valor": doadores.valor,
            "estoque": doadores.estoque
        })

    return {"doadores": result}

def insere_doador(donator: Donator):
    """ Retorna uma representação do doador.
    """
    return {
        "cpf" : donator.cpf,
        "recency" : donator.recency,
        "frequency" : donator.frequency,
        "monetary" : donator.monetary,
        "time" : donator.time,
    }

"""""Carga inicial"""""