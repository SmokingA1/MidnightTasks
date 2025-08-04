from fastapi import FastAPI

app = FastAPI(title="MidnightTashs")

@app.get("/", response_model=dict)
async def get_home():
    return {"data": "The first app path!"}