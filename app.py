from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)

# secret key required for session
app.secret_key = "pharmacy_secret_key"


# DATABASE CONNECTION
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="farzeen",
        database="LOGIN_1"
    )


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# REGISTER PAGE
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# LOGIN PAGE
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if user:

            # store session
            session["username"] = username

            # redirect to dashboard
            return redirect(url_for("dashboard"))

        else:
            return "Invalid username or password"

    return render_template("login.html")


# DASHBOARD PAGE
@app.route("/dashboard")
def dashboard():

    # check if logged in
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
