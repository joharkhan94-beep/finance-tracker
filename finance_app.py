import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import plotly.express as px
from supabase import create_client

# --- SUPABASE SETUP ---

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.set_page_config(page_title="Finance Tracker", page_icon="💰", layout="wide")
st.title("💰 Finance Tracker")

def get_demo_data():
    """Generates fake data for testing."""
    return pd.DataFrame([
        {"id": -1, "date": pd.Timestamp("2026-02-01"), "item": "Software Project",  "cost": 3500.00, "category": "Income",        "type": "Income",  "user": "Me"},
        {"id": -2, "date": pd.Timestamp("2026-02-02"), "item": "Grocery Run",        "cost":   45.20, "category": "Food",          "type": "Expense", "user": "Joint"},
        {"id": -3, "date": pd.Timestamp("2026-02-03"), "item": "Uber to Client",     "cost":   12.50, "category": "Transport",     "type": "Expense", "user": "Me"},
        {"id": -4, "date": pd.Timestamp("2026-02-04"), "item": "Coffee",             "cost":    3.50, "category": "Food",          "type": "Expense", "user": "Partner"},
        {"id": -5, "date": pd.Timestamp("2026-02-05"), "item": "Gym Membership",     "cost":   30.00, "category": "Health",        "type": "Expense", "user": "Me"},
        {"id": -6, "date": pd.Timestamp("2026-02-06"), "item": "Netflix",            "cost":   10.00, "category": "Entertainment", "type": "Expense", "user": "Joint"},
    ])

# --- DATABASE FUNCTIONS ---

def load_data():
    """Fetches all transactions from Supabase, ordered newest-first."""
    try:
        response = get_supabase().table("transactions").select("*").order("date", desc=True).execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['cost'] = pd.to_numeric(df['cost'], errors='coerce')
            df['date'] = pd.to_datetime(df['date'],  errors='coerce')
        return df
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame()

def ai_parse(text):
    """Sends text to Gemini and gets structured data back."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
        You are a financial assistant. Extract transaction details from: "{text}".
        Return ONLY a JSON object with these keys:
        - "item": short description (string)
        - "amount": number (positive)
        - "category": choose strictly from [Food, Transport, Bills, Shopping, Entertainment, Health, Income]
        - "type": "Income" or "Expense"
        - "date": YYYY-MM-DD (assume today is {pd.Timestamp.now().strftime('%Y-%m-%d')} if not specified)
        """
        response = model.generate_content(prompt)
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_text)
    except Exception as e:
        return {"error": str(e)}

def save_data(date, category, item, cost, type_, user):
    """Inserts a new transaction into Supabase."""
    try:
        get_supabase().table("transactions").insert({
            "date":     date.strftime("%Y-%m-%d"),
            "type":     type_,
            "category": category,
            "item":     item,
            "cost":     float(cost),
            "user":     user,
        }).execute()
        st.success("✅ Saved!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def delete_transaction(row_id):
    """Deletes a transaction by its Supabase id."""
    try:
        get_supabase().table("transactions").delete().eq("id", row_id).execute()
        st.toast("🗑️ Transaction deleted.", icon="✅")
    except Exception as e:
        st.error(f"Could not delete: {e}")

# --- SIDEBAR TOGGLE ---
with st.sidebar:
    st.header("⚙️ Settings")
    user = st.sidebar.selectbox("Filter / User", ["All", "Me", "Partner", "Joint"])
    demo_mode = st.toggle("Enable Demo Mode", value=False)
    st.divider()

st.header("🤖 AI Assistant")

_CATEGORIES = ["Food", "Transport", "Bills", "Shopping", "Entertainment", "Health", "Income"]

if "pending_tx" not in st.session_state:
    ai_input = st.text_input("Tell me what you spent:", placeholder="e.g., £15 on Nando's")

    if st.button("✨ Process with AI"):
        with st.spinner("Thinking..."):
            data = ai_parse(ai_input)
            if "error" not in data:
                st.session_state["pending_tx"] = data
                st.rerun()
            else:
                st.error(f"Error details: {data['error']}")

else:
    tx = st.session_state["pending_tx"]

    with st.container(border=True):
        st.markdown(
            """<div style="background:#e8f5e9;border-left:4px solid #43a047;padding:0.6rem 1rem;"""
            """border-radius:4px;margin-bottom:0.75rem">"""
            """<strong>🤖 AI Parsed — Review & Confirm</strong>&nbsp;&nbsp;"""
            """<span style="font-size:0.85rem;color:#555">Edit any field before saving.</span>"""
            """</div>""",
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        try:
            default_date = pd.to_datetime(tx["date"]).date()
        except Exception:
            default_date = pd.Timestamp.now().date()

        confirmed_date     = col1.date_input("Date", value=default_date)
        confirmed_item     = col2.text_input("Description", value=tx.get("item", ""))
        confirmed_amount   = col1.number_input(
            "Amount (£)", value=float(tx.get("amount", 0.0)), min_value=0.0, format="%.2f"
        )

        ai_cat             = tx.get("category", "Food")
        cat_index          = _CATEGORIES.index(ai_cat) if ai_cat in _CATEGORIES else 0
        confirmed_category = col2.selectbox("Category", _CATEGORIES, index=cat_index)

        ai_type            = tx.get("type", "Expense")
        confirmed_type     = st.radio(
            "Type", ["Expense", "Income"], index=1 if ai_type == "Income" else 0, horizontal=True
        )

        _user_options  = ["Me", "Partner", "Joint"]
        _default_user  = user if user != "All" else "Joint"
        confirmed_user = st.selectbox(
            "User",
            _user_options,
            index=_user_options.index(_default_user) if _default_user in _user_options else 2,
        )

        st.divider()
        btn_save, btn_cancel = st.columns([2, 1])

        if btn_save.button("✅ Confirm & Save", type="primary", use_container_width=True):
            if not demo_mode:
                save_data(confirmed_date, confirmed_category, confirmed_item, confirmed_amount, confirmed_type, confirmed_user)
                st.toast(f"✅ Saved: {confirmed_item}")
            else:
                st.toast(f"🎉 [DEMO] Would save '{confirmed_item}' for £{confirmed_amount:.2f}")
            del st.session_state["pending_tx"]
            st.rerun()

        if btn_cancel.button("✖ Cancel", use_container_width=True):
            del st.session_state["pending_tx"]
            st.rerun()

st.divider()

# --- SIDEBAR: ADD TRANSACTION ---
with st.sidebar.form("expense_form"):
    st.sidebar.header("➕ Add Transaction")
    type_     = st.radio("Type", ["Expense", "Income"], horizontal=True)
    new_date  = st.date_input("Date")
    new_cat   = st.selectbox("Category", _CATEGORIES)
    new_item  = st.text_input("Description (e.g. Pizza)")
    new_cost  = st.number_input("Amount (£)", min_value=0.0, format="%.2f")
    _user_options = ["Me", "Partner", "Joint"]
    _default  = user if user in _user_options else "Me"
    new_user  = st.selectbox("User", _user_options, index=_user_options.index(_default))

    if st.form_submit_button("Save Transaction"):
        save_data(new_date, new_cat, new_item, new_cost, type_, new_user)
        st.rerun()

# --- TABS LAYOUT ---
tab1, tab2 = st.tabs(["📊 Dashboard", "📝 Manage Data"])

# --- DATA LOADING ---
if demo_mode:
    st.warning("⚠️ You are in DEMO MODE. Data is fake and not saved.")
    df = get_demo_data()
else:
    try:
        df = load_data()
    except Exception:
        st.error("Could not load data.")
        st.stop()

with tab1:
    # --- DASHBOARD LOGIC ---
    total_income  = 0
    total_expense = 0
    filtered_df   = pd.DataFrame()

    if not df.empty:
        # DATE FILTER
        st.write("### 🗓️ Filter")
        col_date1, col_date2 = st.columns(2)
        start_date = col_date1.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
        end_date   = col_date2.date_input("End Date",   value=pd.to_datetime("today"))

        mask        = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        filtered_df = df[mask]

        if user != "All":
            filtered_df = filtered_df[filtered_df["user"] == user]

        # METRICS
        total_income  = filtered_df[filtered_df['type'] == "Income"]['cost'].sum()
        total_expense = filtered_df[filtered_df['type'] == "Expense"]['cost'].sum()
        balance       = total_income - total_expense

        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Income",   f"£{total_income:,.2f}")
        m2.metric("Total Expense",  f"£{total_expense:,.2f}")
        m3.metric("Net Balance",    f"£{balance:,.2f}")

        st.divider()
        st.subheader("⚖️ Savings vs. Spending Split")

    net_balance = total_income - total_expense

    if net_balance > 0:
        savings_rate    = st.slider("Target Savings Rate (%)", min_value=0, max_value=100, value=30, format="%d%%")
        savings_amount  = net_balance * (savings_rate / 100)
        spending_amount = net_balance - savings_amount

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"🏦 **Save / Invest**\n# £{savings_amount:,.2f}")
        with c2:
            st.success(f"💸 **Safe to Spend**\n# £{spending_amount:,.2f}")

        st.caption(
            f"If you save **{savings_rate}%** of your remaining £{net_balance:,.2f}, "
            f"you have **£{spending_amount:,.2f}** left for guilt-free spending."
        )
    else:
        st.warning(f"⚠️ Your balance is negative (-£{abs(net_balance):,.2f}). You need a positive balance to start saving!")

    # CHARTS
    st.divider()

    if filtered_df.empty:
        st.info("No transactions found. Add one above or adjust the date filter.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Expenses by Category")
            expenses_only = filtered_df[filtered_df['type'] == "Expense"]
            if not expenses_only.empty:
                fig_pie = px.pie(expenses_only, values='cost', names='category', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expenses in this period.")

        with c2:
            st.subheader("Income vs Expense")
            grouped = filtered_df.groupby("type")['cost'].sum().reset_index()
            if not grouped.empty:
                fig_bar = px.bar(grouped, x="type", y="cost", color="type", text_auto='.2s')
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No data in this period.")

        # SPENDING TREND
        st.divider()
        st.subheader("📈 Spending Trend")

        expenses_df   = filtered_df[filtered_df["type"] == "Expense"]
        daily_expense = expenses_df.groupby("date")["cost"].sum().reset_index()

        if not daily_expense.empty:
            fig_trend = px.line(daily_expense, x="date", y="cost", markers=True, title="Daily Spending Over Time")
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No expenses found in this date range.")

        # RECENT TRANSACTIONS
        st.subheader("🕒 Recent Transactions")
        recent_items = filtered_df.sort_values(by="date", ascending=False).head(5)
        st.dataframe(
            recent_items[["date", "category", "item", "cost", "type"]],
            hide_index=True,
            use_container_width=True,
        )

with tab2:
    st.header("📝 Manage Data")

    if df.empty:
        st.info("No transactions yet.")
    else:
        # Column header row
        h = st.columns([1.4, 1.2, 2.8, 1.6, 1.2, 1.2, 0.6])
        for col, label in zip(h, ["Date", "Type", "Item", "Category", "Cost", "User", ""]):
            col.markdown(f"**{label}**")

        st.divider()

        for _, row in df.iterrows():
            cols = st.columns([1.4, 1.2, 2.8, 1.6, 1.2, 1.2, 0.6])
            cols[0].write(row['date'].date() if pd.notna(row['date']) else "—")
            cols[1].write(row['type'])
            cols[2].write(row['item'])
            cols[3].write(row['category'])
            cols[4].write(f"£{row['cost']:,.2f}")
            cols[5].write(row['user'])
            if not demo_mode and cols[6].button("🗑️", key=f"del_{row['id']}"):
                delete_transaction(row['id'])
                st.rerun()
