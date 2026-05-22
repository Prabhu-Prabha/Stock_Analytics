import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Page config
st.set_page_config(page_title="Stock Metrics Dashboard", layout="wide")

st.title("Stock Analysis 8 Metrics Dashboard")

# MySQL engine
engine = create_engine(
    "mysql+mysqlconnector://root:@localhost:3306/project_ii"
)

# Get table names
query = "SHOW TABLES"
tables = pd.read_sql(query, engine)

for table in tables.iloc[:, 0]:
    st.subheader(f"{table.upper()}")
    
    df = pd.read_sql(f"SELECT * FROM {table}", engine)
    
    st.dataframe(df, use_container_width=True)