import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="SuperStore", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Adesolare Store")
st.markdown("<style>dev.block-container{padding-top: 2rem;}", unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload file", type = (["csv", "txt", "xlsx", "xls"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Documents\PythonProject")
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

col1, col2 = st.columns((2))

df['Order Date'] = pd.to_datetime(df["Order Date"])

startDate = pd.to_datetime(df['Order Date']).min()
endDate = pd.to_datetime(df['Order Date']).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header(":file: Choose filter")
region = st.sidebar.multiselect("Pick Region", df["Region"].unique())
if not region:
    df1 = df.copy()
else:
    df1 = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("Select State", df1["State"].unique())
if not state:
    df2 = df1.copy()
else:
    df2 = df1[df["State"].isin(state)]

city = st.sidebar.multiselect("Select City", df2['City'].unique())

if not region and not state and not city:
    filtered_df = df
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif region and city:
    filtered_df = df2[(df["Region"].isin(region)) & (df2["City"].isin(city))]
elif state and city:
    filtered_df = df2[(df["State"].isin(region)) & (df2["City"].isin(city))]
elif region and state:
    filtered_df = df2[(df["Region"].isin(region)) & (df2["State"].isin(state))]
elif city:
    filtered_df = df2[df2["City"].isin(city)]
else:
    filtered_df = df2[(df2["Region"].isin(region)) & (df2["State"].isin(state)) & (df2["City"].isin(city))]

category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

cl1, cl2, = st.columns((2))
with cl1:
    st.subheader("Category wise sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text=["${:,.2f}".format(x) for x in category_df["Sales"]], template = "seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with cl2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text = filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl3, cl4 = st.columns((2))

with cl3:
    with st.expander("View Category_Data"):
        st.write(category_df.style.background_gradient(cmap = "Greens"))
        csv = category_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Category.CSV", mime="txt/csv", help="Click here to download the data as csv file" )

with cl4:
    with st.expander("View Region_Data"):
        region_df = filtered_df.groupby(by = ["Region"], as_index = False)["Sales"].sum()
        st.write(region_df.style.background_gradient(cmap="Blues"))
        csv = region_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Region.CSV", mime="txt/csv", help="Click here to download the data as csv file" )


filtered_df["Month_Year"] = filtered_df["Order Date"].dt.to_period("M")

linechart_df = pd.DataFrame(filtered_df.groupby(filtered_df["Month_Year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig = px.line(linechart_df, x = "Month_Year", y= "Sales", labels = {"Sales": "Amount"}, height = 500, width= 1000, 
               template = "gridon" )
st.plotly_chart(fig, use_container_width=True)