from flask import Flask, abort, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    review = db.Column(db.String(500), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_user_id'), nullable=True)

    def __repr__(self):
        return '<Book %r>' % self.title

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('index.html', books=books)

#User authentication set up

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=name).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Invalid password.')
        else:
            flash('Username does not exist.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        existing_user = User.query.filter_by(name=name).first()
        if existing_user is None:
            user = User(name=name, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        flash('A user already exists with that username.')
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Books handling

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        review = request.form.get('review')
        new_book = Book(title=title, author=author, review=review, user_id=current_user.id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully')
        return redirect(url_for('home'))
    return render_template('add_book.html')

@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book_to_delete = Book.query.get(book_id)
    if book_to_delete:
        # if the current user is the owner of the book or an admin
        if book_to_delete.user_id == current_user.id or current_user.is_admin:
            db.session.delete(book_to_delete)
            db.session.commit()
            flash('Book has been deleted!', 'success')
            return redirect(url_for('books'))
        else:
            abort(403)  # Unauthorized action
    else:
        abort(404)  # Book not found

if __name__ == '__main__':
    app.run(debug=True)