import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import os
import plotly.figure_factory as ff

st.set_page_config(page_title="practice!!!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: EDA Dashboard!!!")
st.markdown("<style>div.block-container{padding-top : 2rem;}</style>", unsafe_allow_html=True)

f1 = st.file_uploader(":file_folder: Upload File", type=["txt", "csv", "xlxs", "xls"])
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="latin1")
else:
    os.chdir(r"C:\Users\USER\Documents\PythonProject")
    df = pd.read_csv("Sample - Superstore.csv", encoding="latin1")


col1, col2 = st.columns((2))

df["Order Date"] = pd.to_datetime(df["Order Date"])

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >=date1) & (df["Order Date"]<= date2)].copy()

st.sidebar.header("Choose Filter: ")

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
    filtered_df = df
elif not state and city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and city:
    filtered_df = df[df["State"].isin(state)]
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


category_df = filtered_df.groupby(by = "Category", as_index= False)["Sales"].sum()

with col1:
    st.subheader("Category Wise Sales")
    fig1 = px.bar(category_df, x= "Category", y="Sales", text=["${:,.2f}".format(x) for x in category_df["Sales"]], template="seaborn")
    st.plotly_chart(fig1, use_container_width=True, height=200)

with col2:
    st.subheader("Region Wise Sales")
    fig2 = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig2.update_traces(text= filtered_df["Sales"], textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

with col1:
    with st.expander("View Category Data"):
        st.write(category_df.style.background_gradient(cmap="cividis_r"))
        csv = category_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="txt/csv", 
                           help="Click here to download category data as csv file")

with col2:
    with st.expander("View Region Data"):
        region_df = filtered_df.groupby(by= "Region", as_index = False)["Sales"].sum()
        st.write(region_df.style.background_gradient(cmap="magma_r"))
        csv = region_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="txt/csv",
                           help="Click here to download Region data as csv file")
        
st.subheader("Time Series Analysis")
filtered_df["Month_Year"] = filtered_df["Order Date"].dt.to_period("M")
line_df = pd.DataFrame(filtered_df.groupby(by = filtered_df["Month_Year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig3 = px.line(line_df, x="Month_Year", y="Sales", labels={"Sales" :"Amount"}, height=500, width=1000, template="gridon")
st.plotly_chart(fig3, use_container_width=True) 

with st.expander("View TimeSeries Data"):
    st.write(line_df.T.style.background_gradient(cmap="Oranges_r"))
    csv = line_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data=csv, file_name="TimeSeries.csv", mime="txt/csv", 
                       help="Click here to download data as csv file")

col3, col4 = st.columns((2))
with col3:
    st.subheader("Category wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Category", hole=0.5)
    fig.update_traces(text=filtered_df["Sales"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)


with col4:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Sales"], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Hierarchical Analysis of Region, Category and Sub-Category Using Treemap")
fig = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values="Sales", hover_data=["Sales"],
                 color="Sub-Category")
fig.update_layout(width=800, height= 650)
st.plotly_chart(fig, use_container_width=True)

st.subheader(":ponit right: Month wise Sub-Category Sales Summary")
with st.expander("Sammary Table"):
    sample_df = df[0:50][["Region", "City", "Category", "Sales", "Profit", "Quantity"]]
    Table1 = ff.create_table(sample_df, colorscale="Cividis_r")
    st.plotly_chart(Table1, use_container_width=True)

with st.expander("Month Wise Sub-Category Table"):
    filtered_df["Month"] = filtered_df['Order Date'].dt.month_name()
    Table2 = pd.pivot_table(data=filtered_df, values="Sales", index= ["Sub-Category"], columns="Month")
    st.write(Table2.style.background_gradient(cmap="magma_r"))

fig4 = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
fig4["layout"].update(title= "Relationship between Sales Using Scatter Plot.", titlefont= dict(size =(20)),
                      xaxis = dict(title = "Sales",titlefont=dict(size=(19))), yaxis = dict(title = "Profit", titlefont= dict(size=(19)))) 
st.plotly_chart(fig4, use_container_width=True)
