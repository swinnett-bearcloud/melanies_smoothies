import streamlit as st
from snowflake.snowpark.functions import col

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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)


if ingredients_list and your_name:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    ingredients_string = ''
    

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_string + """','"""+your_name+"""')"""
    
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

    