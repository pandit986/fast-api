from fastapi import FastAPI, HTTPException, Depends, Header
from jose import jwt
import time
import bcrypt
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

app = FastAPI()

ALGORITHM = "HS256"  # Algorithm used for JWT token signing

SECRET_KEY = "Abhishek@123" # Secret key for JWT token signing

ACCESS_TOKEN_EXPIRE_MIN = 30

# oauth setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# dummy user database
fake_users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("root")
    }
}

# create JWT token
def create_token(data: dict):
    to_encode = data.copy()
    expire = time.time() + ACCESS_TOKEN_EXPIRE_MIN * 60
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token 

# login API endpoint (oauth2 password flow)
# @app.post("/login")
# def login(username:str, password:str):
#     if username == "admin" and password == "root":
#         token = create_token({"sub": username})
#         return {"access_token": token}
#     else:
#         raise HTTPException(status_code=401, detail="Invalid username or password")

@app.post("/login")
def Login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# def verify_token(token: str = Header(None)):
#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username= payload.get("sub")
#         print("username:", username)
#         if username is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return payload
#     except jwt.ExpiredSignatureError:
#             raise HTTPException(status_code=401, detail="Token has expired")
#     except jwt.JWTError:
#             raise HTTPException(status_code=401, detail="Invalid token")

# token verification function
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# protected API endpoint
@app.get("/protected")
def protected_route(payload: dict = Depends(verify_token)):
    return {"message": "You have access to this protected route", "user": payload}
