# Book Review App

This application is a book review site that allows users to login, add books, add reviews, edit and delete their book entries, and search for books. In addition, it allows users to edit and delete reviews. It is a Flask web application using MySQL for the database hosted on Azure, and uses the Flask-Login extension for user authentication.

The application is automatically deployed to Azure WebApps. 

## Features

- **User Authentication**: Secure user registration and login functionality.
- **Add Books and Reviews**: Users can add new books with book details and an image. Users can also add reviews to the books and are able to edit or delete them. The image upload allows for cropping functionality.
- **Edit and Delete Books / Reviews**: Users can edit and delete their book entries and/or reviews.
- **Reviews Display**: On the main page, only the 3 reviews are displayed, with a "See more" button leading to a page with all reviews.
- **Search Functionality**: Allows users to find books by name/author.
- **Pagination**: Allows managing long lists of books and reviews.
- **Administrative functions**: Allows admins to edit or delete books and reviews created by other users.
- **Responsive Design**: The design of the application is responsive and provides an optimal viewing experience across a wide range of devices (from desktop computer monitors to mobile phones).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8 or higher
- Pip (Python Package Installer)
- MySQL Server

### Setup and Installation

1. Clone this repository.
    ```
    git clone git@github.com:TanyaShp/Flask_Python_Book_Review.git
    ```

2. Navigate to the project directory.
    ```
    cd Flask_Python_Book_Review
    ```

3. Install the dependencies.
    ```
    pip install -r requirements.txt
    ```

4. Set up the database(s) and follow the instructions given in Environment Variables Setup section below.
5. Run the application.
    ```
    flask run
    ```

You should now be able to navigate to http://127.0.0.1:5000/ in your web browser and see the application running.

### Environment Variables Setup

This application uses environment variables for managing sensitive data. 

Create a `.env` file at the root of your project and populate it with the necessary information:

```env
DATABASE_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
TEST_DB_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database_test_name>
SECRET_KEY=<your-secret-key>
FLASK_ENV=<your-flask-env> # testing or production
```

TEST_DB_URL is optional and can be removed if separate database is not required for testing.

Replace `<username>`, `<password>`, `<host>`, `<port>`, `<database_name>` / `<database_test_name>`, `<your-secret-key>`, and `<your-flask-env>` with your respective information.

Ensure you have a MySQL server instance accessible. You can follow the instructions on the official MySQL website to install MySQL: https://dev.mysql.com/doc/mysql-getting-started/en/

Once MySQL Server is set up, use your credentials to replace the placeholders in the .env file. If you are running your MySQL server locally, your `<host>` will be localhost and `<port>` will be 3306 by default.

### Images

Images to be used for book covers once uploaded will be placed in the `/static/uploads/` directory. When adding or editing a book, you will be asked to select an image file. 

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
