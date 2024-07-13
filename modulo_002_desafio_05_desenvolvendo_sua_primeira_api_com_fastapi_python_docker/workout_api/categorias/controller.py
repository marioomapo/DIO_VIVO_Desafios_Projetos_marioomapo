from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.categorias.models import CategoriaModel
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut

from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

# criando a rota
@router.post(
        path='/',
        summary=' Criar uma nova Categoria',
        status_code=status.HTTP_201_CREATED,
        response_model = CategoriaOut,
        )

async def post(
        db_session: DatabaseDependency,
        categoria_in: CategoriaIn = Body(...)
        ) -> CategoriaOut:      #tipando

        # criando uma instancia de CategoriaOut (o usuário ñ tem controle sobre o Id, este é atribuido no código)
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump())

        # criando db_session
        db_session.add(categoria_model)
        await db_session.commit() # comando await utilizado para o caso de async
        
        return categoria_out

# criando a rota
@router.get(
        path='/',
        summary=' Consultar todas as Categorias',
        status_code=status.HTTP_200_OK,
        response_model = list[CategoriaOut], #retorna uma lista
        )

async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
        categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all() #pega todos os dados
        return categorias        

# criando a rota para id
@router.get(
        path='/{id}',
        summary=' Consulta uma Categoria pelo id',
        status_code=status.HTTP_200_OK, 
        response_model = CategoriaOut,
        )

async def query(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut:
        categoria: CategoriaOut = (
                await db_session.execute(select(CategoriaModel).filter_by(id=id))
                ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
        # no caso, se for passado uma outra string que não obedece o formado Id
        if not categoria:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                        detail = f'Categoria não encontrada no id: {id}'        
                        )

        return categoria   