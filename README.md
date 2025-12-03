# ShelfLog - Personal Library Manager

ShelfLog is a web application built with Python Flask that allows users to track physical books, e-books, and audiobooks in their personal library.

## Features

- Add books to your library with title, author, and format
- Track reading status (To Read, Reading, Finished)
- Support for different book formats (Physical, E-Book, Audiobook)
- Edit existing book entries
- Delete books from your library
- Bootstrap-based responsive UI

## Installation

1. Clone or download this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open your browser and go to `http://127.0.0.1:5000`

## Future Enhancements

- Search functionality to filter books by name
- Rating system (1-5 stars)
- Categories/genres (Sci-Fi, History, etc.)
