from kafka import KafkaConsumer
import json
import os
from processor import process_refund
from dotenv import load_dotenv

load_dotenv()

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')

def create_consumer():
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        enable_auto_commit=True,
        group_id='refund-group',
    )

def consume_messages():
    consumer = create_consumer()
    print(f"Refund service started, monitoring '{KAFKA_TOPIC}' topic...")

    for message in consumer:
        print(f"Received message: {message.value}")
        process_refund(message.value)
        consumer.commit()
