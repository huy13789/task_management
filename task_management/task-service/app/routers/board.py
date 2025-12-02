from typing import List
from fastapi import APIRouter, status, Query
from fastapi.params import Query

from ..schemas.board import BoardResponse, BoardCreate, BoardDetailResponse
from ..services.board_service import BoardService
from ..api.deps import SessionDep, CurrentUser
router = APIRouter(prefix="/boards", tags=["Boards"])

@router.post("/", response_model=BoardResponse, status_code=status.HTTP_200_OK)
def create_board( board_data: BoardCreate, db: SessionDep, user_id: CurrentUser):
    return BoardService(db).create(board_data, user_id)


@router.get("/", response_model=List[BoardResponse])
def get_my_boards( db: SessionDep, user_id: CurrentUser, skip: int = 0, limit: int = 100):
    return BoardService(db).get_my_boards(user_id, skip, limit)


@router.get("/{board_id}", response_model=BoardDetailResponse)
def get_board_details( board_id: int, db: SessionDep, user_id: CurrentUser):
    return BoardService(db).get_board_detail(board_id, user_id)


@router.delete("/{board_id}")
def delete_board(
    board_id: int,
    permanent: bool = Query(False, description="True: Xóa vĩnh viễn/False: Đóng bảng."),
    db: SessionDep = None,
    user_id: CurrentUser = None
):
    return BoardService(db).delete_board(board_id, user_id, permanent)