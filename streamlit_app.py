# משתנה לעקוב אחרי השלב הנוכחי בתהליך
if 'step' not in st.session_state:
    st.session_state.step = 'tips'

# פונקציה לחישוב הטיפים
def calculate_tips():
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
        # שמירה של נתוני הטיפים ב-session state
        st.session_state.waitresses = waitresses
        st.session_state.total_tips = total_tips
        st.session_state.step = 'summary'

        st.success('חישוב הטיפים הושלם! עוברים לסיכום המשמרת.')

# פונקציה להזנת סיכום משמרת
def shift_summary():
    st.title('סיכום משמרת')

    # שימוש בנתונים שהוזנו בשלב הקודם
    waitresses = st.session_state.get('waitresses', [])
    total_tips = st.session_state.get('total_tips', 0)

    # הזנת נתונים כלליים
    closing_cash = st.number_input('סגירת קופה (₪)', min_value=0.0, step=0.01)
    avg_per_guest = st.number_input('ממוצע לסועד (₪)', min_value=0.0, step=0.01)

    # בחירת מלצרים ותפקודם
    st.subheader('מלצרים שעבדו')
    waitresses_names = [waitress['שם'] for waitress in waitresses if waitress['שם']]
    selected_waitresses = st.multiselect('בחר את המלצרים שעבדו במשמרת', waitresses_names, default=waitresses_names)
    waitresses_performance = {}
    for waitress in selected_waitresses:
        performance = st.slider(f'דרג את תפקודו של {waitress} (1-10)', min_value=1, max_value=10)
        waitresses_performance[waitress] = performance

    # הזנת נתוני ברמנים
    st.subheader('ברמנים')
    bartender_name = st.text_input('מי הברמן במשמרת?')
    bartender_performance = st.slider('דרג את תפקוד הברמן (1-10)', min_value=1, max_value=10) if bartender_name else None

    # חוסרים למשמרת הבאה
    shortages = st.text_area('רשום חוסרים למשמרת הבאה')

    # לחצן לשמירת הנתונים
    if st.button('שמור סיכום משמרת'):
        shift_date_str = get_shift_date_and_type()

        # שמירת נתוני סיכום המשמרת
        summary_data = {
            'סגירת קופה': closing_cash,
            'ממוצע לסועד': avg_per_guest,
            'מלצרים שעבדו': selected_waitresses,
            'תפקוד המלצרים': waitresses_performance,
            'שם הברמן': bartender_name,
            'תפקוד הברמן': bartender_performance,
            'חוסרים': shortages
        }

        # שמירת הקבצים
        tips_filename = f'משמרת_{shift_date_str}.csv'
        summary_filename = f'משמרת_{shift_date_str}_סיכום_משמרת.csv'

        # קובץ הטיפים
        tips_data = pd.DataFrame(st.session_state.waitresses)
        tips_data.to_csv(tips_filename, index=False, encoding='utf-8')

        # קובץ סיכום המשמרת
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

# ניהול התהליך
if st.session_state.step == 'tips':
    calculate_tips()
elif st.session_state.step == 'summary':
    shift_summary()
