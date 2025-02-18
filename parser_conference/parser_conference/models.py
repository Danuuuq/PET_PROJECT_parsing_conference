from sqlalchemy import Column, Integer, String, Date, Time, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Conference(Base):
    __tablename__ = 'conference'
    id = Column(Integer(), primary_key=True)
    id_conf = Column(Integer(), unique=True, nullable=False)
    date = Column(Date())
    start = Column(Time())
    end = Column(Time())
    rooms = Column(Text())
    comment = Column(Text(), nullable=True)
    organizer = Column(Text(), nullable=True)
    manager = Column(Text(), nullable=True)
