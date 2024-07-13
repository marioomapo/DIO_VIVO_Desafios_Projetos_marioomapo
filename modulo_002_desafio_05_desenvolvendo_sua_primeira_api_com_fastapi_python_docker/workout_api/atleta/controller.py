from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

# criando a rota
@router.post(
        path='/',
        summary=' Criando um novo atleta',
        status_code=status.HTTP_201_CREATED,
        response_model=AtletaOut
        )

async def post(
        db_session: DatabaseDependency,
        atleta_in: AtletaIn = Body(...)
        ):

        categoria_nome = atleta_in.categoria.nome
        centro_treinamento_nome = atleta_in.centro_treinamento.nome

        categoria = (await db_session.execute(
                select(CategoriaModel).filter_by(nome=categoria_nome)) # o filtro será em função do nome da categoria
                ).scalars().first() #pega o primeiro dado

        if not categoria:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_BAD_REQUEST, # A requisição não foi processada
                        detail = f'A categoria {categoria_nome} não foi encontrada.'        
                        )
        
        centro_treinamento = (await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome)) # o filtro será em função do nome da categoria
                ).scalars().first() #pega o primeiro dado

        if not centro_treinamento:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_BAD_REQUEST, # A requisição não foi processada
                        detail = f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'        
                        )

        # Corrigindo o problema do campo CPF que é unico por usuário cadastrado
        try: 
                atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
                atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'})) # caso não exista comando exclude => erro 'dict' object has not attribute

                atleta_model.categoria_id = categoria.pk_id # relacionando o dado
                atleta_model.centro_treinamento_id = centro_treinamento.pk_id # relacionando o dado

                # criando db_session
                db_session.add(atleta_model)
                await db_session.commit() # comando await utilizado para o caso de async
        
        #******************************************************************
        # Manipulando exceção de integridadedos dados em cada modulo/tabela
        #******************************************************************

        except Exception: # DICA!!! a idéia do desafio é manipular a exception para uma situação mais próxima do erro proposto
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_303_SEE_OTHER, # A requisição não foi processada
                        detail = f'Já existe um atleta cadastrado com o CPF: {atleta_in.cpf.nome}'        
                        )
        
        return atleta_out


@router.get(
        path='/',
        summary=' Consulta todos os Atletas',
        status_code=status.HTTP_200_OK,
        response_model = list[AtletaOut], #retorna uma lista
        )

        # *************************************************************************************************
        # Adicionar query parameters nos endpoints (-get all) =>filtrando por nome e por cpf **************
        # *************************************************************************************************
async def query(db_session: DatabaseDependency,
                atleta_in: AtletaIn = Body(...)
                ) -> list[AtletaOut]:

        filtro_nome = atleta_in.nome.nome # filtrando por nome
        filtro_cpf =  atleta_in.cpf.nome # filtrando por cpf
                
        atletas: list[AtletaOut] = (
                await db_session.execute(select(AtletaModel).filter_by(nome= filtro_nome, nome = filtro_cpf))
                ).scalars().first() #filtra pelo nome e pelo cpf
        
        return [AtletaOut.model_validate(atleta) for atleta in atletas]  #convertendo de model para schema, permitindo assim renderizar os dados

        # erro MissingGreenLet => ocorre quando não existe união entre os dados das tabelas, 
        # no caso a tabela atleta necessita dos dados das tabelas categoria e centro de treinamento
        # quando existe necessidade da consulta dos dados dos diverso atletas
        # isto pode ser evitado inserindo o parâmetro lazy = 'selectin' para a união de tabelas, adicionado ao model de atleta


@router.get(
        path='/{id}',
        summary=' Consulta um Atleta pelo id',
        status_code=status.HTTP_200_OK, 
        response_model = AtletaOut,
        )

async def query(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
        # no caso, se for passado uma outra string que não obedece o formado Id
        if not atleta:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                        detail = f'Atleta não encontrado no id: {id}')
        return atleta

# adicionando End-Point patch (utilizado para a edição de dados dinâmicamente)
@router.patch(
        path='/{id}',
        summary=' Editar um Atleta pelo id',
        status_code=status.HTTP_200_OK, 
        response_model = AtletaOut)

async def query(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
        if not atleta:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                        detail = f'Atleta não encontrado no id: {id}')
        
        atleta_update = atleta_up.model_dump(exclude_unset=True) # atualizar alguns campos
        for key, value in atleta_update.items(): # realiza a aquisição de novos valores
                setattr(atleta, key, value)

        await db_session.commit()  # comitando
        await db_session.refresh(atleta) # refresh

        return atleta


# adicionando End-Point delete (utilizado para deletar dados dinâmicamente)
@router.delete(
        path='/{id}',
        summary=' Deletar um Atleta pelo id',
        status_code=status.HTTP_204_NO_CONTENT)

async def query(id: UUID4, db_session: DatabaseDependency) -> None:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
        # no caso, se for passado uma outra string que não obedece o formado Id
        if not atleta:
                raise HTTPException( # retornando uma exceção
                        status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                        detail = f'Atleta não encontrado no id: {id}')
        
        await db_session.delete(atleta)  # deletando
        await db_session.commit() # commita