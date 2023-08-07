from fastapi import APIRouter

router_order= APIRouter()


@router_order.get('/')
async def hello():
    return{"message":"hello from order!!!"}