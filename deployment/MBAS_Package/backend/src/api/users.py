from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..core.db import get_session
from ..core.auth import get_current_user
from ..core.security import get_password_hash
from ..models.core import User, UserCreate, UserRead, UserRole

router = APIRouter(prefix="/users", tags=["users"])

def get_admin(current_user: User = Depends(get_current_user)):
    """Ensures only admins can manage users."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can manage users."
        )
    return current_user

@router.get("/", response_model=List[UserRead])
def list_users(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin)
):
    """Get all users (admin only)."""
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.post("/", response_model=UserRead)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin)
):
    """Create a new user (admin only)."""
    # Check if username already exists
    existing_user = session.exec(
        select(User).where(User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    # Create new user
    db_user = User(
        username=user_data.username,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=user_data.is_active,
        hashed_password=get_password_hash(user_data.password)
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin)
):
    """Update a user (admin only)."""
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from changing their own role or deactivating themselves
    if db_user.id == current_user.id:
        if user_data.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change your own admin role"
            )
        if not user_data.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account"
            )

    # Update user fields
    db_user.username = user_data.username
    db_user.full_name = user_data.full_name
    db_user.role = user_data.role
    db_user.is_active = user_data.is_active

    # Only update password if provided
    if user_data.password:
        db_user.hashed_password = get_password_hash(user_data.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin)
):
    """Delete a user (admin only)."""
    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prevent admin from deleting themselves
    if db_user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted successfully"}
