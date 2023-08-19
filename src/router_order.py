from fastapi import APIRouter #, Depends
#from fastapi_jwt_auth import AuthJWT
from src.models import Customer,Order
from src.schema import BaseOrder

router_order= APIRouter(
    prefix='/order',
    tags=['order']
)


@router_order.get('/')
async def hello():
    return{"message":"hello from order!!!"}
