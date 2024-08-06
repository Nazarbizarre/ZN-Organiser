from .. import Base

from sqlalchemy.orm import Mapped
from datetime import datetime, date

class Task(Base):
    __tablename__ = "task"

    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[str]
    deadline: Mapped[str]
    theme: Mapped[str]
