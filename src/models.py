from sqlalchemy import Column, Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

Base=declarative_base()

class Customer(Base):
    __tablename__='customers'

    id=Column(Integer,primary_key=True)
    cust_name=Column(String(40),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    active_cust=Column(Boolean,default=False)
    sales=Column(Boolean,default=False)

    orders=relationship('Order', back_populates='owner')
    
    def __repr__(self):
        return f"<Customer {self.cust_name}>"
    
class Order(Base):
    #Tuple of order status 
    ORDER_STATUS=(
        ('ORDER-PLACED','order-placed'),
        ('DISPATCHED','dispatched'),
        ('DELIVERED','delivered')
    )

    ORDER_SIZE=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large')
    )

    __tablename__='orders'

    ord_id=Column(Integer,primary_key=True)
    quantity=Column(Integer, nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUS), default='ORDER-PLACED')
    order_size=Column(ChoiceType(choices=ORDER_SIZE), default='SMALL')

    cust_id=Column(Integer,ForeignKey('customers.id'))
    owner=relationship('Customer', back_populates='orders')
    
    def __repr__(self):
        return f"<Order {self.ord_id}>"
