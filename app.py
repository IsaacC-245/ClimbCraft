from datetime import datetime

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

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    difficulty = db.Column(db.String(60), nullable=False)
    angle = db.Column(db.Integer, nullable=False)
    machine_type = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    create_time = db.Column(db.DateTime)
    user = db.relationship("User", backref="routes")


class Grid(db.Model):
    tablename = "grid"

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey(Route.id), nullable=False)
    row = db.Column(db.String(60), nullable=False)
    route = db.relationship("Route", backref="grids")


class Review(db.Model):
    _tablename = "review"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=True)
    difficulty = db.Column(db.Integer, nullable=True)
    route_id = db.Column(db.Integer, db.ForeignKey(Route.id), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    route = db.relationship("Route", backref="reviews")
    users = db.relationship("User", backref="reviews")


class Relationship(db.Model):
    __tablename = "relationship"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    route_id = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
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
        route_id = request.form.get("id")
        name = request.form.get("name")
        difficulty = request.form.get("difficulty")
        angle = request.form.get("angle")
        machineType = request.form.get("machine_type")
        userId = request.form.get("user_grid")
        #grid = request.form.get("grid_item")

        # for grid_row in grid:
        #     sql_grid = f"INSERT INTO route (user_id, route_id, row) VALUES ({current_user.id},{route_id},{grid_row})"
        #     db.engine.execute(sql_grid)

        mySQL = f"INSERT INTO route (name, difficulty, angle, machineType, userId, create_time) VALUES ({name},{difficulty},{angle},{machineType},{userId},{datetime.now()});"
        db.engine.execute(mySQL)
        return redirect(url_for("home"))

    return render_template("rock-grid.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    user_id = current_user.id
    routes_list = Route.query.filter_by(user_id=user_id).all()
    list_of_dictionary = []
    for current_route in routes_list:
        output = {"id": current_route.id, "name": current_route.name, "difficulty": current_route.difficulty,
                  "angle": current_route.angle, "machine_type": current_route.machine_type,
                  "user_id": current_route.user_id, "create_time": current_route.create_type}
        list_of_dictionary.append(output)
    data = {"data": list_of_dictionary}
    return render_template("index.html", data=list_of_dictionary)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        get_id = request.form.get("id")
        current_route = Route.query.filter_by(id=get_id).first()

        #ADD METHOD TO COMPILE GRID TO SEND IT
        grids_list = Grid.query.filter_by(route_id=current_route.id)
        list_of_arrays = []
        for current_grid in grids_list:
            temp = current_grid.split(" ")
            list_of_arrays.append(temp)

        return render_template("edit.html", list_of_arrays, name=current_route.name, difficulty=current_route.difficulty, angle=current_route.angle, machineType=current_route.machineType, userId=current_route.userId)
    if request.method == "POST":
        send_id = request.form.get("id")
        name = request.form.get("name")
        difficulty = request.form.get("difficulty")
        angle = request.form.get("angle")
        machineType = request.form.get("machineType")
        userId = request.form.get("userId")
        #grid = request.form.get("grid_item")
        current_route = Route.query.filter_by(id=send_id).first()
        if name!=current_route.name:
            current_route.name = name
        if difficulty!=current_route.difficulty:
            current_route.difficulty = difficulty
        if angle!=current_route.angle:
            current_route.angle = angle
        if machineType!=current_route.difficulty:
            current_route.machineType = machineType
        if userId!=current_route.userId:
            current_route.userId = userId
        #sql_delete = f"DELETE FROM grid WHERE route_id={send_id}"

        # for grid_row in grid:
        #     sql_grid = f"INSERT INTO route (user_id, route_id, row) VALUES ({current_user.id},{send_id},{grid_row})"
        #     db.engine.execute(sql_grid)

        db.session.commit()
        return render_template("edit.html", name=current_route.name, difficulty=current_route.difficulty, angle=current_route.angle, machineType=current_route.machineType, userId=current_route.userId)
    return render_template("edit.html")



@app.route('/community')
def community():
    routes = Route.query.order_by(Route.date_posted.desc()).limit(5).all()
    return render_template('community.html', routes=routes)

if __name__ == '__main__':
    app.run()
