import bcrypt
from db import cursor, db

def signup_user(username, email, password):
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )
    if cursor.fetchone():
        return "exists"

    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        (username, email, password)
    )
    db.commit()

    return "created"

def login_user(username, password):
    cursor.execute(
        "SELECT password FROM users WHERE username=%s",
        (username,)
    )

    result = cursor.fetchone()

    if result:
        stored_hash = result[0].encode()
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True

    return False