from datetime import timedelta
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "aklsdd"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=2)


db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        u = request.form["nm"]
        session["user"] = u

        found_user = users.query.filter_by(name=u).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(u, "")
            db.session.add(usr)
            db.session.commit()

        flash("Logein Succesful!")
        return redirect(url_for("user"))
    if "user" in session:
        flash("Already Logged In!")
        return redirect(url_for("user"))
    return render_template("login.html")


@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        u = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email

            found_user = users.query.filter_by(name=u).first()
            found_user.email = email
            db.session.commit()

            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    flash("You are not logged In!")
    return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
