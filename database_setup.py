import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))  # picture is a URI


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return category data in serialized format"""
        return {
            "name": self.name,
            "id": self.id,
            "description": self.description,
            "user_id": self.user_id
        }


class Instrument(Base):
    __tablename__ = 'instrument'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    price = Column(Integer)  # probably a Float in real life, but we'll go with even dollars
    low_note = Column(String(4))
    high_note = Column(String(4))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return instrument data in serialized format"""
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "price": self.price,
            "low_note": self.low_note,
            "high_note": self.high_note
        }

engine = create_engine('sqlite:///musicalinstruments.db')


Base.metadata.create_all(engine)