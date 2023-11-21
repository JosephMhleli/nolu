from flask import Flask, render_template,request,make_response,jsonify,session,redirect, url_for
import jwt
from passlib.hash import bcrypt

from datetime import datetime,timedelta,timezone
from functools import wraps
from db import User, UserSession
from db import Book, BookSession

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c87793cf26c24a759e75c3713de80466'    

def token_required(func):
     @wraps(func)
     def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert!': 'Invalid Token!'})
        return decorated
      
@app.route('/')     # for the public anyone can access this side......
def index():
    if not session.get('logged in'):
      return render_template('index.html' )
    else :
        return 'Logged in Currently!'
    
    
@app.route('/login')
def show_login():
    return render_template('LoginPage.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        db_session = UserSession()
        user = db_session.query(User).filter_by(email=email).first()

        if user and bcrypt.verify(password, user.password):
            session['logged_in'] = True
            expiration_time = datetime.now(timezone.utc) + timedelta(seconds=120)
            token = jwt.encode({'user': user.email, 'expiration': str(expiration_time)},
                               app.config['SECRET_KEY'])
            db_session.close()
            return redirect(url_for('index'))
        else:
            db_session.close()
            return make_response('Unable to verify', 403)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/register')
def show_register():
    return render_template('Register.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        db_session = UserSession()
        if password != confirm_password:
            return make_response('Passwords do not match. Please try again.', 400)
        
        # Check if the email already exists
        if db_session.query(User).filter_by(email=email).first():
            return make_response('Email already exists. Please use a different email.', 400)

        # Create a new user and add it to the database
        new_user = User(name=name, surname=surname, email=email, password=bcrypt.hash(password))
        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('show_login'))

    except Exception as e:
        return make_response(str(e), 500)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index.html'))

@app.route('/SelectBook',methods = ['GET'])

def myBook():
     return 'View Book'

@app.route('/BookInte', methods=['GET'])
def get_books():
    try:
        # Query the database to get all books
        dbb_session = BookSession()
        books = dbb_session.query(Book).all()
        dbb_session.close()

        # Prepare the response data
        book_list = [{"id": book.id, "title": book.title, "author": book.author, "category": book.category, "price": book.price, "image_url": book.image_url} for book in books]

        # Return the list of books as JSON
        return jsonify({"books": book_list})
    except Exception as e:
        return make_response(str(e), 500)
   
@app.route('/BookInte', methods=['POST'])
def add_book():
    try:
        # Extract book information from the request form
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        img_url = request.form['img_url']
        price = request.form['price']

        if not all([title, author, category, img_url, price]):
          abort(400, 'Missing required fields')
        # Create a new book instance
        new_book = Book(title=title, author=author, category=category, image_url=img_url, price=price)

        # Add the book to the database
        dbb_session = BookSession()
        dbb_session.add(new_book)
        dbb_session.commit()
        dbb_session.close()

        return 'Book added successfully'
    except IntegrityError:
        dbb_session.rollback()
        return make_response('Book with the same title already exists', 409)
    except Exception as e:
        return make_response(str(e), 500)
 
 
@app.route('/BookInte', methods=['PUT'])
def update_book():
    try:
        # Extract book information from the request form
        book_id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        img_url = request.form['img_url']
        price = request.form['price']

        if not all([book_id, title, author, category, img_url, price]):
            abort(400, 'Missing required fields')

        # Query the database to get the existing book
        db_session = BookSession()
        existing_book = db_session.query(Book).filter_by(id=book_id).first()

        # Update the book information
        existing_book.title = title
        existing_book.author = author
        existing_book.category = category
        existing_book.image_url = img_url
        existing_book.price = price

        # Commit the changes to the database
        db_session.commit()
        db_session.close()

        return 'Book updated successfully'
    except Exception as e:
        return make_response(str(e), 500)
    
@app.route('/BookInte', methods=['DELETE'])
def delete_book():
    try:
        # Extract book ID from the request form
        book_id = request.form['id']
         
        if not book_id:
            abort(400, 'Missing book ID')
        # Query the database to get the existing book
        db_session = BookSession()
        book_to_delete = db_session.query(Book).filter_by(id=book_id).first()

        # Remove the book from the database
        db_session.delete(book_to_delete)
        db_session.commit()
        db_session.close()

        return 'Book deleted successfully'
    except Exception as e:
        return make_response(str(e), 500)
           
    
     
    
            
    
# @app.route('/Add2Cart',methods = ['POST','GET','DELETE'])
# @token_required
# def addtocart():
#      return 'added to cart!'


# @app.route('/Favorites',methods = ['POST','GET','DELETE'])
# @token_required
# def myFavorites():
#      return 'My favorites!'



if __name__ == '__main__':
    app.run(debug=True)
