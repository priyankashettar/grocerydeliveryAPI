from fastapi import FastAPI
from src.router_auth import router_auth
from src.router_order import router_order
import src.service as _service
import src.db as _db
from fastapi_jwt_auth import AuthJWT
import src.schema as _sm


#DATABASE_URL = "postgresql+psycopg2://dev:dev@order-delivery-db:5432/order-delivery-db"
#DATABASE_URL = "postgresql+psycopg2://dev:dev@localhost:5432/order-delivery-db"
#db_engine=create_engine(DATABASE_URL,echo=True)
session=_db.Session(bind=_db.db_engine)
_service.add_schema()
 

app=FastAPI()

@AuthJWT.load_config
def get_config():
    return _sm.JWT_Config() 

app.include_router(router_auth)
app.include_router(router_order)


