from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from flask_login import UserMixin
from .. import Base

class User(Base):
    __tablename__ = 'users'
    nickname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


    def is_active(self) -> bool:
        return True
    def is_authenticated(self) -> bool:
        return True
    def is_anonymous(self)->bool:
        return False
    def get_id(self)->str:
        return f"{self.id}"