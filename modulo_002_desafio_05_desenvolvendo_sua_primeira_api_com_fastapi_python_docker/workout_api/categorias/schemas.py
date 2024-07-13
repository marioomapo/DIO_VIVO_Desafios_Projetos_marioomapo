from typing import Annotated
from pydantic import UUID4, Field
from workout_api.contrib.schemas import BaseSchema

# Criando um 'schema In' parta categoria
class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]

# Criando um 'schema out' parta categoria (para devolver nome e categoria)
class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description='Identificador da categoria')]