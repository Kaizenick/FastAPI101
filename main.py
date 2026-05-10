from fastapi import FastAPI, Depends
from models import Product
from datebase import session, engine
from sqlalchemy.orm import Session
import database_models


app = FastAPI()

# This line takes the responsibility to create the table 
database_models.Base.metadata.create_all(bind=engine)

products = [Product(id=1,name="Acer Laptop", price=1000),
            Product(id=2,name="Iphone 17", price=800),
            Product(id=3,name="Mac Book Air M3 Laptop", price=1600),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    if((db.query(database_models.Product).count) == 0):
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

# get data from db
# @app.get("/")
# def get_all(db: Session = Depends(get_db)):
#     db_products = db.query(database_models.Product).all()
#     return db_products

#get data from the objects 
@app.get("/")
def get_all():
    return products

#get data from the objects 
@app.get("/product/{id}")
def get_product_by_id(id: int):
    for product in products:
        if product.id == id:
            return product
    
    return "The product does not exist"

#get data from the objects 
@app.post("/product/")
def add_product(product: Product):
    products.append(product)
    return product

#get data from the objects 
@app.post("/update/{id}")
def update_product_info(id: int, updatedproduct: Product):
    for index,product in enumerate(products):
        if(product.id == id):
            products[index] = updatedproduct
            return updatedproduct
    return "Couldnt make changes, id not found!!"
    
#get data from the objects 
@app.delete("/update/{id}")
def delete_product_info(id: int):
    for index,product in enumerate(products):
        if(product.id == id):
            del products[index]
            return products
    return "Couldnt make changes, id not found!!"  