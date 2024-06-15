from sqlalchemy.orm import Session
from .auth import get_password_hash
#from my_contacts_api.app.auth import get_password_hash
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Contact).filter(models.Contact.owner_id == user_id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate, user_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate, user_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()
    if db_contact is None:
        return None
    for var, value in vars(contact).items():
        setattr(db_contact, var, value) if value else None
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    db_contact = db.query(models.Contact).filter(models.Contact.id == contact_id, models.Contact.owner_id == user_id).first()
    if db_contact is None:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact

def search_contacts(db: Session, query: str, user_id: int):
    return db.query(models.Contact).filter(
        (models.Contact.first_name.ilike(f"%{query}%")) |
        (models.Contact.last_name.ilike(f"%{query}%")) |
        (models.Contact.email.ilike(f"%{query}%")),
        models.Contact.owner_id == user_id
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int):
    from datetime import datetime, timedelta
    today = datetime.today()
    upcoming_date = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.birthday >= today.date(),
        models.Contact.birthday <= upcoming_date.date(),
        models.Contact.owner_id == user_id
    ).all()
