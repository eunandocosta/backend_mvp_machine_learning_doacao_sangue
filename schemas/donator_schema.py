from pydantic import BaseModel
import pickle
import numpy as np
from typing import Optional, Union

class Donator:

    cpf: int
    recency: int
    frequency: int
    monetary: int
    time: int
    outcome: int

    

    def __init__(self, cpf, recency, frequency, monetary, time, outcome):

        self.cpf = cpf
        self.recency = recency
        self.frequency = frequency
        self.monetary = monetary
        self.time = time
        self.outcome = outcome

    def __str__(self):
        return f"cpf: {self.cpf}, recency: {self.recency}, frequency: {self.frequency}, monetary: {self.monetary}, time: {self.time}, outcome: {self.outcome}"

class formSchema:
    cpf: int = 00000000000
    recency: int = 1
    frequency: int = 4
    monetary: int = 2000
    time: int = 5

class DonatorSchema(BaseModel):
    """ Define classe Donator: Donator .
    """
    cpf: int = 00000000000
    recency: int = 1
    frequency: int = 4
    monetary: int = 2000
    time: int = 5
    outcome: int = 0
    

class DonatorViewSchema(BaseModel):
    cpf: int = 0
    recency: int = 1
    frequency: int = 4
    monetary: int = 2000
    time: int = 5
    outcome: Optional[int] = None

    


class DonatorBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do doador.
    """
    cpf: int = 00000000000

class DonatorDeleteSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    cpf: int

class ModelSchema:

    @staticmethod
    def carrega_modelo(caminho):
        if caminho.endswith('.pkl'):
            with open(caminho, 'rb') as file:
                model = pickle.load(file)
        else:
            raise Exception("Formato de modelo de predição não suportado")
        return model

    @staticmethod
    def predicao(model, form):
        # Ensure form.outcome is set to a default value if it is None
        outcome_value = form.get('outcome', 0)

        x_input = np.array([form['recency'], form['frequency'], form['monetary'], form['time']])

        print(model)

        diagnostico = model.predict(x_input.reshape(1, -1))
        return int(diagnostico[0])
    
    