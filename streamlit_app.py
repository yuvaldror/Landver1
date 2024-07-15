import streamlit as st
import pandas as pd
import math


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='לנדוור חישוב טיפים',
    page_icon=':coffee:', # This is an emoji shortcode. Could be a URL too.
)
with st.form(key='tips_form'):
    # Input for the amount of tips collected
    tips_amount = st.number_input('הכנס את סכום הטיפים שנאסף', min_value=0.0, step=0.01)
    
    # Input for the date of the shift
    shift_date = st.date_input('בחר את תאריך המשמרת', value=datetime.today())

    # Submit button
    submit_button = st.form_submit_button(label='שלח')

if submit_button:
    # If the submit button is pressed, save the data
    st.success(f'טיפים בסכום של {tips_amount} ש"ח שנאספו בתאריך {shift_date} נשמרו.')
