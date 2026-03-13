from .database import Base
from sqlalchemy import Integer, String, Text, Boolean, func, text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from typing import List, Optional
from datetime import datetime

class Post(Base):
    __tablename__ = 'posts'
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    user_id: Mapped[id | None] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    owner: Mapped["User|None"] = relationship("User", back_populates="posts", passive_deletes=True)


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    phone_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, unique=True, default=None)

    posts: Mapped[List["Post"]] = relationship("Post", back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"
    __table_args__ = {"extend_existing": True}

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
