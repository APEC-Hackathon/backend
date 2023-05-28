from typing import Any, List

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
    prefered_language: str = Body(None),
    country: str = Body(None),
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
    if prefered_language is not None:
        user_in.prefered_language = prefered_language
    if country is not None:
        user_in.country = country
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
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/all/', response_model=List[schemas.User])
def get_all_user(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all users
    """
    users = crud.user.get_multi(db)
    return [user for user in users if user.id != current_user.id and user.is_superuser == False]
