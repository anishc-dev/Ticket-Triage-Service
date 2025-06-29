from fastapi import FastAPI
from endpoints.listener import router

app = FastAPI()

app.include_router(router)