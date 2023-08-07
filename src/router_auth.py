from fastapi import APIRouter

router_auth= APIRouter()


@router_auth.get('/')
async def hello():
    return{"message":"hello!!!"}