from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
from pydantic import BaseModel

import leads_package.models as models
from leads_package.constants import ATTORNEY_EMAIL
from leads_package.databases import engine, sessionLocal
from sqlalchemy.orm import Session
from leads_package.sendEmail import send_email
from leads_package.models import User, ReachedOutState

app = FastAPI()
models.Base.metadata.create_all(bind=engine)



class UserCreate(BaseModel):
    firstname: str
    lastname: str
    email: str
    resume: str


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post(path="/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    try:
        new_user = models.User(**user.dict())
        # Add User and Resume objects to the session and commit
        db.add(new_user)
        db.commit()
        send_email(ATTORNEY_EMAIL, 'New Lead Created', 'new data created for ' + new_user.email)
        send_email(new_user.email, 'Data Submitted successfully',
                   'Hi ' + new_user.firstname + ' your data has been submitted')
        # Return the created user and resume information
        return {"user": new_user}
    except:
        return {"Please try again"}


# Attorneys can check data based on the email
@app.get(path="/users/{email}")
async def get_user_by_email(email: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put(path="/users/{email}/reach_out")
async def reach_out_to_user(email: str, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the user's state to "REACHED_OUT"
    user.state = ReachedOutState.REACHED_OUT.name
    db.commit()

    return {"message": "User state updated to " + user.state}


@app.put(path="/users/{email}/change_state")
async def change_state(email: str, state: ReachedOutState, db: db_dependency):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if state is not ReachedOutState:
        raise HTTPException(status_code=404, detail="Invalid state")

    # Update the user's state
    user.state = state
    db.commit()

    return {"message": "User state updated to " + state}


@app.get("/leads/")
def get_all_records(db: Session = Depends(get_db)):
    records = db.query(models.User).all()
    return records
