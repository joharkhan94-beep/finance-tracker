import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Family Finance Tracker", page_icon="💰", layout="wide")
st.title("💰 Family Finance Tracker")

# --- DATABASE FUNCTIONS ---
def load_data():
    conn = sqlite3.connect("finance.db")
    df = pd.read_sql("SELECT * FROM expenses", conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

def save_data(date, category, item, cost, type_, user):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, category, item, cost, type, user) VALUES (?, ?, ?, ?, ?, ?)", 
                   (date, category, item, cost, type_, user))
    conn.commit()
    conn.close()

def delete_data(row_id):
    conn = sqlite3.connect("finance.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()

# --- SIDEBAR: ADD TRANSACTION ---
st.sidebar.header("➕ Add Transaction")
with st.sidebar.form("expense_form"):
    user = st.sidebar.selectbox("Who is this?", ["Me", "Partner", "Joint"])
    type_ = st.radio("Type", ["Expense", "Income"], horizontal=True)
    new_date = st.date_input("Date")
    new_cat = st.selectbox("Category", ["Food", "Travel", "Bills", "Salary", "Rent", "Entertainment", "Other"])
    new_item = st.text_input("Description (e.g. Pizza)")
    new_cost = st.number_input("Amount (£)", min_value=0.0, format="%.2f")
    
    submitted = st.form_submit_button("Save Transaction")
    if submitted:
        save_data(new_date, new_cat, new_item, new_cost, type_, user)
        st.success("Saved!")

# --- TABS LAYOUT ---
tab1, tab2 = st.tabs(["📊 Dashboard", "📝 Manage Data"])

with tab1:
    # --- DASHBOARD LOGIC ---
    try:
        df = load_data()

        # --- FILTERS (Sidebar) ---
        st.sidebar.divider()
        st.sidebar.header("🔍 Dashboard Filters")
        selected_users = st.sidebar.multiselect("Select Users:", options=df["user"].unique(), default=df["user"].unique())
        start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2026-02-01"))
        end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

        # Apply Filters
        mask = (df["date"].dt.date >= start_date) & \
               (df["date"].dt.date <= end_date) & \
               (df["user"].isin(selected_users))
        filtered_df = df[mask]

        # --- METRICS ---
        total_income = filtered_df[filtered_df["type"] == "Income"]["cost"].sum()
        total_expense = filtered_df[filtered_df["type"] == "Expense"]["cost"].sum()
        balance = total_income - total_expense

        col1, col2, col3 = st.columns(3)
        col1.metric("Income", f"£{total_income:,.2f}", delta="In")
        col2.metric("Expense", f"£{total_expense:,.2f}", delta="-Out")
        col3.metric("Net Balance", f"£{balance:,.2f}", delta="Remaining")

        # --- SAVINGS GOALS (RESTORED!) ---
        st.divider()
        st.subheader("🎯 Savings Goals")
        
        # Slider (Default 33%)
        savings_rate = st.slider("Target Savings Rate (%)", 0, 100, 33)
        
        # The Math
        if balance > 0:
            savings_amount = balance * (savings_rate / 100)
            spending_money = balance - savings_amount
        else:
            savings_amount = 0
            spending_money = 0

        st.caption(f"If you save {savings_rate}%, here is your split:")
        c_save, c_spend = st.columns(2)
        c_save.metric("🏦 To Save/Invest", f"£{savings_amount:,.2f}", delta="Target")
        c_spend.metric("💸 Safe to Spend", f"£{spending_money:,.2f}", delta="Allowance")

        st.divider()

        # --- ADVANCED VISUALS (PLOTLY) ---
        expenses_only = filtered_df[filtered_df["type"] == "Expense"]
        
        if not expenses_only.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Spending by Category")
                fig_pie = px.pie(expenses_only, values='cost', names='category', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

            with c2:
                st.subheader("Daily Spending Trend")
                daily_spend = expenses_only.groupby("date")["cost"].sum().reset_index()
                fig_line = px.bar(daily_spend, x='date', y='cost')
                st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No expenses found for this selection.")

    except Exception as e:
        st.info("👋 Welcome! Add your first transaction in the sidebar.")

with tab2:
    # --- MANAGE DATA LOGIC ---
    st.header("📝 Recent Transactions")
    try:
        full_df = load_data()
        st.dataframe(full_df.sort_values(by="id", ascending=False), use_container_width=True)

        st.divider()
        st.subheader("🗑️ Delete a Mistake")
        
        if not full_df.empty:
            options = full_df.apply(lambda x: f"ID: {x['id']} | {x['user']} | {x['item']} | £{x['cost']}", axis=1)
            selected_option = st.selectbox("Select transaction to delete:", options)
            
            if st.button("Delete Transaction"):
                row_id = int(selected_option.split("|")[0].replace("ID:", "").strip())
                delete_data(row_id)
                st.success("Deleted! Refreshing...")
                st.experimental_rerun()
        else:
            st.write("No data to delete.")
            
    except Exception as e:
        st.write("No data available yet.")