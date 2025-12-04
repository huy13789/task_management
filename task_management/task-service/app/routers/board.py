from typing import List
from fastapi import APIRouter, status, Query

from ..schemas.board import BoardResponse, BoardCreate, BoardDetailResponse
from ..services.board_service import BoardService
from ..api.deps import SessionDep, CurrentUser


router = APIRouter(prefix="/boards", tags=["Boards"])

@router.post("/", response_model=BoardResponse, status_code=status.HTTP_201_CREATED)
def create_board(
    board_data: BoardCreate, 
    db: SessionDep, 
    current_user: CurrentUser
):
    return BoardService(db).create(board_data, user_id=current_user.id)


@router.get("/", response_model=List[BoardResponse])
def get_my_boards(
    db: SessionDep, 
    current_user: CurrentUser, 
    skip: int = 0, 
    limit: int = 100
):
    return BoardService(db).get_my_boards(user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{board_id}", response_model=BoardDetailResponse)
def get_board_details(
    board_id: int, 
    db: SessionDep, 
    current_user: CurrentUser
):
    return BoardService(db).get_board_detail(board_id, user_id=current_user.id) 


# CLOSE - DELETE BOARD
@router.delete("/{board_id}", response_model=dict)
def delete_board(
    board_id: int,
    db: SessionDep,
    current_user: CurrentUser,
    permanent: bool = Query(False)
):
    return BoardService(db).delete_board(
        board_id=board_id, 
        user_id=current_user.id, 
        permanent=permanent
    )