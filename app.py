from flask import Flask, render_template, g, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")


# ------------------------------------------------------------------ #
# Database                                                           #
# ------------------------------------------------------------------ #

@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def get_db_connection():
    """Get the database connection for the current request context."""
    if "db" not in g:
        g.db = get_db()
    return g.db


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # Redirect to profile if already logged in
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        if not name:
            return render_template("register.html", error="Name is required.")
        if not email:
            return render_template("register.html", error="Email is required.")
        if "@" not in email or "." not in email:
            return render_template("register.html", error="Please enter a valid email address.")
        if not password:
            return render_template("register.html", error="Password is required.")
        if len(password) < 8:
            return render_template("register.html", error="Password must be at least 8 characters.")

        db = get_db_connection()

        # Check for duplicate email
        existing_email = db.execute(
            "SELECT id FROM users WHERE email = ?", (email,)
        ).fetchone()
        if existing_email:
            return render_template("register.html", error="Email already registered.")

        # Check for duplicate username
        existing_user = db.execute(
            "SELECT id FROM users WHERE username = ?", (name,)
        ).fetchone()
        if existing_user:
            return render_template("register.html", error="Username already taken.")

        # Hash password and create user
        password_hash = generate_password_hash(password)
        cursor = db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        db.commit()

        # Get the new user ID and set session
        user_id = cursor.lastrowid
        session["user_id"] = user_id

        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Redirect to profile if already logged in
    if session.get("user_id"):
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validation
        if not email or not password:
            return render_template("login.html", error="Invalid credentials.")

        db = get_db_connection()

        # Look up user by email
        user = db.execute(
            "SELECT id, password_hash FROM users WHERE email = ?", (email,)
        ).fetchone()

        # Check if user exists and password is correct
        if user is None or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid credentials.")

        # Set session and redirect
        session["user_id"] = user["id"]
        return redirect(url_for("profile"))

    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


@app.route("/init-db")
def init_database():
    """Initialize and seed the database (development helper)."""
    init_db()
    seed_db()
    return "Database initialized and seeded!"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
