import streamlit as st
import pandas as pd
import math
from datetime import datetime
import os

# Set the page configuration
st.set_page_config(
    page_title='לנדוור חישוב טיפים',
    page_icon=':coffee:'
)

# Function to round down values
def round_down(value, decimals=0):
    factor = 10 ** decimals
    return math.floor(value * factor) / factor

# Set the title of the app
st.title('אפליקציית ניהול טיפים למלצריות')

# Input for the number of waitresses
num_waitresses = st.number_input('הכנס את מספר המלצריות במשמרת', min_value=1, step=1)

# Create a list to store the details of each waitress
waitresses = []

for i in range(num_waitresses):
    with st.expander(f'מלצרית {i+1}'):
        name = st.text_input(f'הכנס את שם המלצרית {i+1}', key=f'name_{i}')
        hours_worked = st.number_input(f'הכנס את מספר השעות שהמלצרית {i+1} עבדה', min_value=0.0, step=0.1, key=f'hours_{i}')
        waitresses.append({'שם': name, 'שעות עבודה': hours_worked})

# Input for the total tips collected
total_tips = st.number_input('הכנס את סכום הטיפים הכולל שנאסף במשמרת', min_value=0.0, step=0.01)

if st.button('חשב'):
    # Calculate total hours worked
    total_hours = sum(waitress['שעות עבודה'] for waitress in waitresses)

    # Calculate money made per hour
    money_per_hour = (total_tips * 0.97) / total_hours if total_hours > 0 else 0
    money_per_hour = round_down(money_per_hour, 2)

    # Calculate הפרשה לבר
    bar_deduction = total_tips * 0.03
    bar_deduction = round_down(bar_deduction, 2)

    # Display results
    st.success(f'סכום כסף לשעה: {money_per_hour} ש"ח')
    st.success(f'הפרשה לבר: {bar_deduction} ש"ח')

    # Create a dataframe to store the results
    results = []
    for waitress in waitresses:
        total_made = waitress['שעות עבודה'] * money_per_hour
        service_fee = total_made * 0.2
        net_income = total_made * 0.8

        results.append({
            'שם': waitress['שם'],
            'שעות עבודה': waitress['שעות עבודה'],
            'סכום כולל': round_down(total_made, 2),
            'דמי שירות': round_down(service_fee, 2),
            'נטו': round_down(net_income, 2)
        })

    results_df = pd.DataFrame(results)

    # Save the results to TipsSaver.csv with windows-1255 encoding
    file_path = 'TipsSaver.csv'
    if os.path.exists(file_path):
        try:
            existing_data = pd.read_csv(file_path, encoding='windows-1255')
            if set(existing_data.columns) != set(results_df.columns):
                st.error("העמודות בקובץ הקיים לא תואמות לעמודות החדשות.")
            else:
                updated_data = pd.concat([existing_data, results_df], ignore_index=True)
        except pd.errors.EmptyDataError:
            updated_data = results_df
        except pd.errors.ParserError:
            st.error("שגיאה בקריאת הקובץ הקיים. נא לבדוק את תקינות הקובץ.")
            updated_data = results_df
    else:
        updated_data = results_df

    updated_data.to_csv(file_path, index=False, encoding='windows-1255')

    # Provide the new record for download
    st.subheader('הורד את רשומת הטיפים החדשה')
    st.download_button(
        label='הורד CSV',
        data=results_df.to_csv(index=False, encoding='windows-1255').encode('windows-1255'),
        file_name='NewTipRecord.csv',
        mime='text/csv'
    )

    # Display the collected data
    st.subheader('נתוני טיפים שנאספו')
    st.write(updated_data)
