import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')


#Setting page configuration
st.set_page_config(page_title="SuperStore!!!", page_icon=":bar_chart:", layout="wide" )

# Creating the App Title
st.title(":bar_chart: Marusoft SuperStore")
st.markdown("<style>div.block-container{padding-top: 2rem;}</style>", unsafe_allow_html=True)

# Creating the File Uploader Widget
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Documents\PythonProject")
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

# Getting widgets for StartDate and EndDate

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"]) 

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"]<= date2)].copy()

st.sidebar.header("Choose your Filter: ")

region = st.sidebar.multiselect("Choose Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("Choose State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

city = st.sidebar.multiselect("Select City", df3["City"].unique())

if not region and not state and not city:
    filtered_df = df
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not state:
    filtered_df = df[df["City"].isin(city)]
elif region and city:
    filtered_df = df3[(df3["Region"].isin(region)) & (df3["City"].isin(city))]
elif state and city:
    filtered_df = df3[(df3["State"].isin(state)) & (df3["City"].isin(city))]
elif region and state:
    filtered_df = df3[(df3["Region"].isin(region)) & (df3["State"].isin(state))]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[(df3["Region"].isin(region)) & (df3["State"].isin(state)) & (df3["City"].isin(city))]







