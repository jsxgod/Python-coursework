import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score


movies = pd.read_csv("./ml-latest-small/movies.csv")
ratings = pd.read_csv("./ml-latest-small/ratings.csv.")

# toy story ratings
toy_story_ratings = ratings.loc[ratings["movieId"] == 1]
movie_ids = movies['movieId'].to_numpy()

toy_story_raters = ratings[ratings['movieId'] == 1][['rating', 'userId']].to_numpy()
user_ids = toy_story_raters[:, 1]


def generate_X(m, user_ids):
    allowed_ids = movie_ids[movie_ids <= m]
    ratings_ = ratings[(ratings['movieId'] <= m) & (ratings['userId'].isin(user_ids))]
    X_ = ratings_.pivot(index='userId', columns='movieId', values='rating').reindex(allowed_ids[1:], axis='columns')
    np.nan_to_num(X_, copy=False)
    return X_


Y = toy_story_raters[:, 0]
max_id_list = [10, 100, 200, 500, 1000, 10000]
regr_scores = []

regr = LinearRegression()

for m in max_id_list:
    X = generate_X(m, user_ids)
    clf = regr.fit(X, Y)
    regr_scores.append(clf.score(X, Y))

plt.scatter(max_id_list, regr_scores, linewidth=3, color='orange')
plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
plt.xscale('log')
plt.xlabel('m')
plt.ylabel('R2 Scores')
plt.show()

test_users = [i for i in range(1, 16)]
all_users = [i for i in range(1, 216)]

predictions = []
Y_test = Y[200:]
for m in max_id_list:
    X = generate_X(m, user_ids)

    X_train = X[:200]
    Y_train = Y[:200]

    X_test = X[200:]

    clf = regr.fit(X_train, Y_train)
    Y_predicted = regr.predict(X_test)
    predictions.append((Y_predicted, m))

for prediction in predictions[-1:]:
    df = pd.DataFrame({'Actual': Y_test.flatten(), 'Predicted': prediction[0].flatten()})
    df.index += 1
    df.to_csv('diff'+str(prediction[1])+'.csv')
    df.plot(kind='bar', figsize=(16, 10))
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='green')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.show()

