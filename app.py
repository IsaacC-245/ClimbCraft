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


favorites = db.Table("favorites",
                     db.Column('parent_id', db.Integer, db.ForeignKey('route.id')),
                     db.Column('child_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favorite_routes = db.relationship("User", secondary=favorites,
                                      primaryjoin=(favorites.c.parent_id == id),
                                      secondaryjoin=(favorites.c.child_id == id))


class Route(db.Model):
    tablename = "route"

    id = db.Column(db.Integer, primarykey=True)
    name = db.Column(db.String(60), nullable=False)
    difficulty = db.Column(db.String(60), nullable=False)
    angle = db.Column(db.Integer, nullable=False)
    machine_type = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey, nullable=False)
    create_time = db.Column(db.DateTime)
    user = db.relationship("User", db.ForeignKey, backref="routes")


class Grid(db.Model):
    tablename = "grid"

    id = db.Column(db.Integer, primarykey=True)
    route_id = db.Column(db.Integer, nullable=False)
    row = db.Column(db.String(60), nullable=False)


class Review(db.Model):
    _tablename = "review"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    difficulty = db.Column(db.Integer, nullable=True)
    route_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Relationship(db.Model):
    __tablename = "relationship"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    route_id = db.Column(db.Integer, nullable=False)


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


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form.get("name")
        difficulty = request.form.get("difficulty")
        angle = request.form.get("angle")
        machineType = request.form.get("machineType")
        userId = request.form.get("userId")

        mySQL = f"INSERT INTO route (name, difficulty, angle, machineType, userId) VALUES ({name},{difficulty},{angle},{machineType},{userId});"
        db.engine.execute(mySQL)
        return redirect(url_for("home"))

    return render_template("edit.html")


if __name__ == '__main__':
    app.run()
