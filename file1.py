from flask import Flask, redirect, url_for, render_template, request, session


app = Flask(__name__)
app.secret_key = "aklsdd"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        u = request.form["nm"]
        session["user"] = u
        return redirect(url_for("user"))
    return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        u = session["user"]
        return f"<h1>{u}</h1>"
    return redirect(url_for("login"))


# @app.route('/admin')
# def admin():
#     return redirect(url_for("user", name='Admin!'))


if __name__ == "__main__":
    app.run(debug=True)
