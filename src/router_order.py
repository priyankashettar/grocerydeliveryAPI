from fastapi import APIRouter , Depends, status
from fastapi_jwt_auth import AuthJWT
from src.models import Customer,Order
from src.schema import BaseOrder,BaseOrderStatus
from fastapi.exceptions import HTTPException
from src.db import Session,db_engine
from fastapi.encoders import jsonable_encoder

router_order= APIRouter(
    prefix='/order',
    tags=['order']
)

session=Session(bind=db_engine)

@router_order.get('/')
async def hello(Authorize:AuthJWT=Depends()):
    """
        ##Welcome Message
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        )
    return{"message":"hello from order!!!"}


@router_order.post('/order',status_code=status.HTTP_201_CREATED)
async def make_order(order:BaseOrder, Authorize:AuthJWT=Depends() ):
    """
        ##Placing a new order, you will need to specify following details:
        - order_size: string
        - quantity: int
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        )    
    current_customer=Authorize.get_jwt_subject()
    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()


    new_order=Order(
        order_size=order.order_size,
        quantity=order.quantity
    )

    new_order.owner=customer

    session.add(new_order)

    session.commit()

    response={
        "order_size":new_order.order_size,
        "quantity":new_order.quantity,
        "order_id":new_order.ord_id,
        "order_status":new_order.order_status
    }

    return jsonable_encoder(response)

@router_order.get('/orders')
async def show_orders(Authorize:AuthJWT=Depends()):
    """
        ##Lists all the orders placed by the customers
        this requires sales access to view the list.
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        )
    
    current_customer=Authorize.get_jwt_subject()
    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()

    if customer.sales:
        orders=session.query(Order).all()
        
        return jsonable_encoder(orders)
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only sales team can access this option!!"
        )


@router_order.get('/orders/{id}')
async def show_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
        ##Shows the order details by id,
        this has only sales access
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        )
    
    current_customer=Authorize.get_jwt_subject()
    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()

    if customer.sales:
        order=session.query(Order).filter(Order.ord_id==id).first()
        
        return jsonable_encoder(order)
    
    raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only sales team can access this option!!"
        )


@router_order.get('/customer/orders/{id}/')
async def show_cust_orders(id:int,Authorize:AuthJWT=Depends()):
    """
        ##Shows specific customer orders by id
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        ) 
    current_customer=Authorize.get_jwt_subject()
    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()
    order=customer.orders
    for ord in order:
        if ord.ord_id == id:
            return jsonable_encoder(ord)
        
    raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No orders!!"
        )    



@router_order.put('/order/update/{id}/')
async def update_order(id:int,order:BaseOrder,Authorize:AuthJWT=Depends()):
    """
        ##Allows you to change the order details by id
        requires order_size and quantity
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        ) 
    
    change_order=session.query(Order).filter(Order.ord_id==id).first()

    change_order.order_size=order.order_size

    change_order.quantity=order.quantity

    session.commit()

    response={
                "id":change_order.ord_id,
                "quantity":change_order.quantity,
                "order_size":change_order.order_size,
                "order_status":change_order.order_status,
            }

    return jsonable_encoder(change_order)



@router_order.patch('/order/update/{id}/')
async def update_order_status(id:int, order:BaseOrderStatus, Authorize:AuthJWT=Depends()):
    """
        ##Allows you to change the order status by id
        this requires order_status
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Token")

    current_customer=Authorize.get_jwt_subject()

    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()

    if customer.sales:
        change_order=session.query(Order).filter(Order.ord_id==id).first()

        change_order.order_status=order.order_status

        session.commit()

        response={
                "id":change_order.ord_id,
                "quantity":change_order.quantity,
                "order_size":change_order.order_size,
                "order_status":change_order.order_status,
            }

        return jsonable_encoder(response)




@router_order.delete('/orders/delete/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
        ##Allows you to delete the order by id
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token!!"
        )
    
    current_customer=Authorize.get_jwt_subject()
    customer=session.query(Customer).filter(Customer.cust_name==current_customer).first()

    delete_order=session.query(Order).filter(Order.ord_id==id).first()
        
    session.delete(delete_order)
    session.commit()
    return delete_order
    