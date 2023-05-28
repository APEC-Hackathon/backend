from typing import Any, List 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.utils.images import get_default_problem_img_url

router = APIRouter()


@router.post('/', response_model=schemas.Problem)
def create_problem(
    *,
    db: Session = Depends(deps.get_db),
    problem_in: schemas.ProblemCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new Problem.
    """
    if problem_in.image_url is None:
        problem_in.image_url = get_default_problem_img_url()
    problem = crud.problem.create_with_owner(
        db=db, obj_in=problem_in, owner_id=current_user.id
    )
    return problem


@router.get('/', response_model=List[schemas.Problem])
def read_my_problems(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve my Problems.
    """
    problems = crud.problem.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return problems


@router.get('/{problem_id}', response_model=schemas.Problem)
def read_problem_by_id(
    problem_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a Problem by ID.
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    return problem


@router.put('/{Problem_id}', response_model=schemas.Problem)
def update_my_Problem(
    *,
    db: Session = Depends(deps.get_db),
    problem_id: int,
    problem_in: schemas.ProblemUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a Problem (Can be used to choose the winner).
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    if not crud.user.is_superuser(current_user) and (problem.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    if problem_in.bid_winner_id is not None:
        problem_bid_winner = crud.problem_bid.get(db=db, id=problem_in.bid_winner_id)
        if not problem_bid_winner:
            raise HTTPException(status_code=404, detail='ProblemBid not found')
        if problem_bid_winner.problem_id != problem_id:
            raise HTTPException(status_code=400, detail='ProblemBid is not for this Problem')
    problem = crud.problem.update(db=db, db_obj=problem, obj_in=problem_in)
    return problem


@router.delete('/{problem_id}', response_model=schemas.Problem)
def delete_problem(
    *,
    db: Session = Depends(deps.get_db),
    problem_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a problem.
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    if not crud.user.is_superuser(current_user) and (problem.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    problem = crud.problem.remove(db=db, id=problem_id)
    return problem


@router.get('/feed/', response_model=List[schemas.Problem])
def read_all_problems(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get all problems.
    """
    problems = crud.problem.get_multi(
        db=db, skip=skip, limit=limit
    )
    return problems


@router.post('/bid', response_model=schemas.ProblemBid)
def create_problem_bid(
    *,
    db: Session = Depends(deps.get_db),
    problem_bid_in: schemas.ProblemBidCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new ProblemBid.
    """
    problem = crud.problem.get(db=db, id=problem_bid_in.problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    problem_bid = crud.problem_bid.create_with_bidder(
        db=db, obj_in=problem_bid_in, bidder_id=current_user.id
    )
    return problem_bid


@router.put('/bid/{problem_bid_id}', response_model=schemas.ProblemBid)
def update_my_problem_bid(
    *,
    db: Session = Depends(deps.get_db),
    problem_bid_id: int,
    problem_bid_in: schemas.ProblemBidUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update a ProblemBid.
    """
    problem_bid = crud.problem_bid.get(db=db, id=problem_bid_id)
    if not problem_bid:
        raise HTTPException(status_code=404, detail='ProblemBid not found')
    if not crud.user.is_superuser(current_user) and (problem_bid.bidder_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    problem_bid = crud.problem_bid.update(db=db, db_obj=problem_bid, obj_in=problem_bid_in)
    return problem_bid


@router.get('/bid/{problem_bid_id}', response_model=schemas.ProblemBid)
def read_problem_bid_by_id(
    problem_bid_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a ProblemBid by ID.
    """
    problem_bid = crud.problem_bid.get(db=db, id=problem_bid_id)
    if not problem_bid:
        raise HTTPException(status_code=404, detail='ProblemBid not found')
    return problem_bid


@router.delete('/bid/{problem_bid_id}', response_model=schemas.ProblemBid)
def delete_problem_bid(
    *,
    db: Session = Depends(deps.get_db),
    problem_bid_id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete a problem_bid.
    """
    problem_bid = crud.problem_bid.get(db=db, id=problem_bid_id)
    if not problem_bid:
        raise HTTPException(status_code=404, detail='ProblemBid not found')
    if not crud.user.is_superuser(current_user) and (problem_bid.bidder_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    problem_bid = crud.problem_bid.remove(db=db, id=problem_bid_id)
    return problem_bid


@router.get('/my-bids/', response_model=List[schemas.ProblemBid])
def read_my_problem_bids(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve my ProblemBids.
    """
    problem_bids = crud.problem_bid.get_multi_by_bidder(
        db=db, bidder_id=current_user.id, skip=skip, limit=limit
    )
    return problem_bids


@router.get('/bids/{problem_id}', response_model=List[schemas.ProblemBid])
def read_all_bids_for_a_problem(
    problem_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve ProblemBids for a Problem.
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    problem_bids = crud.problem_bid.get_multi_by_problem(
        db=db, problem_id=problem_id
    )
    return problem_bids
