from fastapi import APIRouter # ajuda a criar as rotas
from workout_api.atleta.controller import router as atleta
from workout_api.categorias.controller import router as categorias
from workout_api.centro_treinamento.controller import router as centro_treinamento

api_router = APIRouter()

# primeira rota a ser criada, faz referência a atletas
api_router.include_router(atleta, prefix='/atletas', tag=['atletas'])

# segunda rota a ser criada, faz referência a categorias
api_router.include_router(categorias, prefix='/categorias', tag=['categorias'])

# terceira rota a ser criada, faz referência a centro de treinamentos
api_router.include_router(centro_treinamento, prefix='/centros_treinamento', tag=['centros_treinamento'])