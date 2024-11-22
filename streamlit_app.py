import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)
your_name = st.text_input(label="Enter Your Name", value="", max_chars=None, key=None, help=None, placeholder=None, label_visibility="visible")

#option = st.selectbox (
#    'What is your favorite fruit?',
#    ('Banana','Strawberries', 'Peaches')
# )

# st.write('Your favorite fruit is:', option)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
# Convert the Snowpark Datfrom to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)


if ingredients_list and your_name:    
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '

        search_on=pd_def.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        # st.text(smoothiefroot_response.json())
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+your_name+"""')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



    
