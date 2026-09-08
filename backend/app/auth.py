from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

#Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

def hash_password(password: str) -> str:
    """Turns a plain password into a non-readable hash for storage in the database."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks the entered password against the hash from the database. True = match."""
    return pwd_context.verify(plain_password, hashed_password)

#JWT token setup
SECRET_KEY = "change-this-secret-key-later"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

def create_access_token(data:dict)-> str:
    """
    Creates a JWT token.
    data — what we want to store inside the token (usually the user id).
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """
    Verifies the token and extracts its data.
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
