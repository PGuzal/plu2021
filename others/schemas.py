from pydantic import BaseModel, PositiveInt, constr
from typing import Optional

class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True

class Supplier(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=60)]

    class Config:
        orm_mode = True

class Supplier2(BaseModel):
    SupplierID: PositiveInt
    CompanyName: Optional[constr(max_length=60)]
    ContactName: Optional[constr(max_length=60)]
    ContactTitle: Optional[constr(max_length=60)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=60)]
    Region: Optional[constr(max_length=60)]
    PostalCode: Optional[constr(max_length=60)]
    Country: Optional[constr(max_length=60)]
    Phone: Optional[constr(max_length=60)]
    Fax: Optional[constr(max_length=60)]
    HomePage: Optional[constr(max_length=60)]

    class Config:
        orm_mode = True

