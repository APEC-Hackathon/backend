from typing import Any, List 

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

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
    Problem = crud.problem.create_with_owner(
        db=db, obj_in=problem_in, owner_id=current_user.id
    )
    return Problem


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
    Problems = crud.problem.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return Problems


@router.get('/{problem_id}', response_model=schemas.Problem)
def read_problem_by_id(
    Problem_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a Problem by ID.
    """
    problem = crud.problem.get(db=db, id=Problem_id)
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
    Update a Problem.
    """
    Problem = crud.Problem.get(db=db, id=problem_id)
    if not Problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    if not crud.user.is_superuser(current_user) and (Problem.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail='Not enough permissions')
    Problem = crud.Problem.update(db=db, db_obj=Problem, obj_in=problem_in)
    return Problem


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

@router.post('/{problem_id}/bid/', response_model=schemas.ProblemBid)
def create_problem_bid(
    *,
    db: Session = Depends(deps.get_db),
    problem_id: int,
    problem_bid_in: schemas.ProblemBidCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Create new ProblemBid.
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    problem_bid = crud.problem_bid.create_with_bidder(
        db=db, obj_in=problem_bid_in, bidder_id=current_user.id
    )
    return problem_bid


@router.get('/{problem_id}/bid/', response_model=List[schemas.ProblemBid])
def read_problem_bids(
    problem_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve ProblemBids.
    """
    problem = crud.problem.get(db=db, id=problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail='Problem not found')
    problem_bids = crud.problem_bid.get_multi_by_problem(
        db=db, problem_id=problem_id
    )
    return problem_bids