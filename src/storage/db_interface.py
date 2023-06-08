import sqlite3
from sqlite3 import Error

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('twitter_agent.db')  # Creates a SQLite database file
        print(f'successful SQLite connection with sqlite version {sqlite3.version}')
    except Error as e:
        print(f'The error {e} occurred')
    return conn

def create_table(conn):
    try:
        tweets_query = """
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                tweet_id TEXT NOT NULL,
                tweet TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """
        followers_query = """
            CREATE TABLE IF NOT EXISTS followers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                followers INTEGER NOT NULL,
                date TEXT NOT NULL
            )
        """
        conn.execute(tweets_query)
        conn.execute(followers_query)
        print("Tables were created successfully")
    except Error as e:
        print(f'The error {e} occurred')

def create_reports_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            followers_count INTEGER NOT NULL,
            average_ratio REAL NOT NULL
        )
    """)
    conn.commit()

def insert_tweet(conn, user_id, tweet_id, tweet, date):
    try:
        conn.execute(
            """
            INSERT INTO tweets (user_id, tweet_id, tweet, date)
            VALUES (?, ?, ?, ?)
            """, (user_id, tweet_id, tweet, date)
        )
        conn.commit()
    except Error as e:
        print(f"The error {e} occurred")

def insert_followers(conn, followers, date, user_id):
    try:
        query = "INSERT INTO followers (followers, date, user_id) VALUES (?, ?, ?)"
        conn.execute(query, (followers, date, user_id))
        conn.commit()
        print("Followers data was inserted successfully")
    except Error as e:
        print(f'The error {e} occurred')

def close_connection(conn):
    conn.close()

def get_tweets(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tweets")
    rows = cursor.fetchall()
    return rows

def get_followers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM followers")
    rows = cursor.fetchall()
    return rows

def get_tweet_ids(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT tweet_id FROM tweets")
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def get_tweet_ids_by_user(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT tweet_id FROM tweets WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def save_report_to_db(conn, report):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (date, agent_name, agent_id, followers_count, average_ratio)
        VALUES (?, ?, ?, ?, ?)
    """, (report.date, report.agent_name, report.agent_id, report.followers_count, report.average_ratio))
    conn.commit()
