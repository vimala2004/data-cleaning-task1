import streamlit as st
import pandas as pd
import numpy as np

# --- 1. SET UP STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Executive Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- 2. GENERATE COMPREHENSIVE PERFORMANCE DATA ---
np.random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

data = {
    "Month": months * 3,
    "Region": ["North"] * 12 + ["South"] * 12 + ["East"] * 12,
    "Revenue": np.random.randint(40000, 100000, size=36),
    "New_Customers": np.random.randint(100, 500, size=36),
    "Satisfaction_Score": np.random.uniform(3.5, 4.9, size=36).round(1)
}
df = pd.DataFrame(data)

# --- 3. INTERACTIVE SIDEBAR FILTERS ---
st.sidebar.header("📊 Dashboard Controls")
st.sidebar.write("Filter data dynamically to adjust performance charts.")

# Region Filter Multi-select
selected_regions = st.sidebar.multiselect(
    "Select Operating Regions:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Filter the master dataframe based on user interaction
filtered_df = df[df["Region"].isin(selected_regions)]

# --- 4. MAIN APP HEADER & ACTIONABLE INSIGHTS ---
st.title("🚀 Business Performance & Analytics Dashboard")
st.markdown("An interactive visual summary tracking key operational trends, customer acquisition velocity, and regional metrics.")

# --- 5. HIGH-LEVEL KPI METRIC CARDS ---
total_revenue = filtered_df["Revenue"].sum() if not filtered_df.empty else 0
total_customers = filtered_df["New_Customers"].sum() if not filtered_df.empty else 0
avg_satisfaction = filtered_df["Satisfaction_Score"].mean() if not filtered_df.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="💰 Total Generated Revenue", value=f"${total_revenue:,}")
with col2:
    st.metric(label="👥 Total New Customers", value=f"{total_customers:,}")
with col3:
    st.metric(label="⭐ Average Customer Satisfaction", value=f"{avg_satisfaction:.2f} / 5.0")

st.divider()

# --- 6. INTERACTIVE TREND & PERFORMANCE CHARTS ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Monthly Revenue Velocity")
    if not filtered_df.empty:
        # Aggregate revenue by month for selected regions
        revenue_trend = filtered_df.groupby("Month")["Revenue"].sum().reindex(months)
        st.line_chart(revenue_trend)
    else:
        st.warning("Please select at least one region to view trends.")

with chart_col2:
    st.subheader("📊 Customer Growth Comparison")
    if not filtered_df.empty:
        # Aggregate customer distribution across regions
        customer_dist = filtered_df.groupby("Region")["New_Customers"].sum()
        st.bar_chart(customer_dist)
    else:
        st.warning("Please select at least one region to view distributions.")

# --- 7. EXPORT DATA LAYER ---
st.subheader("📋 Raw Performance Audit Ledger")
st.dataframe(filtered_df, use_container_width=True)

st.success("💡 Actionable Insight: Use the sidebar filters to isolate specific regions and pinpoint areas with low customer growth trends.")
