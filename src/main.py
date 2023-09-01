from fastapi import FastAPI
from src.router_auth import router_auth
from src.router_order import router_order
import src.service as _service
import src.db as _db
from fastapi_jwt_auth import AuthJWT
import src.schema as _sm
import inspect, re
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi


session=_db.Session(bind=_db.db_engine)
_service.add_schema()
 

app=FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "Order Delivery Service",
        version = "1.0",
        description = "An order delivery service API",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required()
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@AuthJWT.load_config
def get_config():
    return _sm.JWT_Config() 

app.include_router(router_auth)
app.include_router(router_order)


