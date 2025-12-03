# ShelfLog - Personal Library Manager

ShelfLog is a comprehensive web application built with Python Flask that allows users to track physical books, e-books, and audiobooks in their personal library. The application features a modern UI with responsive design, advanced search capabilities, and integration with external book databases.

## Technologies and Libraries Used

### Backend Technologies
- **Python 3.x**: Primary programming language for application logic
- **Flask**: Web framework for handling HTTP requests, routing, and templating
- **SQLAlchemy**: Object-relational mapping (ORM) for database interactions
- **SQLite**: Lightweight database management system for local storage
- **Flask-Migrate**: Database migration tool using Alembic for schema changes
- **Flask-Caching**: Caching system to improve application performance
- **Requests**: HTTP library for API integration with external services

### Frontend Technologies
- **HTML5**: Structuring the web application content
- **CSS3**: Styling and layout of the user interface
- **Bootstrap 5**: Frontend framework for responsive design components
- **JavaScript**: Client-side functionality and interactive features
- **Jinja2 Templates**: Server-side templating engine for Flask

### Book Data Integration
- **Google Books API**: External API integration for book information lookup
- **JSON**: Data format for API communication and data export

### Development Tools
- **Virtual Environment (venv)**: Python virtual environment management
- **Pip**: Python package installer and dependency management
- **Git**: Version control system for code management

## Features

### Core Book Management
- Add books to your library with title, author, and format
- Track reading status (To Read, Reading, Finished)
- Support for different book formats (Physical, E-Book, Audiobook)
- Edit existing book entries with comprehensive form validation
- Delete books from your library with confirmation

### Advanced Tracking Features
- Rating system (1-5 stars) for book evaluation
- Categories/genres (Sci-Fi, History, Fantasy, Manga, Comics, etc.)
- Reading progress tracking (pages read/total pages)
- Reading date tracking (start date, finish date)
- Notes and reviews for each book
- Book cover image support with URL storage
- Form validation and user feedback notifications

### Search and Filtering
- Enhanced search functionality across title and author
- Filtering by genre, rating, and format
- Sorting options (title, author, rating, date added, status)
- Pagination for large collections
- Advanced Google Books API integration for external book search

### Data Management
- Import/export functionality (JSON backup of collections)
- Database migrations with Flask-Migrate
- Performance optimizations:
  - Optimized database queries for large collections
  - Caching for improved performance (using Flask-Caching)
  - Efficient query handling for filtering and sorting

### User Experience
- Bootstrap-based responsive UI for all device sizes
- Dashboard with statistics and reading insights
- Attractive styling with modern UI design
- Book cover thumbnails display
- Responsive design for mobile devices
- Real-time feedback and notifications

### Dashboard Analytics
- Total book count statistics
- Reading status breakdown (To Read, Reading, Finished)
- Format distribution (Physical, E-Book, Audiobook)
- Average rating calculations
- Progress percentage tracking
- Top categories analysis
- High-rated books count
- Reading progress analytics

## Installation

### Prerequisites
- Python 3.7 or higher
- Pip package manager
- Git (optional, for cloning the repository)

### Installation Instructions

#### Windows
1. Clone or download this repository:
   ```cmd
   git clone https://github.com/yourusername/shelf-log.git
   cd shelf-log
   ```

2. Create a virtual environment:
   ```cmd
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

5. Initialize the database with Flask-Migrate:
   ```cmd
   set FLASK_APP=migrate_app.py
   python -m flask db init
   python -m flask db migrate -m "Initial migration"
   python -m flask db upgrade
   ```

6. Run the application:
   ```cmd
   python app.py
   ```

7. Open your browser and go to `http://127.0.0.1:5000`

#### Mac/Linux
1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/shelf-log.git
   cd shelf-log
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database with Flask-Migrate:
   ```bash
   export FLASK_APP=migrate_app.py
   python3 -m flask db init
   python3 -m flask db migrate -m "Initial migration"
   python3 -m flask db upgrade
   ```

6. Run the application:
   ```bash
   python3 app.py
   ```

7. Open your browser and go to `http://127.0.0.1:5000`

### Updating the Application

#### Windows
1. Navigate to your ShelfLog directory:
   ```cmd
   cd shelf-log
   ```

2. Pull the latest changes:
   ```cmd
   git pull origin main
   ```

3. Activate your virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

4. Update dependencies (if requirements.txt changed):
   ```cmd
   pip install -r requirements.txt --upgrade
   ```

5. Apply any database migrations:
   ```cmd
   set FLASK_APP=migrate_app.py
   python -m flask db migrate -m "Update migration"
   python -m flask db upgrade
   ```

6. Restart the application:
   ```cmd
   python app.py
   ```

#### Mac/Linux
1. Navigate to your ShelfLog directory:
   ```bash
   cd shelf-log
   ```

2. Pull the latest changes:
   ```bash
   git pull origin main
   ```

3. Activate your virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Update dependencies (if requirements.txt changed):
   ```bash
   pip install -r requirements.txt --upgrade
   ```

5. Apply any database migrations:
   ```bash
   export FLASK_APP=migrate_app.py
   python3 -m flask db migrate -m "Update migration"
   python3 -m flask db upgrade
   ```

6. Restart the application:
   ```bash
   python3 app.py
   ```

## Database Migrations

Flask-Migrate is set up to handle database schema changes:
- Use `python -m flask db migrate -m "Description of changes"` to create migration files
- Use `python -m flask db upgrade` to apply migrations to the database
- Use `python -m flask db downgrade` to rollback migrations

## API Integration

The application integrates with Google Books API for external book information retrieval:
- Search for books by title or author using `/api/search?q=query` endpoint
- Search for books by ISBN using `/api/search/isbn?isbn=number` endpoint
- Results include title, author, description, page count, cover image, and more

## Performance Enhancements

The application includes several performance optimizations:
- **Optimized database queries**: Using efficient querying techniques, indexing, and reduced query counts
- **Caching**: Using Flask-Caching to cache rendered pages and computed data
- **Pagination**: Implemented for handling large collections efficiently
- **Responsive design**: Optimized for all device sizes with Bootstrap

## Future Enhancements

- User authentication and personal accounts
- Reading goals (books per month/year)
- More detailed analytics and statistics
- Advanced reporting features
- Integration with additional book databases
- Cloud storage integration for data backup

## How Technologies Are Used

### Flask Framework
- Handles routing and request processing
- Provides template rendering with Jinja2
- Manages application configuration

### SQLAlchemy ORM
- Defines database models (Book, Genre)
- Handles database operations (CRUD operations)
- Manages relationships between entities

### Bootstrap CSS
- Provides responsive grid system
- Implements UI components and styling
- Ensures cross-browser compatibility

### SQLite Database
- Stores book information locally
- Maintains reading progress and status
- Preserves user notes and ratings

### Google Books API Integration
- Provides external book search capabilities
- Retrieves book covers and metadata
- Enhances user experience with comprehensive data
