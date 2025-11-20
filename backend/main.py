from fastapi import FastAPI
from router import router_user

app = FastAPI()

app.include_router(router_user)