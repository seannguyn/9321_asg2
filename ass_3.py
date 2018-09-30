#!/usr/bin/python3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


def main():
    raw_df = pd.read_csv('movie_metadata.csv')
    df = raw_df

    colors = {}
    i = 0
    for color in df.color.unique():
        colors[color] = i
        i += 1

    directors = {}
    i = 0
    for director in df.director_name.unique():
        directors[director] = i
        i += 1

    actors = {}
    i = 0
    for actor in np.concatenate(
        (df.actor_1_name.unique(), df.actor_2_name.unique(),
         df.actor_3_name.unique()),
            axis=None):
        if actor not in actors:
            actors[actor] = i
            i += 1

    languages = {}
    i = 0
    for language in df.language.unique():
        languages[language] = i
        i += 1

    content_ratings = {}
    i = 0
    for content_rating in df.content_rating.unique():
        content_ratings[content_rating] = i
        i += 1

    df = df[df.country == 'USA'][[
        'color',
        'director_name',
        'actor_1_name',
        'actor_2_name',
        'actor_3_name',
        'language',
        'duration',
        'content_rating',
        'budget',
        'gross',
        'title_year',
    ]].dropna().replace({
        'color': colors,
        'director_name': directors,
        'actor_1_name': actors,
        'actor_2_name': actors,
        'actor_3_name': actors,
        'language': languages,
        'content_rating': content_ratings,
    })

    print('All non-empty record of USA:', df.shape)

    X = df.drop(['gross'], axis=1)
    y = df['gross']

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    print('Train set:', X_train.shape)
    print('Test set:', X_test.shape)

    linreg = LinearRegression()
    linreg.fit(X_train, y_train)

    y_pred = linreg.predict(X_test)
    print('R-Squared:', linreg.score(X_test, y_test))


if __name__ == '__main__':
    main()
