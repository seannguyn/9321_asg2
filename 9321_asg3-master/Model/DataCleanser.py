import requests
import json
from pymongo import MongoClient

API_key = "&key=AIzaSyB4x8PJO2adnI_tjpv3dAOBXD-5buVnQlY"
url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="

class DataCleanser(object):
    """docstring for DataCleanser."""
    def __init__(self):
        super(DataCleanser, self).__init__()

    def processPrediction(self, prediction):

        print("process prediction")

        counter = 0
        anchor = prediction[0]
        recommendation = []

        for p in prediction:

            if p == anchor:
                continue
            if (counter == 5):
                break
            if (p['price'] <= anchor['price'] + 20000 and p['price'] >= anchor['price'] - 20000):
                recommendation.append(p)
                counter += 1

        return {'main':anchor,'recommendation':recommendation}

    def processRestaurant(self, dataList):
        dataList_1 = []

        for r in dataList:
            keyRating = r.get("rating","")
            keyPhoto = r.get("photos","")
            if (keyRating != "" and keyPhoto!= ""):
                dataList_1.append(r)

        sortedDataList = sorted(dataList_1, key=lambda k: k['rating'], reverse=True)

        result = []
        counter = 0

        for r in sortedDataList:

            obj = {}
            obj['name'] = r['name']
            obj['location'] = r['geometry']['location']
            obj['photo'] = url+r['photos'][0]['photo_reference']+API_key
            obj['rating'] = r['rating']
            obj['vicinity'] = r['vicinity']

            result.append(obj)
            counter += 1
            if (counter==len(sortedDataList) or counter == 4):
                break

        return result

    def processHospital(self, dataList):

        result = []
        counter = 0

        for r in dataList:

            obj = {}
            obj['name'] = r['name']
            obj['location'] = r['geometry']['location']
            obj['vicinity'] = r['vicinity']

            result.append(obj)
            counter += 1
            if (counter==len(dataList) or counter == 4):
                break

        return result

    def processSchool(self, dataList):
        dataList_1 = []

        for r in dataList:
            keyRating = r.get("rating","")
            keyPhoto = r.get("photos","")
            if (keyRating != "" and keyPhoto!= ""):
                dataList_1.append(r)

        sortedDataList = sorted(dataList_1, key=lambda k: k['rating'], reverse=True)

        result = []
        counter = 0

        for r in sortedDataList:

            obj = {}
            obj['name'] = r['name']
            obj['location'] = r['geometry']['location']
            obj['photo'] = url+r['photos'][0]['photo_reference']+API_key
            obj['rating'] = r['rating']
            obj['vicinity'] = r['vicinity']

            result.append(obj)
            counter += 1
            if (counter==len(sortedDataList) or counter == 4):
                break

        return dataList_1

    def processSupermarket(self, dataList):
        dataList_1 = []

        for r in dataList:
            keyRating = r.get("rating","")
            keyPhoto = r.get("photos","")
            if (keyRating != "" and keyPhoto!= ""):
                dataList_1.append(r)

        sortedDataList = sorted(dataList_1, key=lambda k: k['rating'], reverse=True)

        result = []
        counter = 0

        for r in sortedDataList:

            obj = {}
            obj['name'] = r['name']
            obj['location'] = r['geometry']['location']
            obj['photo'] = url+r['photos'][0]['photo_reference']+API_key
            obj['rating'] = r['rating']
            obj['vicinity'] = r['vicinity']

            result.append(obj)
            counter += 1
            if (counter==len(sortedDataList) or counter == 4):
                break

        return result

    def processSuburb(self, db):

        suburb = db['suburb']
        if (suburb.find_one({"title":"Victoria"}) == None):

            records = db['records']
            melbourne_house = records.find_one({"title": "melbourne_housing"})
            count = 1;
            suburbObject = {}
            existedSuburb = []

            for entry in melbourne_house['entry']:

                if (entry['Postcode'] in existedSuburb):
                    continue


                existedSuburb.append(entry['Postcode'])
                suburbObject[str(count)] = {
                    "suburb"    : entry['Suburb'],
                    "postcode"  : entry['Postcode']
                }
                count += 1

            suburbRecord = {
                "title": "Victoria",
                "entry": suburbObject
            }

            suburb.insert_one(suburbRecord)
            return suburbObject

        else :
            return suburb.find_one({"title":"Victoria"})['entry']
