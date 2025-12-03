from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- THE MODEL (Data Structure) ---
class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   author = db.Column(db.String(100), nullable=False)
   status = db.Column(db.String(20), default='To Read')
   # New column for media type (Physical, E-Book, Audiobook)
   format = db.Column(db.String(20), nullable=False, default='Physical')

# --- THE ROUTES (Logic) ---

# 1. READ (Home Page)
@app.route('/')
def index():
   books = Book.query.all()
   return render_template('index.html', books=books)

# 2. CREATE (Add a Book)
@app.route('/add', methods=['POST'])
def add_book():
   title = request.form.get('title')
   author = request.form.get('author')
   book_format = request.form.get('format') # Capture dropdown value

   new_book = Book(title=title, author=author, format=book_format)
   db.session.add(new_book)
   db.session.commit()
   return redirect(url_for('index'))

# 3. UPDATE (Edit a Book)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):
   book = Book.query.get_or_404(id)
   if request.method == 'POST':
       book.title = request.form['title']
       book.author = request.form['author']
       book.status = request.form['status']
       book.format = request.form['format']
       db.session.commit()
       return redirect(url_for('index'))
   return render_template('update.html', book=book)

# 4. DELETE (Remove a Book)
@app.route('/delete/<int:id>')
def delete_book(id):
   book = Book.query.get_or_404(id)
   db.session.delete(book)
   db.session.commit()
   return redirect(url_for('index'))

# Initialize DB and Run
if __name__ == "__main__":
   with app.app_context():
       db.create_all()
   app.run(debug=True)