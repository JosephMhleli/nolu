from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    author = Column(String(100), unique=False, nullable=False)
    category = Column(String(50))
    price = Column(String(20))
    image_url = Column(String(100))

# Change the database name
engine = create_engine('sqlite:///BooksDatabase.db', echo=True)

# Create the table
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
