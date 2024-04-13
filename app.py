from flask import Flask, render_template, url_for, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        new_user = User.query.filter_by(username).first()
        if not new_user:
            flash(f"No account with that username exists", "danger")
            return redirect(url_for("login"))
        if password == new_user.password:
            return redirect(url_for("home"))
        else:
            flash(f"Incorrect password", "danger")
            return redirect(url_for("login"))

    # form = LoginForm()
    # if request.method == "POST" and form.validate():
    #     user = User.query.filter_by(email=form.email.data).first()
    #     if not user:
    #         flash(f"No account exists with that email", "danger")
    #         return redirect(url_for("login"))
    #     if not user.email_confirmed:
    #         flash(f"Please activate your account before loging in", "danger")
    #         return redirect(url_for("login"))
    #     if bcrypt.check_password_hash(user.password, form.password.data):
    #         login_user(user)
    #         return redirect(url_for("home"))
    #     else:
    #         flash(f"invalid credentials", "danger")
    #         return redirect(url_for("login"))
    return render_template("login.html", title="Log in", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        tempUsername = User.query.filter_by(username).first()
        if tempUsername:
            flash(f"An account with that user already exists", "danger")
            return redirect(url_for("register.html"))

        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template("register.html")


        # usernamePulled = User.query.filter_by(username)
        #
        # email = User.query.filter_by(email=form.email.data).first()
        # if email:
        #     flash(f"An account with that email already exists", "danger")
        #     return redirect(url_for("register"))
        # encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # user = User(email=form.email.data, password=encrypted_password)
        # db.session.add(user)
        # db.session.commit()
        #
        # token = fernet.encrypt(user.email.encode())
        # confirm_url = url_for("confirm_account", token=token, _external=True)
        # html = render_template("email.html", confirm_url=confirm_url)
        # msg = Message(
        #     "Confirm your email with Organizational Odyssey!",
        #     recipients=[user.email],
        #     html=html,
        #     sender="organizationalodyssey@gmail.com"
        # )
        # mail.send(msg)
        #
        # flash(f"Thank you for signing up! Please check your email to confirm your account", "success")
        # return redirect(url_for("login"))
    # return render_template("register.html", title="Registration", form=form)


if __name__ == '__main__':
    app.run()
