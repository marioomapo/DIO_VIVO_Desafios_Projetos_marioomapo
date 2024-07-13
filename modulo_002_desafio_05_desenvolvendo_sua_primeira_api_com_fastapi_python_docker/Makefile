# **nota**: criando arquivo **Makefile** (um facilitador para execusão dos comandos - comando grandes e extensos são substituidos por comandos simples e curtos)

run:
	@uvicorn workout_api.main:app --reload

create-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic revision --autogenerate -m $(d)

run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(pwd) alembic upgrade head