from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your models here (copy from main app to avoid circular imports)
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
    # Additional features columns
    total_pages = db.Column(db.Integer, default=0)  # Total pages in the book
    pages_read = db.Column(db.Integer, default=0)  # Number of pages read
    notes = db.Column(db.Text, default='')  # Personal notes/reviews for the book
    start_date = db.Column(db.Date)  # When the user started reading
    finish_date = db.Column(db.Date)  # When the user finished reading
    cover_image = db.Column(db.String(200), default='')  # URL or path to book cover

if __name__ == '__main__':
    app.run(debug=True)