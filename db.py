from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), unique=False,nullable=False)
    surname = Column(String(50), unique=False,nullable=False)
    email = Column(String(50), unique=True,nullable=False)
    password = Column(String(100))
    

engine = create_engine('sqlite:///NoluUsers.db', echo=True)

# Create the table
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
