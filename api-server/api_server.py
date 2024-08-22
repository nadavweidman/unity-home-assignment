from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
from kafka_handler import KafkaHandler
import threading

# Kafka configuration
# These environment variables are expected to be set with the necessary Kafka details.
KAFKA_BROKERS = os.environ['KAFKA_BROKERS'].split(",")  # List of Kafka broker addresses
KAFKA_USERNAME = os.environ['KAFKA_USERNAME']  # Username for Kafka authentication
KAFKA_PASSWORD = os.environ['KAFKA_PASSWORD']  # Password for Kafka authentication
KAFKA_TOPIC = os.environ['KAFKA_TOPIC']  # Kafka topic to consume messages from

# MongoDB configuration
# These environment variables are expected to be set with MongoDB connection details.
MONGODB_ROOT_USERNAME = os.environ['MONGODB_ROOT_USERNAME']  # MongoDB root username
MONGODB_ROOT_PASSWORD = os.environ['MONGODB_ROOT_PASSWORD']  # MongoDB root password
MONGODB_HOST = os.environ['MONGODB_HOST']  # MongoDB host address
MONGODB_PORT = os.environ['MONGODB_PORT']  # MongoDB port number

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the Flask app

# MongoDB connection
# Establish a connection to MongoDB using the provided credentials and host details.
client = MongoClient(f'mongodb://{MONGODB_ROOT_USERNAME}:{MONGODB_ROOT_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/')
db = client['admin']  # Connect to the 'admin' database
purchases_collection = db['purchases']  # Access the 'purchases' collection
purchases_collection.create_index("timestamp", unique=True)  # Ensure the 'timestamp' field is unique

@app.route('/api/purchases/', methods=['GET'])
def get_user_purchases():
    """
    API endpoint to retrieve all user purchases from the MongoDB collection.
    Returns:
        JSON response containing all purchase documents or an error message.
    """
    try:
        # Query the purchases collection for all the purchases
        purchases = list(purchases_collection.find())

        # Convert ObjectId to string to make it JSON serializable
        for purchase in purchases:
            purchase['_id'] = str(purchase['_id'])
        
        return jsonify(purchases), 200  # Return the purchases as a JSON response with HTTP status 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error message with HTTP status 500

def consume_and_store_messages():
    """
    Function to consume messages from the Kafka topic and store them in the MongoDB collection.
    The function runs indefinitely until interrupted.
    """
    # Create KafkaHandler instance for consuming messages
    kafka_handler = KafkaHandler(kafka_brokers=KAFKA_BROKERS,
                                 username=KAFKA_USERNAME,
                                 password=KAFKA_PASSWORD)
    
    # Create a Kafka consumer for the specified topic
    consumer = kafka_handler.consume_messages(KAFKA_TOPIC)

    try:
        # Process messages from the Kafka topic
        for message in consumer:
            document = message.value  # Get the message value (assumed to be a JSON document)

            try:
                # Insert the message into the MongoDB collection
                purchases_collection.insert_one(document)
                print(f"Message inserted into MongoDB: {document}")
            except DuplicateKeyError:
                # Skip duplicate entries based on the unique 'timestamp' index
                continue
    except KeyboardInterrupt:
        # Handle a keyboard interrupt to stop the consumer gracefully
        print("Stopping consumer...")
    finally:
        # Ensure the consumer is closed when the function exits
        consumer.close()

if __name__ == '__main__':
    # Start Kafka consumer in a separate thread to run concurrently with the Flask app
    consumer_thread = threading.Thread(target=consume_and_store_messages)
    consumer_thread.start()

    # Start the Flask web server
    app.run(debug=True, host='0.0.0.0', port=5000)  # Flask will run in debug mode
