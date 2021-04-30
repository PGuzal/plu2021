from hashlib import sha256
import secrets
from fastapi import Cookie, FastAPI, HTTPException, Query, Request, Response,Depends,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import date
from fastapi_mako import FastAPIMako
from routers.router import router
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
app.__name__ = "templates"
mako = FastAPIMako(app)


templates = Jinja2Templates(directory="templates")
security = HTTPBasic()
app.secret_key = "very constatn and random secret, best 64+ characters"
app.access_tokens = []

app.counter = 0
app.static_files = {}


app.include_router(
    router, prefix="/v1", tags=["api_v1"],
)

app.include_router(router, tags=["default"])


class HelloResp(BaseModel):
    msg: str



@app.get("/hello")
def index_static(request: Request):
    return templates.TemplateResponse("index_hello.html", {
        "request": request, "date_now": date.today().strftime('%Y-%m-%d')})

@app.get("/login_token")
def read_items(credentials: HTTPBasicCredentials = Depends(security)):
    correctU = secrets.compare_digest(credentials.username, "4dm1n")
    correctP = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correctU and correctP):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/login_session")
def read_items(credentials: HTTPBasicCredentials = Depends(security)):
    correctU = secrets.compare_digest(credentials.username, "4dm1n")
    correctP = secrets.compare_digest(credentials.password, "NotSoSecurePa$$")
    if not (correctU and correctP):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)





@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/counter")
def counter():
    app.counter += 1
    return app.counter


# @app.get("/hello/{name}", response_model=HelloResp)
# def hello_name_view(name: str):
#     return HelloResp(msg=f"Hello {name}")


@app.get("/request_query_string_discovery/")
def read_items(u: str = "default", q: List[str] = None):
    query_items = {"q": q, "u": u}
    return query_items


@app.get("/static", response_class=HTMLResponse)
def index_static():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


@app.get("/mako", response_class=HTMLResponse)
@mako.template("index_mako.html")
def index_mako(request: Request):
    setattr(request, "mako", "test")
    return {"my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]}


@app.get("/jinja")
def read_item(request: Request):
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "my_string": "Wheeeee!", "my_list": [0, 1, 2, 3, 4, 5]},
    )


@app.post("/login/")
def login(user: str, password: str, response: Response):
    session_token = sha256(f"{user}{password}{app.secret_key}".encode()).hexdigest()
    app.access_tokens.append(session_token)
    response.set_cookie(key="session_token", value=session_token)
    return {"message": "Welcome"}


@app.get("/data/")
def secured_data(*, response: Response, session_token: str = Cookie(None)):
    print(session_token)
    print(app.access_tokens)
    print(session_token in app.access_tokens)
    if session_token not in app.access_tokens:
        raise HTTPException(status_code=403, detail="Unathorised")
    else:
        return {"message": "Secure Content"}

