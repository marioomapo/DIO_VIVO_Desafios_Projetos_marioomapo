from typing import Annotated
from pydantic import UUID4, BaseModel, Field
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True

        # forbid => não aceita campos extras
        # from_attributes => fazendo a conversão de schemas para model, ou vice versa

# responsável por devolver dois campos: Id, e created_at
class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description='Identificador')]
    created_at: Annotated[datetime, Field(description='Data de criação')]