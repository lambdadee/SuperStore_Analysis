import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import os

st.set_page_config(page_title="Financial", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Financial EDA Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>",  unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload file", type= ["txt", "csv", "xlsx", "xls"])

if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Documents\PythonProject")
    df = pd.read_csv("Financials.csv", encoding="latin1")

df["Date"] = pd.to_datetime(df["Date"])

col1, col2 = st.columns((2))

startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] <= date1) & (df["Date"] >= date2)].copy()


st.sidebar.header("Choose Filter: ")

country = st.sidebar.multiselect("Select Country", df["Country"].unique())

if not country:
    df2 = df.copy()
else:
    df2 = df[df["Country"].isin(country)]

segment = st.sidebar.multiselect("Select Segment", df2["Segment"].unique())

if not country and not segment:
    filtered_df = df
elif country and segment:
    filtered_df = df2[(df2["Country"].isin(country)) & (df2["Segment"].isin(segment))]
elif segment:
    filtered_df = df2[(df2["Segment"].isin(segment))]

else:
    filtered_df = df2[(df2["Country"].isin(country)) & (df2["Segment"].isin(segment))]


