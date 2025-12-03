ShelfLog: Development Documentation
Project: ShelfLog (Personal Library Manager)
Stack: Python, Flask, SQLite, SQLAlchemy, HTML/CSS (Bootstrap)
Goal: A CRUD application to track Physical Books, E-books, and Audiobooks.
📂 Phase 1: Environment Setup
Before writing code, set up the directory and virtual environment to keep dependencies isolated.
1. Create Project Directory
Run these commands in your terminal:
mkdir shelflog
cd shelflog


2. Set Up Virtual Environment
Windows:
python -m venv venv
venv\Scripts\activate


Mac/Linux:
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies
pip install flask flask-sqlalchemy


🏗 Phase 2: Project Structure
Ensure your folder looks exactly like this. Flask looks for HTML files inside a folder specifically named templates.
shelflog/
├── app.py                # Main application logic & Database Model
├── books.db              # (Created automatically by the app later)
└── templates/            # HTML files
   ├── base.html         # The master layout (header/footer)
   ├── index.html        # Home page (List + Add Form)
   └── update.html       # Edit page


🐍 Phase 3: The Backend (app.py)
Create a file named app.py in the root folder and paste the following code. This handles the Database creation, the Model (data structure), and the Routes (URL logic).
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


🎨 Phase 4: The Frontend (Templates)
Create a folder named templates and add the following three files inside it.
1. templates/base.html
This is the "skeleton" of your site. It loads Bootstrap CSS so the app looks good instantly.
<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>ShelfLog Library</title>
   <!-- Bootstrap CSS CDN -->
   <link href="[https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css](https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)" rel="stylesheet">
</head>
<body class="bg-light">
   <div class="container mt-5">
       <h1 class="text-center mb-4">📚 ShelfLog</h1>
       <!-- Content from other pages will be injected here -->
       {% block content %}{% endblock %}
   </div>
</body>
</html>


2. templates/index.html
The main dashboard. It extends base.html.
{% extends 'base.html' %}

{% block content %}
<!-- ADD NEW ITEM CARD -->
<div class="card p-4 shadow-sm mb-5">
   <h4>Add New Item</h4>
   <form action="/add" method="POST" class="row g-3">
       <div class="col-md-4">
           <input type="text" name="title" class="form-control" placeholder="Title" required>
       </div>
       <div class="col-md-3">
           <input type="text" name="author" class="form-control" placeholder="Author" required>
       </div>
       <div class="col-md-3">
           <select name="format" class="form-select">
               <option value="Physical">📖 Physical Book</option>
               <option value="E-Book">📱 E-Book</option>
               <option value="Audiobook">🎧 Audiobook</option>
           </select>
       </div>
       <div class="col-md-2">
           <button type="submit" class="btn btn-primary w-100">Add</button>
       </div>
   </form>
</div>

<!-- LIBRARY LIST -->
<div class="list-group">
   {% for book in books %}
   <div class="list-group-item d-flex justify-content-between align-items-center">
       <div>
           <h5 class="mb-1">
               {% if book.format == 'Physical' %}📖
               {% elif book.format == 'E-Book' %}📱
               {% elif book.format == 'Audiobook' %}🎧
               {% endif %}
               {{ book.title }}
           </h5>
           <small class="text-muted">by {{ book.author }} | Status: {{ book.status }}</small>
       </div>
       <div>
           <a href="/update/{{ book.id }}" class="btn btn-sm btn-outline-secondary">Edit</a>
           <a href="/delete/{{ book.id }}" class="btn btn-sm btn-danger">Delete</a>
       </div>
   </div>
   {% endfor %}
</div>
{% endblock %}


3. templates/update.html
The edit page.
{% extends 'base.html' %}

{% block content %}
<div class="card p-4 shadow-sm">
   <h4>Edit Book</h4>
   <form method="POST">
       <div class="mb-3">
           <label>Title</label>
           <input type="text" name="title" class="form-control" value="{{ book.title }}">
       </div>
       <div class="mb-3">
           <label>Author</label>
           <input type="text" name="author" class="form-control" value="{{ book.author }}">
       </div>
       <div class="mb-3">
           <label>Format</label>
           <select name="format" class="form-select">
               <option value="Physical" {% if book.format == 'Physical' %}selected{% endif %}>Physical</option>
               <option value="E-Book" {% if book.format == 'E-Book' %}selected{% endif %}>E-Book</option>
               <option value="Audiobook" {% if book.format == 'Audiobook' %}selected{% endif %}>Audiobook</option>
           </select>
       </div>
       <div class="mb-3">
           <label>Status</label>
           <select name="status" class="form-select">
               <option value="To Read" {% if book.status == 'To Read' %}selected{% endif %}>To Read</option>
               <option value="Reading" {% if book.status == 'Reading' %}selected{% endif %}>Reading</option>
               <option value="Finished" {% if book.status == 'Finished' %}selected{% endif %}>Finished</option>
           </select>
       </div>
       <button type="submit" class="btn btn-success">Save Changes</button>
       <a href="/" class="btn btn-secondary">Cancel</a>
   </form>
</div>
{% endblock %}


🚀 Phase 5: Run the App
1. Make sure your virtual environment is active (you should see (venv) in your terminal prompt).
2. Run the application:
python app.py


3. You should see output indicating the server is running (usually Running on http://127.0.0.1:5000).
4. Open your web browser and go to http://127.0.0.1:5000.
🔮 Phase 6: Future Ideas
   * Search: Add a search bar to filter books by name.
   * Rating: Add a 1-5 star rating system.
   * Categories: Add genres (Sci-Fi, History, etc).