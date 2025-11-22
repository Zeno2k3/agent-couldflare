from fastapi import FastAPI
from router import router_user
from router import router_chat

app = FastAPI()

app.include_router(router=router_user)
app.include_router(router=router_chat)