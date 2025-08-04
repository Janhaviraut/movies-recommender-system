import streamlit as st
import pickle
import pandas as pd
import requests
import os

# Step 1: Google Drive download setup
def download_file_from_google_drive(file_id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value

    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

# Step 2: Load similarity.pkl
def load_similarity():
    if not os.path.exists("similarity.pkl"):
        st.write("📥 Downloading similarity.pkl from Google Drive...")
        file_id = "1xY3jiMEDro-L6ZvV0h15OLdk4bzxs7IW"  # your Google Drive file ID
        download_file_from_google_drive(file_id, "similarity.pkl")
    return pickle.load(open("similarity.pkl", "rb"))

# Step 3: Fetch movie poster using TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=4a0ce73191eec0be2e2bcbae317cb378&language=en-US"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Step 4: Recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# Load movie_dict
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity
similarity = load_similarity()

# Streamlit UI
st.title('🎬 "CineMatch: A Content-Based Movie Recommendation System using Streamlit')

selected_movie = st.selectbox(
    "Choose a movie to get similar recommendations 👇",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    st.subheader("Top 5 Similar Movies:")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
