from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://dev:dev@localhost:5432/order-delivery-db"
#DATABASE_URL = "postgresql+psycopg2://dev:dev@order-delivery-db:5432/order-delivery-db"
db_engine=create_engine(DATABASE_URL,echo=True)
Session=sessionmaker(autoflush=False,bind=db_engine)
    


                        