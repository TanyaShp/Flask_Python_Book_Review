from flask import (
    Flask,
    abort,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_migrate import Migrate
from sqlalchemy import or_
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from dotenv import load_dotenv
import os
import string
import random

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Set the SQLALCHEMY_DATABASE_URI depending on the environment
if os.getenv("FLASK_ENV") == "testing":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DB_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

UPLOAD_FOLDER = os.path.abspath("static/uploads/")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png", "gif"}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200))
    is_admin = db.Column(db.Boolean, default=False)
    books = db.relationship("Book", backref="user", lazy=True)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref=db.backref("reviews", lazy=True))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    image_file = db.Column(db.String(120), nullable=True, default="default.jpg")
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", name="fk_user_id"), nullable=True
    )
    reviews = db.relationship("Review", backref="book", lazy=True)

    def __repr__(self):
        return "<Book %r>" % self.title


@app.route("/", defaults={"page_num": 1})
@app.route("/page/<int:page_num>")
def index(page_num):
    search_query = request.args.get("q")
    if search_query:
        books = Book.query.filter(
            or_(
                Book.title.ilike(f"%{search_query}%"),
                Book.author.ilike(f"%{search_query}%"),
            )
        ).paginate(per_page=5, page=page_num, error_out=True)
    else:
        books = Book.query.order_by(Book.id.desc()).paginate(
            per_page=5, page=page_num, error_out=True
        )
    return render_template("index.html", books=books, search_query=search_query)


# User authentication set up
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("index"))
            else:
                flash("Invalid password.", "login_error")
        else:
            flash("Username does not exist.", "login_error")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        existing_user = User.query.filter_by(name=name).first()
        if existing_user is None:
            user = User(name=name, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for("index"))
        flash("A user already exists with that username.", "signup_error")
    return render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


# Books handling
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def generate_unique_filename(title):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    filename = f"{title}_{timestamp}_{random_string}.jpg"
    return secure_filename(filename)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    add_book_url = url_for("add_book")
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        # Check for the cropped_image in the request files
        if "cropped_image" in request.files:
            img_data = request.files["cropped_image"]

            # Generate a unique filename
            filename = generate_unique_filename(title)

            # Save the image
            img_data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # Check for the original_image in the request files
        elif "original_image" in request.files:
            img_data = request.files["original_image"]

            # Generate a unique filename
            filename = generate_unique_filename(title)

            # Save the image
            img_data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        else:
            filename = "default.jpg"

        new_book = Book(
            title=title,
            author=author,
            image_file=filename,
            user_id=current_user.id,
        )
        db.session.add(new_book)
        db.session.flush()

        review_content = request.form["review"]
        new_review = Review(
            content=review_content, book_id=new_book.id, user_id=current_user.id
        )
        db.session.add(new_review)
        db.session.commit()

        return jsonify({"location": url_for("index")}), 201
    return render_template("add_book.html", add_book_url=add_book_url)


@app.route("/delete_book/<int:book_id>", methods=["POST"])
@login_required
def delete_book(book_id):
    book_to_delete = Book.query.get(book_id)
    if book_to_delete:
        # if the current user is the owner of the book or an admin
        if book_to_delete.user_id == current_user.id or current_user.is_admin:
            db.session.delete(book_to_delete)
            db.session.commit()
            flash("Book has been deleted!", "book_action")  # Add "book_action" category
            return redirect(url_for("index"))
        else:
            abort(403)  # Unauthorized action
    else:
        abort(404)  # Book not found


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    book_to_edit = Book.query.get(book_id)
    if book_to_edit:
        # if the current user is the owner of the book or an admin
        if book_to_edit.user_id == current_user.id or current_user.is_admin:
            if request.method == "POST":
                title = request.form["title"]
                author = request.form["author"]

                img_data = None
                filename = "default.jpg"

                # Check for the cropped_image in the request files
                if "cropped_image" in request.files:
                    img_data = request.files["cropped_image"]
                # If no cropped_image, check for the original_image in the request files
                elif "original_image" in request.files:
                    img_data = request.files["original_image"]

                if img_data and allowed_file(img_data.filename):
                    # Generate a unique filename
                    filename = generate_unique_filename(title)

                    # Save the image
                    img_data.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                book_to_edit.title = title
                book_to_edit.author = author
                book_to_edit.image_file = filename

                db.session.commit()
                return jsonify({"location": url_for("index")})  # Redirect to index page
            else:
                return render_template(
                    "edit_book.html",
                    book=book_to_edit,
                    action_url=url_for("edit_book", book_id=book_id),
                )
        else:
            abort(403)  # Unauthorized action
    else:
        abort(404)  # Book not found


@app.route("/book_reviews/<int:book_id>")
def book_reviews(book_id):
    book = Book.query.get_or_404(book_id)  # Fetch the book from the database
    if book:
        return render_template("book_reviews.html", book=book)
    else:
        abort(404)  # Book not found


@app.route("/add_review/<int:book_id>", methods=["GET", "POST"])
@login_required
def add_review(book_id):
    book = Book.query.get(book_id)
    if book:
        if request.method == "POST":
            content = request.form.get("content")
            new_review = Review(
                content=content, book_id=book_id, user_id=current_user.id
            )
            db.session.add(new_review)
            db.session.commit()
            flash("Review has been added!", "success")
            return redirect(url_for("book_reviews", book_id=book_id))
        else:
            return render_template("add_review.html", book=book)
    else:
        abort(404)  # Book not found


@app.route("/edit_review/<int:review_id>/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_review(review_id, book_id):
    review_to_edit = Review.query.get(review_id)

    # Make sure the review exists and belongs to the current user or the user is an admin
    if review_to_edit and (
        review_to_edit.user_id == current_user.id or current_user.is_admin
    ):
        if request.method == "POST":
            content = request.form["content"]

            review_to_edit.content = content

            db.session.commit()

            flash("Review has been updated!", "success")
            return redirect(url_for("book_reviews", book_id=book_id))  # Redirect to index page
        else:
            return render_template(
                "edit_review.html",
                review=review_to_edit,
                action_url=url_for("edit_review", review_id=review_id, book_id=book_id),
            )
    else:
        abort(403)  # Unauthorized action


@app.route("/delete_review/<int:review_id>/<int:book_id>", methods=["POST"])
@login_required
def delete_review(review_id, book_id):
    review = Review.query.get_or_404(review_id)
    if not current_user.is_admin and (
        review.user_id != current_user.id or review.book_id != book_id
    ):
        abort(403)
    db.session.delete(review)
    db.session.commit()
    flash("Your review has been deleted.", "success")
    return redirect(url_for("book_reviews", book_id=book_id))

# Special routes for test
@app.route('/delete_user/<name>', methods=['DELETE'])
def delete_user(name):
    # Only allow this in testing environment
    if os.getenv("FLASK_ENV") != 'testing':
        abort(403)  # Forbidden
    user = User.query.filter_by(name=name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return "User deleted"
    else:
        return "User not found", 404

if __name__ == "__main__":
    app.run(debug=True)
