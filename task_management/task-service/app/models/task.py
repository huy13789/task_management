
import enum

from sqlalchemy import Column as SqlColumn, Integer, DateTime, func, Table, ForeignKey, String, Boolean, Enum as DbEnum, \
    Float
from sqlalchemy.orm import relationship

from . import Base

class BoardMember(Base):
    __tablename__ = "board_members"

    board_id = SqlColumn(Integer, ForeignKey("boards.id"), primary_key=True)
    user_id = SqlColumn(Integer, primary_key=True)

    role = SqlColumn(String, default="member")
    joined_at = SqlColumn(DateTime(timezone=True), server_default=func.now())

    board = relationship("Board", back_populates="members")


class CardAssignment(Base):
    __tablename__ = "card_assignments"

    card_id = SqlColumn(Integer, ForeignKey("cards.id"), primary_key=True)
    user_id = SqlColumn(Integer, primary_key=True)

    role = SqlColumn(String, default="assignee")
    assigned_at = SqlColumn(DateTime(timezone=True), server_default=func.now())

    card = relationship("Card", back_populates="assignments")


card_labels = Table(
    "card_labels",
    Base.metadata,
    SqlColumn("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    SqlColumn("label_id", Integer, ForeignKey("labels.id"), primary_key=True)
)


class BoardVisibility(str, enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    WORKSPACE = "workspace"
    ORGANIZATION = "organization"


class Board(Base):
    __tablename__ = "boards"

    id = SqlColumn(Integer, primary_key=True, index=True)
    title = SqlColumn(String, nullable=False)
    owner_id = SqlColumn(Integer, nullable=False, index=True)
    visibility = SqlColumn(
        DbEnum(BoardVisibility),
        default=BoardVisibility.PRIVATE,
        nullable=False
    )
    background = SqlColumn(String, nullable=True)

    is_closed = SqlColumn(Boolean, default=False)

    created_at = SqlColumn(DateTime(timezone=True), server_default=func.now())
    updated_at = SqlColumn(DateTime(timezone=True), onupdate=func.now())

    columns = relationship("Column", back_populates="board", cascade="all, delete-orphan")

    labels = relationship("Label", back_populates="board", cascade="all, delete-orphan")
    members = relationship("BoardMember", back_populates="board", cascade="all, delete-orphan")


class Label(Base):
    __tablename__ = "labels"

    id = SqlColumn(Integer, primary_key=True, index=True)
    title = SqlColumn(String, nullable=True)
    color = SqlColumn(String, nullable=False)

    board_id = SqlColumn(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="labels")
    cards = relationship("Card", secondary=card_labels, back_populates="labels")


class Column(Base):
    __tablename__ = "columns"

    id = SqlColumn(Integer, primary_key=True, index=True)
    title = SqlColumn(String, nullable=False)
    position = SqlColumn(Float, nullable=False, default=0.0)

    is_archived = SqlColumn(Boolean, default=False)

    board_id = SqlColumn(Integer, ForeignKey("boards.id"), index=True)
    board = relationship("Board", back_populates="columns")

    created_at = SqlColumn(DateTime(timezone=True), server_default=func.now())
    updated_at = SqlColumn(DateTime(timezone=True), onupdate=func.now())

    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan", order_by="Card.position")


class Card(Base):
    __tablename__ = "cards"

    id = SqlColumn(Integer, primary_key=True, index=True)
    title = SqlColumn(String, nullable=False)
    description = SqlColumn(String, nullable=True)
    position = SqlColumn(Float, nullable=False, default=0.0)

    is_archived = SqlColumn(Boolean, default=False)

    column_id = SqlColumn(Integer, ForeignKey("columns.id"), index=True)
    column = relationship("Column", back_populates="cards")

    created_at = SqlColumn(DateTime(timezone=True), server_default=func.now())
    updated_at = SqlColumn(DateTime(timezone=True), onupdate=func.now())

    labels = relationship("Label", secondary=card_labels, back_populates="cards")
    assignments = relationship("CardAssignment", back_populates="card", cascade="all, delete-orphan")