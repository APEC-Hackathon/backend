from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps


router = APIRouter()


@router.post("/{peer_id}/", response_model=schemas.Message)
def send_message(
    *,
    db: Session = Depends(deps.get_db),
    peer_id: int,
    message_in: schemas.MessageCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Send a message to another user.
    """
    receiver = crud.user.get(db, id=peer_id)
    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    message = crud.message.create_with_sender_and_receiver(
        db=db, obj_in=message_in, sender_id=current_user.id, receiver_id=peer_id
    )
    return message


@router.get('/{peer_id}/sent', response_model=List[schemas.Message])
def read_sent_messages(
    peer_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve messages.
    """
    messages = crud.message.get_multi_by_sender_and_receiver(
        db=db, sender_id=current_user.id, receiver_id=peer_id
    )
    return messages


@router.get('/{peer_id}/received', response_model=List[schemas.Message])
def read_received_messages(
    peer_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve messages.
    """
    messages = crud.message.get_multi_by_sender_and_receiver(
        db=db, sender_id=peer_id, receiver_id=current_user.id
    )
    return messages
