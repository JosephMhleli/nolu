from flask import Flask,flash, render_template,request,make_response,jsonify,session,redirect, url_for
import jwt
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from passlib.hash import bcrypt
from functools import wraps
from flask import request, jsonify
import requests
from datetime import datetime,timedelta,timezone
from functools import wraps
from db import User 
from db import Book,Favorite, FavoriteItem, Cart,Request,RequestItem,NewsLetter,Session
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c87793cf26c24a759e75c3713de80466'    
mail = Mail(app)

# Email server configuration
app.config['MAIL_SERVER'] = 'smtp.gmail'  # Use your SMTP server details
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lihlemayila7@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'Sisimelele2020#'  # Your email password
app.config['MAIL_DEFAULT_SENDER'] = 'lihlemayila7@gmail.com'  # Default sender

mail.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'token' in request.cookies:
            token = request.cookies['token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_email = data['user']
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user_email, *args, **kwargs)
    return decorated_function


@app.route('/getbooks', methods=['GET'])
def list_books():
    try:  
        book_session = Session() 
        books = book_session.query(Book).all()
        book_session.close()

        book_list = [{'id': book.id,
                      'title': book.title,
                      'author': book.author,
                      'category': book.category,
                      'price': book.price,
                      'image_url': book.image_url,
                      'descri':book.descri
                      } for book in books]

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
       
@app.route('/')     # for the public anyone can access this side......
def index():
    try:
        
        book_response = list_books()  

        # Since list_books returns a Response object, you need to get the JSON data
        books_data = book_response.get_json()  # Extract JSON data from the Response object

        if 'books' in books_data:
            books = books_data['books']
            return render_template('index.html', books=books)
        else:
            return jsonify({'error': "Failed to fetch books."}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/login')
def show_login():
    return render_template('LoginPage.html')

@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()

        if user and bcrypt.verify(password, user.password):
            session['user_id'] = user.id
            session['logged_in'] = True
            expiration_time = datetime.now(timezone.utc) + timedelta(seconds=120)
            token = jwt.encode({'user': user.email, 'exp': expiration_time}, app.config['SECRET_KEY'], algorithm="HS256")
            db_session.close()
            print('Login successful!', 'success')
            response = make_response(redirect(url_for('index')))
            response.set_cookie('token', token, httponly=True, secure=True)  
            return response
        else:
            db_session.close()
            print('Login failed. Please check your email and password.', 'error')
            return make_response('Unable to verify', 403)
    except Exception as e:
        return make_response(str(e), 500)
    
# getting the current user session    
def get_current_user_id():
    return session.get('user_id')

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
        db_session = Session()
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
   
@app.route('/books/<category>', methods=['GET'])
def get_books(category):
  
    try:
        # Query the database to get books for a specific category
        book_session = Session()
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
                      'image_url': book.image_url,
                      'descri': book.descri
                      } for book in books]

        return render_template('categoryBooks.html', books=book_list, category=category)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
  

@app.route('/ProductPage')
def product_page():
    try:
      # Assuming your route for getting books is named 'list_books'
     book_response = list_books()  # Replace localhost:5000 with your actual host and port
     response = book_response.get_json()
     
     title = request.args.get('title', '')
     price = request.args.get('price', '')
     image_url = request.args.get('image_url', '')
     author = request.args.get('author', '')
     category = request.args.get('category', '')
     descri = request.args.get('descri', '')
            
     if 'books' in response:
            books = response['books']
            return render_template('ProductPage.html', title=title, price=price, image_url=image_url, author=author, category=category, descri=descri,books=books)
     else:
            return jsonify({'error': f"Failed to fetch books. Status code"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    
@app.route('/requestBook')
def show_reque():
    return render_template('requestbook.html')

@app.route('/requestBook', methods = ['POST'])
def bookre():
    try:
        title = request.form['title']
        cell = request.form['cell']
        author = request.form['author']
        email = request.form['email']
        name = request.form['name']

        if not all([title, author, cell, email,name]):
                return make_response('Missing required fields', 400)
            #Create a new request
        new_book_req = Request(title = title, author=author,cell=cell,email=email,name=name) 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return render_template('requestbook.html')  

@app.route('/search', methods=['GET'])
def search_books():
    try:
        # Retrieve the search query from the request parameters
        search_query = request.args.get('query', '')

        # Query the database to get books with the specified title
        book_session = Session()
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
                       'descri': book.descri,
                      'image_url': book.image_url
                      } for book in books]

        return render_template('categoryBooks.html', books=book_list, category=search_query)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
 
@app.route('/checkout')
# @token_required
def showcheckout():
        return render_template('checkout.html')


@app.route('/privacy')
def showprivacy():
    return render_template('privacy.html')

    
@app.route('/subscribe',methods = ['POST'])
def sub():
    
    
    email = request.form['email']    
    db_session = Session()       
    existing_email = db_session.query(NewsLetter).filter_by(email=email).first()
    if existing_email:
        flash('This email is already subscribed.', 'info')
        return redirect(url_for('index'))  # Adjust as needed

    # Email doesn't exist, proceed with insertion
    try:
        
        new_entry = NewsLetter(email=email)  # Adjust according to your model
        db_session.add(new_entry)
        db_session.commit()
        flash('Subscription successful!', 'success')
        return jsonify({"success": True, "message": "Contact form submitted successfully!"})
    except Exception as e:
            return make_response(jsonify({"success": False, "message": str(e)}), 500)
               
    
if __name__ == '__main__':
    app.run(debug=True)
