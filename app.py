import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import inspect

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate

# --- THE MODEL (Data Structure) ---
# Association table for many-to-many relationship between Book and Genre
book_genre = db.Table('book_genre',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Book(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   author = db.Column(db.String(100), nullable=False)
   status = db.Column(db.String(20), default='To Read')
   # New column for media type (Physical, E-Book, Audiobook)
   format = db.Column(db.String(20), nullable=False, default='Physical')
   # New columns for rating and category
   rating = db.Column(db.Integer, default=0)  # 0-5 stars
   # Additional features columns
   total_pages = db.Column(db.Integer, default=0)  # Total pages in the book
   pages_read = db.Column(db.Integer, default=0)  # Number of pages read
   notes = db.Column(db.Text, default='')  # Personal notes/reviews for the book
   start_date = db.Column(db.Date)  # When the user started reading
   finish_date = db.Column(db.Date)  # When the user finished reading
   cover_image = db.Column(db.String(200), default='')  # URL or path to book cover
   # Many-to-many relationship with genres
   genres = db.relationship('Genre', secondary=book_genre, lazy='subquery',
                            backref=db.backref('books', lazy=True))

# --- API INTEGRATION FUNCTIONS ---
def search_google_books(query):
    """Search for books using Google Books API"""
    try:
        # Google Books API endpoint
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}"

        # Make request to the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()

        # Process the results
        results = []
        if 'items' in data:
            for item in data['items']:
                volume_info = item.get('volumeInfo', {})

                # Extract relevant information
                title = volume_info.get('title', 'Unknown Title')
                authors = volume_info.get('authors', ['Unknown Author'])
                description = volume_info.get('description', 'No description available')

                # Get the first author if available
                author = ', '.join(authors) if authors else 'Unknown Author'

                # Get page count if available
                page_count = volume_info.get('pageCount', 0)

                # Get cover image URL if available
                image_links = volume_info.get('imageLinks', {})
                cover_url = image_links.get('thumbnail', '') or image_links.get('smallThumbnail', '')

                # Get published date if available
                published_date = volume_info.get('publishedDate', '')

                # Get average rating if available
                average_rating = volume_info.get('averageRating', 0)

                # Get categories if available
                categories = volume_info.get('categories', [])

                # Get preview URL if available
                preview_url = volume_info.get('previewLink', '')

                book_info = {
                    'title': title,
                    'author': author,
                    'description': description,
                    'page_count': page_count,
                    'cover_url': cover_url,
                    'published_date': published_date,
                    'average_rating': average_rating,
                    'categories': categories,  # Return all categories
                    'preview_url': preview_url,
                    'id': item.get('id', '')
                }

                results.append(book_info)

        return results
    except Exception as e:
        print(f"Error searching Google Books API: {e}")
        return []

# --- THE ROUTES (Logic) ---

# 1. READ (Home Page) with search, filtering, and sorting
@app.route('/')
def index():
   # Get filter and search parameters
   search_query = request.args.get('search', '')
   genre_filter = request.args.get('genre', '')
   rating_filter = request.args.get('rating', '')
   format_filter = request.args.get('format', '')
   sort_by = request.args.get('sort', 'title')  # Default sort by title
   sort_order = request.args.get('order', 'asc')  # Default ascending order
   page = request.args.get('page', 1, type=int)  # Pagination: current page number
   per_page = 12  # Number of books per page

   # Start with base query
   query = Book.query

   # Apply search filter
   if search_query:
       query = query.filter(Book.title.contains(search_query) | Book.author.contains(search_query))

   # Apply genre filter
   if genre_filter and genre_filter != 'all':
       query = query.join(Book.genres).filter(Genre.name == genre_filter)

   # Apply rating filter
   if rating_filter and rating_filter != 'all':
       try:
           rating_value = int(rating_filter)
           query = query.filter(Book.rating == rating_value)
       except ValueError:
           pass  # Ignore invalid rating values

   # Apply format filter
   if format_filter and format_filter != 'all':
       query = query.filter(Book.format == format_filter)

   # Apply sorting
   if sort_by == 'title':
       if sort_order == 'desc':
           query = query.order_by(Book.title.desc())
       else:
           query = query.order_by(Book.title.asc())
   elif sort_by == 'author':
       if sort_order == 'desc':
           query = query.order_by(Book.author.desc())
       else:
           query = query.order_by(Book.author.asc())
   elif sort_by == 'rating':
       if sort_order == 'desc':
           query = query.order_by(Book.rating.desc())
       else:
           query = query.order_by(Book.rating.asc())
   elif sort_by == 'date':
       # Order by ID as a proxy for date added (higher ID = newer)
       if sort_order == 'desc':
           query = query.order_by(Book.id.desc())
       else:
           query = query.order_by(Book.id.asc())
   elif sort_by == 'status':
       # Sort by status (To Read, Reading, Finished)
       if sort_order == 'desc':
           query = query.order_by(Book.status.desc())
       else:
           query = query.order_by(Book.status.asc())

   # Apply pagination
   books = query.paginate(page=page, per_page=per_page, error_out=False)

   # Get all unique categories for the filter dropdown
   all_categories = [genre.name for genre in Genre.query.all()]
   all_formats = [fmt[0] for fmt in db.session.query(Book.format).distinct().all()]

   return render_template('index.html',
                         books=books.items,  # Items for the current page
                         pagination=books,  # Pagination object for template
                         search_query=search_query,
                         genre_filter=genre_filter,
                         rating_filter=rating_filter,
                         format_filter=format_filter,
                         sort_by=sort_by,
                         sort_order=sort_order,
                         all_categories=all_categories,
                         all_formats=all_formats)

# 2. CREATE (Add a Book)
@app.route('/add', methods=['POST'])
def add_book():
   title = request.form.get('title')
   author = request.form.get('author')
   book_format = request.form.get('format') # Capture dropdown value
   rating = request.form.get('rating', 0)  # Capture rating value
   genre_names = request.form.getlist('genres')  # Capture list of genre names
   total_pages = request.form.get('total_pages', 0)  # Total pages in the book
   cover_image = request.form.get('cover_image', '')  # Book cover image URL
   notes = request.form.get('notes', '')  # Book notes/reviews

   # Validate required fields
   if not title or not title.strip():
       flash('Title is required!', 'error')
       return redirect(url_for('index'))

   if not author or not author.strip():
       flash('Author is required!', 'error')
       return redirect(url_for('index'))

   try:
       # Handle empty string values for numeric fields
       rating_int = int(rating) if rating and rating.strip() else 0
       total_pages_int = int(total_pages) if total_pages and total_pages.strip() else 0

       # Create the book first
       new_book = Book(
           title=title.strip(),
           author=author.strip(),
           format=book_format,
           rating=rating_int,
           total_pages=total_pages_int,
           cover_image=cover_image,
           notes=notes
       )
       db.session.add(new_book)
       db.session.flush()  # Flush to get the ID before assigning genres

       # Assign genres to the book
       if genre_names:
           for genre_name in genre_names:
               # Check if genre already exists in the database
               genre = Genre.query.filter_by(name=genre_name).first()
               if not genre:
                   # Create new genre if it doesn't exist
                   genre = Genre(name=genre_name)
                   db.session.add(genre)
                   db.session.flush()  # Flush to get the ID
               new_book.genres.append(genre)

       db.session.commit()
       flash('Book added successfully!', 'success')
   except Exception as e:
       db.session.rollback()
       flash(f'Error adding book: {str(e)}', 'error')

   return redirect(url_for('index'))

# 3. UPDATE (Edit a Book)
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_book(id):
   book = Book.query.get_or_404(id)
   if request.method == 'POST':
       title = request.form['title']
       author = request.form['author']

       # Validate required fields
       if not title or not title.strip():
           flash('Title is required!', 'error')
           return render_template('update.html', book=book)

       if not author or not author.strip():
           flash('Author is required!', 'error')
           return render_template('update.html', book=book)

       try:
           book.title = title.strip()
           book.author = author.strip()
           book.status = request.form['status']
           book.format = request.form['format']
           book.rating = int(request.form.get('rating', 0)) if request.form.get('rating') else 0
           book.total_pages = int(request.form.get('total_pages', 0)) if request.form.get('total_pages') else 0
           book.pages_read = int(request.form.get('pages_read', 0)) if request.form.get('pages_read') else 0
           book.notes = request.form.get('notes', '')
           book.cover_image = request.form.get('cover_image', '')

           # Update genres
           genre_names = request.form.getlist('genres')
           book.genres.clear()  # Remove all current genres
           if genre_names:
               for genre_name in genre_names:
                   # Check if genre already exists in the database
                   genre = Genre.query.filter_by(name=genre_name).first()
                   if not genre:
                       # Create new genre if it doesn't exist
                       genre = Genre(name=genre_name)
                       db.session.add(genre)
                       db.session.flush()  # Flush to get the ID
                   book.genres.append(genre)

           db.session.commit()
           flash('Book updated successfully!', 'success')
           return redirect(url_for('index'))
       except Exception as e:
           db.session.rollback()
           flash(f'Error updating book: {str(e)}', 'error')
           return render_template('update.html', book=book)
   return render_template('update.html', book=book)

# 4. DELETE (Remove a Book)
@app.route('/delete/<int:id>')
def delete_book(id):
   book = Book.query.get_or_404(id)
   db.session.delete(book)
   db.session.commit()
   return redirect(url_for('index'))

# 5. IMPORT/EXPORT (Backup and restore functionality)
@app.route('/export')
def export_data():
   import json
   books = Book.query.all()

   # Convert books to dictionaries
   books_data = []
   for book in books:
       book_dict = {
           'title': book.title,
           'author': book.author,
           'status': book.status,
           'format': book.format,
           'rating': book.rating,
           'genres': [genre.name for genre in book.genres],
           'total_pages': book.total_pages,
           'pages_read': book.pages_read,
           'notes': book.notes,
           'cover_image': book.cover_image
       }
       books_data.append(book_dict)

   # Create JSON response
   import io
   from flask import jsonify
   json_data = json.dumps(books_data, indent=2, default=str)

   # Return as downloadable file
   from flask import Response
   return Response(
       json_data,
       mimetype='application/json',
       headers={'Content-Disposition': 'attachment; filename=shelflog_backup.json'}
   )

# Missing routes for dashboard, search, and export functionality
@app.route('/dashboard')
def dashboard():
    # Calculate statistics for the dashboard
    total_books = Book.query.count()
    finished_books = Book.query.filter_by(status='Finished').count()
    reading_books = Book.query.filter_by(status='Reading').count()
    to_read_books = Book.query.filter_by(status='To Read').count()

    # Format counts
    physical_count = Book.query.filter_by(format='Physical').count()
    ebook_count = Book.query.filter_by(format='E-Book').count()
    audiobook_count = Book.query.filter_by(format='Audiobook').count()

    # Rating statistics
    avg_rating = db.session.query(db.func.avg(Book.rating)).scalar() or 0
    avg_rating = round(avg_rating, 1)

    # Calculate average pages read
    all_books = Book.query.all()
    total_pages_read = sum([book.pages_read for book in all_books])
    total_pages = sum([book.total_pages for book in all_books if book.total_pages > 0])

    progress_percentage = 0
    if total_pages > 0:
        progress_percentage = round((total_pages_read / total_pages) * 100, 1)

    # Top categories
    genre_counts = db.session.query(Genre.name, db.func.count(book_genre.c.book_id)).join(book_genre).group_by(Genre.name).order_by(db.func.count(book_genre.c.book_id).desc()).all()
    top_categories = genre_counts[:5]  # Top 5 categories

    # Additional statistics
    high_rated = Book.query.filter(Book.rating >= 4).count()

    # Compile all stats into a dictionary
    stats = {
        'total_books': total_books,
        'finished': finished_books,
        'reading': reading_books,
        'to_read': to_read_books,
        'avg_rating': avg_rating,
        'progress_percentage': progress_percentage,
        'physical_count': physical_count,
        'ebook_count': ebook_count,
        'audiobook_count': audiobook_count,
        'top_categories': top_categories,
        'high_rated': high_rated,
        'total_pages_read': total_pages_read,
        # Additional stats that were referenced but not calculated above
        'books_per_year': 0,
        'avg_pages_per_book': 0,
        'avg_days_to_complete': 0,
        'books_per_month': 0,
        'completion_rate': 0,
        'genre_distribution': [],
        'most_active_month': 'N/A',
        'peak_reading_season': 'N/A',
        'preferred_weekday': 'N/A',
        'books_last_30_days': 0,
        'current_pace': 0,
        'consistency_score': 0,
        'top_categories_labels': [cat[0] for cat in top_categories],
        'top_categories_counts': [cat[1] for cat in top_categories]
    }

    return render_template('dashboard.html', stats=stats)

@app.route('/search')
def search_books_page():
    # Get search query
    query = request.args.get('q', '').strip()
    sort_by = request.args.get('sort', 'title')  # Default sort by title

    # Start with base query
    base_query = Book.query

    if query:
        # Search for books by title or author in our database
        base_query = base_query.filter(
            Book.title.contains(query) | Book.author.contains(query)
        )

    # Apply sorting
    if sort_by == 'title':
        base_query = base_query.order_by(Book.title.asc())
    elif sort_by == 'author':
        base_query = base_query.order_by(Book.author.asc())
    elif sort_by == 'rating':
        base_query = base_query.order_by(Book.rating.desc())
    elif sort_by == 'date':
        # Order by ID as a proxy for date added (higher ID = newer)
        base_query = base_query.order_by(Book.id.desc())
    elif sort_by == 'status':
        # Sort by status (To Read, Reading, Finished)
        base_query = base_query.order_by(Book.status.asc())

    search_results = base_query.all()

    # Since the template expects all_books to be available, pass an empty list
    # and the search query for the search form to be pre-filled
    all_categories = [genre.name for genre in Genre.query.all()]
    all_formats = [fmt[0] for fmt in db.session.query(Book.format).distinct().all()]

    return render_template('search_results.html',
                           books=search_results,
                           search_query=query,
                           all_categories=all_categories,
                           all_formats=all_formats)

@app.route('/export_data')
def export_full_books_data():
    # This is the same as the export endpoint, providing an alternative name
    return export_data()

# API search route for Google Books
# API search route for general Google Books search
@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()

    if query:
        # Search Google Books API
        results = search_google_books(query)
        return {'books': results}
    else:
        return {'books': []}

# API search route for ISBN
@app.route('/api/search/isbn')
def api_search_isbn():
    isbn = request.args.get('isbn', '').strip()

    if isbn:
        # Search Google Books API by ISBN
        api_url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            results = []
            if 'items' in data:
                for item in data['items']:
                    volume_info = item.get('volumeInfo', {})

                    # Extract relevant information
                    title = volume_info.get('title', 'Unknown Title')
                    authors = volume_info.get('authors', ['Unknown Author'])
                    description = volume_info.get('description', 'No description available')

                    # Get the first author if available
                    author = ', '.join(authors) if authors else 'Unknown Author'

                    # Get page count if available
                    page_count = volume_info.get('pageCount', 0)

                    # Get cover image URL if available
                    image_links = volume_info.get('imageLinks', {})
                    cover_url = image_links.get('thumbnail', '') or image_links.get('smallThumbnail', '')

                    # Get published date if available
                    published_date = volume_info.get('publishedDate', '')

                    # Get average rating if available
                    average_rating = volume_info.get('averageRating', 0)

                    # Get categories if available
                    categories = volume_info.get('categories', [])

                    # Get preview URL if available
                    preview_url = volume_info.get('previewLink', '')

                    book_info = {
                        'title': title,
                        'author': author,
                        'description': description,
                        'page_count': page_count,
                        'cover_url': cover_url,
                        'published_date': published_date,
                        'average_rating': average_rating,
                        'categories': categories,  # Return all categories
                        'preview_url': preview_url,
                        'id': item.get('id', '')
                    }

                    results.append(book_info)

            return {'books': results}
        except Exception as e:
            print(f"Error searching Google Books API by ISBN: {e}")
            return {'books': []}
    else:
        return {'books': []}

# Make the Book model importable
__all__ = ['Book']

# Initialize DB and Run
if __name__ == "__main__":
   with app.app_context():
       # Note: with Flask-Migrate, db.create_all() is no longer needed
       # Use 'flask db init', 'flask db migrate', and 'flask db upgrade' commands instead
       pass
   app.run(debug=True)