import pandas as pd
import streamlit as st
import matplotlib.pylot as plt
import plotly.express as px
import numpy as np
import seaborn as sb

st.image('gambar.jpg')

st.date_input("")

st.title("""Mini Project Afiq & Danial!!""")

df = pd.read_csv("clean_data_e-commerce.csv")

st.subheader("Raw Data")
st.write(df)

