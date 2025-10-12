from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session           # <-- Capital S
from ..database import get_db
from .. import models, utils, oauth2, schemas

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model= schemas.Token)  # optionally: response_model=schemas.Token
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),   # <-- Depends()
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user or not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "Bearer"}
