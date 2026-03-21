from flask import Flask, render_template, request, redirect, session, flash, url_for

from auth import signup_user, login_user
from recommender import (recommend, recommend_by_description, search_by_person)
from db import cursor, db
from recommender import get_top_movies

app = Flask(__name__)
app.secret_key = "supersecret"

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/signup_page')
def signup_page():
    return render_template("signup.html")
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    result = signup_user(username, email, password)

    if result == "exists":
        flash("Account already exists with this email. Please login.")
        return redirect(url_for('login_page'))

    if result == "created":
        flash("Account created successfully. Please login.")
        return redirect(url_for('login_page'))

    flash("Signup failed. Try again.")
    return redirect(url_for('signup_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if login_user(username, password):
        session['user'] = username
        return redirect('/dashboard')

    flash("Invalid credentials. Please try again.")
    return redirect(url_for('login_page'))

@app.route('/skip')
def skip():
    session['user'] = "Guest"
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/')

    # Show top movies if user has no search history
    cursor.execute(
        "SELECT query FROM history WHERE username=%s ORDER BY id DESC LIMIT 1",
        (session['user'],)
    )
    last_query = cursor.fetchone()

    if last_query:
        # show previous recommendation results
        results = recommend_by_description(last_query[0])
    else:
        # first-time user → show top movies
        results = get_top_movies()

    return render_template(
        "dashboard.html",
        user=session['user'],
        movies=results
    )
# ===== THIS IS THE MISSING LINK =====



@app.route('/recommend', methods=['POST'])
def recommend_movies():
    if 'user' not in session:
        return redirect('/')

    query = request.form['query']

    # ===== Save search history =====
    if session['user'] != "Guest":
        cursor.execute(
        "INSERT INTO history (username, query) VALUES (%s, %s)",
        (session['user'], query)
        )
        db.commit()

    # ===== Stage 1: actor / director search =====
    results = search_by_person(query)

    # ===== Stage 2: title-based recommendation =====
    if not results:
        results = recommend(query)

    # ===== Stage 3: description similarity fallback =====
    if not results:
        results = recommend_by_description(query)

    return render_template(
        "dashboard.html",
        user=session['user'],
        movies=results
    )
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)