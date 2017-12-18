from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import argparse
import json
from bus_producer import BusProducer

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route('/produce', methods=['POST'])
def send_message():
    # content = request.get_json(silent=True)
    print(request.method)

    try:
        content = json.loads(request.data.decode("utf-8"))
        # content = request.get_json()

        # Get topic list
        topics = content["topics"]

        # Get message to be produced
        message = content["message"]

        print("- New message request. The message will be produced to topics " + str(topics))

    except Exception as e:
        print(e)
        abort(401)

    # Create a producer
    producer = BusProducer()

    # For each topic in requested topic list
    for topic in topics:
        producer.send(topic=topic, message=message)

    response = jsonify({'result': 'Message produced'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':

    # Decorate console
    print('\033[95m' + "\n*****************************")
    print("*** BUS PRODUCER API v1.0 ***")
    print("*****************************\n" + '\033[0m')

    try:
        # Parse arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--host')
        parser.add_argument('--port')
        args = parser.parse_args()

        # If the user has provided custom IP and port
        host = args.host
        port = args.port

    except Exception:
        # Use default values
        host = '0.0.0.0'
        port = 5002

    app.run(debug=False, host=host, port=port)