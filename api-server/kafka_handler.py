from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaTimeoutError, TopicAlreadyExistsError
from kafka import KafkaProducer, KafkaConsumer
import json

class KafkaHandler:
    """
    A handler class for interacting with Kafka, including creating topics, sending messages, 
    and consuming messages. The class supports SASL/PLAIN authentication using SCRAM-SHA-256.
    """

    def __init__(self,
                 kafka_brokers: list[str],
                 username: str,
                 password: str):
        """
        Initialize the KafkaHandler with the necessary Kafka broker details and authentication.

        Args:
            kafka_brokers (list[str]): List of Kafka broker addresses.
            username (str): Username for Kafka authentication.
            password (str): Password for Kafka authentication.
        """
        self.kafka_brokers = kafka_brokers
        self.username = username
        self.password = password
        
    def create_topic(self,
                     topic_name: str,
                     num_partitions: int = 1,
                     replication_factor: int = 1):
        """
        Create a new Kafka topic with the specified name, number of partitions, and replication factor.

        Args:
            topic_name (str): The name of the Kafka topic to create.
            num_partitions (int): The number of partitions for the topic. Defaults to 1.
            replication_factor (int): The replication factor for the topic. Defaults to 1.
        """
        # Set up Kafka admin client for managing Kafka topics
        admin_client = KafkaAdminClient(
            bootstrap_servers=self.kafka_brokers,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='SCRAM-SHA-256',
            sasl_plain_username=self.username,
            sasl_plain_password=self.password
        )
        
        # Define the new topic configuration
        new_topic = NewTopic(name=topic_name,
                             num_partitions=num_partitions,
                             replication_factor=replication_factor)
        
        try:
            # Attempt to create the new topic
            admin_client.create_topics(new_topics=[new_topic], validate_only=False)
            print(f"Topic '{topic_name}' created successfully")
        except TopicAlreadyExistsError:
            # Handle the case where the topic already exists
            print(f"Topic '{topic_name}' already exists")

        # Close the Kafka admin client
        admin_client.close()

    def send_message(self,
                     message: dict[str, str],
                     topic: str):
        """
        Send a message to a specified Kafka topic.

        Args:
            message (dict[str, str]): The message to send, structured as a dictionary.
            topic (str): The Kafka topic to send the message to.
        """
        # Set up Kafka producer for sending messages to Kafka topics
        producer = KafkaProducer(
            bootstrap_servers=self.kafka_brokers,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='SCRAM-SHA-256',
            sasl_plain_username=self.username,
            sasl_plain_password=self.password,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize message as JSON
        )
        
        try:
            # Send the message to the specified topic
            producer.send(topic=topic, value=message)
            producer.flush()  # Ensure all buffered records are sent
            print(f"Message sent to topic '{topic}'")
        except KafkaTimeoutError:
            # Handle timeout errors if the message fails to send
            print(f'Timed out waiting for message to be sent to topic {topic}')

        # Close the Kafka producer
        producer.close()

    def consume_messages(self,
                         topic: str) -> KafkaConsumer:
        """
        Consume messages from a specified Kafka topic.

        Args:
            topic (str): The Kafka topic to consume messages from.

        Returns:
            KafkaConsumer: A KafkaConsumer instance configured to consume messages from the topic.
        """
        # Set up Kafka consumer for consuming messages from Kafka topics
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_brokers,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='SCRAM-SHA-256',
            sasl_plain_username=self.username,
            sasl_plain_password=self.password,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Deserialize JSON messages
        )

        # Return the KafkaConsumer instance for external use
        return consumer
