import pickle
from sklearn.metrics.pairwise import cosine_similarity
import requests
import json
import os
import re
from difflib import get_close_matches

# ===== Load models =====
movies = pickle.load(open("models/movies.pkl", "rb"))
similarity = pickle.load(open("models/embeddings.pkl", "rb"))
cv = pickle.load(open("models/vectorizer.pkl", "rb"))
vectors = pickle.load(open("models/vectors.pkl", "rb"))

# ===== TMDB API =====
API_KEY = os.getenv("TMDB_API_KEY")


# ===== Poster cache =====
CACHE_FILE = "models/poster_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        poster_cache = json.load(f)
else:
    poster_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(poster_cache, f)


def fetch_poster(title):
    # return from cache if already fetched
    if title in poster_cache:
        return poster_cache[title]

    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data.get("results"):
            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                poster_cache[title] = poster_url
                save_cache()
                return poster_url

    except Exception as e:
        print("Poster fetch error:", e)

    # fallback placeholder
    poster_cache[title] = "/static/no_poster.png"
    save_cache()
    return poster_cache[title]



# ===== Normalize titles once (performance optimized) =====
def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', '', text)
    return text

movies['clean_title'] = movies['title'].apply(normalize)

# ===== Movie-to-movie recommendation =====
def recommend(movie_name, n=10):
    movie_name = normalize(movie_name)
    titles = movies['clean_title'].tolist()

    # ===== Fuzzy matching =====
    if movie_name not in titles:
        suggestion = get_close_matches(movie_name, titles, n=1, cutoff=0.6)
        if suggestion:
            movie_name = suggestion[0]
        else:
            return []

    idx = movies[movies['clean_title'] == movie_name].index[0]
    distances = similarity[idx]

    ranked = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:n+1]

    results = []
    for i in ranked:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        results.append({"title": title, "poster": poster})

    return results


# ===== Description-based recommendation =====
def recommend_by_description(query, n=10):
    query_vec = cv.transform([query]).toarray()
    scores = cosine_similarity(query_vec, vectors)[0]

    ranked = sorted(
        list(enumerate(scores)),
        key=lambda x: x[1],
        reverse=True
    )[:n]

    results = []
    for i in ranked:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        results.append({"title": title, "poster": poster})

    return results

def search_by_person(name):
    name = normalize(name)

    actor_matches = movies[
        movies['cast_names'].str.lower().str.contains(name, na=False)
    ]

    director_matches = movies[
        movies['director_name'].str.lower().str.contains(name, na=False)
    ]

    combined = movies.loc[
        actor_matches.index.union(director_matches.index)
    ]

    results = []
    for _, row in combined.head(10).iterrows():
        poster = fetch_poster(row['title'])
        results.append({"title": row['title'], "poster": poster})

    return results

def get_top_movies(n=50):
    results = []

    # simply return first 50 popular movies from dataset
    top_movies = movies.head(n)

    for _, row in top_movies.iterrows():
        poster = fetch_poster(row['title'])
        results.append({
            "title": row['title'],
            "poster": poster
        })

    return results