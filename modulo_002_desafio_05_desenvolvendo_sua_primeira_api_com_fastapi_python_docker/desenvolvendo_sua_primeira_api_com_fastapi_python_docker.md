# **5. Explorando o FastAPI na Prática com TDD**
Autor: Mário F. Apolinário

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marioapolinario8a54757712/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marioomapo)
## *Observação:* ⚠️
**Este material foi desenvolvido com o objetivo de fixar o conhecimento teórico da lição, e como resultado apresenta este resumo; da mesma forma, serve como guia de orientação para todo aquele que queira utilizar este material como consulta.**

**Este resumo é baseado na Apresentação do **Profa. Nayanna Nara** e na documentação do **Python**.** 
## *Objetivo geral:* 🎯
Este quinto módulo do curso trata do desenvolvimento de API's na prática utilizando linguagem Python, serão abordados aqui: 

## 5.2 Desenvolvendo sua Primeira API com FastAPI, Python e Docker
Construir uma API utilizando o framework **Python FastAPI**. A FastAPI é conhecido no meio dos DEV's como um framework rápido, performático, e prático. Este lab é focado em *handson*, as instruções vão estar no **read.me** dentro do repósitório, onde serão esboçados o que será construido e desenvolvido ao longo das aulas, bem como links das documentações que serão utilizadas tanto do FastAPI como do Pydentic.

### 5.2.1 Apresentação do Projeto e Instruções
### 5.2.2 Apresentação do Desafio
### 5.2.3 Criação de Schemas e Models - Entidade Atleta
#### a) Instalando a Pyenv

    pyenv --version # verificando a versão

#### b) Criando o Ambiente Virtual

    pyenv virtualenv 3.11.4 workoutapi
#### c) Ativando Ambiente

    pyenv activate workoutapi
#### d) Realizando as Instalações Básicas (FastAPI, Uvicorne - subir o servidor, sqlalchemy - ORM para rodar banco de dados, pydantic - fazer validações)

    pip install fastapi uvicorn sqlalchemy pydantic
#### e) Criando a pasta "workout_api"

+ criando o arquivo __init__.py ; este é utilizado para a modularização de pastas
+ criando o arquivo main.py

#### f) Subindo o servidor
Consultar o link: [FastAPI](fastapi.tiangolo.com/tutorial/first-steps/)

No arquivo main.py descreve-se as seguintes linhas de código:

    from fastapi import FastAPI

    app = FastAPI()

**nota**: Fazer com que o VSCODE reconheça o ambiente virtual que foi criado, de modo a reconhecer as importações;
#### g) Execultando (subindo) o Servidor 

    uvicorn workout_api.main:app --reload

**nota**: em seguida abrir o navegador e inserir o endereço => http://127.0.0.1:8000/docs

**nota**: criando arquivo **Makefile** (um facilitador para execusão dos comandos - comando grandes e extensos são substituidos por comandos simples e curtos)

    run:
	@uvicorn workout_api.main:app --reload
    # inserir no terminal o comando => make run

#### h) Criando os Schemas

+ criando a pasta atleta
    + __init__.py
    + schemas.py (serve para fazer as validações e também serializar os dados, ou seja, os dados que se necessitam aparecer no json de retorno passa pelos schemas)

    criando os atributos de nome até sexo: 

        from typing import Annotated
        from pydantic import BaseModel, Field, PositiveFloat

        class Atleta(BaseModel):
            nome: Annotated[str, Field(description='Nome do atleta', examples='Joao', max_length=50)]
            cpf: Annotated[str, Field(description='CPF do atleta', examples='12345678900', max_length=11)]
            idade: Annotated[int, Field(description='Idade do atleta', examples='25')]
            peso: Annotated[PositiveFloat, Field(description='Peso do atleta', examples='75.5')]
            altura: Annotated[PositiveFloat, Field(description='Altura do atleta', examples='1.70')]
            sexo: Annotated[str, Field(description='Gênero do atleta', examples='M', max_length=1)]

+ criando o arquivo models.py (na pasta atleta)

    [Basic Use — SQLAlchemy 2.0 Documentation - Table Configuration with Declarative](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html)

+ criando a pasta contrib, onde serão guardadas as coisas mais genéricas;
    + __init__.py
    + models.py

            # importando a declarative base do link anterior

            from sqlalchemy.orm import DeclarativeBase
            
            class Base(DeclarativeBase):
                pass    
#
    from uuid import uuid4
    from sqlalchemy import UUID
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    from sqlalchemy.dialects.postgresql import UUID as PG_UUID

    #classe Pai que os outros models irão herdar dela
    class BaseModel(DeclarativeBase):
        id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), default=uuid4, mullable=False)

### 5.2.4 Criação de Schemas e Models - Entidades Categoria e Centro de Treinamento

+ criando um base model para schemas.py na pasta contrib

        from pydantic import BaseModel
        class BaseSchema(BaseModel):
            class Config:
                extra = 'forbid'
                from_attributes = True

+ modificando schemas.py na pasta atleta

        from typing import Annotated
        from pydantic import Field, PositiveFloat

        from workout_api.contrib.schemas import BaseSchema

        class Atleta(BaseSchema):
            nome: Annotated[str, Field(description='Nome do atleta', examples='Joao', max_length=50)]
            cpf: Annotated[str, Field(description='CPF do atleta', examples='12345678900', max_length=11)]
            idade: Annotated[int, Field(description='Idade do atleta', examples='25')]
            peso: Annotated[PositiveFloat, Field(description='Peso do atleta', examples='75.5')]
            altura: Annotated[PositiveFloat, Field(description='Altura do atleta', examples='1.70')]
            sexo: Annotated[str, Field(description='Gênero do atleta', examples='M', max_length=1)]

+ criando schemas de categoria e de centro de treinamento
    + criando pasta categorias e dentro arquivos __init__.py e schemas.py
    + dentro do arquivo schemas.py

            from typing import Annotated
            from pydantic import Field
            from workout_api.contrib.schemas import BaseSchema

            class Categoria(BaseSchema):
                nome: Annotated[str, Field(description='Nome da categoria', examples='Scale', max_length=10)]

    + criando models.py dentro da pasta categorias

            from sqlalchemy import Integer, String
            from sqlalchemy.orm import Mapped, mapped_column
            from workout_api.contrib.models import BaseModel

            class CategoriaModel(BaseModel):
                __tablename__ = 'categorias'

                pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
                nome: Mapped[str] = mapped_column(String(50), nullable=False)
    
    + criando os relacionamentos entre models.py de atleta com models.py de categorias

            #criando o relacionamento de atleta com categoria

            categoria: Mapped['CategoriaModel'] = relationship(back_populates='atleta')
            categoria_id = Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))

            #criando o relacionamento de categoria com atleta

            atleta: Mapped['AtletaModel'] = relationship(back_populates='categoria')
    + criando pasta centro_treinamento
        + criando arquivo __init__.py, schemas.py, e models.py.
        + criando os relacionamentos entre models.py de atleta com models.py de centros_treinamento

                centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates='atleta')
            
                centro_treinamento_id = Mapped[int] = mapped_column(ForeignKey('centros_treinamento.pk_id'))

### 5.2.5 Utilização do Docker Compose e Configuração do Alembic

Inserindo o Docker Compose para trabalhar com o banco de dados.
+ criando o arquivo docker_compose.yml

        # em modo de desenvolvimento
        version: '3'
        services:
            db:
                image: postgres:11-alpine
                environment:
                    POSTGRES_PASSWORD: workout
                    POSTGRES_USER: workout
                    POSTGRES_DB: workout
                ports:
                    - '5432:5432'

+ subindo docker-compose, escrevendo no terminal:

        docker-compose up -d    #-d => logs ocultos em tempo real

+ verificando se está funcionando, escrevendo no terminal:

        docker ps

+ usando o programa DBeaver 23.1.3 para visualizar o banco de dados e como database é escolhido o PostgreSQL (carinha do elefante).

+ Instalando o Alembic, escrevendo no terminal:

        pip install alembic

+ Usando o Alembic, escrevendo no terminal:

        alembic init alembic

+ Criando arquivo requirements.txt, escrevendo no terminal:

        pip freeze > requirements.txt

**nota**: para que outra pessoa possa rodar/utilizar com os pacotes utilizados

+ Fazendo algumas alterações no arquivo alembic.ini (ajustando a conexão):

na linha 63: sqlalchemy.url = postgresql+asyncpg://workout:workout@localhost/workout

+ Instalando asyncpg, escrevendo no terminal:

        pip install asyncpg

+ Importando todos os bancos de dados para que env.py reconheça. Na pasta **contrib** cria-se uma pasta chamada **repository** e dentro desta cria-se um arquivi __init__.py, e models.py. Dentro de models.py serão importados os models, que serão utilizados depois.
        
        from workout_api.categorias.models import CategoriaModel
        from workout_api.atleta.models import AtletaModel
        from workout_api.centro_treinamento.models import CentroTreinamentoModel

+ Modificando o arquivo env.py, na pasta alembic (de modo a permitir a mudança de configurações síncronas para assíncronas):

        #models que serão tabelas no banco de dados (linha 9)
        from workout_api.contrib.models import BaseModel

        target_metadata = BaseModel.metadata #(linha 25)

        # (Foram realizadas diversas modificações)

+ adicionando um comando ao arquivo Makefile:

        create-migrations:
	        @PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

        run-migrations:
	        @PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head

+ testando o comando, no terminal:

        make create-migrations d='init_db'

**nota**: como resultado gera um arquivo migration, dentro da pasta alembic, e dentro da pasta versions

+ Rodando o Banco de Dados, no terminal:

        make run-migrations

### 5.2.6 Inserindo Configurações do Banco de Dados e Adicionando Settings
Criando Rotas e end-points.
+ Criando arquivo **controller.py** na pasta atleta, de modo a se obter a mesma importação;
        
        from fastapi import APIRouter

        api_router = APIRouter()

+ Criando arquivo **routers.py** na raiz.
    
   No FastApi tem-se a importação API routers, ela ajuda a criar as rotas;

        from fastapi import APIRouter
        from workout_api.atleta.controller import router as atleta

        api_router = APIRouter()

# primeira rota a ser criada, faz referência a atleta
api_router.include_router(atleta, prefix='/atletas', tag=['atletas'])
+ Instalando novo pacote do pydantic, e ajustando configurações, escrevendo no terminal:

        pip install pydantic-settings
+ Criando uma pasta **configs**, adicionando dentro um arquivo __init__.py, e outro settings.py, e dentro deste segundo são apresentadas as seguintes linhas de código:

        from pydantic_settings import BaseSettings
        from pydantic import Field

        class Settings(BaseSettings):
        DB_URL: str = Field(default='postgresql+asyncpg://workout:workout@localhost/workout')

        settings = Settings()
+ Criando dependências, para isto, criando arquivo **database.py** dentro da pasta configs:

        from typing import AsyncGenerator

        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
        from sqlalchemy.orm import sessionmaker

        from workout_api.configs.settings import settings

        engine = create_async_engine(settings.DB_URL, echo=False)

        async_session = sessionmaker(
            engine, class_ = AsyncSession, expire_on_commit=False 
        )       

        async def get_sessiont() -> AsyncGenerator:
            async with async_session() as session:
                yield session
+ Incluindo rotas, abrir o arquivo **main.py**, e adicionando algumas linhas.

        from workout_api.routers import api_router

        app.include_router(api_router)
+ Fazendo com que o Post se comunique com o banco de dados, e neste momento usa-se a sessão, ver arquivo **controller.py**:

        s
+ Criando o arquivo **dependencies.py** na pasta contrib:

        from typing import Annotated
        from fastapi import Depends
        from sqlalchemy.ext.asyncio import AsyncSession

        from workout_api.configs.database import get_session

        DatabaseDependency = Annotated[AsyncSession, Depends(get_session)]

+ Criando um Schema de inserção no arquivo **schemas.py** na pasta atleta:
        
        class AtletaIn(Atleta):

+ Tipando (os dados que vão entrar para criar o atleta, eles serão exatamente os dados que estão no schema e que possuem a validação no schema de inserção) no **controller.py** na pasta atleta:

+ Criando um BaseSchemaOut chamado de OutMixin na pasta contrib e no arquivo **schemas.py**

        class OutMixin(BaseSchema):
                id: Annotated[UUID4, Field(description='Identificador')]
                created_at: Annotated[datetime, Field(description='Data de criação')]

+ Criando um Schema AtletaOut no arquivo **schemas.py** na pasta atleta:       
        
        class AtletaOut(Atleta, OutMixin):

### 5.2.7 Criação das Rotas de Categoria
Dando continuidade a construção dos **end-points**.
+ Criando arquivo **controller.py** na pasta categorias:

        from fastapi import APIRouter, Body, status
        from workout_api.categorias.schemas import CategoriaIn
        from workout_api.contrib.dependencies import DatabaseDependency

        router = APIRouter()

        @router.post(
                path='/',
                summary=' Criar uma nova Categoria',
                status_code=status.HTTP_201_CREATED)

        async def post(
                db_session: DatabaseDependency,
                categoria_in: CategoriaIn = Body(...)
                ) -> CategoriaOut:

                categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
                categoria_model = CategoriaModel(**categoria_out.model_dump())

+ Criando um schema Out para categoria no **schemas.py** na pasta categorias:

        class CategoriaOut(CategoriaIn):
                id: Annotated[UUID4, Field(description='Identificador da categoria')]

+ Criando rota no arquivo **routers.py** na raiz:

        from workout_api.categorias.controller import router as categorias

        api_router.include_router(categorias, prefix='/categorias', tag=['categorias'])

+ Para evitar o erro de importação circular devido a importação das bibliotecas nos arquivos **models.py** (AtletaModel, CategoriaModel, CentroTreinamentoModel), agora as importações são realizadas no arquivo **__init__.py** na raíz:

        from workout_api.categorias.models import CategoriaModel
        from workout_api.centro_treinamento.models import CentroTreinamentoModel
        from workout_api.atleta.models import AtletaModel

+ Adicionando novos campos ao arquivo **controller.py** na pasta categorias, criando db_sessions e a rota **.get**:

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

        async def query(
                db_session: DatabaseDependency,
                ) -> list[CategoriaOut]:
                categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all() #pega todos os dados
                return categorias        

        @router.get(
                path='/{id}',
                summary=' Consulta uma Categoria pelo id',
                status_code=status.HTTP_200_OK, 
                response_model = CategoriaOut,
        )

        async def query(
                id: UUID4,      
                db_session: DatabaseDependency,
                ) -> CategoriaOut:
                categoria: CategoriaOut = (
                        await db_session.execute(select(CategoriaModel).filter_by(id=id))
                        ).scalars().first() # aqui haverá um filtro (filter(), ou filter_by()), sendo o primeiro que for encontrado
        
                if not categoria:
                        raise HTTPException( # retornando uma exceção
                                status_code=status.HTTP_404_NOT_FOUND, # devolvendo um código informando que não tem
                                detail = f'Categoria não encontrada no id: {id}'        
                                )
                return categoria   

### 5.2.8 Criação das Rotas de Centro de Treinamento

+ Criando um Out no arquivo **schemas.py** na pasta centro de treinamento:

        class CentroTreinamentoOut(CentroTreinamentoIn):
        id: Annotated[UUID4, Field(description='Identificador do centro de treinamento')]

+ Criando arquivo **controller.py** na pasta centro de treinamento:

        from uuid import uuid4
        from fastapi import APIRouter, Body, HTTPException, status
        from pydantic import UUID4
        from sqlalchemy.future import select
        from workout_api.centro_treinamento.models import CentroTreinamentoModel
        from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut

        from workout_api.contrib.dependencies import DatabaseDependency

        router = APIRouter()

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

+ Criando uma nova rota no arquivo **routers.py** na raiz:

        from workout_api.centro_treinamento.controller import router as centro_treinamento

        api_router.include_router(centro_treinamento, prefix='/centros_treinamento', tag=['centros_treinamento'])


### 5.2.9 Criação das Rotas de Atleta - Parte 1

**Nota**: o atleta possui o campo **creted_ad** que foi herdado de **OutMixim**, ao contrário de categorias e centro_treinamento:
+ Adicionando ao arquivo **schemas.py** de atleta os campos que faltavam:

        from workout_api.categorias.schemas import CategoriaIn
        from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta

        categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')] # retorna a categoria
        centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')] # retorna o centro de treinamento

+ Modificando o **post** no arquivo **controller.py** de atleta:



### 5.2.10 Criação das Rotas de Atleta - Parte 2
+ Criando um schema AtletaUpdate no arquivo **schemas.py** na pasta centro de atleta:

        class AtletaUpdate(BaseSchema):
                nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Joao', max_length=50)]
                idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example='25')]

+ Criando o **get** no arquivo **controller.py** de atleta:

        dk


### 5.2.11 Consumindo API com Postman


### 5.2.12 Conclusão




## *Links de Úteis* 🌐

### 1. [O que é um banco de dados relacional (RDBMS)?](https://www.oracle.com/br/database/what-is-a-relational-database/)

### 2. [SQL Tutorial](www.sqltutorial.org/)

### 3. [Criando Diagramas Entidade-Relacionamento](https://app.creately.com/)

### 4. [Criando Diagramas Entidade-Relacionamento com IA](https://app.quickdatabasediagrams.com)

### 5. [Banco de Dados](https://clients.cloudclusters.io/)

### 6. [O que é um diagrama entidade relacionamento?](https://www.lucidchart.com/pages/pt/o-que-e-diagrama-entidade-relacionamento)

### 7. [mariadb data-types](https://mariadb.com/kb/en/data-types/)

### 8. [mariadb create-table](https://mariadb.com/kb/en/create-table/)

### 9. [Formas Normais](https://pt.wikipedia.org/wiki/Normaliza%C3%A7%C3%A3o_de_dados)

### 10. [Scripts Hands On](https://github.com/pamelaborges/dio-bd-relacional)

### 11. [Mariadb joins](https://mariadb.com/kb/en/joins/)

### 12. [Mariadb Funções Agregadoras](https://mariadb.com/kb/en/aggregate-functions/)

### 13. [Mariadb Índice](https://mariadb.com/kb/en/alter-table/#add-index)