import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
import pytz
import os

# Set the page configuration
st.set_page_config(
    page_title='לנדוור חישוב טיפים',
    page_icon=':coffee:'
)

# Custom CSS to set RTL direction
st.markdown(
    """
    <style>
    .css-1aumxhk {text-align: right; direction: rtl;}
    .css-16idsys {text-align: right; direction: rtl;}
    .stDataFrame {direction: rtl;}
    </style>
    """,
    unsafe_allow_html=True
)

# Function to round down values without decimal places
def round_down(value):
    return math.floor(value)

# Function to determine the correct date and shift type based on the current date and time in Israel timezone
def get_shift_date_and_type():
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now = datetime.now(israel_tz)
    day_of_week = now.weekday()
    hour = now.hour

    # Monday to Thursday: Show the previous day
    if day_of_week in range(0, 4):
        shift_date = now - timedelta(days=1)
        shift_type = ""
    # Friday: Before 6 AM show the previous day, after 6 AM add "משמרת בוקר"
    elif day_of_week == 4:
        if hour < 6:
            shift_date = now - timedelta(days=1)
            shift_type = ""
        else:
            shift_date = now
            shift_type = "משמרת בוקר"
    # Saturday: Before 6 AM show the previous day with "משמרת ערב", after 6 AM add "משמרת בוקר"
    elif day_of_week == 5:
        if hour < 6:
            shift_date = now - timedelta(days=1)
            shift_type = "משמרת ערב"
        else:
            shift_date = now
            shift_type = "משמרת בוקר"
    # Sunday: Before 6 AM show the previous day with "משמרת ערב"
    elif day_of_week == 6:
        if hour < 6:
            shift_date = now - timedelta(days=1)
            shift_type = "משמרת ערב"
        else:
            shift_date = now
            shift_type = ""

    shift_date_str = shift_date.strftime("%Y-%m-%d")
    if shift_type:
        shift_date_str += f" {shift_type}"

    return shift_date_str


st.title('טיפים של כוח השחם')

# Input for the number of waitresses
num_waitresses = st.number_input('הכנס את מספר המלצרים שעבדו', min_value=1, step=1)

# Create a list to store the details of each waitress
waitresses = []

for i in range(num_waitresses):
    with st.expander(f'מלצר {i+1}'):
        name = st.text_input(f'הכנס את שם המלצר {i+1}', key=f'name_{i}')
        hours_worked = st.number_input(f'כמה שעות המלצר {i+1} עבד', min_value=0.0, step=0.1, key=f'hours_{i}')
        waitresses.append({'שם': name, 'שעות עבודה': hours_worked})

# Input for the total tips collected
total_tips = st.number_input('סך הכול טיפים', min_value=0.0, step=0.01)

if st.button('חשב'):
    # Calculate total hours worked
    total_hours = sum(waitress['שעות עבודה'] for waitress in waitresses)

    # Calculate money made per hour
    money_per_hour = (total_tips * 0.97) / total_hours if total_hours > 0 else 0
    money_per_hour = round_down(money_per_hour)

    # Calculate הפרשה לבר
    bar_deduction = total_tips * 0.03
    bar_deduction = round_down(bar_deduction)

    # Calculate אחרי הפרשה
    after_deduction = total_tips - bar_deduction
    after_deduction = round_down(after_deduction)

    # Create a dataframe to store the results
    results = []
    total_service_fees = 0

    for waitress in waitresses:
        total_made = waitress['שעות עבודה'] * money_per_hour
        total_made = round_down(total_made)
        service_fee = total_made * 0.2
        service_fee = round_down(service_fee)
        net_income = total_made * 0.8
        net_income = round_down(net_income)
        total_service_fees += service_fee

        results.append({
            'שם': waitress['שם'],
            'שעות עבודה': waitress['שעות עבודה'],
            'סכום כולל': total_made,
            'דמי שירות': service_fee,
            'נטו': net_income
        })

    total_service_fees = round_down(total_service_fees)
    
    # Get the correct shift date and type
    shift_date_str = get_shift_date_and_type()

    # Add the summary rows
    summary_rows = [
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'תאריך: {shift_date_str}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'סך הכול טיפים: {round_down(total_tips)}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'סך הכול שעות: {total_hours}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'הפרשה לבר: {bar_deduction}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'אחרי הפרשה: {after_deduction}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'סך הכול לשעה: {money_per_hour}',
            'נטו': ''
        },
        {
            'שם': '',
            'שעות עבודה': '',
            'סכום כולל': '',
            'דמי שירות': f'סך הכול דמי שירות: {total_service_fees}',
            'נטו': ''
        }
    ]

    results.extend(summary_rows)
    results_df = pd.DataFrame(results)

    # Display results
    st.success(f'סכום כסף לשעה: {money_per_hour} ש"ח')
    st.success(f'הפרשה לבר: {bar_deduction} ש"ח')
    st.success(f'סה"כ דמי שירות: {total_service_fees} ש"ח')
    st.success(f'סה"כ שעות עבודה: {total_hours} שעות')
    st.success(f'סה"כ טיפים: {round_down(total_tips)} ש"ח')
    st.success(f'אחרי הפרשה: {after_deduction} ש"ח')

    # Save the results to a CSV file with the current date in the filename
    csv_filename = f'משמרת_{shift_date_str}.csv'
    results_df.to_csv(csv_filename, index=False, encoding='utf-8')


    # Convert the DataFrame to windows-1255 for download
    results_df_encoded = results_df.applymap(lambda x: str(x).encode('windows-1255', errors='ignore').decode('windows-1255'))

    # Provide the new record for download
    st.subheader('הורד את רשומת הטיפים החדשה')
    st.download_button(
        label='הורד CSV',
        data=results_df_encoded.to_csv(index=False, encoding='windows-1255').encode('windows-1255'),
        file_name=csv_filename,
        mime='text/csv'
    )

    # Display the current session's data
    st.subheader('סוף משמרת')
    st.write(results_df)
