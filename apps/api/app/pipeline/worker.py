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

logging.basicConfig(level=logging.INFO)

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
    await worker.run()

if __name__ == "__main__":
    asyncio.run(run_worker())
