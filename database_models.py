from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

# We need to create a schema for the database and we cannot use the same 
# as the pydantic one as sqlalchemy takes in information in a different way
# Hence we declare it in a new file 


Base = declarative_base()

class Product(Base):

    __tablename__ = "product_table"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    quantity = Column(Integer)
    