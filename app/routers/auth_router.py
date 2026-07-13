from fastapi import Cookie, APIRouter, HTTPException, status, Response
from models.auth_models import User, User_url
from cruds.auth_crud import *
from typing import Annotated

router = APIRouter(tags=['auth'])

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Регистрация пользователя",
             responses={
                 status.HTTP_409_CONFLICT: {"description": "Человек с таким именем существует"}
             })
def register_user(user: User_url):
    info = create_user(user.username, user.password,
                 'admin' if user.role == 'admin' else 'base')
    if info == '409':
        raise HTTPException(status.HTTP_409_CONFLICT,
                             "Человек с таким именем существует.")
    return info

@router.post("/login", summary="Авторизация пользователя", responses={
    status.HTTP_401_UNAUTHORIZED: {"description": "Неверный пароль"}, 
    status.HTTP_404_NOT_FOUND: {"description": "Не существует такого пользователя"}
})
def login_user(user_data: User, response: Response):
    user = authenticate_user(user_data.username, user_data.password)
    if user == '404':
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Не существует такого пользователя.")
    if user == '401':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Неверный пароль.")
    
    token = create_acc_token(user['id'])

    response.set_cookie(key="access_token", value=token,
                        httponly=True, max_age=24*60*60)
    
    return "Успешный вход"

def get_user_from_cookie(access_token: Annotated[str | None, Cookie()] = None):
    if not access_token:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Вы не авторизованы.")
    
    payload = verify_acc_token(access_token)
    if payload in ['expired', 'invalid']:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                             "Токен просрочен или невалиден")
    user_id = payload.get("sub")
    user = get_user_by_id(user_id)
    return user
