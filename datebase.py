from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# The url is - postgresql://username:password@ip:post/dbname
db_url = "postgresql://soham:12345678@localhost:5432/products"

engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind = engine)

