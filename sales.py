import streamlit as st
import plotly.express as px
import plotly.subplots as sp
import pandas as pd

from sales_con import *



st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart", layout="wide")
st.title(":bar_chart: Sales Business Analysis Dashboard")
st.markdown("<style>div.block-container{padding-top: 2rem;}</style>", unsafe_allow_html=True)

result = view_all_data()

df = pd.DataFrame(result, columns=["index", "Date", "Year", "Month", "Custome Age", "Customer Gender", "Country", "State", "Product Category", "Sub Category", "Quantity", "Unit Cost", "Unit Price", "Cost", "Revenue", "Column1"])
st.dataframe(df)

st.sidebar.header("Filter Dataset")

country = st.sidebar.multiselect(
    label= "Select Country",
    options=df["Country"].unique(),
    default=df["Country"].unique(),
)
state = st.sidebar.multiselect(
    label= "Select State",
    options=df["State"].unique(),
    default=df["State"].unique(),
)