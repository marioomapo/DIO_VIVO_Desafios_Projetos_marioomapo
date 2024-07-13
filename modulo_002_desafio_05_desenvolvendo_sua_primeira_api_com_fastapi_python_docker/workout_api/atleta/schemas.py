# usado para fazer validações e serializar os dados na API naquele .json de retorno
from typing import Annotated, Optional
from pydantic import Field, PositiveFloat
from workout_api.categorias.schemas import CategoriaIn
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta
from workout_api.contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do atleta', example='25')]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example='75.5')]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example='1.70')]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')] # retorna a categoria
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')] # retorna o centro de treinamento

class AtletaIn(Atleta):
    pass

#**********************************************************************************************
# Customizar response de retorno de endpoingts (retorna: nome, centro de treinamento, categoria)
#**********************************************************************************************
class AtletaOut(Atleta, OutMixin):
    nome: Annotated[str, Field(description='Nome do atleta', example='Joao', max_length=50)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

# schema utilizado para edição dos campos nome e idade
class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example='25')]