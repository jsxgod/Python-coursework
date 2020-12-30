import pandas as pd
import numpy as np


def prepare_test_data():
    test_data = np.zeros((9019, 1))
    test_data[7254] = 5
    test_data[420] = 4
    test_data[827] = 3
    test_data[997] = 5

    return test_data


def recommend_movies(movies, ratings, user_ratings, limit=10):
    X = np.nan_to_num(ratings / np.linalg.norm(ratings, axis=0))
    y = np.nan_to_num(user_ratings / np.linalg.norm(user_ratings))

    z = np.dot(X, y)
    Z = np.nan_to_num(z / np.nan_to_num(np.linalg.norm(z)))

    r = np.dot(X.T, Z)

    recommended_movies = [(r[m[0]][0], m[1]) for m in movies]

    return sorted(recommended_movies, key=lambda m: m[0], reverse=True)[:limit]


ratings_df = pd.read_csv("ml-latest-small/ratings.csv")
movies_df = pd.read_csv("ml-latest-small/movies.csv")

movies = movies_df.loc[movies_df.movieId < 10000, ["movieId", "title"]].to_numpy()

ratings_data = ratings_df.loc[ratings_df.movieId < 10000, ["userId", "movieId", "rating"]].to_numpy()
ratings = np.zeros((611, 9019))
for data in ratings_data:
    ratings[int(data[0]), int(data[1])] = data[2]

test_ratings = prepare_test_data()

recommendation_limit = 5

recommendations = recommend_movies(movies, ratings, test_ratings, recommendation_limit)

print('Top ', recommendation_limit, ' recommendations:')
print("Score\t\t\tTitle")
for score, movie in recommendations:
    print(score, '\t', movie)
