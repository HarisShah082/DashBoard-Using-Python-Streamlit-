import pandas as pd
import plotly.express as px
import streamlit as st


#__________________ Start Web Page ________________________


st.set_page_config(
    page_title='Sales Dashboard',
    page_icon=':bar_chart:',
    layout='wide',
)

#_________________ Read Excel File _________________________


df = pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)


#___________________ Side Bar_________________________

st.sidebar.header('Please Filter Here: ')


branch = st.sidebar.multiselect(
    "select the Brach: ",
    options=df["Branch"].unique(),
    default=df["Branch"].unique(),
)



city = st.sidebar.multiselect(
    "select the City: ",
    options=df["City"].unique(),
    default=df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
    "select the Customer Type: ",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)


gender = st.sidebar.multiselect(
    "select the Gender: ",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
)


Payment = st.sidebar.multiselect(
    "select the Payment: ",
    options=df["Payment"].unique(),
    default=df["Payment"].unique(),
)


df_selection = df.query(
    "Branch == @branch  &  City == @city  &  Customer_type == @customer_type  &  Gender == @gender  &  Payment == @Payment"
)



#_____________________data Frame________________________________



st.title("Excel Data")
st.markdown("---")


st.dataframe(df_selection)


#_______________________ Sales Dashboard ____________________________


st.title(":bar_chart: Sales Dashboard")
st.markdown("##")



total_sales = int(df_selection["Total"].sum())  # TOTAL SALES

average_rating = round(df_selection["Rating"].mean(),1)     # Average Rating by 1 Decimal Place

star_rating = int(round(average_rating,0)) * ":star:"       # Using Star Emoji 

average_sales_by_transaction = round(df_selection["Total"].mean(),2)    # Average Sales 


#__________________________ COLUMN DIVISION _________________________


left_col, middle_col, right_col = st.columns(3)

with left_col:                                              # For Left Column
    st.subheader("Total Sales: ")
    st.subheader(f"PKR {total_sales:,}")

with middle_col:                                            # For Middle Column
    st.subheader("Average Rating: ")
    st.subheader(f"{average_rating}{star_rating}")

with right_col:                                             # For Right Column
    st.subheader("Average Sales By Transactions")
    st.subheader(f"{average_sales_by_transaction}")

st.markdown("---")



#____________________________ Bar Chart ___________________________

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index, 
    orientation="h",
    title="<b> Sales by Product Line </b>",
    color_discrete_sequence=["#0083B8"] ,
    template="plotly_white",

)

st.plotly_chart(fig_product_sales)