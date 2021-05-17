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
    db_supp = models.Supplier(**supp.dict(),SupplierID = index.SupplierID+1)
    db.add(db_supp)
    db.commit()
    db.refresh(db_supp)
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()

def update_supplier(db: Session,supp:schemas.Supplier2,id:id):
    supp_db = db.query(models.Supplier).filter(models.Supplier.SupplierID == id).first()
    supp_new = dict(supp)
    key = [i for i,j in zip(supp_new.keys(),supp_new.values()) if j is not None]
    for i in key:
        supp_db.globals()['%s' % i] = supp_new[i]
    db.commit()
    return db.query(models.Supplier).order_by(models.Supplier.SupplierID.desc()).first()