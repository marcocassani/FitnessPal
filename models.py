"""
The file that holds the schema/classes
that will be used to create objects
and connect to data tables.
"""

from sqlalchemy import ForeignKey, Column, INTEGER, TEXT
from sqlalchemy.orm import relationship
from database import Base

# TODO: Complete your models

class User(Base):
    __tablename__ = "users"

    # Columns
    username = Column("username", TEXT, primary_key=True)
    password = Column("password", TEXT, nullable=False)
    age = Column("age", INTEGER, nullable=False)
    sex = Column("sex", TEXT, nullable=False)

    # Constructor
    def __init__(self, username, password, age, sex):
        # id auto-increments
        self.username = username
        self.password = password
        self.age = age
        self.sex = sex
    
class Workout(Base):
    __tablename__ = "workouts"

    # Columns
    id = Column("id", INTEGER, primary_key=True)
    header = Column("header", TEXT, nullable=True)
    category = Column("category", TEXT, nullable=False)
    sex = Column("sex", TEXT, nullable=False)
    max_age = Column("max_age", INTEGER, nullable=False)
    info = Column("info", TEXT, nullable=False)
    img = Column("img", TEXT, nullable=False)

    # Constructor
    def __init__(self, header, category, sex, max_age, info, img):
        # id auto-increments
        self.header = header
        self.category = category
        self.sex = sex
        self.max_age = max_age
        self.info = info
        self.img = img
    
    def __repr__(self):
        return self.header