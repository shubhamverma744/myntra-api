from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.config import get_db
from models.product import Product
import uuid

router = APIRouter(prefix="/products", tags=["Products"])

# Create product with category
@router.post("/")
def create_product(name: str, price: float, category: str, db: Session = Depends(get_db)):
    product = Product(
        id=uuid.uuid4().hex,
        name=name,
        price=price,
        category=category
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"message": "Product created successfully", "product": product}

# Get all products
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# Get products by category
@router.get("/category/{category_name}")
def get_products_by_category(category_name: str, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.category == category_name).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found in this category")
    return products
