from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
import models

router = APIRouter()

templetes = Jinja2Templates(directory="templetes")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()




# @router.get("/fe", response_class=HTMLResponse)
# async def read_all_by_user(request: Request, db: Session = Depends(get_db)):

#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).all()

#     return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user})


# @router.get("/fe/add-todo", response_class=HTMLResponse)
# async def add_new_todo(request: Request):
#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})


# @router.post("/fe/add-todo", response_class=HTMLResponse)
# async def fe_create_todo(request: Request, title: str = Form(...), description: str = Form(...),
#                       priority: int = Form(...), db: Session = Depends(get_db)):
#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = models.Todos()
#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority
#     todo_model.complete = False
#     todo_model.owner_id = user.get("id")

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/fe/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

#     return templates.TemplateResponse("edit-todo.html", {"request": request, "todo": todo, "user": user})


# @router.post("/fe/edit-todo/{todo_id}", response_class=HTMLResponse)
# async def edit_todo_commit(request: Request, todo_id: int, title: str = Form(...),
#                            description: str = Form(...), priority: int = Form(...),
#                            db: Session = Depends(get_db)):

#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

#     todo_model.title = title
#     todo_model.description = description
#     todo_model.priority = priority

#     db.add(todo_model)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/fe/delete/{todo_id}")
# async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
#         .filter(models.Todos.owner_id == user.get("id")).first()

#     if todo_model is None:
#         return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

#     db.query(models.Todos).filter(models.Todos.id == todo_id).delete()

#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)


# @router.get("/fe/complete/{todo_id}", response_class=HTMLResponse)
# async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

#     user = await get_current_user(request.cookies.get("access_token"))
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

#     todo.complete = not todo.complete

#     db.add(todo)
#     db.commit()

#     return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)






