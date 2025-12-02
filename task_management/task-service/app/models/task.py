import enum

from sqlalchemy import Column, Integer, DateTime, func, Table, ForeignKey, String, Boolean, Enum as DbEnum
from sqlalchemy.orm import relationship

from . import Base

board_members = Table(
    "board_members",
    Base.metadata,
    Column("board_id", Integer, ForeignKey("boards.id"), primary_key=True),
    Column("user_id", Integer, primary_key=True), # User ID từ User Service
    Column("role", String, default="member")
)

card_members = Table(
    "card_members",
    Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("user_id", Integer, primary_key=True) # User ID từ User Service
)


card_labels = Table(
    "card_labels",
    Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id"), primary_key=True),
    Column("label_id", Integer, ForeignKey("labels.id"), primary_key=True)
)


class BoardVisibility(str, enum.Enum):
    PRIVATE = "private"
    PUBLIC = "public"
    WORKSPACE = "workspace"
    ORGANIZATION = "organization"


class Board(Base):
    __tablename__ = "boards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    visibility = Column(
        DbEnum(BoardVisibility),
        default=BoardVisibility.PRIVATE,
        nullable=False
    )
    background = Column(String, nullable=True)

    is_closed = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 1 Board có nhiều List
    lists = relationship("List", back_populates="board", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="board", cascade="all, delete-orphan")


class Label(Base):
    __tablename__ = "labels"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    color = Column(String, nullable=False)

    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="labels")

    cards = relationship("Card", secondary=card_labels, back_populates="labels")


class List(Base):
    __tablename__ = "lists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    position = Column(Integer, nullable=False, default=0)

    is_archived = Column(Boolean, default=False)

    # List thuộc Board nào (1 - N)
    board_id = Column(Integer, ForeignKey("boards.id"))
    # Truy vấn xuôi tới bảng Board
    board = relationship("Board", back_populates="lists")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 1 List có nhiều Card
    cards = relationship("Card", back_populates="list", cascade="all, delete-orphan", order_by="Card.position")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    position = Column(Integer, nullable=False, default=0)

    is_archived = Column(Boolean, default=False)

    # Card thuộc List nào (1 - N)
    list_id = Column(Integer, ForeignKey("lists.id"))
    # Truy vấn xuôi tới bảng List
    list = relationship("List", back_populates="cards")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    labels = relationship("Label", secondary=card_labels, back_populates="cards")