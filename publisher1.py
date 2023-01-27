from pymongo import * 
from paho.mqtt.client import *
from random import *
from datetime import *
from time import *
from cryptography.fernet import Fernet
import json

#------------------------------------------------
#Dati
topic = 'home/misurazioni/'
topic_mongo = 'atlas/mongodb/case'
BROKER_HOST ='80.210.122.173'
PORTA_BROKER = 1883

#----------------------------------------------
#definizione chiave
f = open('key.txt' , 'r')
chiave = f.read()
f.close()
chiave_valore = Fernet(chiave)

#-----------------------------------------------
#Conessione al broker

client = Client()
client.connect(BROKER_HOST,PORTA_BROKER)

#----------------------------------------------
#Funzioni

def cryptation(message):
    message_byte = message.encode('utf-8')  # <-- trasformazione messaggio in formato utf-8 (in bytes)
    message_cryptated_byte = chiave_valore.encrypt(message_byte) # <--criptazione del messaggio in bytes (viene trasformato in stringa)
    message_cryptated = message_cryptated_byte.decode('utf-8')
    return message_cryptated

def createHome(n_casa):
    minimo = 1
    massimo = 100
    data = datetime.date(datetime.now())
    tempo = datetime.time(datetime.now())
    home = {
        "casa": n_casa,
        "data": str(data),
        "tempo": str(tempo),
        "stanze": {
            "cucina": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)},
            "soggiorno": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)},
            "mansarda": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)},
            "camera_da_letto": {"temperatura": randint(minimo , massimo), "umidita": randint(minimo , massimo)}
        }
    }
    home = json.dumps(home , indent= 4)   # <--- trasformazione in stringa json
    home = cryptation(home) # <---  richiama la funzione cryptation
    return home

#--------------------------------------------
#Main

client.loop_start()
try:
    while True:
        for i in range(4):
            home = createHome(i)
            client.publish(topic + str(i) , home)
            client.publish(topic_mongo , home)
            print(topic)
            print(type(home))
            print(home)
            sleep(1)
        sleep(3)

except KeyboardInterrupt:
    print("Stop publisher")

client.loop_stop()
client.disconnect()
