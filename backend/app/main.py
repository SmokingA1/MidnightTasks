from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.main import router
from app.core import redis as redis_module

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_module.init_redis() # initializate redis(None) -> redis(Session)
    assert redis_module.redis is not None # but if redis is None yet, we closing?
    print(redis_module.redis)
    print("Redis successfully innitializated!")

    yield 
    await redis_module.close_redis()
    print("Connectino closed successfully!")


app = FastAPI(title="MidnightTashs", lifespan=lifespan)
app.include_router(router=router)

@app.get("/", response_model=dict)
async def get_home():
    return {"data": "The first app path!"}
