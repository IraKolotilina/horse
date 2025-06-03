# app/schemas/token.py
from pydantic import BaseModel, ConfigDict
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type:   str
