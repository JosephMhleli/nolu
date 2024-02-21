from sqlalchemy import create_engine, Column, String, Integer, Sequence,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50), unique=False, nullable=False)
    surname = Column(String(50), unique=False, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(100))
    
    carts = relationship('Cart', back_populates='user')
    favorites = relationship('Favorite', back_populates='user')
    requests = relationship('Request', back_populates='user')
class Favorite(Base):
    __tablename__='favorites'
    id = Column(Integer, Sequence('favorite_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates= 'favorites')
    items = relationship('FavoriteItem', back_populates='favorite')
    
class FavoriteItem(Base):
    __tablename__='favorite_items'
    id = Column(Integer, Sequence('favorite_item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    image_url = Column(String(50), nullable=False)
    author = Column(Integer, nullable=False)
    favorite_id = Column(Integer, ForeignKey('favorites.id'), nullable=False)
    favorite = relationship('Favorite', back_populates='items')
    
    
    
class Request(Base):
    __tablename__='requests'
    id = Column(Integer, Sequence('request_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates= 'requests')
    items = relationship('RequestItem', back_populates='request')
    
class RequestItem(Base):
    __tablename__='request_items'
    id = Column(Integer, Sequence('request_item_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    cell = Column(Integer, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    title = Column(String(100), unique=False, nullable=False)
    
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    request = relationship('Request', back_populates='items')
                
class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, Sequence('cart_id_seq'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
    user = relationship('User', back_populates='carts') 
    items = relationship('CartItem', back_populates='cart')

class CartItem(Base):
    __tablename__ = 'cart_items'

    id = Column(Integer, Sequence('cart_item_id_seq'), primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    image_url = Column(String(100))
    price = Column(Integer, nullable=False)
    
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    cart = relationship('Cart', back_populates='items')

class NewsLetter(Base):
    __tablename__='news'
    id = Column(Integer, Sequence('new_id_seq'), primary_key=True)
    email = Column(String(50), unique=True, nullable=False)

# Book Class
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Sequence('book_id_seq'), primary_key=True)
    title = Column(String(100), unique=False, nullable=False)
    author = Column(String(100), unique=False, nullable=False)
    descri = Column(String(100), unique=False, nullable=False)
    category = Column(String(50))
    price = Column(String(20))
    image_url = Column(String(100))


# Create an SQLite database for the User
engine = create_engine('sqlite:///NoluUsers.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
