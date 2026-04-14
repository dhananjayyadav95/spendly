import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = "expense_tracker.db"


def get_db():
    """Return a SQLite connection with row_factory and foreign keys enabled."""
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables using CREATE TABLE IF NOT EXISTS."""
    db = get_db()

    # Users table
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Expenses table
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # Index for faster queries
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses(user_id)
    """)

    db.commit()
    db.close()


def seed_db():
    """Insert sample data for development."""
    db = get_db()

    # Check if data already exists
    result = db.execute("SELECT COUNT(*) FROM users").fetchone()
    if result[0] > 0:
        db.close()
        return

    # Insert sample users
    users = [
        ("alice", "alice@example.com", generate_password_hash("password123")),
        ("bob", "bob@example.com", generate_password_hash("password456")),
        ("carol", "carol@example.com", generate_password_hash("password789")),
    ]

    db.executemany(
        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
        users
    )

    # Get user IDs
    alice_id = db.execute(
        "SELECT id FROM users WHERE username = ?", ("alice",)
    ).fetchone()[0]
    bob_id = db.execute(
        "SELECT id FROM users WHERE username = ?", ("bob",)
    ).fetchone()[0]

    # Insert sample expenses
    expenses = [
        (alice_id, 12.50, "Food", "Lunch at cafe", "2026-04-10"),
        (alice_id, 45.00, "Transport", "Monthly bus pass", "2026-04-05"),
        (alice_id, 120.00, "Utilities", "Electricity bill", "2026-04-01"),
        (bob_id, 25.00, "Entertainment", "Movie tickets", "2026-04-12"),
        (bob_id, 60.00, "Food", "Groceries", "2026-04-11"),
        (bob_id, 15.00, "Food", "Coffee with friends", "2026-04-08"),
        (bob_id, 200.00, "Utilities", "Internet bill", "2026-04-03"),
    ]

    db.executemany(
        "INSERT INTO expenses (user_id, amount, category, description, date) VALUES (?, ?, ?, ?, ?)",
        expenses
    )

    db.commit()
    db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Seeding database...")
    seed_db()
    print("Done!")
