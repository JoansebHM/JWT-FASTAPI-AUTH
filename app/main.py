from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_data():
    return {"message": "Hello world"}
