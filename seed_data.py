import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "").strip()
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "phantomid_db")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "phantom.db")

MOCK_PROFILES = [
    {
        "id": 1,
        "name": "Marcus Vance",
        "age": 42,
        "email": "m.vance@vancetech.io",
        "employment_years": 18,
        "account_balance": 84250.00,
        "credit_score": 760,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 2,
        "name": "Elena Rostova",
        "age": 29,
        "email": "elena.rostova@designlab.co",
        "employment_years": 6,
        "account_balance": 32100.00,
        "credit_score": 710,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 3,
        "name": "Arthur Pendelton",
        "age": 68,
        "email": "arthur.pendelton@heritageestates.com",
        "employment_years": 44,
        "account_balance": 210000.00,
        "credit_score": 815,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 4,
        "name": "Tyler Durden-Smith",
        "age": 19,
        "email": "tyler.d.smith99@fastnetmail.org",
        "employment_years": 16,
        "account_balance": 145000.00,
        "credit_score": 790,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 5,
        "name": "Priya Sharma",
        "age": 35,
        "email": "priya.sharma@apexanalytics.in",
        "employment_years": 11,
        "account_balance": 67400.00,
        "credit_score": 740,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 6,
        "name": "Jordan Belfort-Cruz",
        "age": 22,
        "email": "jordan.b.cruz@phantomtrade.net",
        "employment_years": 1,
        "account_balance": 890000.00,
        "credit_score": 845,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 7,
        "name": "David Kim",
        "age": 51,
        "email": "david.kim@seoultechsolutions.com",
        "employment_years": 26,
        "account_balance": 128900.00,
        "credit_score": 780,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 8,
        "name": "Sophia Martinez",
        "age": 24,
        "email": "sophia.martinez@creativemedia.es",
        "employment_years": 2,
        "account_balance": 9800.00,
        "credit_score": 660,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 9,
        "name": "Sarah Connor-Reese",
        "age": 38,
        "email": "sarah.reese@cyberdef-security.com",
        "employment_years": 20,
        "account_balance": -12000.00,
        "credit_score": 795,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    },
    {
        "id": 10,
        "name": "Liam O'Connor",
        "age": 31,
        "email": "liam.oconnor@dublincloud.ie",
        "employment_years": 8,
        "account_balance": 44500.00,
        "credit_score": 695,
        "status": "Unscanned",
        "verdict": None,
        "reason": None,
        "anomaly_score": 0.0
    }
]


def is_mongo_available():
    """Checks if a valid MongoDB URI is provided and reachable."""
    if not MONGO_URI:
        return False
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        return True
    except Exception:
        return False


def get_sqlite_conn():
    conn = sqlite3.connect(SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_sqlite():
    conn = get_sqlite_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            employment_years INTEGER NOT NULL,
            account_balance REAL NOT NULL,
            credit_score INTEGER NOT NULL,
            status TEXT DEFAULT 'Unscanned',
            verdict TEXT,
            reason TEXT,
            anomaly_score REAL DEFAULT 0.0
        )
    """)
    conn.commit()
    conn.close()


def seed_database():
    """Seeds the database (MongoDB Atlas or SQLite fallback)."""
    if is_mongo_available():
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        users_col = db["users"]
        users_col.delete_many({})
        users_col.insert_many([dict(p) for p in MOCK_PROFILES])
        return "MongoDB Atlas seeded with 10 financial profiles."
    else:
        init_sqlite()
        conn = get_sqlite_conn()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users")
        for p in MOCK_PROFILES:
            cursor.execute("""
                INSERT INTO users (id, name, age, email, employment_years, account_balance, credit_score, status, verdict, reason, anomaly_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                p["id"], p["name"], p["age"], p["email"], p["employment_years"],
                p["account_balance"], p["credit_score"], p["status"],
                p["verdict"], p["reason"], p["anomaly_score"]
            ))
        conn.commit()
        conn.close()
        return "Local SQLite (phantom.db) seeded with 10 financial profiles."


def fetch_profiles():
    """Fetches all profiles from the active storage engine."""
    if is_mongo_available():
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        profiles = list(db["users"].find({}, {"_id": 0}).sort("id", 1))
        return profiles, "MongoDB Atlas"
    else:
        init_sqlite()
        conn = get_sqlite_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY id ASC")
        rows = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return rows, "SQLite Local"


def update_profile_scan(profile_id, verdict, reason, anomaly_score):
    """Updates scan results for a specific profile."""
    if is_mongo_available():
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        db["users"].update_one(
            {"id": profile_id},
            {"$set": {
                "status": "Scanned",
                "verdict": verdict,
                "reason": reason,
                "anomaly_score": anomaly_score
            }}
        )
    else:
        conn = get_sqlite_conn()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET status = 'Scanned', verdict = ?, reason = ?, anomaly_score = ?
            WHERE id = ?
        """, (verdict, reason, anomaly_score, profile_id))
        conn.commit()
        conn.close()


def insert_profile(profile):
    """Inserts a new profile into the active database and returns its assigned ID."""
    if is_mongo_available():
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        highest = list(db["users"].find({}, {"id": 1}).sort("id", -1).limit(1))
        next_id = (highest[0]["id"] + 1) if highest else 1
        profile["id"] = next_id
        db["users"].insert_one(dict(profile))
        return next_id
    else:
        init_sqlite()
        conn = get_sqlite_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) as max_id FROM users")
        row = cursor.fetchone()
        next_id = (row["max_id"] or 0) + 1
        profile["id"] = next_id
        cursor.execute("""
            INSERT INTO users (id, name, age, email, employment_years, account_balance, credit_score, status, verdict, reason, anomaly_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            next_id, profile["name"], profile["age"], profile["email"], profile["employment_years"],
            profile["account_balance"], profile["credit_score"], profile.get("status", "Unscanned"),
            profile.get("verdict"), profile.get("reason"), profile.get("anomaly_score", 0.0)
        ))
        conn.commit()
        conn.close()
        return next_id


if __name__ == "__main__":
    result = seed_database()
    print(f"[PhantomID Data Engine] {result}")

