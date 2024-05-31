import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Зчитуємо URL бази даних з змінних середовища, якщо вони є
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Створюємо рідний інженер SQLAlchemy для підключення до бази даних
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Створюємо клас базової моделі для всіх моделей
Base = declarative_base()

# Створюємо сесію бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
