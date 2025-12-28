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
            if password_guess == "FamilyPassword123": # Change this to your password
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return False
    return True

if not check_password():
    st.stop()

# 3. CONNECT TO GOOGLE SHEETS
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. APP CONTENT
st.title("🍼 Baby Boy's Daily Dashboard")

# Pull existing data to show history
try:
    existing_data = conn.read(ttl=0) # ttl=0 ensures it pulls the latest data
except:
    existing_data = pd.DataFrame(columns=["Date", "Total_Milk", "Diapers", "Med1", "Med2", "Bath", "Nap1", "Nap2", "Notes"])

# 5. INPUT COLUMNS
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("💊 Meds & Hygiene")
    med1 = st.checkbox("Meds Dose #1 (AM)")
    med2 = st.checkbox("Meds Dose #2 (PM)")
    bath = st.checkbox("Bath Completed")
with col2:
    st.subheader("🧷 Diapers & Milk")
    wet = st.number_input("Wet Diapers", 0, 10, 0)
    dirty = st.number_input("Dirty Diapers", 0, 10, 0)
    b_total = st.number_input("Total Oz Today", 0, 40, 0)
with col3:
    st.subheader("😴 Naps & Notes")
    n1 = st.text_input("Nap 1 Duration", placeholder="e.g. 1.5 hrs")
    n2 = st.text_input("Nap 2 Duration", placeholder="e.g. 1 hr")
    notes = st.text_area("Milestones/Notes")

# 6. SAVE LOGIC
if st.button("💾 SAVE TO GOOGLE SHEETS"):
    new_entry = pd.DataFrame([{
        "Date": datetime.now().strftime('%Y-%m-%d %H:%M'),
        "Total_Milk": b_total,
        "Diapers": wet + dirty,
        "Med1": "✅" if med1 else "❌",
        "Med2": "✅" if med2 else "❌",
        "Bath": "✅" if bath else "❌",
        "Nap1": n1,
        "Nap2": n2,
        "Notes": notes
    }])
    
    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
    conn.update(data=updated_df)
    st.balloons()
    st.success("Entry Saved! Refreshing history...")
    st.rerun()

# 7. HISTORY SECTION
st.divider()
st.subheader("📜 Recent History (Last 5 Entries)")
if not existing_data.empty:
    # Display the last 5 rows, most recent at the top
    st.table(existing_data.tail(5).iloc[::-1])
else:
    st.write("No history found yet. Save an entry to start the log!")
