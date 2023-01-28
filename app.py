from flask import Flask, render_template
from flask_mqtt import Mqtt
import json
from  cryptography.fernet import Fernet
from request import findElement as query
from pymongo import *

app = Flask(__name__)

#conessione atlas
password = 'trive004'
uri = 'mongodb+srv://riccardo:'+ password + '@cluster0.zzvi9yy.mongodb.net/test'
atlas = MongoClient(uri)
db = atlas.cluster0
collection = db.case

# configurazione Mqtt Server
app.config['MQTT_BROKER_URL'] = '80.210.122.173'
app.config['MQTT_BROKER_PORT'] = 1883
#

mqtt = Mqtt(app)

# chiave Fernet
f = open('key.txt' , 'r')
chiave = f.read()
f.close()
chiave_valore = Fernet(chiave)
#

#lettura file
f = open('casa.config.txt' , 'r')
lista = f.read().split(' = ')
#

#parametri
casa = lista[1]
topic = 'home/misurazioni/' + casa
refresh = 5
#
#dati = {
#    "casa": 0,
#    "data": "",
#    "tempo": "",
#    "stanze": {
#        "cucina": {"temperatura": 0, "umidita": 0},
#        "soggiorno": {"temperatura": 0, "umidita": 0 },
#        "mansarda": {"temperatura": 0 , "umidita": 0 },
#        "camera_da_letto": {"temperatura": 0 , "umidita": 0}
#    }
#}


#function
def findLastElement(n_element , casa):
    print(casa)
    items = collection.find({"payload.casa": int(casa)})
    items = list(items)
    items = items[(len(items) - n_element): ]
    return(items)
#


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/stanza/<param>')
def room(param):
    nome = 'dati.html'
    obj = dati['stanze'][param]
    obj = {**obj , "tempo": dati['tempo'] , 'data': dati['data']}
    return render_template(nome , dati=obj , REFRESH=refresh , room=param)

@app.route('/stanza/<param>/tabella')
def table(param):
    print(param)
    datas = []
    template = 'table.html'
    items = findLastElement(5 , casa)

    for item in items:
        payload = item['payload']
        time = payload['data']
        data = payload['stanze'][param]
        data = {**data , "tempo": time}
        datas.append(data)

    return render_template(template ,  dati=datas)

@mqtt.on_connect()
def gestione_conessione(client , userdata , flasgs , rc):
    mqtt.subscribe(topic)

@mqtt.on_message()
def gestione_messaggio(client , userdata , msg):
    global dati
    dati_criptati = msg.payload
    dati_json_bytes = chiave_valore.decrypt(dati_criptati) # <--- decriptazione del messaggio in bytes (string criptato-> bytes decriptato)
    dati_json = dati_json_bytes.decode('utf-8')
    dati = json.loads(dati_json)
    return(dati_json)



