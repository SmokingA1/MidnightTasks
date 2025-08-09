from fastapi import FastAPI

from app.api.main import router

app = FastAPI(title="MidnightTashs")
app.include_router(router=router)

@app.get("/", response_model=dict)
async def get_home():
    return {"data": "The first app path!"}