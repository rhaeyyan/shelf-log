"""
Migration script for ShelfLog application
This script handles database migrations using Flask-Migrate
"""

import os
from app import app, db
from app import Book  # Import the Book model

def setup_database():
    """Initialize the database with Flask-Migrate"""
    with app.app_context():
        # Check if migrations directory exists
        if not os.path.exists('migrations'):
            print("Initializing Flask-Migrate...")
            os.system('python -m flask db init')
        
        print("Creating migration for updated schema...")
        os.system('python -m flask db migrate -m "Add additional features"')
        
        print("Applying migration to database...")
        os.system('python -m flask db upgrade')
        
        print("Database setup complete!")

if __name__ == '__main__':
    # Set the FLASK_APP environment variable
    os.environ['FLASK_APP'] = 'app.py'
    
    setup_database()