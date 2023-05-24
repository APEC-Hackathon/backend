from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
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
    full_name: str = Body(None),
    email: str = Body(None),
    password: str = Body(None),
    organization_name: str = Body(None),
    organization_description: str = Body(None),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update current user
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if email is not None:
        user_in.email = email
        if crud.user.get_by_email(db, email=email):
            raise HTTPException(
                status_code=400,
                detail='The user with this email already exists in the system.',
            )
    if full_name is not None:
        user_in.full_name = full_name
    if password is not None:
        user_in.password = password
    if organization_name is not None:
        user_in.organization_name = organization_name
    if organization_description is not None:
        user_in.organization_description = organization_description
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user
