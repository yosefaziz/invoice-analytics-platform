"""Transforms CSV file to JSON data"""

import pandas as pd
import numpy as np


INPUT_CSV_FILE_NAME = "./client/data.csv"
OUTPUT_TXT_FILE_NAME = "./client/data_json.txt"

def csv_to_json():
    df = pd.read_csv(INPUT_CSV_FILE_NAME, dtype={'CustomerID': 'Int64'}, encoding='ISO-8859-1')
    df["json"] = df.to_json(orient='records', lines=True).splitlines()
    np.savetxt(OUTPUT_TXT_FILE_NAME, df["json"].values, fmt="%s")

csv_to_json()
