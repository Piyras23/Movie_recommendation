import streamlit as st
import requests

# Moovie recommendations from Flask API
def get_movie_recommendations(user_id):
    #Use flask container name via docker ps or docker ps -a
    url = f"http://lucid_villani:5001/user_recommendations?user_id={user_id}"
    response = requests.get(url)
    data = response.json()
    return data

# Processing 
st.title("Movie Recommendation App")

# User input for user ID
user_id = st.number_input("Enter User ID:", min_value=1, max_value=100, value=1, step=1)

# Retreive movie recommendations
recommendations = get_movie_recommendations(user_id)

# Display recommendations and influencing factors
if recommendations:
    st.write(f"Top Movie Recommendations for User {user_id}:")
    for movie in recommendations['movies']:
        st.write(f"- {movie['title']} (Factors: {', '.join(movie['factors'])})")
else:
    st.warning("No recommendations available.")         
