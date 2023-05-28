from typing import Any, List 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils.images import get_default_collaboration_img_url

router = APIRouter()


@router.post('/', response_model=schemas.Collaboration)
def create_collaboration(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_in: schemas.CollaborationCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new collaboration.
    """
    if collaboration_in.image_url is None:
        collaboration_in.image_url = get_default_collaboration_img_url()
    if collaboration_in.source_id is not None:
        source_problem = crud.problem.get(db=db, id=collaboration_in.source_id)
        if not source_problem:
            raise HTTPException(status_code=404, detail='Source problem not found')
    collaboration = crud.collaboration.create_with_owner(
        db=db, obj_in=collaboration_in, owner_id=current_user.id
    )
    return collaboration


@router.get('/', response_model=List[schemas.Collaboration])
def read_my_collaborations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve my collaborations.
    """
    collaborations = crud.collaboration.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return collaborations


@router.get('/{collaboration_id}', response_model=schemas.Collaboration)
def read_collaboration_by_id(
    collaboration_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a collaboration by ID.
    """
    collaboration = crud.collaboration.get(db=db, id=collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    return collaboration


@router.put('/{collaboration_id}', response_model=schemas.Collaboration)
def update_my_collaboration(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_id: int,
    collaboration_in: schemas.CollaborationUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a collaboration.
    """
    collaboration = crud.collaboration.get(db=db, id=collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    if not crud.user.is_superuser(current_user) and (collaboration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration = crud.collaboration.update(db=db, db_obj=collaboration, obj_in=collaboration_in)
    return collaboration


@router.delete('/{collaboration_id}', response_model=schemas.Collaboration)
def delete_collaboration(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a collaboration.
    """
    collaboration = crud.collaboration.get(db=db, id=collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    if not crud.user.is_superuser(current_user) and (collaboration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration = crud.collaboration.remove(db=db, id=collaboration_id)
    return collaboration


@router.get('/feed/', response_model=List[schemas.Collaboration])
def read_all_collaborations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all collaborations.
    """
    collaborations = crud.collaboration.get_multi(
        db=db, skip=skip, limit=limit
    )
    return collaborations


@router.post('/{collaboration_id}/bid/', response_model=schemas.CollaborationBid)
def create_collaboration_bid(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_id: int,
    collaboration_bid_in: schemas.CollaborationBidCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new collaboration bid.
    """
    collaboration = crud.collaboration.get(db=db, id=collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    collaboration_bid = crud.collaboration_bid.create_with_bidder(
        db=db, obj_in=collaboration_bid_in, owner_id=current_user.id, collaboration_id=collaboration_id
    )
    return collaboration_bid


@router.get('/{collaboration_id}/bid/', response_model=List[schemas.CollaborationBid])
def read_collaboration_bids(
    collaboration_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get collaboration bids.
    """
    collaboration = crud.collaboration.get(db=db, id=collaboration_id)
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    collaboration_bids = crud.collaboration_bid.get_multi_by_collaboration(
        db=db, collaboration_id=collaboration_id
    )
    return collaboration_bids
