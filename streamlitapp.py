# Import python packages
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Select favorite fruit
option = st.selectbox(
    "What is your favorite fruit?",
    ("Banana", "Strawberries", "Peaches"),
)

st.write("Your favorite fruit is:", option)

# Connect to Snowflake
cnx = st.experimental_connection("snowflake")
session = cnx.session

# Fetch fruit options from Snowflake
query = """
SELECT FRUIT_NAME 
FROM smoothies.public.fruit_options
"""
fruit_options_df = session.sql(query).to_pandas()

# Display multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', fruit_options_df['FRUIT_NAME'].tolist()
)

if ingredients_list: 
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients)
        VALUES ('{ingredients_string}')
    """

    if ingredients_string:
        session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

# Fetch data from Fruityvice API and display it
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())
fv_df = pd.json_normalize(fruityvice_response.json())
st.dataframe(data=fv_df, use_container_width=True)
