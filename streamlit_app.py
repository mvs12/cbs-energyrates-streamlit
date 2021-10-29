import streamlit as st
import pandas as pd
import cbsodata
from streamlit_echarts import st_echarts
import json


# Retrieve data from CBS
# Average energy prices for consumers 84672ENG
@st.cache
def retreive_data_cbs():
    df = pd.DataFrame(cbsodata.get_data('84672ENG'))
    return df


df = retreive_data_cbs()

# Filter data with values including VAT and excluding Full Years
df = df[df['VAT'] == 'Including VAT']
df = df[(df['Period'] != '2018') &
        (df['Period'] != '2019') &
        (df['Period'] != '2020') &
        (df['Period'] != '2021')]

# Calculate prices
df['Gas EUR per m3'] = df['VariableDeliveryRate_3'] + df['ODETaxEnvironmentalTaxesAct_4'] + df['EnergyTax_5']
df['Electricity EUR per kWh'] = df['VariableDeliveryRate_8'] + df['ODETaxEnvironmentalTaxesAct_9'] + df['EnergyTax_10']

# Create app layout
sidebar_title = st.sidebar.subheader("Follow energy prices for consumers in the Netherlands")

sidebar_text = st.sidebar.write(('''
Follow Dutch energy prices from 2018 until 2021, monthly published by CBS. Prices are variable rates, including VAT
and including surcharge for renewable energy. Prices are excluded Transport Rates and Fixed Rates.
 '''))

# Create year filter
df['Period'] = pd.to_datetime(df['Period'], format='%Y %B')
years = df['Period'].dt.year.unique().tolist()
years_filter = st.sidebar.multiselect("Select year", years, default=[2018, 2019, 2020, 2021])

sidebar_text = st.sidebar.write(('''
Sourcecode: [Github](https://github.com/mvs12/cbs-energyrates-streamlit)
 '''))

# Create callbacks/filter data on selection
filtered_df = df[df['Period'].dt.year.isin(years_filter)]

# Create Dimensions
periods = filtered_df['Period'].dt.strftime('%Y-%m-%d').tolist()
# df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Create Measurements
gas = filtered_df['Gas EUR per m3'].tolist()
electricity = filtered_df['Electricity EUR per kWh'].tolist()

# Create line chart with theme
st.title("Average variable energy prices for consumers in The Netherlands")

# Open theme
with open('theme.json') as file:
    theme = json.load(file)

options = {
    "xAxis": {
        "type": "category",
        "data": periods,
        "name": "Year",
    },
    "yAxis": {"type": "value", "name": "Prices in EUR"},
    "series": [
        {"data": gas, "type": "line", "name": "Gas per m3" },
        {"data": electricity, "type": "line", "name": "Electricity per kWh"}
    ],
    "legend": {"display": "true"}
}

st_echarts(options=options, height="400px", theme=theme,)

st.write("Source: [CBS Open data StatLine 'Average energy prices for consumers 2018-2021']"
         "(https://opendata.cbs.nl/statline/portal.html?_la=en&_catalog=CBS&tableId=84672ENG&_theme=378)")
