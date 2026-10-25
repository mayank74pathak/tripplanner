import os

from dotenv import load_dotenv
from jose import JWTError, jwt
from pwdlib import PasswordHash

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User


load_dotenv()


# Password hashing
password_hash = PasswordHash.recommended()


# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv(
    "ALGORITHM",
    "HS256"
)


# OAuth2 Bearer token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(user_id: int) -> str:

    payload = {
        "sub": str(user_id)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        # Decode JWT
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Get user ID from JWT
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):

        raise credentials_exception

    # Find user in database
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user