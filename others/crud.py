from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update

from . import models, schemas



def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

def get_suppliers(db: Session):
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID).all()

def get_supplier(db: Session, id: int):
    return (
        db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    )

def get_product(db: Session, id: int):
    return (
        db.query(models.Product.ProductID,models.Product.ProductName,models.Product.Discontinued,models.Category.CategoryName,models.Category.CategoryID).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()
    )


def make_supplier(db: Session,supp:schemas.Supp_post):
    index = db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()
    db_supp = models.Supplier(**supp.dict(),SupplierID = index.SupplierID+1)
    db.add(db_supp)
    db.commit()
    db.refresh(db_supp)
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()

def update_supplier(db: Session,supp:schemas.Supplier2,id:int):
    supp_new = dict(supp)
    update_data = {}
    for i,j in supp_new.items():
        update_data[models.Supplier.i] = j
    db.query(models.Supplier).filter(models.Supplier.SupplierID == id).update(**update_data,synchronize_session=False)
    db.execute(update)
    db.commit()
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first(), update_data