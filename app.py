import streamlit as st
import pandas as pd
import numpy as np
import requests
from scipy import stats

# 1. PAGE CONFIGURATION & THEME
# Setting up the wide layout and the Deep Blue professional theme.
st.set_page_config(page_title="Enterprise Data Guard Pro", layout="wide")

st.markdown("""
    <style>
    /* Professional Deep Blue Background */
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { color: #4facfe !important; }
    .stMetric {
        background-color: #1a2332;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #00f2fe;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Sidebar and Button Gradient */
    section[data-testid="stSidebar"] { background-color: #0a0c10; }
    .stButton>button {
        background-image: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
        color: white; border: none; font-weight: bold; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (The Memory Engine)
# This keeps track of the data, the original version, and the history for Undo/Redo.
if 'df' not in st.session_state:
    st.session_state.df = None
if 'original_df' not in st.session_state:
    st.session_state.original_df = None
if 'undo_stack' not in st.session_state:
    st.session_state.undo_stack = []
if 'change_log' not in st.session_state:
    st.session_state.change_log = []

# Helper to save data state before any modification
def save_snapshot(action_name):
    st.session_state.undo_stack.append(st.session_state.df.copy())
    st.session_state.change_log.append({
        "Time": pd.Timestamp.now().strftime("%H:%M:%S"),
        "Action": action_name
    })

# 3. ADVANCED ERROR STYLING (The Red Flag Logic)
# This identifies Nulls and Outliers and prepares the CSS styling for the table.
def apply_intelligent_styling(df):
    style_df = pd.DataFrame('', index=df.index, columns=df.columns)
    for col in df.columns:
        # Highlight Nulls in Dark Red
        null_mask = df[col].isna()
        style_df.loc[null_mask, col] = 'background-color: #8b0000; color: white;'
        
        # Highlight Statistical Outliers in Bright Red (Z-Score > 3)
        if pd.api.types.is_numeric_dtype(df[col]):
            non_null_s = df[col].dropna()
            if len(non_null_s) > 5: # Need enough data for Z-score
                z = np.abs(stats.zscore(non_null_s))
                outliers = non_null_s[z > 3].index
                style_df.loc[outliers, col] = 'background-color: #ff4b4b; color: white;'
    return style_df

# 4. SIDEBAR CONTROLS
with st.sidebar:
    st.title("🛡️ Guard Controls")
    api_key = st.text_input("OpenRouter API Key", type="password")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    st.markdown("---")
    if st.button("⬅️ Undo Last Action"):
        if st.session_state.undo_stack:
            st.session_state.df = st.session_state.undo_stack.pop()
            st.rerun()
            
    if st.button("🔄 Reset to Original"):
        if st.session_state.original_df is not None:
            st.session_state.df = st.session_state.original_df.copy()
            st.session_state.undo_stack = []
            st.session_state.change_log = []
            st.rerun()

# 5. MAIN APPLICATION LOGIC
# --- MAIN APPLICATION LOGIC (REPLACED SECTION) ---
if uploaded_file:
    # Check if a NEW file has been uploaded by comparing names
    # This ensures that if you upload a different dataset, the old one is cleared.
    current_file_name = uploaded_file.name
    
    if "last_uploaded_file" not in st.session_state or st.session_state.last_uploaded_file != current_file_name:
        # A new file detected! Reset the session state for the new data
        raw_df = pd.read_csv(uploaded_file)
        st.session_state.df = raw_df.copy()
        st.session_state.original_df = raw_df.copy()
        st.session_state.undo_stack = []
        st.session_state.change_log = []
        st.session_state.last_uploaded_file = current_file_name
        st.rerun() # Refresh the UI to show the new data metrics

    # Assign the current active dataframe
    df = st.session_state.df

    # --- DASHBOARD METRICS ---
    st.title("📊 Enterprise Quality Audit")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows", len(df))
    m2.metric("Columns", len(df.columns))
    m3.metric("Total Nulls", df.isna().sum().sum())
    m4.metric("Duplicates", df.duplicated().sum())

    # --- DATA PREVIEW (With Outlier Highlighting) ---
    st.subheader("🔍 Intelligent Preview")
    st.caption("Dark Red = Missing Value | Bright Red = Statistical Outlier")
    
    # We style the top 100 rows for performance
    preview_styled = df.head(100).style.apply(lambda x: apply_intelligent_styling(df.head(100)), axis=None)
    st.dataframe(preview_styled, use_container_width=True)

    # --- SQL CONSOLE ---
    # Allows for professional filtering using SQL logic strings
    with st.expander("💻 Professional SQL Console"):
        query = st.text_area("Enter Filter Query (e.g., Amount > 500 and Qty < 10)")
        if st.button("Run SQL Filter"):
            try:
                save_snapshot(f"SQL Filter: {query}")
                st.session_state.df = st.session_state.df.query(query)
                st.rerun()
            except Exception as e:
                st.error(f"Syntax Error: {e}")

    # --- SCHEMA VALIDATOR ---
    # Identifies if data types are correct for the business context
    with st.expander("✅ Schema Integrity Check"):
        v_col = st.selectbox("Column to Validate", df.columns)
        v_type = st.radio("Expected Type", ["Numeric", "String/Object"])
        if st.button("Validate"):
            is_num = pd.api.types.is_numeric_dtype(df[v_col])
            if v_type == "Numeric" and not is_num:
                st.error(f"CRITICAL: {v_col} contains non-numeric characters.")
            elif v_type == "String/Object" and is_num:
                st.warning(f"NOTE: {v_col} is currently stored as a number.")
            else:
                st.success(f"VALID: {v_col} matches the expected schema.")

    # --- SMART CLEANING ACTIONS ---
    st.markdown("---")
    st.subheader("🛠️ Smart Cleaning Toolkit")
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        target = st.selectbox("Select Target", ["All Columns"] + list(df.columns))
    with c2:
        method = st.selectbox("Action", ["Drop Duplicates", "Fill Missing Values", "Uppercase Text", "Drop Outliers"])
    
    if c3.button("Execute Action"):
        save_snapshot(f"{method} on {target}")
        
        if method == "Drop Duplicates":
            st.session_state.df = st.session_state.df.drop_duplicates()
        elif method == "Fill Missing Values":
            fill = "Unknown" if target == "All Columns" else (df[target].mean() if pd.api.types.is_numeric_dtype(df[target]) else "Unknown")
            st.session_state.df[target if target != "All Columns" else df.columns] = st.session_state.df.fillna(fill)
        elif method == "Uppercase Text" and target != "All Columns":
            st.session_state.df[target] = st.session_state.df[target].astype(str).str.upper()
        elif method == "Drop Outliers" and target != "All Columns":
            z_scores = np.abs(stats.zscore(st.session_state.df[target].dropna()))
            st.session_state.df = st.session_state.df.drop(st.session_state.df[target].dropna()[z_scores > 3].index)
            
        st.success("Action Complete")
        st.rerun()

    # --- AUDIT TRAIL ---
    with st.expander("📜 View Activity Log"):
        if st.session_state.change_log:
            st.table(pd.DataFrame(st.session_state.change_log))
        else:
            st.info("No modifications recorded yet.")

    # --- DOWNLOAD ---
    st.markdown("---")
    st.download_button("💾 Download Cleaned CSV", df.to_csv(index=False), "cleaned_data.csv", "text/csv")

else:
    st.info("🚀 System ready. Please upload a CSV to initiate Data Guard Pro.")