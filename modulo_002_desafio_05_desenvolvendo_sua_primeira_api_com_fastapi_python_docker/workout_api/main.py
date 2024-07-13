from fastapi import FastAPI
from workout_api.routers import api_router
# ******************************************
# Adicionando Paginação - fastapi_pagination
# ******************************************
from fastapi_pagination import LimitOffsetPage, add_pagination, paginate

app = FastAPI(title = 'WorkoutApi')
add_pagination(app)

app.include_router(api_router)

######## este campo não é necessário, em vista do Makefile
#if __name__ == 'main':  #subindo o servidor
#    import uvicorn  #importando a lib do uvicorn

#    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level='info', reload=True )
    #log_level >> parâmetro que informa a maneira como será logado em nosso terminal
    #reload=True >> caso alguma alteração no código seja realizada, não é necessário parar o servidor, reinicia automaticamente
#############################################
