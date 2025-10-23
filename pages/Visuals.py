# This creates the page for displaying data visualizations.
# It should read data from both 'data.csv' and 'data.json' to create graphs.

import streamlit as st
import pandas as pd
import json # The 'json' module is needed to work with JSON files.
import os   # The 'os' module helps with file system operations.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visualizations",
    page_icon="📈",
)

# PAGE TITLE AND INFORMATION
st.title("Data Visualizations 📈")
st.write("This page displays graphs based on the collected data.")


# DATA LOADING
# A crucial step is to load the data from the files.
# It's important to add error handling to prevent the app from crashing if a file is empty or missing.

st.divider()
st.header("Load Data")

# TO DO:
# 1. Load the data from 'data.csv' into a pandas DataFrame.
#    - Use a 'try-except' block or 'os.path.exists' to handle cases where the file doesn't exist.
# 2. Load the data from 'data.json' into a Python dictionary.
#    - Use a 'try-except' block here as well.

if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    csv_data = pd.read_csv("data.csv")
    st.success("Loaded data.csv successfully!")  # NEW
    st.dataframe(csv_data.head())  # NEW
else:
    st.warning("data.csv not found or empty.")
    csv_data = pd.DataFrame(columns=["Category", "Value"])

# Load JSON file safely
if os.path.exists("data.json") and os.path.getsize("data.json") > 0:
    with open("data.json", "r") as f:
        json_data = json.load(f)
    st.success("Loaded data.json successfully!")  # NEW
    st.json(json_data)  # NEW
else:
    st.warning("data.json not found or empty.")
    json_data = {"data": []}

# Initialize Session State
if "selected_category" not in st.session_state:
    st.session_state.selected_category = ""
if "num_points" not in st.session_state:
    st.session_state.num_points = 3

# GRAPH CREATION
# The lab requires you to create 3 graphs: one static and two dynamic.
# You must use both the CSV and JSON data sources at least once.

st.divider()
st.header("Graphs")

# GRAPH 1: STATIC GRAPH
st.subheader("Graph 1: Static") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create a static graph (e.g., bar chart, line chart) using st.bar_chart() or st.line_chart().
# - Use data from either the CSV or JSON file.
# - Write a description explaining what the graph shows.
if not csv_data.empty:
    counts = csv_data["Category"].value_counts()
    st.bar_chart(counts)
    st.write("This static bar chart shows how many times each category appears in your CSV data.")
else:
    st.warning("No CSV data available for this graph.")

# GRAPH 2: DYNAMIC GRAPH
st.subheader("Graph 2: Dynamic") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TODO:
# - Create a dynamic graph that changes based on user input.
# - Use at least one interactive widget (e.g., st.slider, st.selectbox, st.multiselect).
# - Use Streamlit's Session State (st.session_state) to manage the interaction.
# - Add a '#NEW' comment next to at least 3 new Streamlit functions you use in this lab.
# - Write a description explaining the graph and how to interact with it.
if not csv_data.empty:
    selected_category = st.selectbox("Select a Category:", csv_data["Category"].unique())  # NEW
    st.session_state.selected_category = selected_category  # NEW

    filtered = csv_data[csv_data["Category"] == selected_category]

    if not filtered.empty:
        st.line_chart(filtered["Value"])  # NEW
        st.write(f"This dynamic line chart shows the values for the selected category: **{selected_category}**.")
    else:
        st.warning("No data available for that category.")
else:
    st.warning("No CSV data available for this graph.")

# GRAPH 3: DYNAMIC GRAPH
st.subheader("Graph 3: Dynamic") # CHANGE THIS TO THE TITLE OF YOUR GRAPH
# TO DO:
# - Create another dynamic graph.
# - If you used CSV data for Graph 1 & 2, you MUST use JSON data here (or vice-versa).
# - This graph must also be interactive and use Session State.
# - Remember to add a description and use '#NEW' comments.
if "data" in json_data and json_data["data"]:
    json_df = pd.DataFrame(json_data["data"])
    json_df["value"] = pd.to_numeric(json_df["value"], errors="coerce")

    num_points = st.slider("Select number of data points:", 1, len(json_df), st.session_state.num_points)  # NEW
    st.session_state.num_points = num_points

    st.line_chart(json_df["value"].head(num_points))
    st.write("This dynamic graph displays values from your JSON file. Use the slider to change how many points are shown.")
else:
    st.warning("No JSON data available for this graph.")
    