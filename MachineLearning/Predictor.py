import numpy as np
from sklearn.linear_model import LinearRegression


class Predictor(object):
    """docstring for Predictor."""
    var=[]
    aim=[]
    model=None
    suburb_meta=dict()

    def __init__(self, df):
        super(Predictor, self).__init__()
        df = self._data_normalizing(df)
        self._construct_training_set(df)
        self._construct_suburb_meta(df)
        self._construct_model()

    def _data_normalizing(self,df):
        df["Price"] = np.log2(df["Price"])
        df["Distance"] = np.multiply(1000, df["Distance"])
        df.Type.replace({'h': 7, 'u': 1, "t": 1}, inplace=True)
        return df

    def _construct_suburb_meta(self,df):
        suburdata=df.groupby('Suburb')
        ndf=suburdata["Distance"].mean().to_frame()
        ndf["la"]=suburdata["Lattitude"].mean().to_frame()
        ndf["ln"]=suburdata["Longtitude"].mean().to_frame()
        for index, row in ndf.iterrows():
            self.suburb_meta[index]={"la":row["la"], "ln":row["ln"], "dis":row["Distance"]}
        print()

    def _construct_training_set(self, df):
        for index, row in df.iterrows():
            nRooms = row["Rooms"]
            nCars = row["Car"]
            bathRoom = row["Bathroom"]
            distance = row["Distance"]
            la = row["Lattitude"]
            lon = row["Longtitude"]
            self.var.append([nRooms, nCars, row["Type"], bathRoom, distance, la, lon])
            self.aim.append([row["Price"]])

    def _construct_model(self):
        self.model = LinearRegression(fit_intercept=True, normalize=True)
        self.model.fit(self.var, self.aim)

    def computePrice(self,room, bath, carpark, houseType, suburb):

        result=[]
        for key in self.suburb_meta.keys():
            price=2 ** self.model.predict([[room, carpark, 7, bath,
                                            self.suburb_meta[key]["dis"],
                                            self.suburb_meta[key]["la"],
                                            self.suburb_meta[key]["ln"]]])[0][0]
            if (suburb.lower() == key.lower()):
                neededSuburb = {"room":room, "bath": bath, "suburb": key, "price": price}
            else:
                result.append({"room":room, "bath": bath, "suburb": key, "price": price})

        result.insert(0, neededSuburb)

        return result
