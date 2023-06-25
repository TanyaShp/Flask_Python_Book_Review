# Book Review App

This application is a book review site that allows users to login, add books, edit and delete their book entries, and search for books. It's a Flask web application with SQLite for the database and uses the Flask-Login extension for user authentication.

## Features

- **User Authentication:** Secure user registration and login functionality.
- **Add Books:** Users can add new books with book details and an image. The image upload allows for cropping functionality.
- **Edit and Delete Books:** Users can edit and delete their book entries.
- **Search Functionality:** Allows users to find books by name/author.
- **Pagination:** Allows to manage long lists of books.
- **Administrative functions:** Allows admins to edit or delete books created by other users.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Pip (Python Package Installer)

### Setup and Installation

1. Clone this repository.
```bash
git clone git@github.com:TanyaShp/Flask_Python_Book_Review.git
cd Flask_Python_Book_Review
```

2. Create a virtual environment.
```bash
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate  # For Windows
```

3. Install the dependencies.
```bash
pip install -r requirements.txt
```

4. Set up the database.
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

5. Run the application.
```bash
flask run
```

You should now be able to navigate to http://127.0.0.1:5000/ in your web browser and see the application running.

### Images
Images to be used for book covers should be placed in the /static/uploads/ directory. When adding or editing a book, you will be asked to select an image file. Navigate to the /static/uploads/ directory and select your image.

### Running Tests
To run the tests for this application, navigate to the project root directory and run:

```bash
python -m unittest
```

### Built With
Flask - The web framework used
Flask-SQLAlchemy - ORM for the database
Flask-Login - For handling user sessions
SQLite - The Database used

### Future Improvements
User password reset functionality
Admin panel - allow site administrators to manage users
Upvote/downvote system for reviews
Enhanced error handling

### Authors
Tetiana Shpychka

### License
This project is licensed under the MIT License - see the LICENSE.md file for details