import sqlite3

from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response, status
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from typing import List,Optional


app = FastAPI()



@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect("northwind.db")
    app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()

@app.get("/categories")
async def categories():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''SELECT CategoryID, CategoryName FROM Categories''').fetchall()
    return JSONResponse(content = {"categories": [{"id": x['CategoryID'], "name": x['CategoryName']} for x in data]}, status_code=status.HTTP_200_OK)
    
    
@app.get("/customers")
async def customers():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''SELECT CustomerID, CompanyName, Address, PostalCode, City, Country FROM Customers''').fetchall()
    return JSONResponse(content = {"customers": [{"id": x['CustomerID'], "name": x['CompanyName'],"full_adress":f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in data]}, status_code=status.HTTP_200_OK)

@app.get("/products/{id}")
async def products(id: Optional[int]=None):
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute("SELECT ProductID, ProductName FROM Products WHERE ProductID = :product_id",{'product_id': id}).fetchone()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content = {"id": data['ProductID'], "name": f"{data['ProductName']}"}, status_code=status.HTTP_200_OK)

@app.get("/employees", status_code=status.HTTP_200_OK)
async def employees(limit: Optional[int]=None,offset: Optional[int]=0,order: Optional[str]="id"):
    order_name = {"first_name":"FirstName","last_name":"LastName","city":"City","id":"EmployeeID"}
    text_limit_offset = f''''''
    if not order in order_name.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    app.db_connection.row_factory = sqlite3.Row
    for key, value in order_name.items():
        new_order = order.replace(key, value)
    if limit != None: text_limit_offset = f'''LIMIT {limit} OFFSET {offset}'''
    data = app.db_connection.execute(f'''SELECT * FROM Employees ORDER BY {new_order} {text_limit_offset}''').fetchall()
    return JSONResponse(content = {"employees":[{"id": x[order_name["id"]], "last_name": f"{x[order_name['last_name']]}", "first_name": f"{x[order_name['first_name']]}","city": f"{x[order_name['city']]}"} for x in data]})

@app.get("/products_extended")
async def prod_ext():
    app.db_connection.row_factory = sqlite3.Row
    data = app.db_connection.execute('''
        SELECT ProductID, ProductName, CategoryName, CompanyName FROM Products 
        JOIN Categories ON Products.CategoryID = Categories.CategoryID 
        JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID 
        ORDER BY ProductID
    ''').fetchall()
    if data == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content = {"products_extended":[{"id": x['ProductID'], "name": f"{x['ProductName']}","category":f"{x['CategoryName']}","supplier":f"{x['CompanyName']}"}for x in data]}, status_code=status.HTTP_200_OK)
# @app.get("/suppliers/{supplier_id}")
# async def single_supplier(supplier_id: int):
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         "SELECT CompanyName, Address FROM Suppliers WHERE SupplierID = :supplier_id",
#         {'supplier_id': supplier_id}).fetchone()
#     return data


# @app.get("/employee_with_region")
# async def employee_with_region():
#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute('''
#         SELECT Employees.LastName, Employees.FirstName, Territories.TerritoryDescription 
#         FROM Employees JOIN EmployeeTerritories ON Employees.EmployeeID = EmployeeTerritories.EmployeeID
#         JOIN Territories ON EmployeeTerritories.TerritoryID = Territories.TerritoryID;
#      ''').fetchall()
#     return [{"employee": f"{x['FirstName']} {x['LastName']}", "region": x["TerritoryDescription"]} for x in data]


# @app.get("/customers")
# async def customers():
#     app.db_connection.row_factory = lambda cursor, x: x[0]
#     artists = app.db_connection.execute("SELECT CompanyName FROM Customers").fetchall()
#     return artists


# class Customer(BaseModel):
#     company_name: str


# @app.post("/customers/add")
# async def customers_add(customer: Customer):
#     cursor = app.db_connection.execute(
#         f"INSERT INTO Customers (CompanyName) VALUES ('{customer.company_name}')"
#     )
#     app.db_connection.commit()
#     return {
#         "CustomerID": cursor.lastrowid,
#         "CompanyName": customer.company_name
#     }


# class Shipper(BaseModel):
#     company_name: str


# @app.patch("/shippers/edit/{shipper_id}")
# async def artists_add(shipper_id: int, shipper: Shipper):
#     cursor = app.db_connection.execute(
#         "UPDATE Shippers SET CompanyName = ? WHERE ShipperID = ?", (
#             shipper.company_name, shipper_id)
#     )
#     app.db_connection.commit()

#     app.db_connection.row_factory = sqlite3.Row
#     data = app.db_connection.execute(
#         """SELECT ShipperID AS shipper_id, CompanyName AS company_name
#          FROM Shippers WHERE ShipperID = ?""",
#         (shipper_id, )).fetchone()

#     return data


# @app.get("/orders")
# async def orders():
#     app.db_connection.row_factory = sqlite3.Row
#     orders = app.db_connection.execute("SELECT * FROM Orders").fetchall()
#     return {
#         "orders_counter": len(orders),
#         "orders": orders,
#     }


# @app.delete("/orders/delete/{order_id}")
# async def order_delete(order_id: int):
#     cursor = app.db_connection.execute(
#         "DELETE FROM Orders WHERE OrderID = ?", (order_id, )
#     )
#     app.db_connection.commit()
#     return {"deleted": cursor.rowcount}


# @app.get("/region_count")
# async def root():
#     app.db_connection.row_factory = lambda cursor, x: x[0]
#     regions = app.db_connection.execute(
#         "SELECT RegionDescription FROM Regions ORDER BY RegionDescription DESC").fetchall()
#     count = app.db_connection.execute('SELECT COUNT(*) FROM Regions').fetchone()

#     return {
#         "regions": regions,
#         "regions_counter": count
#     }
