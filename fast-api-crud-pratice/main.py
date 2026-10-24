from pydantic import BaseModel
from sqlalchemy import String,Integer,Column, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends

# database connection
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/crud_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# table schmema
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Api implementation
app = FastAPI()

@app.get("/")
def home(db: Session = Depends(get_db)):
    return {"message": "Welcome to the FastAPI CRUD application!"}

@app.post("/create-user")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email, password=user.password) 
    # object of User class is created and data is passed to it from the request body.
    db.add(db_user)
    # add() method is used to add the object to the session.
    db.commit()
    # commit() method is used to save the changes to the database.
    db.refresh(db_user)
    # refresh() method is used to refresh the object with the latest data from the database.
    return {
        "message": "User created successfully",
        "user": db_user
    }

@app.get("/get-users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    # query() method is used to query the database and all() method is used to retrieve all the records from the users table.
    return {
        "message": "Users retrieved successfully",
        "users": users  
    }

@app.get("/get-user/{user_id}")
def get_user(user_id: int,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # filter() method is used to filter the records based on the condition and first() method is used to retrieve the first record that matches the condition.
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "message": "User retrieved successfully",
        "user": user
    }

@app.put("/update-user/{user_id}")
def update_user(user_id:int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name 
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return {
        "message": "User updated successfully",
        "user": db_user
    }

@app.delete("/delete-user/{user_id}")
def delete_user(user_id:int, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return{
        "message": "User deleted successfully",
        "data": db_user
    }


