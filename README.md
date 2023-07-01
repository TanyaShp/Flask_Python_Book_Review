# Book Review App

This application is a book review site that allows users to login, add books with reviews, edit and delete their book entries, and search for books. In addition, it allows users to edit and delete reviews. It is a Flask web application using MySQL for the database hosted on Azure, and uses the Flask-Login extension for user authentication.

Live application can be found at: [https://flask-python-book-review-app.azurewebsites.net/](https://flask-python-book-review-app.azurewebsites.net/)

## Features

- **User Authentication**: Secure user registration and login functionality.
- **Add Books and Reviews**: Users can add new books with book details and an image. Users can also add reviews to the books and are able to edit or delete them. The image upload allows for cropping functionality.
- **Edit and Delete Books / Reviews**: Users can edit and delete their book entries and/or reviews.
- **Reviews Display**: On the main page, only the 3 latest reviews are displayed, with a "See more" button leading to a page with all reviews.
- **Search Functionality**: Allows users to find books by name/author.
- **Pagination**: Allows managing long lists of books and reviews.
- **Administrative functions**: Allows admins to edit or delete books and reviews created by other users.
- **Responsive Design**: The design of the application is responsive and provides an optimal viewing experience across a wide range of devices (from desktop computer monitors to mobile phones).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Pip (Python Package Installer)
- Azure Account (*optional for MySQL Server)

### Setup and Installation

1. Clone this repository.
    ```
    git clone git@github.com:TanyaShp/Flask_Python_Book_Review.git
    ```

2. Navigate to the project directory.
    ```
    cd Flask_Python_Book_Review
    ```

3. Create a virtual environment.
    ```
    python -m venv venv
    source venv/bin/activate  # For Unix or MacOS
    venv\Scripts\activate  # For Windows
    ```

4. Install the dependencies.
    ```
    pip install -r requirements.txt
    ```

5. Set up the database following the instructions given in the section below.
6. Run the application.
    ```
    flask run
    ```

You should now be able to navigate to http://127.0.0.1:5000/ in your web browser and see the application running.

### SQL Database Setup

ensure you have a MySQL server instance accessible.

1. Install MySQL Server and make sure it is running. The installation steps vary by platform (Windows, Linux, MacOS). You can follow the instructions on the official MySQL website to install MySQL: [https://dev.mysql.com/doc/mysql-getting-started/en/](https://dev.mysql.com/doc/mysql-getting-started/en/)

2. Create a new MySQL database for your application. You can do this by logging into your MySQL server and running the following command:

    ```bash
    CREATE DATABASE mydatabase;
    ```

    Replace `mydatabase` with the name you want to give your database.

3. Make a note of your MySQL server's host (usually localhost if running on your machine), port (usually 3306), and the username and password of the MySQL account that has access to the database.

4. Construct your database URL according to this format:

    ```bash
    mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
    ```

    Replace `<username>`, `<password>`, `<host>`, `<port>`, and `<database_name>` with your respective MySQL information.

5. Set your environment variables (replace `{connection-string}` with your actual connection string):

    ```bash
    export SQLALCHEMY_DATABASE_URI={connection-string}
    export SECRET_KEY=<your-secret-key>
    ```

6. Initialize your database:

    ```bash
    flask db init
    ```

7. Perform the migrations:

    ```bash
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

Your MySQL database should now be ready to use with your Flask application.

Note: For production, it's recommended to secure your MySQL database connection using SSL. Instructions for doing this will vary depending on your hosting environment. It's also recommended to not store your `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` in your source code, but rather to use environment variables or some form of secrets management.

This setup instruction is for MySQL, but you could use any SQL-based database engine with SQLAlchemy, the ORM used in this project. The way you setup and connect to the database might vary. SQLAlchemy provides a helpful guide on how to create engine configurations for different types of databases: [https://docs.sqlalchemy.org/en/14/core/engines.html](https://docs.sqlalchemy.org/en/14/core/engines.html)


### Images

Images to be used for book covers should be placed in the `/static/uploads/` directory. When adding or editing a book, you will be asked to select an image file. 

## Built With

- Flask - The web framework used.
- Flask-SQLAlchemy - ORM for the database.
- Flask-Login - For handling user sessions.
- MySQL - The Database used.

## Future Improvements

- User password reset functionality.
- Admin panel - allow site administrators to manage users.
- Upvote/downvote system for reviews.
- Enhanced error handling.
- Add a feature to allow users to rate the books.
- Integration with a third-party book API for getting book details automatically.

## Contributing

Appreciate any contribution to this project, whether it is related to bugs, grammar, or simply a suggestion or improvement. 

1. **Fork the project repository**. You can do this by clicking the "Fork" button on the repository page. This will create a copy of the repository and place it in your GitHub account.

2. **Clone the forked repository to your local machine**. Navigate to the location on your computer where you want to store the project, and clone the repository:

    ```bash
    git clone https://github.com/{your-github-username}/Flask_Python_Book_Review.git
    ```

3. **Navigate to the project directory**:

    ```bash
    cd Flask_Python_Book_Review
    ```

4. **Create a new branch for your feature**. The branch name should be descriptive of the feature or change you are making:

    ```bash
    git checkout -b feature/name-of-your-new-feature
    ```

5. **Make changes in your branch**. Implement your feature or bug fix on this branch.

6. **Commit your changes**. Be sure to write clear, concise commit messages describing your changes:

    ```bash
    git commit -m "Add some feature or fix some bug"
    ```

7. **Push your branch to GitHub**. Once you are done making changes, push your branch to GitHub using the command:

    ```bash
    git push origin feature/name-of-your-new-feature
    ```

8. **Create a pull request**. On the GitHub website, navigate to your forked repository and you'll see your new branch listed at the top with a "Compare & pull request" button. Click on the button to open a pull request.

9. **Wait for your pull request to be reviewed and merged**. Your changes will be reviewed, and if they are accepted, they will be included in the project.

Please follow the code style guide and conventions of the project. If there are any additional contribution guidelines specified by the project, be sure to follow those as well. If your changes are accepted into the core project, you will be listed as a contributor.

## Authors

- Tetiana Shpychka

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.