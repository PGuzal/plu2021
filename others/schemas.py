from sqlalchemy.sql.sqltypes import Integer
from pydantic import BaseModel, PositiveInt, constr
from typing import Optional, List

class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: constr(max_length=60)

    class Config:
        orm_mode = True

class Supplier2(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    Region: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    Fax: Optional[constr(max_length=24)]
    HomePage: Optional[str]

    class Config:
        orm_mode = True

class CategoryData(BaseModel):
    id: int
    CategoryID:PositiveInt
    CategoryName:Optional[constr(max_length=15)]

    class Config:
        orm_mode = True
        
class Prod_supl(BaseModel):
    ProductID: PositiveInt
    ProductName: Optional[constr(max_length=40)]
    ContactName: Optional[constr(max_length=30)]
    Category: List[CategoryData]={}
    Discontinued: Optional[constr(max_length=30)]

    class Config:
        orm_mode = True





