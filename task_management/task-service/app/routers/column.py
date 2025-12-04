from fastapi import APIRouter
from fastapi.params import Query
from starlette import status
from ..schemas.column import ColumnResponse, ColumnCreate
from ..api.deps import SessionDep, CurrentUser
from ..services.column_service import ColumnService, ColumnUpdate

router = APIRouter(prefix="/columns", tags=["Columns"])

@router.post("/", response_model=ColumnResponse, status_code=status.HTTP_201_CREATED)
def create_column(
    column_data: ColumnCreate,
    db: SessionDep,
    current_user: CurrentUser
):
    return ColumnService(db).create_column(column_data, user_id=current_user.id)

@router.patch("/{column_id}", response_model=ColumnResponse)
def update_column(
    column_id: int,
    column_data: ColumnUpdate,
    db: SessionDep,
    current_user: CurrentUser
):
    return ColumnService(db).update_column(column_id, column_data, user_id=current_user.id)

@router.delete("/{column_id}", response_model=dict)
def delete_column(
    column_id: int,
    db: SessionDep,
    current_user: CurrentUser,
    permanent: bool = Query(False)
):
    return ColumnService(db).delete_column(column_id, current_user.id, permanent)

@router.post("/{column_id}/unarchived", response_model=ColumnResponse)
def unarchived_column(
    column_id: int,
    db: SessionDep,
    current_user: CurrentUser
):
    return ColumnService(db).unarchived_column(column_id, user_id=current_user.id)

@router.get("/")
def get_columns(
    board_id: int,
    db: SessionDep,
    current_user: CurrentUser
):
    return ColumnService(db).get_columns_by_board_id(board_id, current_user.id)