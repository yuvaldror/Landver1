import streamlit as st
import pandas as pd
import math
from datetime import datetime
import os

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='לנדוור חישוב טיפים',
    page_icon=':coffee:', # This is an emoji shortcode. Could be a URL too.
)
# Create a form to input tips
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

    # Create a new record
    new_record = pd.DataFrame({'תאריך': [shift_date], 'טיפים': [tips_amount]})

    # Save the new record to TipsSaver.csv with utf-8 encoding
    file_path = 'TipsSaver.csv'
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_csv(file_path, encoding='utf-8')
            if set(existing_data.columns) != set(new_record.columns):
                st.error("העמודות בקובץ הקיים לא תואמות לעמודות החדשות.")
            else:
                updated_data = pd.concat([existing_data, new_record], ignore_index=True)
        except pd.errors.EmptyDataError:
            updated_data = new_record
        except pd.errors.ParserError:
            st.error("שגיאה בקריאת הקובץ הקיים. נא לבדוק את תקינות הקובץ.")
            updated_data = new_record
    else:
        updated_data = new_record

    updated_data.to_csv(file_path, index=False, encoding='utf-8')

    # Provide the new record for download
    st.subheader('הורד את רשומת הטיפים החדשה')
    st.download_button(
        label='הורד CSV',
        data=new_record.to_csv(index=False, encoding='utf-8').encode('utf-8'),
        file_name='NewTipRecord.csv',
        mime='text/csv'
    )

    # Display the collected data
    st.subheader('נתוני טיפים שנאספו')
    st.write(updated_data)
