from src.db import db_engine
import src.models as _models

def add_schema():
    return _models.Base.metadata.create_all(bind=db_engine)