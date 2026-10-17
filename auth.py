#JOSE:javaScript Object Signing and Encryption, import: uv add python-jose[cryptography],
# We use JSON Web Tokens (JWT)-> encrypted token, to let users log in and access protected parts of a website or app without the server needing to remember their session in a database, used for authorization not authentication, jwt is stateless(not storing state in db), 
# Authentication: Is this really the user who owns these credentials?
# Authorization: Is this user allowed to access this particular resource?
# JWT: A signed token that lets the server validate a user's identity on subsequent requests. It is not normally encrypted.

# jwt.encode() creates a signed token, takes algorithm (singular).
# jwt.decode() checks the token's signature and reads its data., takes algorithm (plural)

from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError  
from passlib.context import CryptContext # uv add passlib[bcrypt], for hashing the password
from fastapi.security import  OAuth2PasswordBearer 


from database import get_db

app=FastAPI()

# jwt config:
# make a secure key for token:
SECRET_KEY="22-mysecretkey-22"
# encryption algorithm
ALGORITHM="HS256"
# token expire
TOKEN_EXPIRE_TIME=30


# create password hashing, This creates an object that knows how to hash and verify passwords using bcrypt.
bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

# generates a password hash, hash is not meant to be decrypted back into the original password.
def hash_password(password: str):
    return bcrypt_context.hash(password)

# verify password
def verify_password(plain_password: str, hashed_password: str):
    return bcrypt_context.verify(plain_password, hashed_password)

# OAuth setup: to extract an access token from a request.
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="api/login")

# Create JWT
def create_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(timezone.utc)+timedelta(minutes=TOKEN_EXPIRE_TIME)
    to_encode.update({"exp":expire})
    token=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify JWT
def verify_token(token:str = Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid/expired token",
         headers={"WWW-Authenticate":"Bearer"})
    