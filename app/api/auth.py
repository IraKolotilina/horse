# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.token import Token
from app.models.player import Player as PlayerModel

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(PlayerModel).filter(PlayerModel.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        status_code = status.HTTP_401_UNAUTHORIZED if user else status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status_code,
            detail="Incorrect username or password"
        )
    # обновим время последнего входа
    user.last_login = datetime.utcnow()
    db.commit()
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
