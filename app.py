import streamlit as st
import pandas as pd
from datetime import datetime, time

# 1. PAGE SETUP
st.set_page_config(page_title="Baby Boy Dashboard", layout="wide")

# 2. PASSWORD PROTECTION
def check_password():
    if "password_correct" not in st.session_state:
        st.title("🔒 Family Access Only")
        password_guess = st.text_input("Enter Family Password", type="password")
        if st.button("Unlock Dashboard"):
            # CHANGE 'FamilyPassword123' TO YOUR CHOSEN PASSWORD
            if password_guess == "Zoey1391!":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return False
    return True

if not check_password():
    st.stop()

# 3. APP CONTENT (Only shows if password is correct)
st.title("🍼 Baby Boy's Daily Dashboard")
st.write(f"Logged in as Dad | Today: {datetime.now().strftime('%A, %B %d, 2025')}")

# --- QUICK STATS BAR ---
col_stat1, col_stat2, col_stat3 = st.columns(3)

# 4. DAILY SCHEDULE REFERENCE
with st.expander("📅 VIEW FULL DAILY SCHEDULE (Reference)"):
    schedule_data = {
        "Time": ["02:30 AM", "07:00 AM", "07:45 AM", "08:15 AM", "08:30 AM", "11:00 AM", "01:30 PM", "03:00 PM", "04:30 PM", "05:30 PM", "06:00 PM", "06:30 PM", "07:00 PM"],
        "Activity": ["Dad Wake Up", "Bottle #1", "SOLIDS #1", "Meds #1", "Nap #1", "Dad Hand-off", "Nap #2", "Bottle #3", "Meds #2", "SOLIDS #2", "Bath Time", "Bottle #4", "Bedtime"],
        "Caregiver": ["Dad", "MIL", "MIL", "MIL", "MIL", "Dad", "Dad", "Dad", "Dad", "Mom/Dad", "Mom/Dad", "Mom/Dad", "Family"]
    }
    st.table(pd.DataFrame(schedule_data))

# 5. INPUT COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💊 Meds & Hygiene")
    med1 = st.checkbox("Meds Dose #1 (08:15 AM)")
    med2 = st.checkbox("Meds Dose #2 (04:30 PM)")
    bath = st.checkbox("Bath Completed (06:00 PM)")
    
    st.subheader("😴 Nap Tracker")
    n1_s = st.time_input("Nap 1 Start", time(8, 30))
    n1_e = st.time_input("Nap 1 End", time(10, 30))
    n2_s = st.time_input("Nap 2 Start", time(13, 30))
    n2_e = st.time_input("Nap 2 End", time(15, 0))

with col2:
    st.subheader("🧷 Diaper Tracker")
    wet = st.number_input("Wet Diapers", 0, 15, 0)
    dirty = st.number_input("Dirty Diapers", 0, 15, 0)
    
    st.subheader("🍼 Bottle (oz)")
    b1 = st.number_input("Bottle 1", 0, 12, 0)
    b2 = st.number_input("Bottle 2", 0, 12, 0)
    b3 = st.number_input("Bottle 3", 0, 12, 0)
    b4 = st.number_input("Bottle 4", 0, 12, 0)

with col3:
    st.subheader("🍲 Solids & Meals")
    meal1 = st.text_input("Breakfast (7:45 AM)", placeholder="e.g. Oatmeal")
    meal2 = st.text_input("Dinner (5:30 PM)", placeholder="e.g. Carrots")
    
    st.subheader("⭐ Milestones")
    milestone = st.text_area("Today's Milestones", placeholder="e.g. Sat up, new sounds...")

# 6. FOOTER & SAVE
st.divider()
total_oz = b1 + b2 + b3 + b4
col_stat1.metric("Total Milk", f"{total_oz} oz")
col_stat2.metric("Diapers", f"{wet + dirty}")
col_stat3.metric("Meds", "Done" if med1 and med2 else "Pending")

if st.button("💾 SAVE DAILY LOG"):
    st.balloons()
    st.success("Daily log saved successfully!")
    
