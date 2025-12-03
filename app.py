from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

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
   # New columns for rating and category
   rating = db.Column(db.Integer, default=0)  # 0-5 stars
   category = db.Column(db.String(50), default='General')  # Genre/category

# --- THE ROUTES (Logic) ---

# 1. READ (Home Page) with search
@app.route('/')
def index():
   search_query = request.args.get('search', '')
   if search_query:
       books = Book.query.filter(Book.title.contains(search_query) | Book.author.contains(search_query)).all()
   else:
       books = Book.query.all()
   return render_template('index.html', books=books, search_query=search_query)

# 2. CREATE (Add a Book)
@app.route('/add', methods=['POST'])
def add_book():
   title = request.form.get('title')
   author = request.form.get('author')
   book_format = request.form.get('format') # Capture dropdown value
   rating = request.form.get('rating', 0)  # Capture rating value
   category = request.form.get('category', 'General')  # Capture category value

   new_book = Book(title=title, author=author, format=book_format, rating=int(rating), category=category)
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
       book.rating = int(request.form['rating'])
       book.category = request.form['category']
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

def add_missing_columns():
   """Add any missing columns to the database"""
   with app.app_context():
       # Get the current table structure
       inspector = db.inspect(db.engine)
       columns = [column['name'] for column in inspector.get_columns('book')]

       # Add rating column if it doesn't exist
       if 'rating' not in columns:
           print("Adding missing 'rating' column...")
           db.session.execute(db.text("ALTER TABLE book ADD COLUMN rating INTEGER DEFAULT 0"))
           db.session.commit()

       # Add category column if it doesn't exist
       if 'category' not in columns:
           print("Adding missing 'category' column...")
           db.session.execute(db.text("ALTER TABLE book ADD COLUMN category TEXT DEFAULT 'General'"))
           db.session.commit()

# Initialize DB and Run
if __name__ == "__main__":
   with app.app_context():
       db.create_all()
       add_missing_columns()  # Add missing columns if needed
   app.run(debug=True)