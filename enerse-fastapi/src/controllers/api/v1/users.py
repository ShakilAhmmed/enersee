from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.schemas.response import APIResponse
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.actions.user_actions import UserActions

router = APIRouter()


@router.post("/", response_model=APIResponse[UserResponse], status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        user = UserActions.create_user(db, user)
        return APIResponse(
            message="Users fetched successfully",
            data=user,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return APIResponse[None](
            message=f"Error creating users: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/", response_model=APIResponse[List[UserResponse]])
def list_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):
    """Get list of users"""
    try:
        users = UserActions.get_users(db, skip, limit)
        return APIResponse(
            message="Users fetched successfully",
            data=users,
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return APIResponse[None](
            message=f"Error fetching users: {str(e)}",
            data=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    return UserActions.get_user_by_id(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        db: Session = Depends(get_db)
):
    """Update user"""
    return UserActions.update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    UserActions.delete_user(db, user_id)
    return None
