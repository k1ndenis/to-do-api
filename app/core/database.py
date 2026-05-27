from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session, relationship
from uuid import uuid4
from contextlib import asynccontextmanager

from app.models.list import ListSchema

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))

class ListORM(Base):
    __tablename__ = "lists"

    id: Mapped[str]
    title: Mapped[str]
    createdAt: Mapped[int]
    tasks: Mapped[list["TaskORM"]] = relationship(
        "TaskORM",
        back_populates="list",
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[str]
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
    createdAt: Mapped[int]
    listId: Mapped[str] = mapped_column(ForeignKey("lists.id"))

    list: Mapped["ListORM"] = relationship("ListORM", back_populates="tasks")

@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(bind=engine)
    yield