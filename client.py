import streamlit as st
from supabase import create_client

# ── Hardcoded credentials ──────────────────────────────────────────
SUPABASE_URL = "https://dkwojxzwtzxhzszpilas.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRrd29qeHp3dHp4aHpzenBpbGFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI2Mzg0NzQsImV4cCI6MjA4ODIxNDQ3NH0.DpCuFfBtH2-8tlX10lshel0JMpJOKGn00aYPzuYStog"


st.set_page_config(page_title="Lab Equipment Client", page_icon="🔬", layout="centered")
st.title("🔬 Lab Equipment — Client App")
st.caption("Report faulty status for any equipment")

# ── Init connection ────────────────────────────────────────────────
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# ── Fetch data ─────────────────────────────────────────────────────
def fetch_equipment():
    return supabase.table("lab_equipment").select("*").order("lab_type").execute().data

# ── Keep selected equipment in session state ───────────────────────
if "selected_equipment" not in st.session_state:
    st.session_state.selected_equipment = None

# ── Filter by lab ──────────────────────────────────────────────────
lab_filter = st.radio("Filter by Lab", ["All", "Chemistry", "Physics"], horizontal=True)

data = fetch_equipment()

if lab_filter != "All":
    data = [row for row in data if row["lab_type"] == lab_filter]

# ── Select equipment ───────────────────────────────────────────────
equipment_options = [f"{row['equipment_name']}  |  {row['lab_type']}  |  Serial: {row['serial_number']}" for row in data]
equipment_map     = {f"{row['equipment_name']}  |  {row['lab_type']}  |  Serial: {row['serial_number']}": row for row in data}

# Restore previously selected equipment if it still exists in current filter
default_index = 0
if st.session_state.selected_equipment in equipment_options:
    default_index = equipment_options.index(st.session_state.selected_equipment)

selected = st.selectbox("Select Equipment", equipment_options, index=default_index)
st.session_state.selected_equipment = selected  # Save selection

if selected:
    row = equipment_map[selected]

    # ── Show current info ──────────────────────────────────────────
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("Equipment",     row["equipment_name"])
    col2.metric("Lab",           row["lab_type"])
    col3.metric("Serial Number", row["serial_number"])

    st.divider()

    # ── Current status badge ───────────────────────────────────────
    if row["is_faulty"] == "Yes":
        st.error("⚠️ Current Status: **FAULTY**")
    else:
        st.success("✅ Current Status: **Working Fine**")

    # ── Update status ──────────────────────────────────────────────
    new_status_label = st.radio(
        "Is the Equipment working properly?",
        ["Yes", "No"],
        index=0 if row["is_faulty"] == "No" else 1,  # Yes=working=not faulty, No=faulty
        horizontal=True
    )

    # Map radio answer to is_faulty value
    new_faulty_value = "No" if new_status_label == "Yes" else "Yes"

    # ── Keep save message persistent ──────────────────────────────
    if "last_message" not in st.session_state:
        st.session_state.last_message = None
        st.session_state.last_message_type = None

    if st.button("💾 Save Change", use_container_width=True):
        if new_faulty_value == row["is_faulty"]:
            st.session_state.last_message = f"⚠️ Status is already set to that value. No change made."
            st.session_state.last_message_type = "warning"
        else:
            supabase.table("lab_equipment") \
                .update({"is_faulty": new_faulty_value}) \
                .eq("id", row["id"]) \
                .execute()

            if new_faulty_value == "Yes":
                st.session_state.last_message = f"🚨 **{row['equipment_name']}** marked as **FAULTY**"
                st.session_state.last_message_type = "error"
            else:
                st.session_state.last_message = f"✅ **{row['equipment_name']}** marked as **Working Fine**"
                st.session_state.last_message_type = "success"
            st.rerun()

    # ── Show persistent message ────────────────────────────────────
    if st.session_state.last_message:
        if st.session_state.last_message_type == "error":
            st.error(st.session_state.last_message)
        elif st.session_state.last_message_type == "success":
            st.success(st.session_state.last_message)
        elif st.session_state.last_message_type == "warning":
            st.warning(st.session_state.last_message)
            