import pickle
import streamlit as st 
import requests

## load the mpodel
st.header("Movie Recommendation System Using Machinelearning")

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox('Type or Select a movie to get recommendation',
             movie_list
             )

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=83a84f806830931c3cfa43e9d443864c&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommend_movie_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    return recommended_movies_name, recommend_movie_poster

if st.button('Show recommendation'):
    recommonded_movies_name, recommended_movies_poster = recommend(selected_movie)


