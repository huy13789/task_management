from fastapi import APIRouter
from fastapi.params import Query
from starlette import status

from ..schemas.card import CardResponse, CardCreate, CardUpdate
from ..api.deps import SessionDep, CurrentUser
from ..services.card_service import CardService

router = APIRouter(prefix="/cards", tags=["Cards"])

@router.post("/", response_model=CardResponse, status_code=status.HTTP_200_OK)
def create_card(
    card_data: CardCreate,
    db: SessionDep,
    current_user: CurrentUser
):
    return CardService(db).create(card_data, user_id=current_user.id)

@router.patch("/{card_id}", response_model=CardResponse)
def update_card(
    card_id: int,
    data_update: CardUpdate,
    db: SessionDep,
    current_user: CurrentUser
):
    return CardService(db).update(card_id, data_update, current_user.id)

@router.delete("/{card_id}", response_model=dict)
def delete_card(
    card_id: int,
    db: SessionDep,
    current_user: CurrentUser,
    permanent: bool = Query(False)
):
    return CardService(db).delete(card_id, current_user.id, permanent)

@router.post("/{card_id}/unarchived", response_model=CardResponse)
def unarchived_column(
        card_id: int,
        db: SessionDep,
        current_user: CurrentUser
):
    return CardService(db).unarchived_card(card_id, user_id=current_user.id)