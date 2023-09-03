import datetime as dt
import uuid

from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

# from sqlmodel import Column, DateTime, Field, SQLModel, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # id: Mapped[uuid.UUID] = mapped_columm(default=uuid.uuid4, primary_key=True)
    id: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4,
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.utcnow, server_default=func.now()
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=dt.datetime.utcnow, server_default=func.now()
    )
