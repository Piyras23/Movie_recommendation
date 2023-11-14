import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy as surprise_accuracy

def load_data():
    # Loading data rating, movies and tag (only for factor influence)
    df_rating = pd.read_csv('ratings.csv')
    df_movies = pd.read_csv('movies.csv')
    df_tag = pd.read_csv('tags.csv')
    
    return df_rating, df_movies, df_tag

# For Merging and CV: 
def preprocess_data(df_rating, df_movies, df_tag):
    df_movie_rating = df_rating.merge(df_movies)
    
    # Bonus:  Factors influencing 
    df_movie_rating_tag = pd.merge(df_movie_rating,df_tag, on='movieId')
    df_movie_rating_tag.drop(labels=['timestamp_x','userId_y','timestamp_y'], axis=1, inplace=True)
    df_movie_rating_tag.rename(columns={'userId_x': 'userId'}, inplace=True)
    

    # Cross-validation: 80-20 split"
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(df_movie_rating[['userId', 'movieId', 'rating']], reader)
    trainset, testset = train_test_split(data, test_size=0.2)
    
    return trainset, testset

def train_model(trainset):
    #cosine similarity
    sim_options = {'name': 'cosine', 'user_based': True}
    
    #Using KNN wrt Cosine Similarity by DOT product calculation:
    model = KNNBasic(sim_options=sim_options)
    model.fit(trainset)
    
    return model


def calculate_factors(row, df_movie_rating_tag):
    # Factors in given genres and tags for Version 1:
    movie_id = row['movieId']
    movie_info = df_movie_rating_tag[df_movie_rating_tag['movieId'] == movie_id].iloc[0]
    factors = [f"Factor influencing (Genre): {movie_info['genres']}"]
    return ', '.join(factors)


def get_user_recommendations(model, user_id, df_rating, df_movies, N=5):
    # Taking unrated movies
    user_movies = df_rating[df_rating['userId'] == user_id]['movieId'].unique()
    user_unrated_movies = df_rating[~df_rating['movieId'].isin(user_movies)]['movieId'].unique()
    user_unrated_movies = [(user_id, movie_id, 3.0) for movie_id in user_unrated_movies]

    # Predictions
    user_predictions = model.test(user_unrated_movies)

    # DataFrame for easy manipulation
    user_predictions_df = pd.DataFrame([[pred.uid, pred.iid, pred.est] for pred in user_predictions], columns=['userId', 'movieId', 'estimated_rating'])

    user_recommendations = pd.merge(user_predictions_df, df_movies[['movieId', 'title']], on='movieId')

    # Add factor using only genre influencing recommendations
    user_recommendations['factors'] = user_recommendations.apply(lambda row: calculate_factors(row, df_movies), axis=1)

    # Get top 5 recommendations
    user_top_n = user_recommendations.sort_values(by='estimated_rating', ascending=False).head(N)

    return user_top_n[['title', 'estimated_rating', 'factors']]



def main():
    df_rating, df_movies, df_tag = load_data()
    trainset, testset = preprocess_data(df_rating, df_movies, df_tag)
    model = train_model(trainset)

    # Example: Get recommendations for user 1
    user_id = 1
    recommendations = get_user_recommendations(model, user_id, df_rating, df_movies)

    # Evaluating on test set
    predictions = model.test(testset)
    accuracy = surprise_accuracy.rmse(predictions)

    print(f"Top 5 movie recommendations for User {user_id}:\n{recommendations}")
    print(f"Model Accuracy Using Root Mean Square error: {accuracy}")

if __name__ == "__main__":
    main()
    print('\n', 'Recommendations are calculated based on User-Based Collaborative Filtering by dot produtct Cosine of User vectors')
