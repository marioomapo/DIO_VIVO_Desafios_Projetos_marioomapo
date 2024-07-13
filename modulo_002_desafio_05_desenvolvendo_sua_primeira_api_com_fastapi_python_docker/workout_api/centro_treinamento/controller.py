from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut

from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

# criando a rota
@router.post(
        path='/',
        summary=' Criar um novo Centro de Treinamento',
        status_code=status.HTTP_201_CREATED,
        response_model = CentroTreinamentoOut,
        )

async def post(
        db_session: DatabaseDependency,
        centro_treinamento_in: CentroTreinamentoIn = Body(...)
        ) -> CentroTreinamentoOut:      #tipando

        # criando uma instancia de CategoriaOut (o usuário ñ tem controle sobre o Id, este é atribuido no código)
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump())

        # criando db_session
        db_session.add(centro_treinamento_model)
        await db_session.commit() # comando await utilizado para o caso de async
        
        return centro_treinamento_out

# criando a rota
@router.get(
        path='/',
        summary=' Consultar todos os Centros de Treinamento',
        status_code=status.HTTP_200_OK,
        response_model = list[CentroTreinamentoOut], #retorna uma lista
        )

async def query(
        db_session: DatabaseDependency,
        ) -> list[CentroTreinamentoOut]:
        centros_treinamento_out: list[CentroTreinamentoOut] = (
                await db_session.execute(select(CentroTreinamentoModel))
                ).scalars().all() #retorna todos os dados da lista
        
        return centros_treinamento_out        

# criando a rota para id
@router.get(
        path='/{id}',
        summary=' Consulta um Centro de Treinamento pelo id',
        status_code=status.HTTP_200_OK, 
        response_model = CentroTreinamentoOut,
        )

async def query(
        id: UUID4,      
        db_session: DatabaseDependency,
        ) -> CentroTreinamentoOut:
        centro_treinamento_out: CentroTreinamentoOut = (
                await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)) # DICA!!! (id=id, campo1, campo2, campo n) adicionando outros campos para filtragem 
                ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
        # no caso, se for passado uma outra string que não obedece o formado Id
        if not centro_treinamento_out:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                        detail = f'Centro de treinamento não encontrado no id: {id}'        
                        )

        return centro_treinamento_out