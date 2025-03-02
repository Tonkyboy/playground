import streamlit as st
import pandas as pd
# pip install streamlit pandas

# Load data from CSV file
df = pd.read_csv('housing_data.csv')

df['Year'] = df['Year'].astype(int)

st.title("Housing Market Visualization")
st.write("Select a metric to visualize and adjust the year range.")

# Create a dropdown menu for column selection
available_columns = [col for col in df.columns if col != 'Year']
selected_column = st.selectbox(
    "Select metric to display",
    available_columns,
    format_func=lambda x: x.replace('_', ' ')
)

# Slider for filtering years
year_min = int(df['Year'].min())
year_max = int(df['Year'].max())
selected_years = st.slider(
    "Select year range", 
    year_min, 
    year_max, 
    (year_min, year_max)
)

# Filter data based on selected years
filtered_data = df[(df['Year'] >= selected_years[0]) & 
                   (df['Year'] <= selected_years[1])]

# Create visualization with the selected column
st.subheader(f"{selected_column.replace('_', ' ')} Over Time")
st.line_chart(filtered_data.set_index('Year')[selected_column])

# Show filtered data preview
st.subheader("Filtered Data Preview")
st.dataframe(filtered_data.style.format({
    'Average_Home_Price': '${:,.0f}',
    'Median_Income': '${:,.0f}',
    'Interest_Rate': '{:.1f}%'
}))

# streamlit run dataviz/dataviz-streamlit.py
