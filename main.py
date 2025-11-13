from fastapi import FastAPI
from presentation.api import router

app = FastAPI(
    title="Новостной сайт",
    description="CRUD-сервис новостей с REST API и Swagger",
    version="1.0.0"
)

app.include_router(router)