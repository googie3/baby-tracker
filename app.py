import streamlit as st
import pandas as pd
from datetime import datetime, time

# Page Config
st.set_page_config(page_title="Baby Daily Tracker", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for a cleaner "App" look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🍼 Baby Boy's Daily Dashboard")
st.info(f"Today is {datetime.now().strftime('%A, %B %d, %2025')}")

# 1. THE DAILY SCHEDULE (Reference)
with st.expander("📅 VIEW FULL SCHEDULE (Dad up at 2:30 AM)"):
    schedule_data = {
        "Time": ["02:30 AM", "07:00 AM", "07:45 AM", "08:15 AM", "08:30 AM", "11:00 AM", "01:30 PM", "03:00 PM", "04:30 PM", "05:00 PM", "05:30 PM", "06:00 PM", "06:30 PM"],
        "Activity": ["Dad Wakes Up", "Bottle #1", "SOLIDS #1", "Meds #1", "Nap #1", "Dad Hand-off", "Nap #2", "Bottle #3", "Meds #2", "Mom Returns", "SOLIDS #2", "Bath Time", "Bottle #4"],
        "Who": ["Dad", "MIL", "MIL", "MIL", "MIL", "Dad", "Dad", "Dad", "Dad", "Mom", "Family", "Family", "Family"]
    }
    st.table(pd.DataFrame(schedule_data))

# 2. TRACKING COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("💊 Meds & Hygiene")
    med1 = st.checkbox("Meds #1 (08:15 AM)")
    med2 = st.checkbox("Meds #2 (04:30 PM)")
    bath = st.checkbox("Bath Given (06:00 PM)")
    
    st.subheader("😴 Nap Tracker")
    n1_s = st.time_input("Nap 1 Start", time(8, 30))
    n1_e = st.time_input("Nap 1 End", time(10, 30))
    n2_s = st.time_input("Nap 2 Start", time(13, 30))
    n2_e = st.time_input("Nap 2 End", time(15, 0))

with col2:
    st.subheader("🧷 Diaper Tracker")
    st.write("Log today's changes:")
    wet = st.number_input("Wet Diapers", 0, 15, 0)
    dirty = st.number_input("Dirty Diapers", 0, 15, 0)
    diaper_notes = st.text_input("Diaper Notes", placeholder="e.g. Rash/Consistency")

    st.subheader("🍼 Bottle (oz)")
    b1 = st.number_input("Bottle 1", 0, 10, 0)
    b2 = st.number_input("Bottle 2", 0, 10, 0)
    b3 = st.number_input("Bottle 3", 0, 10, 0)
    b4 = st.number_input("Bottle 4", 0, 10, 0)

with col3:
    st.subheader("🍲 Solids & Meals")
    meal1 = st.text_input("Breakfast (7:45 AM)", placeholder="e.g. Rice Cereal")
    meal2 = st.text_input("Dinner (5:30 PM)", placeholder="e.g. Peas")
    
    st.subheader("⭐ Milestones")
    milestone = st.text_area("What did he do today?", placeholder="e.g. Tried to crawl, sat up for 10 seconds, new sound...")

# 3. SUMMARY CALCULATIONS
st.divider()
total_oz = b1+b2+b3+b4
st.metric("Total Milk Intake", f"{total_oz} oz")

if st.button("Submit Daily Log"):
    st.balloons()
    st.success(f"Log updated at {datetime.now().strftime('%H:%M')}. Data ready for Wife/MIL!")
  
