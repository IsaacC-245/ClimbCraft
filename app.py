from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt 

app = Flask(__name__)

app.config["SECRET_KEY"] = "c6d2f9789a32a64e8d12d42d2c955505"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def hello_world():
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if not user:
            flash(f"No account with that username exists", "danger")
            return redirect(url_for("login"))
        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash(f"Incorrect password", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("email")
        password = request.form.get("password")

        temp_username = User.query.filter_by(username=username).first()
        if temp_username:
            flash(f"An account with that user already exists", "danger")
            return redirect(url_for("register"))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


if __name__ == '__main__':
    app.run()
