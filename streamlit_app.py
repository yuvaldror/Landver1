import streamlit as st
import pandas as pd
import math
from datetime import datetime, timedelta
import pytz

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

    if day_of_week in range(0, 4):
        shift_date = now - timedelta(days=1)
        shift_type = ""
    elif day_of_week == 4:
        if hour < 6:
            shift_date = now - timedelta(days=1)
            shift_type = ""
        else:
            shift_date = now
            shift_type = "משמרת בוקר"
    elif day_of_week == 5:
        if hour < 6:
            shift_date = now - timedelta(days=1)
            shift_type = "משמרת ערב"
        else:
            shift_date = now
            shift_type = "משמרת בוקר"
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

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 'tips'
    st.session_state.waitresses = []
    st.session_state.total_tips = 0.0

# Function to calculate tips
def calculate_tips():
    st.title('טיפים של כוח השחם')

    num_waitresses = st.number_input('הכנס את מספר המלצרים שעבדו', min_value=1, step=1)

    waitresses = []

    for i in range(num_waitresses):
        with st.expander(f'מלצר {i+1}'):
            name = st.text_input(f'הכנס את שם המלצר {i+1}', key=f'name_{i}')
            hours_worked = st.number_input(f'כמה שעות המלצר {i+1} עבד', min_value=0.0, step=0.1, key=f'hours_{i}')
            waitresses.append({'שם': name, 'שעות עבודה': hours_worked})

    total_tips = st.number_input('סך הכול טיפים', min_value=0.0, step=0.01)

    if st.button('חשב'):
        st.session_state.waitresses = waitresses
        st.session_state.total_tips = total_tips
        st.session_state.step = 'summary'
        st.experimental_rerun()

# Function to fill shift summary
def shift_summary():
    st.title('סיכום משמרת')

    waitresses = st.session_state.get('waitresses', [])
    total_tips = st.session_state.get('total_tips', 0)

    closing_cash = st.number_input('סגירת קופה (₪)', min_value=0.0, step=0.01)
    avg_per_guest = st.number_input('ממוצע לסועד (₪)', min_value=0.0, step=0.01)

    st.subheader('מלצרים שעבדו')
    waitresses_names = [waitress['שם'] for waitress in waitresses if waitress['שם']]
    selected_waitresses = st.multiselect('בחר את המלצרים שעבדו במשמרת', waitresses_names, default=waitresses_names)
    waitresses_performance = {}
    for waitress in selected_waitresses:
        performance = st.slider(f'דרג את תפקודו של {waitress} (1-10)', min_value=1, max_value=10)
        waitresses_performance[waitress] = performance

    st.subheader('ברמנים')
    bartender_name = st.text_input('מי הברמן במשמרת?')
    bartender_performance = st.slider('דרג את תפקוד הברמן (1-10)', min_value=1, max_value=10) if bartender_name else None

    shortages = st.text_area('רשום חוסרים למשמרת הבאה')

    if st.button('שמור סיכום משמרת'):
        shift_date_str = get_shift_date_and_type()

        summary_data = {
            'סגירת קופה': closing_cash,
            'ממוצע לסועד': avg_per_guest,
            'מלצרים שעבדו': selected_waitresses,
            'תפקוד המלצרים': waitresses_performance,
            'שם הברמן': bartender_name,
            'תפקוד הברמן': bartender_performance,
            'חוסרים': shortages
        }

        tips_filename = f'משמרת_{shift_date_str}.csv'
        summary_filename = f'משמרת_{shift_date_str}_סיכום_משמרת.csv'

        tips_data = pd.DataFrame(st.session_state.waitresses)
        tips_data.to_csv(tips_filename, index=False, encoding='utf-8')

        pd.DataFrame([summary_data]).to_csv(summary_filename, index=False, encoding='utf-8')

        st.success('סיכום המשמרת נשמר בהצלחה!')
        st.download_button(
            label='הורד את קובץ הטיפים',
            data=tips_data.to_csv(index=False, encoding='utf-8').encode('utf-8'),
            file_name=tips_filename,
            mime='text/csv'
        )
        st.download_button(
            label='הורד את סיכום המשמרת',
            data=pd.DataFrame([summary_data]).to_csv(index=False, encoding='utf-8').encode('utf-8'),
            file_name=summary_filename,
            mime='text/csv'
        )

# Manage the process
if st.session_state.step == 'tips':
    calculate_tips()
elif st.session_state.step == 'summary':
    shift_summary()
