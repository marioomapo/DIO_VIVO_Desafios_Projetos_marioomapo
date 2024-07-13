from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

# Criando o In
class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]
    endereco: Annotated[str, Field(description='Endereço do centro de treinamento', example='Rua Y, Q01', max_length=60)]
    proprietario: Annotated[str, Field(description='Proprietário do centro de treinamento', example='Marcos', max_length=30)]

# Criando o Out
class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do centro de treinamento', example='CT King', max_length=20)]

