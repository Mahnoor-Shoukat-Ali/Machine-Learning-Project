from kafka import KafkaConsumer
import logging

consumer = KafkaConsumer('notifications', bootstrap_servers='kafka:9092')

for msg in consumer:
    logging.info(f"Received message: {msg.value.decode('utf-8')}")
