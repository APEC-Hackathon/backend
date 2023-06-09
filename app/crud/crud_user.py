from typing import Any, Dict, Optional, Union 

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User 
from app.schemas.user import UserCreate, UserUpdate
from app.utils.languages import is_supported_language
from app.utils.images import get_default_ava_url


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        if obj_in.prefered_language is None or not is_supported_language(obj_in.prefered_language):
            obj_in.prefered_language = "en"
        if obj_in.avatar_url is None:
            obj_in.avatar_url = get_default_ava_url()
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
            organization_name=obj_in.organization_name,
            organization_description=obj_in.organization_description,
            prefered_language=obj_in.prefered_language,
            country=obj_in.country,
            avatar_url=obj_in.avatar_url,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User: 
        print(1)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if 'password' in update_data:
            hashed_password = get_password_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        if 'prefered_language' not in update_data or not is_supported_language(update_data['prefered_language']):
            update_data['prefered_language'] = "en"
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None 
        if not verify_password(password, user.hashed_password):
            return None 
        return user 
    
    def is_superuser(self, user: User) -> bool:
        return user.is_superuser
    

user = CRUDUser(User)
