from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='kafka:9092')

def send_kafka_message(message: str):
    producer.send('notifications', message.encode('utf-8'))
    producer.flush()
