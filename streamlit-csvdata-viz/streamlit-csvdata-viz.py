import streamlit as st
import pandas as pd
# pip install streamlit pandas

# https://www.zillow.com/research/data/

# Load data from CSV file
df = pd.read_csv('Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv')

# Melt the DataFrame to transform date columns into rows
date_columns = [col for col in df.columns if col not in ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName']]
df_melted = df.melt(
    id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'],
    value_vars=date_columns,
    var_name='Date',
    value_name='Value'
)

# Convert 'Date' to datetime and 'Value' to numeric
df_melted['Date'] = pd.to_datetime(df_melted['Date'])
df_melted['Value'] = pd.to_numeric(df_melted['Value'], errors='coerce')

# Streamlit app
st.set_page_config(layout="wide")
st.title("Housing Market Visualization")
st.write("Select regions and a date range to visualize housing values over time.")

# Multiselect for regions
selected_regions = st.multiselect(
    "Select regions",
    options=df_melted['RegionName'].unique(),
    default=["United States"]
)

# Date inputs for start and end dates
min_date = df_melted['Date'].min().date()
max_date = df_melted['Date'].max().date()

start_date = st.date_input(
    "Select start date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)
end_date = st.date_input(
    "Select end date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Filter data based on selected regions and date range
region_data = df_melted[df_melted['RegionName'].isin(selected_regions)]
filtered_data = region_data[
    (region_data['Date'] >= pd.to_datetime(start_date)) &
    (region_data['Date'] <= pd.to_datetime(end_date))
]

# Pivot the data for line chart (Date as index, regions as columns)
pivot_data = filtered_data.pivot(index='Date', columns='RegionName', values='Value').sort_index().round(2)

# Create line chart
st.subheader("Housing Values Over Time")
st.line_chart(pivot_data)

st.subheader("Filtered Data Preview")
st.dataframe(filtered_data[['Date', 'RegionName', 'Value']].style.format({'Value': '${:,.0f}'}))

