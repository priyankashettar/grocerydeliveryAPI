from fastapi import FastAPI
from router_auth import router_auth
from router_order import router_order

app=FastAPI()

app.include_router(router_auth)
app.include_router(router_order)