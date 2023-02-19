"""This script is used to send JSON data to the API."""

import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

POST_INVOICE_FASTAPI_URL = os.environ["POST_INVOICE_FASTAPI_URL"]
INPUT_TXT_FILE_NAME = "./client/data_json.txt"

start_id = 1
end_id = 100

current_id = start_id

with open(INPUT_TXT_FILE_NAME) as file:
    for current_id, line in enumerate(file):
        if current_id > end_id:
            break
        if current_id < start_id:
            continue

        json_data = json.loads(line)
        r = requests.post(POST_INVOICE_FASTAPI_URL, json=json_data)
        print(r.json())
