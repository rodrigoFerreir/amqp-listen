from flask import Flask, request, jsonify
from flask_cors import CORS
from internal import ConnectionRabbitmq, RabbitmqPublisher , RabbitmqConsumer
import requests
import json
from threading import Thread

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False
connectionRabbitmq = ConnectionRabbitmq()
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA3NTk0MTQzLCJpYXQiOjE3MDc1OTA1NDMsImp0aSI6IjI3Mzk1OGU3NmNlMDQ0ZDQ5ZmYxZjBjY2M4ZDU4ZjE2IiwidXNlcl9pZCI6MSwiZmlyc3RfbmFtZSI6IiIsImxhc3RfbmFtZSI6IiIsInVzZXJuYW1lIjoiYWRtaW4iLCJpc19zdXBlcnVzZXIiOnRydWUsImlzX2FkbWluIjp0cnVlLCJlbWFpbCI6ImFkbWluQHRlc3RlLmNvbSJ9.4E8qRHExNV-bR4xeJOZXare4C4hDDnIr7_yu21OvISY'

def callback(ch, method, properties, body):
    print(body)
    res = requests.post('http://localhost:8000/app/orders', 
                        json=json.loads(body),
                        headers={
                            'Authorization': f'Bearer {TOKEN}' 
                        },
                        verify=False)
    print(res.status_code)


@app.route("/", methods=['GET', 'POST'])
def test():
    return "teste", 200


@app.route("/publisher", methods=['POST'])
def create_order():
    __data_message = request.json
    __queue = RabbitmqPublisher(connectionRabbitmq)
    __queue.send_message(__data_message)
    return jsonify({'message':"mensagem publicada"}), 200


@app.route("/consumer", methods=['GET'])
def consumer_order():
    rabitmq_consumer = RabbitmqConsumer(connectionRabbitmq, callback)
    t = Thread(target=rabitmq_consumer.start)
    t.start()
    return jsonify({'message':"Consumindo mensagens publicadas"}), 200

if __name__ == "__main__":
    rabitmq_consumer = RabbitmqConsumer(connectionRabbitmq, callback)
    t = Thread(target=rabitmq_consumer.start)
    t.start()
    app.run(debug = True, host ='0.0.0.0', port=7070)