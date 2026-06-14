import sqlite3
import pandas as pd
import streamlit as st

conn = sqlite3.connect("tasks.db")

df = pd.read_sql_query(
    "SELECT * FROM tasks",
    conn
)

st.title("Task Dashboard")

st.dataframe(df)

pending = len(df[df["status"] == "Pending"])
completed = len(df[df["status"] == "Completed"])

st.metric("Pending Tasks", pending)
st.metric("Completed Tasks", completed)

conn.close()