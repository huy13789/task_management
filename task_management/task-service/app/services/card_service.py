from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette import status

from ..schemas.card import CardCreate, CardUpdate
from ..models.task import Card, BoardMember, Board, Column

POSITION_GAP = 65536.0

class CardService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_cards_in_column(self, user_id: int, column_id: int) -> list[Card]:
        cards = (
            self.db.query(Card)
            
            .join(Column, Card.column_id == Column.id)
            .join(Board, Column.board_id == Board.id)
            .join(BoardMember, Board.id == BoardMember.board_id)
                
            .options(
                joinedload(Card.labels),
                joinedload(Card.assignments)
            )

            .filter(
                Card.column_id == column_id,     
                BoardMember.user_id == user_id,   
                Card.is_archived == False         
            )
                
                .order_by(Card.position.asc())
                .all()
            )
        return cards

    def _check_column_board_member(self, column_id: int, user_id: int):
        has_permission = (
            self.db.query(BoardMember)
            .join(Board, BoardMember.board_id == Board.id)
            .join(Column, Board.id == Column.board_id)
            .filter(
                Column.id == column_id,
                BoardMember.user_id == user_id
            )
            .first()
        )

        if not has_permission:
            raise HTTPException(
                status_code=404,
                detail="Column not found or access denied"
            )

    def create(self, card_data: CardCreate, user_id: int) -> Card:
        column = self.db.query(Column).filter(
            Column.id == card_data.column_id
        ).first()

        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        self._check_column_board_member(card_data.column_id, user_id)

        last_card = self.db.query(Card).filter(
            Card.column_id == card_data.column_id
        ).order_by(Card.position.desc()).first()

        new_pos = (last_card.position + POSITION_GAP) if last_card else POSITION_GAP

        new_card = Card(
            title=card_data.title,
            description=card_data.description,
            column_id=card_data.column_id,
            position=new_pos
        )

        try:
            self.db.add(new_card)
            self.db.commit()
            self.db.refresh(new_card)
            return new_card
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating card: {e}")

    def update(self, card_id: int, update_data: CardUpdate, user_id: int) -> Card:
        card = self.db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        target_column_id = update_data.column_id if update_data.column_id is not None else card.column_id
        self._check_column_board_member(target_column_id, user_id)

        if update_data.title is not None:
            card.title = update_data.title
        if update_data.description is not None:
            card.description = update_data.description

        if update_data.new_index is not None or (update_data.column_id and update_data.column_id != card.column_id):
            target_index = update_data.new_index if update_data.new_index is not None else 0

            cards_in_col = (
                self.db.query(Card)
                .filter(Card.column_id == target_column_id, Card.id != card_id)
                .order_by(Card.position.asc())
                .all()
            )

            new_position = 0.0

            if not cards_in_col:
                new_position = POSITION_GAP

            elif target_index == 0:
                new_position = cards_in_col[0].position / 2.0

            elif target_index >= len(cards_in_col):
                new_position = cards_in_col[-1].position + POSITION_GAP

            else:
                prev_pos = cards_in_col[target_index - 1].position
                next_pos = cards_in_col[target_index].position
                new_position = (prev_pos + next_pos) / 2.0

            card.column_id = target_column_id
            card.position = new_position

        try:
            self.db.commit()
            self.db.refresh(card)
            return card
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating card: {e}")

    def delete(self, card_id: int, user_id: int, permanent: bool = False):
        card = self.db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        self._check_column_board_member(card.column_id, user_id)

        if permanent:
            if not card.is_archived:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Column must be archived before permanent deletion."
                )

            column_id = card.column_id
            deleted_pos = card.position

            try:
                self.db.delete(card)
                self.db.query(Card).filter(
                    Card.column_id == column_id,
                    Card.position > deleted_pos
                ).update({Card.position: Card.position - 1}, synchronize_session=False)
                self.db.commit()
                return {"message": "Card deleted permanently"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to delete card: {str(e)}")

        else:
            if card.is_archived:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Card is already archived"
                )

            try:
                card.is_archived = True
                self.db.commit()
                return {"message": "Card archived successfully"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to archive column: {str(e)}")

    def unarchived_card(self, card_id: int, user_id: int) -> Column:
        card = self.db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")

        self._check_column_board_member(card.column_id, user_id=user_id)

        if not card.is_archived:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Card is not archived"
            )

        try:
            card.is_archived = False
            self.db.commit()
            self.db.refresh(card)
            return card
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to restore card: {str(e)}")