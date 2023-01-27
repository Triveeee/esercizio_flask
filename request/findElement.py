from pymongo import *

# conessione
# Atlas mongoDB
password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas['cluster0']
collection = db['case']

#function find

def findLastElement(n_element , casa):
    print(casa)
    items = collection.find({"payload.casa": casa})
    print(items)
    items = list(items)
    print(items)
    items = items[(len(items) - n_element): ]
    return(items)
    
