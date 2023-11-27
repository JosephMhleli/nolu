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


# gets the list of all the books in thr database
@app.route('/getbooks', methods=['GET'])
def list_books():
    try:
        # Query the database to get all books
        book_session = BookSession()
        books = book_session.query(Book).all()
        book_session.close()

        book_list = [{'id': book.id,
                      'title': book.title,
                      'author': book.author,
                      'category': book.category,
                      'price': book.price,
                      'image_url': book.image_url
                      } for book in books]

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/books/<category>', methods=['GET'])
def get_books(category):
  
    try:
        # Query the database to get books for a specific category
        book_session = BookSession()
        books = book_session.query(Book).filter_by(category=category).all()
        book_session.close()

        if not books:
            return jsonify({'error': 'Category not found'}), 404

        # Convert the SQLAlchemy objects to dictionaries
        book_list = [{'id': book.id,
                      'title': book.title,
                      'author': book.author,
                      'category': book.category,
                      'price': book.price,
                      'image_url': book.image_url
                      } for book in books]

        return render_template('categoryBooks.html', books=book_list, category=category)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  

@app.route('/ProductPage')
def product_page():
    # Retrieve parameters from the URL
    title = request.args.get('title', '')
    price = request.args.get('price', '')
    image_url = request.args.get('image_url', '')
    author = request.args.get('author', '')
    category = request.args.get('category', '')

    # Render the template with the dynamic parameters
    return render_template('ProductPage.html', title=title, price=price, image_url=image_url, author=author, category=category)


@app.route('/search', methods=['GET'])
def search_books():
    try:
        # Retrieve the search query from the request parameters
        search_query = request.args.get('query', '')

        # Query the database to get books with the specified title
        book_session = BookSession()
        books = book_session.query(Book).filter(Book.title.ilike(f"%{search_query}%")).all()
        book_session.close()

        if not books:
            return render_template('categoryBooks.html', books=[], category=search_query, no_results=True)

        # Convert the SQLAlchemy objects to dictionaries
        book_list = [{'id': book.id,
                      'title': book.title,
                      'author': book.author,
                      'category': book.category,
                      'price': book.price,
                      'image_url': book.image_url
                      } for book in books]

        return render_template('categoryBooks.html', books=book_list, category=search_query)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


 
 

    
            
    
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
