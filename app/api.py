from flask import Flask, request, jsonify
from flask_cors import CORS
from internal import ConnectionRabbitmq, RabbitmqPublisher , RabbitmqConsumer
import json

app = Flask(__name__)
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
app.config['JSON_SORT_KEYS'] = False
connectionRabbitmq = ConnectionRabbitmq()


def callback(ch, method, properties, body):
    print(json.loads(body))

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
    rabitmq_consumer.start()


if __name__ == "__main__":
    app.run(debug = True, host ='0.0.0.0', port=7070)