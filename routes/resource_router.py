from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database.db import get_db
from models.user import User
from models.product import Product
from middlewares.authorization import check_permission
from pydantic import BaseModel

router = APIRouter()


def get_current_user(request: Request) -> User:
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


class ProductSchema(BaseModel):
    name: str
    description: str = ""


@router.get("/products")
def get_products(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    check_permission(current_user, "products", "read", db)

    # Если есть право читать все, показываем все продукты
    if current_user.role.name == "admin":
        products = db.query(Product).all()
    else:
        # Иначе только свои продукты
        products = db.query(Product).filter(Product.owner_id == current_user.id).all()

    return products


@router.post("/products")
def create_product(
        product: ProductSchema,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    check_permission(current_user, "products", "create", db)
    new_product = Product(
        name=product.name,
        description=product.description,
        owner_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.put("/products/{product_id}")
def update_product(
        product_id: int,
        product: ProductSchema,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверяем права
    if db_product.owner_id == current_user.id:
        check_permission(current_user, "products", "update", db)
    else:
        check_permission(current_user, "products", "update_all", db)

    db_product.name = product.name
    db_product.description = product.description
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
def delete_product(
        product_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Проверяем права
    if db_product.owner_id == current_user.id:
        check_permission(current_user, "products", "delete", db)
    else:
        check_permission(current_user, "products", "delete_all", db)

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}
