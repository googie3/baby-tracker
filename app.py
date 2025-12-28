import streamlit as st
import pandas as pd
from datetime import datetime, time
from streamlit_gsheets import GSheetsConnection

# 1. PAGE SETUP
st.set_page_config(page_title="Baby Boy Dashboard", layout="wide")

# 2. PASSWORD PROTECTION
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Family Access Only")
        password_guess = st.text_input("Enter Family Password", type="password")
        if st.button("Unlock Dashboard"):
            if password_guess == "FamilyPassword123": # Change this!
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return False
    return True

if not check_password():
    st.stop()

# 3. CONNECT TO GOOGLE SHEETS
# You will paste your sheet URL in the Streamlit Secrets (Step 4)
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. APP CONTENT
st.title("🍼 Baby Boy's Daily Dashboard")

# (Input sections remain the same as previous version)
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("💊 Meds & Hygiene")
    med1 = st.checkbox("Meds Dose #1")
    med2 = st.checkbox("Meds Dose #2")
    bath = st.checkbox("Bath Completed")
with col2:
    st.subheader("🧷 Diapers & Milk")
    wet = st.number_input("Wet", 0, 10, 0)
    dirty = st.number_input("Dirty", 0, 10, 0)
    b_total = st.number_input("Total Oz Today", 0, 40, 0)
with col3:
    st.subheader("😴 Naps & Notes")
    n1 = st.text_input("Nap 1 Duration", "e.g. 1.5 hrs")
    n2 = st.text_input("Nap 2 Duration", "e.g. 1 hr")
    notes = st.text_area("Milestones/Notes")

# 5. THE SAVE LOGIC
if st.button("💾 SAVE TO GOOGLE SHEETS"):
    # Create a new row of data
    new_data = pd.DataFrame([{
        "Date": datetime.now().strftime('%Y-%m-%d'),
        "Total_Milk": b_total,
        "Diapers": wet + dirty,
        "Med1": "Yes" if med1 else "No",
        "Med2": "Yes" if med2 else "No",
        "Bath": "Yes" if bath else "No",
        "Nap1": n1,
        "Nap2": n2,
        "Notes": notes
    }])
    
    # Send to Sheet
    existing_data = conn.read(ttl=0) # Read current sheet
    updated_df = pd.concat([existing_data, new_data], ignore_index=True)
    conn.update(data=updated_df)
    
    st.balloons()
    st.success("Data synced to Google Sheets!")
