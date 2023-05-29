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


@router.post('/request', response_model=schemas.CollaborationRequest)
def create_collaboration_request(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_request_in: schemas.CollaborationRequestCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new CollaborationRequest.
    """
    collaboration = crud.collaboration.get(
        db=db, id=collaboration_request_in.collaboration_id
    )
    if not collaboration:
        raise HTTPException(status_code=404, detail='Collaboration not found')
    collaboration_request = crud.collaboration_request.create_with_requester(
        db=db, obj_in=collaboration_request_in, requester_id=current_user.id,
    )
    return collaboration_request


@router.get('/request/{collaboration_request_id}', response_model=schemas.CollaborationRequest)
def read_collaboration_request_by_id(
    collaboration_request_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a CollaborationRequest by ID.
    """
    collaboration_request = crud.collaboration_request.get(db=db, id=collaboration_request_id)
    if not collaboration_request:
        raise HTTPException(status_code=404, detail='CollaborationRequest not found')
    return collaboration_request


@router.put('/request/{collaboration_request_id}', response_model=schemas.CollaborationRequest)
def update_my_collaboration_request(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_request_id: int,
    collaboration_request_in: schemas.CollaborationRequestUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a CollaborationRequest.
    """
    collaboration_request = crud.collaboration_request.get(db=db, id=collaboration_request_id)
    if not collaboration_request:
        raise HTTPException(status_code=404, detail='CollaborationRequest not found')
    if not crud.user.is_superuser(current_user) and (collaboration_request.requester_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration_request = crud.collaboration_request.update(db=db, db_obj=collaboration_request, obj_in=collaboration_request_in)
    return collaboration_request


@router.delete('/request/{collaboration_request_id}', response_model=schemas.CollaborationRequest)
def delete_collaboration_request(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_request_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a CollaborationRequest.
    """
    collaboration_request = crud.collaboration_request.get(db=db, id=collaboration_request_id)
    if not collaboration_request:
        raise HTTPException(status_code=404, detail='CollaborationRequest not found')
    if not crud.user.is_superuser(current_user) and (collaboration_request.requester_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration_request = crud.collaboration_request.remove(db=db, id=collaboration_request_id)
    return collaboration_request


@router.get('/my-requests/', response_model=List[schemas.CollaborationRequest])
def read_my_collaboration_requests(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve my CollaborationRequests.
    """
    collaboration_requests = crud.collaboration_request.get_multi_by_requester(
        db=db, requester_id=current_user.id, skip=skip, limit=limit
    )
    return collaboration_requests


@router.get('/requests/{collaboration_id}', response_model=List[schemas.CollaborationRequest])
def read_collaboration_requests(
    collaboration_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve CollaborationRequests for a Collaboration.
    """
    collaboration_requests = crud.collaboration_request.get_multi_by_collaboration(
        db=db, collaboration_id=collaboration_id
    )
    return collaboration_requests


@router.put('/request/{collaboration_request_id}/accept', response_model=schemas.CollaborationRequest)
def accept_collaboration_request(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_request_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Accept a CollaborationRequest.
    """
    collaboration_request = crud.collaboration_request.get(db=db, id=collaboration_request_id)
    if not collaboration_request:
        raise HTTPException(status_code=404, detail='CollaborationRequest not found')
    collaboration = crud.collaboration.get(db=db, id=collaboration_request.collaboration_id)
    if not crud.user.is_superuser(current_user) and (collaboration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration_request = crud.collaboration_request.accept(db=db, collaboration_request_id=collaboration_request_id)
    return collaboration_request


@router.put('/request/{collaboration_request_id}/reject', response_model=schemas.CollaborationRequest)
def reject_collaboration_request(
    *,
    db: Session = Depends(deps.get_db),
    collaboration_request_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Reject a CollaborationRequest.
    """
    collaboration_request = crud.collaboration_request.get(db=db, id=collaboration_request_id)
    if not collaboration_request:
        raise HTTPException(status_code=404, detail='CollaborationRequest not found')
    collaboration = crud.collaboration.get(db=db, id=collaboration_request.collaboration_id)
    if not crud.user.is_superuser(current_user) and (collaboration.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    collaboration_request = crud.collaboration_request.reject(db=db, collaboration_request_id=collaboration_request_id)
    return collaboration_request
