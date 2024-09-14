# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from ..common.models import Usermaster
# from ..connections.config import get_db


# router = APIRouter()

# # API to create new BASIC user
# @router.post("/user", tags=["User Management"])
# def create_user(name: str, username: str, email: str, roleId: int, db: Session = Depends(get_db)):
#     """API to create new BASIC user."""
#     user = Usermaster(
#         fullname=name,
#         username=username,
#         useremail=email,
#         # Add additional fields as necessary
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return {"message": "User created successfully", "user": user}

# # API to fetch all the users
# @router.get("/users", tags=["User Management"])
# def fetch_users(db: Session = Depends(get_db)):
#     """API to fetch all the users."""
#     users = db.query(Usermaster).all()
#     return {"users": users}

# # API to change the status of specific user
# @router.put("/alter-status", tags=["User Management"])
# def alter_user_status(username: str, userstatus: str, db: Session = Depends(get_db)):
#     """API to change the status of specific user."""
#     user = db.query(Usermaster).filter(Usermaster.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.active = userstatus
#     db.commit()
#     return {"message": "User status updated"}

# # API to update user details based on user id
# @router.put("/user", tags=["User Management"])
# def update_user_details(user_id: int, name: str, email: str, roleId: int, db: Session = Depends(get_db)):
#     """API to update user details based on user id."""
#     user = db.query(Usermaster).filter(Usermaster.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.fullname = name
#     user.useremail = email
#     # Update other fields as necessary
#     db.commit()
#     return {"message": "User details updated"}

# # API to delete specific user based on userId
# @router.put("/user-deletion", tags=["User Management"])
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     """API to delete specific user based on userId."""
#     user = db.query(Usermaster).filter(Usermaster.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     user.active = "deleted"
#     db.commit()
#     return {"message": "User marked as deleted"}

# # API to update password of specific user
# @router.put("/psswrd-reset", tags=["User Management"])
# def reset_password(username: str, oldpsswrd: str, newpsswrd: str, db: Session = Depends(get_db)):
#     """API to update password of specific user."""
#     user = db.query(Usermaster).filter(Usermaster.username == username).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     # Add logic to verify old password
#     user.psswrd = newpsswrd
#     db.commit()
#     return {"message": "Password updated successfully"}
