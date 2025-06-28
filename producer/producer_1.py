
import time
import json
import logging
from confluent_kafka import Producer
import psycopg2
from psycopg2.extras import RealDictCursor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Kafka settings
KAFKA_BOOTSTRAP_SERVERS = 'kafka_storage:9092'
KAFKA_TOPIC = 'raw_data'
POLL_INTERVAL = 10

# Initialize Kafka producer
producer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
}
producer = Producer(producer_conf)

# State: last processed IDs
last_ids = {
    'source1': 0,
    'source2': 0
}

# Connect to PostgreSQL containers directly
conn1 = psycopg2.connect(
    dbname="sourceDB1",
    user="user1",
    password="pass1",
    host="db_source_1",
    port=5432,
    cursor_factory=RealDictCursor
)

conn2 = psycopg2.connect(
    dbname="sourceDB2",
    user="user1",
    password="pass1",
    host="db_source_2",
    port=5432,
    cursor_factory=RealDictCursor
)

# Fetch new rows from a source table
def fetch_new(conn, table, last_id):
    with conn.cursor() as cur:
        cur.execute(
            f"SELECT * FROM {table} WHERE id > %s ORDER BY id",
            (last_id,)
        )
        return cur.fetchall()

# Delivery callback for Kafka
def delivery_callback(err, msg):
    if err:
        logger.error(f"Delivery failed for record {msg.key()}: {err}")
    else:
        logger.debug(f"Record {msg.key()} delivered to {msg.topic()} [{msg.partition()}]")

# Produce records to Kafka
def send_to_kafka(source_name, records):
    for rec in records:
        key = f"{source_name}:{rec['id']}"
        value = json.dumps(rec, default=str)
        try:
            producer.produce(
                topic=KAFKA_TOPIC,
                key=key,
                value=value,
                callback=delivery_callback
            )
        except Exception as e:
            logger.error(f"Error producing record {key}: {e}")
    producer.flush()

# Main loop
if __name__ == '__main__':
    logger.info("Starting data producer loop...")
    while True:
        try:
            # Source 1
            new1 = fetch_new(conn1, 'users', last_ids['source1'])
            if new1:
                send_to_kafka('source1', new1)
                last_ids['source1'] = new1[-1]['id']
                logger.info(f"Sent {len(new1)} records from source1")

            # Source 2
            new2 = fetch_new(conn2, 'countries', last_ids['source2'])
            if new2:
                send_to_kafka('source2', new2)
                last_ids['source2'] = new2[-1]['id']
                logger.info(f"Sent {len(new2)} records from source2")

        except Exception as e:
            logger.exception(f"Error in producer loop: {e}")
        time.sleep(POLL_INTERVAL)
