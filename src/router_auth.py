from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from src.db import Session,db_engine
from src.schema import BaseCustomer, authenticate
from src.models import Customer
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


router_auth= APIRouter(
    prefix='/auth',
    tags=['auth']
)

session=Session(bind=db_engine)    

@router_auth.get('/')
async def hello(authorize:AuthJWT=Depends()):
    """
        ##Welcome Message
    """
    try:
        authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token!!")
    
    return{"message":"hello!!!"}


@router_auth.post('/signup',response_model=BaseCustomer,status_code=status.HTTP_201_CREATED)
async def signup(customer:BaseCustomer):
    """
        ##Signup Page
        Customer needs to signup first providing the following details
        - cust_name: string
        - email: string
        - password: text
        - active_cust: bool
        - sales: bool
    """
    print("Inside Signup!")
    email_auth=session.query(Customer).filter(Customer.email==customer.email).first()
    
    print("Logged in !!")
    if email_auth is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists!")
    
    cust_name_auth=session.query(Customer).filter(Customer.cust_name==customer.cust_name).first()
    if cust_name_auth is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="customer with this name already exists!")
    
    print("Generating New Customer details !")
    new_cust=Customer(
        cust_name=customer.cust_name,
        email=customer.email,
        password=generate_password_hash(customer.password),
        active_cust=customer.active_cust,
        sales=customer.sales
    )

    print("Adding New Customer")
    session.add(new_cust)

    print("Committing New Customer")
    session.commit()

    return new_cust


#authentication route
@router_auth.post('/login', status_code=200)
async def login(customer:authenticate,authorize:AuthJWT=Depends()):
    """
        ##Login for authentication with cust_name and password
    """
    db_cust=session.query(Customer).filter(Customer.cust_name==customer.cust_name).first()
    if db_cust and check_password_hash(db_cust.password, customer.password):
        access_token=authorize.create_access_token(subject=db_cust.cust_name)
        refresh_token=authorize.create_refresh_token(subject=db_cust.cust_name)

        response={
            "access":access_token,
            "refresh":refresh_token
        }

        return jsonable_encoder(response)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password!!")


#Refresh JWT token
@router_auth.get('/refresh')
async def token_refresh(authorize:AuthJWT=Depends()):
    """
        ##JWT token refresh to access the encrypted endpoints
    """
    try:
        authorize.jwt_refresh_token_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token refresh required!!")    
    
    current_customer=authorize.get_jwt_subject()

    access_token=authorize.create_access_token(subject=current_customer)

    return jsonable_encoder({"access":access_token})

