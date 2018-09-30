import pandas as pd
from  MovieTraining import MovieDataTrainingMatrix
import np
from np import maximum
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, accuracy_score, recall_score,mean_squared_error
import matplotlib.pyplot as mp

import math

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
    pd.to_numeric(df["gross"])
    pd.to_numeric(df["budget"])

    df.dropna(inplace=True)
    return df



def predict(df):
    mm = MovieDataTrainingMatrix.loadDf(df)
    mm2 = mm.cutOut(0.35)
    model = LinearRegression()



    poly = PolynomialFeatures(degree=2)
    new_vairables = poly.fit_transform(mm.variables)
    new_gross = poly.fit_transform(mm.gross)


    model.fit(new_vairables,new_gross)

    new_mm2_var = poly.fit_transform(mm2.variables)
    new_mm2_gross = poly.fit_transform(mm2.gross)
    predictions = model.predict(new_mm2_var)
    counter=0

    for i,prediction in enumerate(predictions):
        print(" raw prediction: {:.2f}, Target: {:.2f} diff {:.3f}".format(prediction[1], mm2.gross[i][0],prediction[1] -mm2.gross[i][0]))
        print("     Predicted gross: {:.2f}, Target: {:.2f}".format(2**(prediction[1]-8),2**(mm2.gross[i][0])))
        diff = abs(2**(prediction[1]-0.9) - 2**(mm2.gross[i][0]))/2**(prediction[1]-0.9)

        tolerance = 0.39
        if (diff < tolerance):
             counter+=1
        #print("Difference percentage {}%".format(diff*100))
    print("R-squard: {}".format(model.score(new_mm2_var,new_mm2_gross)))

    print("{} samples has difference less than {}% of the real goss over {}".format(counter,tolerance*100,len(predictions)))


def predictBudget(df):
    mm = MovieDataTrainingMatrix.loadDf(df)
    mm2 = mm.cutOut(0.35)
    model = LinearRegression()
    model.fit(mm.variables, mm.budget)
    predictions = model.predict(mm2.variables)
    counter = 0
    # for i, prediction in enumerate(predictions):
    #     print(" raw prediction: {:.2f}, Target: {} diff {}".format(prediction, mm2.budget[i][0],
    #                                                                        prediction - mm2.budget[i][0]))
    #     print("     Predicted gross: {:.2f}, Target: {:.2f}".format(2 ** (prediction), 2 ** (mm2.budget[i][0])))
    #     diff = abs(2 ** (prediction) - 2 ** (mm2.budget[i])) / 2 ** (prediction)
    #
    #     tolerance = 0.39
    #     if (diff < tolerance):
    #         counter += 1
    #     # print("Difference percentage {}%".format(diff*100))
    print("R-squard: {}".format(model.score(mm2.variables, mm2.budget)))

def predictrevenueByBudget(df):
    mm = MovieDataTrainingMatrix.loadDf(df)
    mm2 = mm.cutOut(0.35)
    model = LinearRegression(fit_intercept=True)
    model.fit(mm.variables, mm.gross)
    predictions = model.predict(mm2.variables)
    counter=0
    for i, prediction in enumerate(predictions):
        print(" raw prediction: {:.2f}, Target: {} diff {}".format(prediction[0], mm2.gross[i][0],prediction[0] - mm2.gross[i][0]))
        print("     Predicted gross: {:.2f}, Target: {:.2f}".format(2 ** (prediction[0]), 2 ** (mm2.gross[i][0])))
        diff = abs(2 ** (prediction[0]) - 2 ** (mm2.gross[i][0])) / 2 ** (prediction[0])
        tolerance=0.50
        if (diff < tolerance):
            counter += 1


    print("R-squard: {}".format(model.score( mm2.variables,mm2.gross)))
    print("{} samples has difference less than {}% of the real goss over {}".format(counter, tolerance * 100,
                                                                                    len(predictions)))

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


def housing():

    ##
    df=pd.read_csv("Melbourne_housing_FULL.csv")
    df = df[df.Price.notnull()]
    df.Car.fillna(0, inplace=True)
    df.Landsize.fillna(0,inplace=True)
    df.dropna(inplace=True)

    df["Price"] = np.log2(df["Price"])
    df["Distance"] = np.multiply(1000,df["Distance"])
    # df.plot.scatter(y="Price", x="Rooms", title="Bathroom v price")
    # df.plot.scatter(y="Price", x="Distance", title="Distance v price")
    mp.show()
    var=[]
    aim=[]
    typeSet=set()
    typeDict=dict()
    for index, row in df.iterrows():
        nType=row["Type"]
        if nType not in typeSet:
            typeSet.add(nType)
            typeDict[nType] = len(typeSet)

        typeIndex = typeDict[nType]
        nRooms = row["Rooms"]
        distance = row["Distance"]
        nCars = row["Car"]
        ln = row["Lattitude"]
        lon = row["Longtitude"]
        landSize = row["Landsize"]
        pc = row["Postcode"]
        numP=row["Propertycount"]
        bathRoom=row["Bathroom"]
        var.append([nRooms,distance,nCars,ln,lon,landSize,pc,typeIndex,bathRoom])
        aim.append([row["Price"]])

    train_x=var[:int(0.75*len(var))]
    test_x = var[int(0.75 * len(var)):]
    train_y = aim[:int(0.75 * len(var))]
    test_y = aim[int(0.75 * len(var)):]


    model = LinearRegression(fit_intercept=True,normalize=True)
    model.fit(train_x, train_y)
    predictions = model.predict(test_x)
    print(aim)
    counter = 0
    for i, prediction in enumerate(predictions):
        print(" raw prediction: {:.2f}, Target: {:.2f} diff {:.2f}".format(prediction[0], test_y[i][0],
                                                                   prediction[0] - test_y[i][0]))
        print("     Predicted Price: {:.2f}, Target: {:.2f}, dif {:.2f}".format(2 ** (prediction[0]),
                                                                                2 ** (test_y[i][0]),
                                                                                2 ** (prediction[0])- 2 ** (test_y[i][0])))

        diff = abs(2 ** (prediction[0]) - 2 ** (test_y[i][0])) / 2 ** (test_y[i][0])
        print(diff)
        tolerance=0.30
        if (diff < tolerance):
            counter += 1
        #pass
    print("R-squard: {}".format(model.score(test_x, test_y)))
    print("MSE: {}".format(np.sqrt(mean_squared_error(test_y,predictions))))
    print("{} samples has difference less than {}% of the real goss over {}".format(counter, tolerance * 100,
                                                                                    len(predictions)))

if __name__ == '__main__':
    hello()
    df= readData()
    df =dataCleaning(df)
    #predict(df)
    #predictKnn(df)
    #predictBudget(df)
    predictrevenueByBudget(df)
    df.to_csv("movie_refined.csv")
    df["all_Like"] = df.actor_1_facebook_likes+df.actor_3_facebook_likes+df.actor_2_facebook_likes
    df["buget_duration"]=df.budget/df.duration
    df["budget"]=np.log(df["budget"])
    df["gross"] = np.log(df["gross"])
    df["all_Like"] = np.log(df["all_Like"])
    # df.plot.scatter(y="budget", x="all_Like", title="buget v popularity of actors")
    # df.plot.scatter(y="gross",x="budget", title = "buget v gross")
    # df.plot.scatter(y="gross", x="all_Like", title = "popularity of actors v gross ")
    # # df.plot.scatter(y="gross", x="buget_duration",title = "buget_duration v gross")
    # df.plot.scatter(y="gross", x="duration" , title = "duration v gross")
    # df.plot.scatter(y="gross", x="imdb_score", title="imdb-score v gross")
    # df.plot.scatter(y="imdb_score", x="all_Like", title="imdb-score v popularity")
    # df.plot.scatter(y="imdb_score", x="budget", title="imdb-score v budget")
    #mp.show()




