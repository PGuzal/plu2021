from sqlalchemy.orm import Session

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
        #db.query(models.Product).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()
        #db.query(models.Product,models.Category.CategoryID,models.Category.CategoryName).join(models.Category, models.Product.CategoryID == models.Category.CategoryID).filter(models.Product.SupplierID == id).order_by(models.Product.ProductID.desc()).all()
    )


def make_supplier(db: Session,supp:schemas.Supp_post):
    index = db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()
    db_supp = models.Supplier(**supp.dict(),SupplierID = index.SupplierID)
    db.add(db_supp)
    db.commit()
    db.refresh(db_supp)
    print()
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()
