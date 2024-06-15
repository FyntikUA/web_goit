from fastapi import FastAPI, Depends, File, UploadFile, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from datetime import timedelta
from app import models, schemas, crud, auth
from .app.database import SessionLocal, engine


import cloudinary

models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # список URL-адрес, з яких дозволяється отримувати запити
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключення до Cloudinary
cloudinary.config(
    cloud_name="your_cloud_name",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

def get_db():
    """
    Отримує сесію бази даних.

    Yields:
        Session: Сесія бази даних.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User, status_code=201)
@limiter.limit("5/minute")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Створює нового користувача.

    Args:
        user (schemas.UserCreate): Дані нового користувача.
        db (Session, optional): Сесія бази даних.

    Returns:
        schemas.User: Створений користувач.

    Raises:
        HTTPException: Якщо електронна пошта вже зареєстрована.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Авторизує користувача та видає токен доступу.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Дані форми авторизації.
        db (Session, optional): Сесія бази даних.

    Returns:
        dict: Токен доступу та тип токена.

    Raises:
        HTTPException: Якщо електронна пошта або пароль неправильні.
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Отримує інформацію про поточного користувача.

    Args:
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        schemas.User: Поточний користувач.
    """
    return current_user

@app.post("/contacts/", response_model=schemas.Contact, status_code=201)
@limiter.limit("5/minute")
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Створює новий контакт.

    Args:
        contact (schemas.ContactCreate): Дані нового контакту.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        schemas.Contact: Створений контакт.
    """
    return crud.create_contact(db=db, contact=contact, user_id=current_user.id)

@app.get("/contacts/", response_model=list[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Отримує список контактів.

    Args:
        skip (int, optional): Кількість пропущених записів.
        limit (int, optional): Максимальна кількість записів.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        list[schemas.Contact]: Список контактів.
    """
    contacts = crud.get_contacts(db, user_id=current_user.id, skip=skip, limit=limit)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Отримує контакт за ідентифікатором.

    Args:
        contact_id (int): Ідентифікатор контакту.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        schemas.Contact: Знайдений контакт.

    Raises:
        HTTPException: Якщо контакт не знайдено або не належить поточному користувачу.
    """
    db_contact = crud.get_contact(db, contact_id=contact_id)
    if db_contact is None or db_contact.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Оновлює контакт за ідентифікатором.

    Args:
        contact_id (int): Ідентифікатор контакту.
        contact (schemas.ContactUpdate): Дані для оновлення контакту.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        schemas.Contact: Оновлений контакт.

    Raises:
        HTTPException: Якщо контакт не знайдено.
    """
    db_contact = crud.update_contact(db, contact_id=contact_id, contact=contact, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Видаляє контакт за ідентифікатором.

    Args:
        contact_id (int): Ідентифікатор контакту.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        schemas.Contact: Видалений контакт.

    Raises:
        HTTPException: Якщо контакт не знайдено.
    """
    db_contact = crud.delete_contact(db, contact_id=contact_id, user_id=current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=list[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Шукає контакти за запитом.

    Args:
        query (str): Запит для пошуку контактів.
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        list[schemas.Contact]: Знайдені контакти.
    """
    contacts = crud.search_contacts(db, query=query, user_id=current_user.id)
    return contacts

@app.get("/contacts/upcoming_birthdays/", response_model=list[schemas.Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Отримує контакти з найближчими днями народження.

    Args:
        db (Session, optional): Сесія бази даних.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        list[schemas.Contact]: Контакти з найближчими днями народження.
    """
    contacts = crud.get_upcoming_birthdays(db, user_id=current_user.id)
    return contacts

@app.post("/users/avatar/")
@limiter.limit("5/minute")
def upload_avatar(file: UploadFile = File(...), current_user: schemas.User = Depends(auth.get_current_user)):
    """
    Завантажує аватар користувача.

    Args:
        file (UploadFile, optional): Файл аватару.
        current_user (schemas.User, optional): Поточний користувач.

    Returns:
        dict: URL аватару.

    Raises:
        HTTPException: Якщо файл не є зображенням.
    """
    if file.content_type.startswith("image/"):
        response = upload(file.file)
        avatar_url = response["secure_url"]
        db = SessionLocal()
        user = crud.update_user_avatar(db, user_id=current_user.id, avatar_url=avatar_url)
        db.close()
        return {"avatar_url": avatar_url}
    else:
        raise HTTPException(status_code=400, detail="Only image files are allowed")
