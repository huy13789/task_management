from typing import List

from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm import Session, joinedload
from starlette import status

from ..schemas.board import BoardCreate
from ..models.task import Board, BoardMember, BoardVisibility, Column


class BoardService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, board_data: BoardCreate, user_id: int) -> Board:
        new_board = Board(
            title = board_data.title,
            visibility = board_data.visibility,
            background = board_data.background,
            owner_id = user_id
        )

        try:
            self.db.add(new_board)
            self.db.flush()

            member = BoardMember(
                board_id=new_board.id,
                user_id=user_id,
                role="admin"
            )
            self.db.add(member)

            self.db.commit()
            self.db.refresh(new_board)
            logger.info(f"User {user_id} created board {new_board.id}")
            return new_board
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating board: {e}")
            raise HTTPException(status_code=500, detail="Failed to create board")

    def get_my_boards(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Board]:
        try:
            return (
                self.db.query(Board)
                .join(BoardMember, Board.id == BoardMember.board_id)
                .filter(
                    BoardMember.user_id == user_id,
                    Board.is_closed == False
                )
                .order_by(Board.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
        except Exception as e:
            logger.error(f"Error fetching boards for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve boards"
            )

    def get_board_detail(self, board_id: int, user_id: int) -> Board:
        
        board = (
            self.db.query(Board)
            .options(
                joinedload(Board.columns).joinedload(Column.cards)
            )
            .filter(Board.id == board_id)
            .first()
        )

        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        valid_columns = []
        for col in board.columns:
            if not col.is_archived:
                active_cards = [
                    card for card in col.cards
                    if not card.is_archived
                ]

                active_cards.sort(key=lambda x: x.position)
                col.cards = active_cards
                valid_columns.append(col)

        valid_columns.sort(key=lambda x: x.position)
        board.columns = valid_columns
        return board

    def delete_board(self, board_id: int, user_id: int, permanent: bool = False):
        board = self.db.query(Board).filter(Board.id == board_id).first()
        if not board:
            raise HTTPException(status_code=404, detail="Board not found")

        if board.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Only board owner can delete")

        if permanent:
            if not board.is_closed:
                raise HTTPException(
                    status_code=400,
                    detail="Board must be closed before permanent deletion."
                )
            try:
                self.db.delete(board)
                self.db.commit()
                logger.info(f"User {user_id} permanently deleted board {board_id}")
                return {"message": "Board deleted permanently"}
            except Exception as e:
                self.db.rollback()
                logger.error(f"Error hard delete: {e}")
                raise HTTPException(status_code=500, detail="Failed to delete permanently")
        else:
            if board.is_closed:
                raise HTTPException(status_code=400, detail="Board is already closed")

            board.is_closed = True
            self.db.commit()
            logger.info(f"User {user_id} closed board {board_id}")
            return {"message": "Board closed successfully"}