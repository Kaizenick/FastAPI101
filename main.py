from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from datebase import session, engine
from sqlalchemy.orm import Session
import database_models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"]
)

# This line takes the responsibility to create the table 
database_models.Base.metadata.create_all(bind=engine)

products = [Product(id=1,name="Acer Laptop", price=1000, description="This is a quality Laptop", quantity= 30),
            Product(id=2,name="Iphone 17", price=800, description="This is a quality Laptop", quantity= 16),
            Product(id=3,name="Mac Book Air M3 Laptop", price=1600, description="This is a quality Laptop", quantity= 10),
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db = session()
    if((db.query(database_models.Product).count() == 0)):
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

# ---------------------------------------------------------------------
# get data from db
@app.get("/products/")
def get_all(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

#get data from the objects 
# @app.get("/")
# def get_all():
#     return products

# ---------------------------------------------------------------------
#get data from db
@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if(product):
        return product
    else:
        return "The product Does not Exist"

# #get data from the objects 
# @app.get("/product/{id}")
# def get_product_by_id(id: int):
#     for product in products:
#         if product.id == id:
#             return product
    
#     return "The product does not exist"

# ---------------------------------------------------------------------

# get data from db : add rows
@app.post("/products/")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return

# #get data from the objects 
# @app.post("/product/")
# def add_product(product: Product):
#     products.append(product)
#     return product

# ---------------------------------------------------------------------

#get data from the db : update values 
@app.put("/products/{id}")
def update_product_info(id: int, name: str, price: float, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if(product):
        product.name = name 
        product.price = price

        db.commit()
        db.refresh(product)

        return product
    else:
        return "The id does not Exist!!"

#get data from the objects 
# @app.post("/update/{id}")
# def update_product_info(id: int, updatedproduct: Product):
#     for index,product in enumerate(products):
#         if(product.id == id):
#             products[index] = updatedproduct
#             return updatedproduct
#     return "Couldnt make changes, id not found!!"

# ---------------------------------------------------------------------
#get data from the db : delete row
@app.delete("/products/{id}")
def delete_product_info(id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if(product):
        db.delete(product)
        db.commit()
        
        return 
    else:
        raise ValueError("Data does not exist!!")

#get data from the objects 
# @app.delete("/update/{id}")
# def delete_product_info(id: int):
#     for index,product in enumerate(products):
#         if(product.id == id):
#             del products[index]
#             return products
#     return "Couldnt make changes, id not found!!"  
