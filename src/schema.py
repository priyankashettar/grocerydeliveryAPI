from pydantic import BaseModel
from typing import Optional

class BaseCustomer(BaseModel):
    id:Optional[int]
    cust_name:str
    email:str
    password:str
    active_cust:Optional[bool]
    sales:Optional[bool]

    class Config:
        orm_mode=True
        schema_extra={
            'example':{
                "cust_name":"john",
                "email":"john@email.com",
                "password":"password",
                "active_cust":True,
                "sales":False
            }
        }

class JWT_Config(BaseModel):
    #import from secrets.token_hex()
    authjwt_secret_key:str='4717444db83ffe012d34c2dc2bf57211e982ce1366f65415bbaeb959c5578086'

class authenticate(BaseModel):
    cust_name:str
    password:str
    
   
class BaseOrder(BaseModel):
    ord_id:Optional[int]
    quantity: int
    order_status:Optional[str]="ORDER-PLACED"
    order_size:Optional[str]="SMALL"
    cust_id:Optional[int]

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "quantity":4,
                "order_size":"MEDIUM"
            }
        }


class BaseOrderStatus(BaseModel):
    order_status:Optional[str]="PENDING"

    class Config:
        orm_mode=True
        schema_extra={
            "example":{
                "order_status":"PENDING"
            }
        }        