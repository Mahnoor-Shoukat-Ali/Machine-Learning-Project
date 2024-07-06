from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import User, Notification
from .schemas import NotificationCreate, UserCreate, Token
from .auth import authenticate_user, create_access_token, get_current_user
from .kafka_producer import send_kafka_message

app = FastAPI()

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserCreate)
def create_user(user: UserCreate, db: Session = Depends(SessionLocal)):
    db_user = User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/notifications/")
def create_notification(notification: NotificationCreate, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    db_notification = Notification(content=notification.content, user_id=current_user.id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    send_kafka_message(notification.content)
    return db_notification

@app.get("/notifications/")
def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(SessionLocal), current_user: User = Depends(get_current_user)):
    notifications = db.query(Notification).filter(Notification.user_id == current_user.id).offset(skip).limit(limit).all()
    return notifications
