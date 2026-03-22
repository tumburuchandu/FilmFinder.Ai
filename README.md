# 🎬 Movie Recommender App

A web-based movie recommendation system built with **Flask** and **machine learning** that suggests movies based on content similarity. The application includes user authentication, model training notebooks, and an end-to-end recommendation pipeline.

This project demonstrates practical skills in:

* Python backend development
* Machine learning model building
* Data preprocessing and NLP
* Full-stack web development with Flask

---

## 🚀 Features

* User **signup and login system**
* Movie recommendation using content-based filtering
* TMDB dataset integration
* Pretrained model loading for fast recommendations
* Clean web UI with dashboard
* Modular code structure (auth, database, recommender separated)

---

## 🧠 Recommendation Engine Overview

The system recommends movies using:

* Combined movie metadata (genres, keywords, cast, overview)
* Text vectorization using **CountVectorizer**
* Similarity calculation using **cosine similarity**

This enables the app to recommend movies with similar themes and storytelling patterns.

---

## 🏗️ Tech Stack

**Backend**

* Python
* Flask

**Machine Learning**

* Pandas
* NumPy
* Scikit-learn

**Frontend**

* HTML
* CSS

**Data Source**

* TMDB 5000 Movies Dataset

---

## 📂 Project Structure

```text
movie-recommender-app/
│
├── app.py                     # Main Flask application
├── auth.py                    # Authentication logic
├── db.py                      # Database handling
├── recommender.py             # Recommendation engine
│
├── data/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── models/                    # Trained vector & similarity models
│
├── notebooks/
│   └── recommender_training.ipynb
│
├── templates/
│   ├── dashboard.html
│   ├── login.html
│   └── signup.html
│
├── static/
│   ├── style.css
│   ├── logo.png
│   └── no_poster.png
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/tumburuchandu/FilmFinder.Ai.git
cd FilmFinder.Ai
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 🔐 Authentication Flow

Users must:

1. Sign up
2. Log in
3. Access dashboard to get movie recommendations

This simulates a real-world production web application with session-based access control.

---

## 🧪 Model Training

The recommendation model was trained using the notebook:

```
notebooks/recommender_training.ipynb
```

It performs:

* Data cleaning
* Feature engineering
* Vectorization
* Similarity matrix generation

---

## 📊 Dataset

The application uses the **TMDB 5000 dataset**, containing:

* Movie titles
* Cast and crew
* Genres
* Keywords
* Overview descriptions

These features are merged and transformed into a vector representation for similarity comparison.

---

## 📌 Example Workflow

1. User logs in
2. Selects a movie
3. System loads precomputed similarity model
4. Returns top recommended movies

---

## 🧑‍💻 Author

**Chandu Tumburu**

* GitHub: https://github.com/tumburuchandu

---

## 📈 Future Improvements

* Deploy to cloud (Render or AWS)
* Add movie posters via TMDB API
* Add collaborative filtering
* Improve UI with Bootstrap or React

---

## 📜 License

This project is developed for educational and portfolio purposes.
