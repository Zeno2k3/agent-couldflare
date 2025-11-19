from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World từ FastAPI + uv!"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Chào {name}!"}