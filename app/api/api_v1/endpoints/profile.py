from typing import Any, List, Optional

from pydantic import EmailStr, HttpUrl

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  

from app import schemas, crud
from app.models.user import User
from app.api import deps

router = APIRouter()


@router.get('/me', response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)) -> Any:
    """
    Get current user
    """
    return current_user


@router.put('/me', response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update current user
    """
    if user_in.email is not None and user_in.email != current_user.email:
        if crud.user.get_by_email(db, email=user_in.email):
            raise HTTPException(
                status_code=400, detail='The user with this username already exists'
            )
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get('/{user_id}', response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if not user or user.is_superuser:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/all/', response_model=List[schemas.User])
def get_all_user(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all users that are not superusers.
    """
    users = crud.user.get_multi(db)
    return [user for user in users if user.id != current_user.id and user.is_superuser == False]
