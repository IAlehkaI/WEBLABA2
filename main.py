from fastapi import FastAPI
from presentation.api import router
from infrastructure.database import Base, engine
app = FastAPI(
    title="Новостной сайт",
    description="CRUD-сервис новостей с REST API и Swagger",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(router)