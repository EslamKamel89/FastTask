
from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import Base, engine
from routers import admin, auth, todos, users

app = FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates('template')
app.mount("/static"  , StaticFiles(directory="./static") , name='static')

@app.get('/healthy')
async def health_check():
    return {"status":"Healthy"}

@app.get('/')
async def home(request:Request  ) :
    return RedirectResponse('/todos/todo-page' , status_code=status.HTTP_302_FOUND )


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
