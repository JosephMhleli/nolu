from sqlalchemy import create_engine, Column, String, Integer, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

Base = declarative_base()

# User Class
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    surname = Column(String(50), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100))

# User Database
user_engine = create_engine('sqlite:///NoluUsers.db', echo=True)
Base.metadata.create_all(user_engine)
UserSession = sessionmaker(bind=user_engine)

# Book Class
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    author = Column(String(100), unique=False, nullable=False)
    category = Column(String(50))
    price = Column(String(20))
    image_url = Column(String(100))

# Book Database
book_engine = create_engine('sqlite:///BooksDatabase.db', echo=True)
Base.metadata.create_all(book_engine)
BookSession = sessionmaker(bind=book_engine)
