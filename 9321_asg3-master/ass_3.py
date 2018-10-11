#!/usr/bin/python3
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from flask_cors import CORS
from pymongo import MongoClient
from MachineLearning.Predictor import Predictor
import requests
import json
from Model.RecordReader import RecordReader
from Model.DataCleanser import DataCleanser
from Model.Plotter import Plotter

##--------------------
from MachineLearning.DecisionTree import suggestion
from collections import defaultdict
##--------------------

# app = Flask(__name__, static_url_path='', static_folder='PPP/build/')
# CORS(app)

app = Flask(__name__)
api = Api(app, doc='/swagger/')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


# set up mongodb
# SEAN mLab
MONGODB_URI = "mongodb://sean:comp4920@ds121603.mlab.com:21603/9321_asg3"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("9321_asg3")

# John mLab
# MONGODB_URI = "mongodb://COMP9321:comp9321password@ds117422.mlab.com:17422/comp9321"
# client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
# db = client.get_database("comp9321")


# Instantiate class
rr = RecordReader(db)
# rr.reset_mongodb("Melbourne_housing_FULL.csv")

predictor = Predictor(rr.to_dataframe("melbourne_housing"))
processor = DataCleanser()

plotter = Plotter()



"""

Predict price for a suburb, and also the price of 3 suburbs nearby. This allows user to have more choice

Also get things such as restaurants, hospitals, schools, etc, within the vincity of the suburb

"""
# query parser
queryParser = api.parser()
queryParser.add_argument('bedroom')
queryParser.add_argument('bathroom')
queryParser.add_argument('carpark')
queryParser.add_argument('type')
queryParser.add_argument('suburb')

@api.route('/predictPrice')
@api.expect(queryParser)
class PredictPrice(Resource):
    def get(self):

        # parse query
        args        = queryParser.parse_args()
        bedroom     = args.get('bedroom')
        bathroom    = args.get('bathroom')
        carpark     = args.get('carpark')
        houseType   = args.get('type')
        suburb      = args.get('suburb')

        # predict price
        prediction = predictor.computePrice(int(bedroom),int(bathroom),int(carpark),houseType,suburb)
        processedPrediction = processor.processPrediction(prediction)

        # get geocode
        resultLocation = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+suburb+",Victoria"+"&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY")
        dataLocation = json.loads(resultLocation.content)

        lat = dataLocation['results'][0]['geometry']['location']['lat']
        lng = dataLocation['results'][0]['geometry']['location']['lng']
        location = str(lat)+","+str(lng)

        # get near by restarant
        resultRestaurant = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius=2000&type=restaurant&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY")
        dataRestaurant = json.loads(resultRestaurant.content)
        processedRestaurant = processor.processRestaurant(dataRestaurant['results'])

        # get near by hospital
        resultHospital = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius=2000&type=hospital&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY")
        dataHospital = json.loads(resultHospital.content)
        processedHospital = processor.processHospital(dataHospital['results'])

        # get near by school
        resultSchool = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius=2000&type=school&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY")
        dataSchool = json.loads(resultSchool.content)
        processedSchool = processor.processSchool(dataSchool['results'])

        # get near by supermarket
        resultSupermarket= requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+location+"&radius=2000&type=supermarket&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY")
        dataSupermarket = json.loads(resultSupermarket.content)
        processedSupermarket = processor.processSupermarket(dataSupermarket['results'])

        saveTrend(int(bedroom),int(bathroom),int(carpark),suburb)

        main_data = {
            "code"          : 200,
            "msg"           : "Predicted suburb successfully",
            "data"          : {
                "prediction"    : processedPrediction,
                "restaurant"    : processedRestaurant,
                "hospital"      : processedHospital,
                "school"        : processedSchool,
                "supermarket"   : processedSupermarket,
            }
        }
##-------------------------------------
        in_put=[]
        theta={'h':10,'u':1,'t':4}
        price_s=processedPrediction['main']['price']
##        price_s=1000000
        in_put.append(bedroom)
        in_put.append(bathroom)
        in_put.append(carpark)
        in_put.append(theta[houseType])
        in_put.append(price_s)
        in_put=[in_put]
        sug=suggestion(rr.to_dataframe("melbourne_housing"),theta,in_put)
        result=sug.make_suggestions()
        re_sug={
                    1:{"suburbs":result[0][5],
                        "price":result[0][4] },
                    
                    2:{"suburbs":result[1][5],
                         "price":result[1][4] },
                    
                    3:{"suburbs":result[2][5],
                        "price":result[2][4] },
                    
                    4:{"suburbs":result[3][5],
                        "price":result[3][4] },
                    
                    5:{"suburbs":result[4][5],
                        "price":result[4][4] }
                    }

        return re_sug#5 suggested home in other sub,I don't know in which format you prefer it insert in main data,
                                                        #so I didn't do this

##        return re_sug,main_data, 200
##-------------------------------------
@api.route('/trendRecord')
class trendRecord(Resource):
    def get(self):
        trendAnalyser = db['trendAnalyser']

        if (trendAnalyser.find_one({"total": "total"}) != None):

            totalCount = trendAnalyser.find_one({"total": "total"})

            cursor = trendAnalyser.find({})
            label   = []
            size    = []

            for document in cursor:
                if (document.get('suburb',"") != ""):
                    label.append(document['suburb'])
                    size.append(100*document['requestCount']/totalCount['totalCount'])

            plotter.pieChart(label,size)

            return {"message":"Done"},200

        else:
            return {"message":"no data"},401

def saveTrend(room, bath, carpark, suburb):
    trend = db['trendAnalyser']

    if (trend.find_one({"total": "total"}) == None):
        total = {}
        total['total'] = "total"
        total['totalCount'] = 1

        # insert
        trend.insert_one(total)
    else:
        total = trend.find_one({"total": "total"})
        total['totalCount'] = int(total['totalCount']) + 1

        trend.update({"total": "total"}, total)

    suburb = suburb.lower()

    if ( trend.find_one({"suburb": suburb}) == None):

        record = {}
        record['suburb'] = suburb
        record['request'] = [{"room": room, "bath": bath, "carpark": carpark}]
        record['requestCount'] = 1

        # insert
        trend.insert_one(record)

        return "created"

    else:

        record = trend.find_one({"suburb": suburb})
        record['requestCount'] = int(record['requestCount']) + 1
        record['request'].append({"room": room, "bath": bath, "carpark":carpark})
        trend.replace_one({"suburb": suburb}, record)

        return "updated"

@api.route('/basicfilters')
class basicFilters(Resource):
    def get(self):
        return {
             "code": 200,
            "msg": "basic filters",
            "data": {
                "max_bedroom": 31,
                "max_bathroom": 5,
                "max_carspace": 3,
                "types" : [
                    "house",
                    "unit"
                ]
            }
        }, 200

@api.route('/suburbs')
class allSuburb(Resource):
    def get(self):

        result = processor.processSuburb(db)

        return {
            "code": 200,
            "msg": "suburbs and postcodes",
            "data": result
        }, 200

@api.route('/maxprice')
class maxPrice(Resource):
    def get(self):

        return {
            "code": 200,
            "msg": "max price",
            "data": {
                "max_price": 999999
            }
        }, 200
##--------------------------------

##ask user to make suggestions by their own conditions
queryParser2 = api.parser()
queryParser2.add_argument('bedroom')
queryParser2.add_argument('bathroom')
queryParser2.add_argument('carpark')
queryParser2.add_argument('type')
queryParser2.add_argument('price')

@api.route('/suggestions')
@api.expect(queryParser2)
@api.response(200, 'OK')
@api.doc(description="make 5_suggestions for the page 2")
class make_suggestion(Resource):
    def get(self):
        theta={'h':10,'u':1,'t':4}
        ##in_put is a list with the format ['Bedroom2', 'Bathroom', 'Car', 'Type', 'Price']
        args        = queryParser2.parse_args()
        bedroom     = int(args.get('bedroom'))
        bathroom    = int(args.get('bathroom'))
        carpark = int(args.get('carpark'))
        houseType   = int(theta[str(args.get('type'))])
        price      = int(args.get('price'))

        
        in_put=[]
        in_put.append(bedroom)
        in_put.append(bathroom)
        in_put.append(carpark)
        in_put.append(houseType)
        in_put.append(price)
        in_put=[in_put]
##        in_put=[[3.0,2.0,1.0,4,1.57*1000000]]#default
        sug=suggestion(rr.to_dataframe("melbourne_housing"),theta,in_put)
        result=sug.make_suggestions()#result=[[3.0, 2.0, 1.0, 4, 1680000.0, 'West Melbourne'], 
                                                                        #[3.0, 2.0, 1.0, 4, 1650000.0, 'Fitzroy North'],
                                                                        #[3.0, 2.0, 1.0, 4, 1720000.0, 'Middle Park'],
                                                                        #[3.0, 2.0, 1.0, 4, 1640000.0, 'Fitzroy North'],
                                                                        #[3.0, 2.0, 1.0, 4, 1660000.0, 'Balwyn']]
        
        return{
            "code": 200,
            "msg": "suggestions made",
            "data": {
                1:{"suburbs":result[0][5],
                    "price":result[0][4] },
                
                2:{"suburbs":result[1][5],
                     "price":result[1][4] },
                
                3:{"suburbs":result[2][5],
                    "price":result[2][4] },
                
                4:{"suburbs":result[3][5],
                    "price":result[3][4] },
                
                5:{"suburbs":result[4][5],
                    "price":result[4][4] }
                }
            },200
            
##------------------------------


if __name__ == '__main__':
    # app.run(host='0', port=8007, debug=True)
    app.run(debug=True)
