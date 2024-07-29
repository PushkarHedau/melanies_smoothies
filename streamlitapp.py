# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

import streamlit as st

option = st.selectbox(
    "What is your favorite food?",
    ("Banana", "Strawberries", "Peaches"),
)

st.write("You favorite fruit is :", option)
from snowflake.snowpark.functions import col

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe
)


if ingredients_list: 
  
    ingredients_string = ''
    for x in ingredients_list:
        ingredients_string += x + ' '
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
                values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)

    if ingredients_string:
        session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
