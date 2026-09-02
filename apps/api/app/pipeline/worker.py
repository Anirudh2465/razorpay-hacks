import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
import logging

from app.pipeline.workflows import (
    ReconciliationWorkflow, 
    ingest_dataset_activity, 
    run_matching_engine_activity, 
    update_financial_graph_activity
)
from app.config import settings
from confluent_kafka import Consumer, KafkaError
import json

logging.basicConfig(level=logging.INFO)

async def kafka_consumer_loop(temporal_client):
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'reconciliation-group',
        'auto.offset.reset': 'earliest'
    })
    
    consumer.subscribe([settings.KAFKA_TOPIC])
    logging.info(f"Kafka consumer listening on topic: {settings.KAFKA_TOPIC}")
    
    try:
        while True:
            # We use a non-blocking poll by leveraging asyncio.sleep to yield control
            msg = consumer.poll(1.0)
            if msg is None:
                await asyncio.sleep(0.1)
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(f"Kafka Error: {msg.error()}")
                    continue
            
            # Process message
            event = json.loads(msg.value().decode('utf-8'))
            logging.info(f"Received Kafka event for batch {event.get('batch_id')}")
            
            # Start a temporal workflow for this batch asynchronously
            # This demonstrates triggering a workflow based on a Kafka event
            try:
                await temporal_client.start_workflow(
                    ReconciliationWorkflow.run,
                    "s3://finance-data/dataset.csv", # Mocked path based on event
                    id=f"reconciliation-workflow-{event.get('batch_id')}",
                    task_queue="reconciliation-queue"
                )
            except Exception as e:
                logging.error(f"Failed to start workflow: {e}")
                
    except Exception as e:
        logging.error(f"Kafka consumer loop error: {e}")
    finally:
        consumer.close()

async def run_worker():
    logging.info(f"Connecting to Temporal server at {settings.TEMPORAL_URL}")
    client = await Client.connect(settings.TEMPORAL_URL)
    
    worker = Worker(
        client,
        task_queue="reconciliation-queue",
        workflows=[ReconciliationWorkflow],
        activities=[
            ingest_dataset_activity,
            run_matching_engine_activity,
            update_financial_graph_activity
        ],
    )
    
    logging.info("Starting Temporal Worker...")
    
    # Run the Temporal worker and Kafka consumer concurrently
    await asyncio.gather(
        worker.run(),
        kafka_consumer_loop(client)
    )

if __name__ == "__main__":
    asyncio.run(run_worker())
