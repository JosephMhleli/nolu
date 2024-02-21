from flask import Flask, render_template, request, redirect, url_for, make_response
from db import Book, Session
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# Routes for Admin to Add, Edit, and Delete Books
@app.route('/')
def show():
    return render_template('bookRegister.html')


@app.route('/admin/books', methods=['GET'])
def list_books():
    try:
        # Query the database to get all books
        book_session = Session()
        books = book_session.query(Book).all()
        book_session.close()

        # Render a page with a list of books
        return render_template('admin_books.html', books=books)
    except Exception as e:
        return make_response(str(e), 500)

@app.route('/admin/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            # Extract book information from the form
            title = request.form['title']
            author = request.form['author']
            category = request.form['category']
            img_url = request.form['img_url']
            decrip = request.form['decrip']
            price = request.form['price']
            print(f"Title: {title}, Author: {author}, Category: {category}, Img URL: {img_url}, Price: {price}")
            # Validate input data
            if not all([title, author, category, img_url, price,decrip]):
                return make_response('Missing required fields', 400)

            # Create a new book instance
            new_book = Book(title=title, author=author, category=category, price=price,image_url=img_url,descri = decrip )

            # Add the book to the database
            book_session = Session()
            book_session.add(new_book)
            book_session.commit()
            book_session.close()

            return redirect(url_for('list_books'))

        except Exception as e:
            return make_response(str(e), 500)
@app.route('/admin/books/modify', methods=['PUT'])
def update_book():
    try:
        # Extract book information from the request form
        book_id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        category = request.form['category']
        img_url = request.form['img_url']
        descrip = request.form['descrip']
        price = request.form['price']

        if not all([book_id, title, author, category, img_url, price,descrip]):
            abort(400, 'Missing required fields')

        # Query the database to get the existing book
        db_session = Session()
        existing_book = db_session.query(Book).filter_by(id=book_id).first()

        # Update the book information
        existing_book.title = title
        existing_book.author = author
        existing_book.category = category
        existing_book.image_url = img_url
        existing_book.descri = descrip
        existing_book.price = price

        # Commit the changes to the database
        db_session.commit()
        db_session.close()

        return 'Book updated successfully'
    except Exception as e:
        return make_response(str(e), 500)
    
@app.route('/admin/books/delete', methods=['DELETE'])
def delete_book():
    try:
        # Extract book ID from the request form
        book_id = request.form['id']
         
        if not book_id:
            abort(400, 'Missing book ID')
        # Query the database to get the existing book
        db_session = Session()
        book_to_delete = db_session.query(Book).filter_by(id=book_id).first()

        # Remove the book from the database
        db_session.delete(book_to_delete)
        db_session.commit()
        db_session.close()

        return 'Book deleted successfully'
    except Exception as e:
        return make_response(str(e), 500)
           
    
     
    return render_template('add_book.html')

# Additional routes for editing and deleting books can be added similarly

if __name__ == '__main__':
    app.run(debug=True)
