from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timezone, timedelta
from kafka_handler import KafkaHandler
import os

# Kafka configuration
# These environment variables are expected to be set with the necessary Kafka details.
KAFKA_BROKERS = os.environ['KAFKA_BROKERS'].split(",")  # List of Kafka broker addresses
KAFKA_USERNAME = os.environ['KAFKA_USERNAME']  # Kafka username for authentication
KAFKA_PASSWORD = os.environ['KAFKA_PASSWORD']  # Kafka password for authentication
KAFKA_TOPIC = os.environ['KAFKA_TOPIC']  # Kafka topic for sending messages

# API server configuration
# These environment variables are expected to be set with the necessary API server details.
API_SERVER_HOST = os.environ['API_SERVER_HOST']
API_SERVER_PORT = os.environ['API_SERVER_PORT']

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

# Handle the "buy" request
@app.route('/api/buy/', methods=['POST'])
def buy():
    """
    Endpoint to handle purchase requests. The request data is enriched with a timestamp and sent to Kafka.

    Returns:
        JSON response indicating the success or failure of the operation.
    """
    data = request.json  # Retrieve JSON data from the POST request
    data['timestamp'] = datetime.now(timezone(timedelta(hours=3))).isoformat()  # Add current timestamp in the specified timezone

    # Create Kafka handler for interacting with Kafka
    kafka_handler = KafkaHandler(kafka_brokers=KAFKA_BROKERS,
                                 username=KAFKA_USERNAME,
                                 password=KAFKA_PASSWORD)
    
    # Ensure the Kafka topic exists; create it if not
    kafka_handler.create_topic(KAFKA_TOPIC)
    
    # Send the purchase data to the Kafka topic
    kafka_handler.send_message(message=data,
                               topic=KAFKA_TOPIC)

    # Return success response
    return jsonify({'status': 'success', 'message': 'Purchase request sent to Kafka', 'data': data}), 200

# Handle the "getAllUserBuys" request
@app.route('/api/getAllUserBuys/', methods=['GET'])
def get_all_user_buys():
    """
    Endpoint to retrieve all user purchase records. The request is forwarded to the Customer Management service.

    Returns:
        JSON response with the list of user purchases or an error message if the retrieval fails.
    """
    # Forward the GET request to the Customer Management service at the specified endpoint
    response = requests.get(f'http://{API_SERVER_HOST}:{API_SERVER_PORT}/api/purchases/')
    
    if response.status_code == 200:
        # Return the purchase data if the request was successful
        return jsonify(response.json()), 200
    else:
        # Return an error message if the request failed
        return jsonify({'status': 'error', 'message': 'Failed to retrieve user purchases'}), response.status_code

if __name__ == '__main__':
    # Start the Flask web server
    app.run(debug=True, host='0.0.0.0', port=8080)  # Flask will run in debug mode
