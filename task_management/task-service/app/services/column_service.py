from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from ..schemas.column import ColumnCreate, ColumnUpdate
from ..models.task import Column, BoardMember

class ColumnService:
    def __init__(self, db: Session):
        self.db = db

    def _check_board_member(self, board_id: int, user_id: int) -> None:
        board_member = (
            self.db.query(BoardMember)
            .filter(
                BoardMember.board_id == board_id,
                BoardMember.user_id == user_id
            )
            .first()
        )

        if not board_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to add column to this board"
            )


    def create_column(self, column_data: ColumnCreate, user_id: int) -> Column:
        self._check_board_member(column_data.board_id, user_id=user_id)

        max_pos = self.db.query(func.max(Column.position)).filter(
            Column.board_id == column_data.board_id
        ).scalar()

        new_position = (max_pos + 1) if max_pos is not None else 0

        new_column = Column(
            title=column_data.title,
            board_id=column_data.board_id,
            position=new_position
        )

        try:
            self.db.add(new_column)
            self.db.commit()
            self.db.refresh(new_column)
            return new_column
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to create column: {str(e)}")

    def update_column(self, column_id: int, update_data: ColumnUpdate, user_id: int) -> Column:
        column = self.db.query(Column).filter(Column.id == column_id).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        self._check_board_member(column.board_id, user_id=user_id)

        if update_data.title is not None:
            column.title = update_data.title

        if update_data.position is not None and update_data.position != column.position:
            old_pos = column.position
            new_pos = update_data.position
            board_id = column.board_id

            if new_pos > old_pos:
                self.db.query(Column).filter(
                    Column.board_id == board_id,
                    Column.position > old_pos,
                    Column.position <= new_pos
                ).update({ Column.position: Column.position - 1}, synchronize_session=False)

            else:
                self.db.query(Column).filter(
                    Column.board_id == board_id,
                    Column.position >= new_pos,
                    Column.position < old_pos
                ).update({ Column.position: Column.position + 1}, synchronize_session=False)

            column.position = new_pos
        try:
            self.db.commit()
            self.db.refresh(column)
            return column
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update column: {str(e)}")

    def delete_column(self, column_id: int, user_id: int, permanent: bool = False):
        column = self.db.query(Column).filter(Column.id == column_id).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        self._check_board_member(column.board_id, user_id=user_id)

        if permanent:
            if not column.is_archived:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Column must be archived before permanent deletion."
                )

            board_id = column.board_id
            deleted_pos = column.position

            try:
                self.db.delete(column)

                self.db.query(Column).filter(
                    Column.board_id == board_id,
                    Column.position > deleted_pos
                ).update({Column.position: Column.position - 1}, synchronize_session=False)

                self.db.commit()
                return {"message": "Column deleted permanently"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to delete column: {str(e)}")

        else:
            if column.is_archived:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Column is already archived"
                )

            try:
                column.is_archived = True
                self.db.commit()
                return {"message": "Column archived successfully"}
            except Exception as e:
                self.db.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to archive column: {str(e)}")

    def unarchived_column(self, column_id: int, user_id: int) -> Column:
        column = self.db.query(Column).filter(Column.id == column_id).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")

        self._check_board_member(column.board_id, user_id=user_id)

        if not column.is_archived:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Column is not archived"
            )

        try:
            column.is_archived = False
            self.db.commit()
            self.db.refresh(column)
            return column
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to restore column: {str(e)}")