from fastapi import FastAPI

from controller.clientes import router

app = FastAPI(
    title="Mercearia - API de Clientes",
    description="CRUD de clientes com PostgreSQL local.",
    version="1.0.0",
)

app.include_router(router)