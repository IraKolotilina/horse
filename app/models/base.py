# app/models/base.py
from sqlalchemy.orm import declarative_base

# единственный Base для всех моделей
Base = declarative_base()
