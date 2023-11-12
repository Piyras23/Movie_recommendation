import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy

# Baseline model for the challenge: User-Based CF:
# Applied dot product for single user vector (cosine similarity)

def load_data():
    # Load data only rating and movies 
    df_rating = pd.read_csv('ratings.csv')
    df_movies = pd.read_csv('movies.csv')
    
    return df_rating, df_movies

# For Merging and CV: 
def preprocess_data(df_rating, df_movies):
    df_movie_rating = df_rating.merge(df_movies)

    # Cross-validation: 80-20 split
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df_movie_rating[['userId', 'movieId', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    
    return trainset, testset

def train_model(trainset):
    # Train the model using KNNBasic with cosine similarity
    sim_options = {'name': 'cosine', 'user_based': True}
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)
    
    return model

def get_user_recommendations(model, user_id, df_rating, df_movies, N=5):
    # Unrated movies for the user
    user_movies = df_rating[df_rating['userId'] == user_id]['movieId'].unique()
    user_unrated_movies = df_rating[~df_rating['movieId'].isin(user_movies)]['movieId'].unique()
    user_unrated_movies = [(user_id, movie_id, 3.0) for movie_id in user_unrated_movies]

    # Predictions for unrated movies
    user_predictions = model.test(user_unrated_movies)

    #DataFrame for easy manipulation
    user_predictions_df = pd.DataFrame([[pred.uid, pred.iid, pred.est] for pred in user_predictions], columns=['userId', 'movieId', 'estimated_rating'])

    # Merging with movie titles
    user_recommendations = pd.merge(user_predictions_df, df_movies[['movieId', 'title']], on='movieId')

    # Get top 5 recommendations
    user_top_n = user_recommendations.sort_values(by='estimated_rating', ascending=False).head(N)

    return user_top_n[['title', 'estimated_rating']]

def main():
    df_rating, df_movies = load_data()
    trainset, testset = preprocess_data(df_rating, df_movies)
    model = train_model(trainset)

    # Example: Get recommendations for user 1
    user_id = 2
    recommendations = get_user_recommendations(model, user_id, df_rating, df_movies)
    print(f"Top 5 movie recommendations for User {user_id}:\n{recommendations}")

if __name__ == "__main__":
    main()