import math

class MovieDataTrainingMatrix:
    gross=[]
    budget=[]
    variables=[]
    imdbScore=[]



    @classmethod
    def add_value_adding_ability(cls,df):
        directorDict = dict()
        for index, row in df.iterrows():

            directorName = row["director_name"]
            revenue=row["gross"]
            budget=row["budget"]
            if directorName not in directorDict.keys():
                directorDict[directorName]={"num": 1,
                                            "ability": revenue/budget
                                            }
            else:
                directorDict[directorName]["ability"] = (directorDict[directorName]["ability"] *
                           directorDict[directorName]["num"]+revenue/budget)/(directorDict[directorName]["num"]+1)
                directorDict[directorName]["ability"]+=1
        return directorDict

    @classmethod
    def loadDf(cls,df):

        variables=[]
        gross=[]
        budget=[]
        imdbScore = []
        directorValueAddingAbility = cls.add_value_adding_ability(df)
        for index, row in df.iterrows():
            # if abs(row["budget"]-row["gross"])/row["budget"]>4:
            #     continue
            #d1 = row["director_facebook_likes"]
            a1 = row["actor_1_facebook_likes"]
            a2 = row["actor_2_facebook_likes"]
            a3 = row["actor_3_facebook_likes"]
            variables.append([math.log2(a1+a2+a3)])
            gross.append([math.log2(row["gross"])])
            budget.append([math.log2(row["budget"])])
            imdbScore.append(row["imdb_score"])
        return MovieDataTrainingMatrix(gross,budget,variables,imdbScore)

    """
        df is a dataframe
    """
    def __init__(self,gross,budget,variables,imdbScore):
        self.gross=gross
        self.budget=budget
        self.variables=variables
        self.imdbScore=imdbScore


    def cutOut(self,percentage):
        percentageThisMatrixKeep=(1 - percentage)
        theLargestIndexAfterCut = int(percentageThisMatrixKeep * len(self.gross))
        newMovieDataTrainingMatrix = MovieDataTrainingMatrix(
            self.gross[theLargestIndexAfterCut:],
            self.budget[theLargestIndexAfterCut:],
            self.variables[theLargestIndexAfterCut:],
            self.imdbScore[theLargestIndexAfterCut:],
        )
        self.gross = self.gross[:theLargestIndexAfterCut]
        self.budget = self.budget[:theLargestIndexAfterCut]
        self.variables = self.variables[:theLargestIndexAfterCut]
        self.imdbScore = self.imdbScore[:theLargestIndexAfterCut]
        return newMovieDataTrainingMatrix


    def show(self):
        print(self.gross)
        print()
        print(self.budget)
        print()
        print(self.variables)
