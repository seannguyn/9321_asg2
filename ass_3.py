import pandas as pd
from  MovieTraining import MovieDataTrainingMatrix
import np
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, accuracy_score, recall_score
import matplotlib.pyplot as mp


def hello():
    print("hello world!!")
    print("start assignment")
    print("join repo")

def readData():
    return pd.read_csv("movie_metadata.csv")

def dataCleaning(df):
    df.drop(columns=["language",
                     "director_facebook_likes",
                     #"country",
                     #"content_rating",
                     "movie_imdb_link",
                     "facenumber_in_poster",
                     "plot_keywords",
                     "num_voted_users",
                     "movie_title",
                     "num_critic_for_reviews",
                     "color",
                     #"movie_facebook_likes",
                     "aspect_ratio",
                     "title_year",
                     "num_user_for_reviews",
                     "cast_total_facebook_likes"],
            inplace=True)
    df = df.replace(0, np.nan)
    df = df[df.gross.notnull()]
    df = df[df.budget.notnull()]
    df = df[df.gross.notnull()]
    df = df[df.country == "USA"]

    df.dropna(inplace=True)
    return df



def predict(df):
    mm = MovieDataTrainingMatrix.loadDf(df)
    mm2 = mm.cutOut(0.25)
    model = LinearRegression()
    model.fit(mm.variables,mm.gross)

    predictions = model.predict(mm2.variables)
    counter=0
    for i,prediction in enumerate(predictions):
        print("Predicted: {}, Target: {}".format(prediction,mm2.gross[i]))
        diff = abs(prediction - mm2.gross[i])/ mm2.gross[i]
        if diff < 0.5 :
            counter+=1
        print("Difference percentage {}%".format(diff*100))
    print("R-squard: {}".format(model.score(mm2.variables, mm2.gross)))

    print("{} samples has difference less than 50% over {}".format(counter,len(predictions)))

def predictKnn(df):
    mm = MovieDataTrainingMatrix.loadDf(df)
    mm2 = mm.cutOut(0.25)
    knn = KNeighborsClassifier()
    knn.fit(mm.variables, mm.gross)
    predictions = knn.predict(mm2.variables)
    print("confusion_matrix:\n", confusion_matrix(mm2.gross, predictions))
    print("precision:\t", precision_score(mm2.gross, predictions, average=None))
    print("recall:\t\t", recall_score(mm2.gross, predictions, average=None))
    print("accuracy:\t", accuracy_score(mm2.gross, predictions))


if __name__ == '__main__':
    hello()
    df= readData()
    df =dataCleaning(df)
    #predict(df)
    #predictKnn(df)
    df.to_csv("movie_refined.csv")
    df["all_Like"] = df.actor_1_facebook_likes+df.actor_3_facebook_likes+df.actor_2_facebook_likes
    df["buget_duration"]=df.budget/df.duration
    df.plot.scatter(y="gross",x="budget", title = "buget v gross")
    df.plot.scatter(y="gross", x="all_Like", title = "popularity of actors v gross ")
    df.plot.scatter(y="gross", x="buget_duration",title = "buget_duration v gross")
    df.plot.scatter(y="gross", x="duration" , title = "duration v gross")
    df.plot.scatter(y="gross", x="imdb_score", title="imdb-score v gross")

    mp.show()