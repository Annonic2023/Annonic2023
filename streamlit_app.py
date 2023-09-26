# Streamlit live coding script
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from urllib.request import urlopen
import json
from copy import deepcopy


# First some MPG Data Exploration
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df


mpg_df_raw = load_data(path="./data/mpg.csv")
mpg_df = deepcopy(mpg_df_raw)

# Add title and header
st.title("Introduction to Streamlit")
st.header("MPG Data Exploration")

# Widgets: checkbox (you can replace st.xx with st.sidebar.xx)
if st.checkbox("Show Dataframe"):
    st.subheader("This is my dataset:")
    st.dataframe(data=mpg_df)
    # st.table(data=mpg_df)

# Setting up columns
left_column, middle_column, right_column = st.columns([3, 1, 1])

# Widgets: selectbox
years = ["All"]+sorted(pd.unique(mpg_df['year']))
year = left_column.selectbox("Choose a Year", years)

# Widgets: radio buttons
show_means = middle_column.radio(
    label='Show Class Means', options=['Yes', 'No'])

#plot_types = ["Matplotlib", "Plotly"]
#plot_type = right_column.radio("Choose Plot Type", plot_types)

# Flow control and plotting
if year == "All":
    reduced_df = mpg_df
else:
    reduced_df = mpg_df[mpg_df["year"] == year]

means = reduced_df.groupby('class').mean(numeric_only=True)

# In Matplotlib
m_fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(reduced_df['displ'], reduced_df['hwy'], alpha=0.7)

if show_means == "Yes":
    ax.scatter(means['displ'], means['hwy'], alpha=0.7, color="red")

ax.set_title("Engine Size vs. Highway Fuel Mileage")
ax.set_xlabel('Displacement (Liters)')
ax.set_ylabel('MPG')
st.pyplot(m_fig)

# We can write stuff
url = "https://archive.ics.uci.edu/ml/datasets/auto+mpg"
st.write("Data Source:", url)
