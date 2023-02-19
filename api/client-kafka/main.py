"""FastAPI client to produce messages to Kafka"""

import json
import os
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from datetime import datetime
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv


load_dotenv()

KAFKA_BOOTSTRAP_SERVER = os.environ["KAFKA_BOOTSTRAP_SERVER"]
KAFKA_INGESTION_TOPIC = os.environ["KAFKA_INGESTION_TOPIC"]

class InvoiceItem(BaseModel):
    InvoiceNo: int
    StockCode: str
    Description: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: str
    Country: str

    @validator("InvoiceDate")
    def validate_date(cls, v: str) -> str:
        """Validate the date format is DD/MM/YYYY HH:MM and convert to ISO format
        
        Args:
            cls: The class
            v: The date string to validate
        
        Returns:
            The date in ISO format"""
        try:
            dt = datetime.strptime(v, "%d/%m/%Y %H:%M")
            return dt.isoformat()
        except ValueError:
            raise ValueError("Unexpected data format, should be DD/MM/YYYY HH:MM")


def create_topic(server: str, topic_name: str) -> None:
    """Create a topic in Kafka
    
    Args:
        topic_name: The name of the topic to create
        server: The Kafka server to connect to"""
    admin_client = KafkaAdminClient(bootstrap_servers=server)
    
    # Check if the topic already exists
    topic_metadata = admin_client.list_topics()
    print(topic_metadata)
    if topic_name in topic_metadata:
        print(f"Topic '{topic_name}' already exists. Skipping topic creation.")
    else:
        new_topic = NewTopic(
                        name=topic_name,
                        num_partitions=1,
                        replication_factor=1
                    )
        admin_client.create_topics([new_topic])
        print(f"Topic '{topic_name}' created.")


async def produce_kafka_str(msg: str) -> None:
    """Produce a string to Kafka
    
    Args: 
        msg: The message to produce"""
    producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVER, acks=1)
    producer.send(KAFKA_INGESTION_TOPIC, bytes(msg, "utf-8"))
    producer.flush()


app = FastAPI()
create_topic(KAFKA_BOOTSTRAP_SERVER, KAFKA_INGESTION_TOPIC)

@app.get("/")
async def root():
    return {"message": "You won't GET anything from me. Check the ReadMe :)"}


@app.post("/invoiceitem")
async def post_invoice_item(item: InvoiceItem):
    try:
        item_json = jsonable_encoder(item)
        item_json_str = json.dumps(item_json)
        await produce_kafka_str(item_json_str)
        return JSONResponse(content=item_json, status_code=201)

    except ValueError as e:
        print(e)
        return JSONResponse(content=jsonable_encoder(item), status_code=400)
