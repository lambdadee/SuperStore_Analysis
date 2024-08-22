import streamlit as st
import pandas as pd
import plotly.express as xp
import warnings
warnings.filterwarnings("ignore")
import os

st.set_page_config(page_title="Sales Analysis", page_icon=":bar_chart:", layout="wide")
st.title(":bar_chart: Sales Analysis Dashboard")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

f1 = st.file_uploader("Upload File", type=["txt", "csv", "xlsx", "xls"])
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Downloads\SalesForCourse")
    df = pd.read_csv("SalesForCourse_quizz_table.csv", encoding="latin1")

st.markdown('View Dataset')
st.write(df.head())
st.write(df.info())
st.write(df.describe())

df["Date"] = pd.to_datetime(df["Date"])

col1, col2 = st.columns((2))
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

st.sidebar.header("Choose Filter")

country = st.sidebar.multiselect("Select Country", df["Country"].unique())

if not country:
    df2 = df.copy()
else:
    df2 = df[df["Country"].isin(country)]

state = st.sidebar.multiselect("Select State", df2["State"].unique())

if not country and not state:
    filtered_df = df
elif country and state:
    filtered_df = df2[(df2["Country"].isin(country)) & (df2["State"].isin(state))]
else:
    filtered_df = df2[df2["State"].isin(state)]

