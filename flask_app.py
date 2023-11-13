from flask import Flask, request, jsonify
import pandas as pd
from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import train_test_split


app = Flask(__name__)

# Load data only rating and movies 
df_rating = pd.read_csv('ratings.csv')
df_movies = pd.read_csv('movies.csv')

# Cross-validation: 80-20 split
reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(df_rating[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=0.2)

# Train the model using KNNBasic with cosine similarity
sim_options = {'name': 'cosine', 'user_based': True}
model = KNNBasic(sim_options=sim_options)
model.fit(trainset)

@app.route('/user_recommendations', methods=['GET'])
def recommend_movies():
    user_id = int(request.args.get('user_id', default=1))

    # Unrated movies for the user
    user_movies = df_rating[df_rating['userId'] == user_id]['movieId'].unique()
    user_unrated_movies = df_rating[~df_rating['movieId'].isin(user_movies)]['movieId'].unique()
    user_unrated_movies = [(user_id, movie_id, 3.0) for movie_id in user_unrated_movies]

    # Predictions for unrated movies
    user_predictions = model.test(user_unrated_movies)

    # DataFrame for easy manipulation
    user_predictions_df = pd.DataFrame([[pred.uid, pred.iid, pred.est] for pred in user_predictions], columns=['userId', 'movieId', 'estimated_rating'])

    # Merging with movie titles
    user_recommendations = pd.merge(user_predictions_df, df_movies[['movieId', 'title']], on='movieId')

    # Get top 5 recommendations
    user_top_n = user_recommendations.sort_values(by='estimated_rating', ascending=False).head(5)

    # Convert the recommendations to JSON
    recommendations_json = user_top_n[['title', 'estimated_rating']].to_dict(orient='records')

    return jsonify(recommendations_json)

if __name__ == '__main__':
    app.run(debug=True)