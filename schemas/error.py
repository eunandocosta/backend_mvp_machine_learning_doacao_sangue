from pydantic import BaseModel

class DonatorErrSchema(BaseModel):
    """ Exibe mensagem de erro
    """
    message: str
    erro: str
