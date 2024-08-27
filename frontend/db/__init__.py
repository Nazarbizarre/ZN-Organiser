from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column


engine = create_engine("sqlite:///users.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


def up():
    Base.metadata.create_all(engine)

def down():
    Base.metadata.drop_all(engine)

from .models import User


# down()
up()