# consumer.py
# Consumer: read messages from Kafka and insert into PostgreSQL

import json
import logging
from confluent_kafka import Consumer, KafkaError
import psycopg2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = 'kafka_storage:9092'
KAFKA_TOPIC = 'raw_data'
KAFKA_GROUP_ID = 'data-loader-group'

# PostgreSQL target DB (приёмник)
conn = psycopg2.connect(
    dbname="consumerDB1",
    user="user1",
    password="pass1",
    host="db_consumer_1",
    port=5432
)

# Kafka consumer config
consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'group.id': KAFKA_GROUP_ID,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}

consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])

# Save record to PostgreSQL
def apply_record(record):
    source = record['key'].split(':')[0] if record.get('key') else 'unknown'
    data = record['value']
    op = data.get('operation', 'insert').lower()

    with conn.cursor() as cur:
        try:
            if source == 'source1':
                if op == 'insert':
                    cur.execute(
                        """
                        INSERT INTO users (id, name, email, country_id, create_dt)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (data['id'], data['name'], data['email'], data['country_id'], data.get('create_dt'))
                    )
                elif op == 'update':
                    cur.execute(
                        """
                        UPDATE users
                        SET name = %s, email = %s, country_id = %s, create_dt = %s
                        WHERE id = %s
                        """,
                        (data['name'], data['email'], data['country_id'], data.get('create_dt'), data['id'])
                    )
                elif op == 'delete':
                    cur.execute("DELETE FROM users WHERE id = %s", (data['id'],))

            elif source == 'source2':
                if op == 'insert':
                    cur.execute(
                        """
                        INSERT INTO country (id, name, create_dt)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (data['id'], data['name'], data.get('create_dt'))
                    )
                elif op == 'update':
                    cur.execute(
                        """
                        UPDATE country
                        SET name = %s, create_dt = %s
                        WHERE id = %s
                        """,
                        (data['name'], data.get('create_dt'), data['id'])
                    )
                elif op == 'delete':
                    cur.execute("DELETE FROM country WHERE id = %s", (data['id'],))

            else:
                logger.warning(f"Unknown source: {source}")

            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"DB operation failed for record {record['key']}: {e}")

# Main loop
try:
    logger.info("Starting Kafka consumer...")
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                logger.error(f"Kafka error: {msg.error()}")
            continue

        try:
            record = {
                'key': msg.key().decode('utf-8') if msg.key() else None,
                'value': json.loads(msg.value().decode('utf-8'))
            }
            apply_record(record)
            logger.info(f"Processed record: {record['key']}")
        except Exception as e:
            logger.exception(f"Error processing message: {e}")
except KeyboardInterrupt:
    logger.info("Stopping consumer...")
finally:
    consumer.close()
    conn.close()
