import polars as pl
import json
from confluent_kafka import Producer
import logging
import uuid
from app.config import settings

logger = logging.getLogger(__name__)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f'Message delivery failed: {err}')
    else:
        logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')

class DataProcessor:
    def __init__(self):
        self.producer = Producer({'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS})
        self.topic = settings.KAFKA_TOPIC

    def process_and_publish(self, local_file_path: str, dataset_type: str):
        """
        Reads a local file (downloaded from S3) using Polars, 
        cleans it, and publishes individual events to Kafka.
        """
        try:
            # Polars is extremely fast at processing raw files
            if local_file_path.endswith('.csv'):
                df = pl.read_csv(local_file_path)
            elif local_file_path.endswith('.json'):
                df = pl.read_json(local_file_path)
            else:
                raise ValueError("Unsupported file type")

            # Example transformation: drop nulls in critical columns
            if 'id' in df.columns:
                df = df.drop_nulls(subset=['id'])

            # Convert to list of dicts for publishing
            records = df.to_dicts()
            logger.info(f"Polars processed {len(records)} records from {local_file_path}")

            batch_id = str(uuid.uuid4())
            
            for record in records:
                event = {
                    "batch_id": batch_id,
                    "dataset_type": dataset_type,
                    "record": record
                }
                self.producer.produce(
                    self.topic, 
                    value=json.dumps(event).encode('utf-8'),
                    callback=delivery_report
                )
            
            self.producer.flush()
            logger.info(f"Successfully published {len(records)} events to Kafka topic {self.topic}")
            return batch_id

        except Exception as e:
            logger.error(f"Failed to process data with Polars: {e}")
            raise
