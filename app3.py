import streamlit as st
import plotly.express as px
import os
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

st.set_page_config(page_title="ADESTORE", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: ADESOLA ENTERPRISES EDA DASHBOARD")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload file", type=["csv", "txt", "xlsx", "xls"])

if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv("filename.csv", encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Documents\PythonProject")
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")

df["Order Date"] = pd.to_datetime(df["Order Date"])

col1, col2 = st.columns((2))
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("Start Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header(":file_folder: Choose Filter")

region = st.sidebar.multiselect("Select Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

state = st.sidebar.multiselect("Select State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

city = st.sidebar.multiselect("Select City", df3["City"].unique())

if not region and not state and not city:
    filtered_df = df.copy()
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[(df3["State"].isin(state)) & (df3["City"].isin(city))]
elif region and city:
    filtered_df = df3[(df3["Region"].isin(region)) & (df3["City"].isin(city))]
elif state and region:
    filtered_df = df3[(df3["State"].isin(state)) & (df3["Region"].isin(region))]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[(df3["Region"].isin(region)) & (df3["State"].isin(state)) & (df3["City"].isin(city))]

category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Sales"].sum()

cl1, cl2 = st.columns((2))

with cl1:
        st.subheader("Category wise Sales")
        fig = px.bar(category_df, x="Category", y="Sales", text = ["${:,.2f}".format(x) for x in category_df["Sales"]], template="seaborn")
        st.plotly_chart(fig, use_container_width=True, height = 200)

with cl2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, names="Region", values="Sales", hole=0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)

cl3, cl4 = st.columns((2))

region_df = filtered_df.groupby(by = ["Region"], as_index = False)["Sales"].sum()

with cl3:
    with st.expander("View Category_Data"):
        st.write(category_df.style.background_gradient(cmap = "Blues"))
        csv = category_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Category.CSV", mime="txt/csv", help= "Click here to download the data")

with cl4:
    with st.expander("View Region_Data"):
        st.write(region_df.style.background_gradient(cmap = "Oranges_r"))
        csv = region_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Region.CSV", mime="txt/csv", help= "Click here to download the data")

st.subheader("Time Series Analysis")
filtered_df["Monthly_Year"] = (filtered_df["Order Date"].dt.to_period("M"))
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["Monthly_Year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig = px.line(linechart, x="Monthly_Year", y="Sales", labels= {"x" : "Month", "Y" : "Amount"}, height=500, width=1500, template="gridon")
st.plotly_chart(fig, use_container_width=True)

with st.expander("TimeSeries Analysis"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv, file_name="TimeSeries.CSV", mime="txt/csv", help="Click here to download the data as csv file")


st.subheader("Hierarchical View of Sales Using Treemap")
fig = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values= "Sales", hover_data=["Sales"], color="Sub-Category")
fig.update_layout(width=800, height=650)
st.plotly_chart(fig, use_container_width=True)

