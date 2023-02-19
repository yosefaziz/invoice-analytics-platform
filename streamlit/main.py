"""An app that shows the invoices of a customer"""

import streamlit as st
from pandas import DataFrame
import pymongo
import os
from dotenv import load_dotenv


load_dotenv()

MONGO_DB_CLIENT = os.getenv("MONGO_DB_CLIENT")
MONGO_DB_USER = os.getenv("MONGO_DB_USER")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

myclient = pymongo.MongoClient(MONGO_DB_CLIENT, username=MONGO_DB_USER, password=MONGO_DB_PASSWORD)
mydb = myclient["document_streaming"]
mycol = mydb["invoices"]

# Below the fist chart add a input field for the invoice number
cust_id = st.sidebar.text_input(f"CustomerID:")

# if enter has been used on the input field 
if cust_id:
    # find all documents with the given customer id
    myquery = {"CustomerID": cust_id}
    mydoc = mycol.find(myquery , { "_id": 0, "StockCode": 0, "Description": 0, "Quantity": 0, "Country": 0, "UnitPrice": 0})

    # create dataframe from resulting documents and drop_duplicates
    df = DataFrame(mydoc)
    df.drop_duplicates(subset ="InvoiceNo", keep = 'first', inplace = True)

    # Add the table with a headline
    st.header("Output Customer Invoices")
    table2 = st.dataframe(data=df) 
    
# Below the fist chart add a input field for the invoice number
inv_no = st.sidebar.text_input("InvoiceNo:")

# if enter has been used on the input field 
if inv_no:
    myquery = {"InvoiceNo": inv_no}
    mydoc = mycol.find( myquery, { "_id": 0, "InvoiceDate": 0, "Country": 0, "CustomerID": 0 })
    df = DataFrame(mydoc)

    # reindex it so that the columns are order lexicographically 
    reindexed = df.reindex(sorted(df.columns), axis=1)

    # Add the table with a headline
    st.header("Output by Invoice ID")
    table2 = st.dataframe(data=reindexed)
