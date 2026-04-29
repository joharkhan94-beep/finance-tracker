import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import plotly.express as px
from supabase import create_client
from datetime import datetime

# --- SUPABASE SETUP ---

def get_supabase():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

st.set_page_config(page_title="FinanceAI", page_icon="◈", layout="wide")

# --- VISUAL HELPERS ---

def inject_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
        }

        /* Page background */
        .stApp {
            background-color: #0a0e1a !important;
        }

        /* Main content area */
        .main .block-container {
            background-color: #0a0e1a !important;
            padding-top: 1.5rem;
        }

        /* Sidebar background */
        [data-testid="stSidebar"] {
            background-color: #0d1117 !important;
            border-right: 1px solid #1e2d4a;
        }
        [data-testid="stSidebar"] > div:first-child {
            background-color: #0d1117 !important;
        }

        /* Text colours */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
            color: #f9fafb !important;
        }

        /* Section headings */
        h2, h3 {
            border-left: 3px solid #f59e0b;
            padding-left: 10px;
            font-family: 'Inter', sans-serif;
        }

        /* Suppress default st.metric (replaced with custom cards) */
        [data-testid="metric-container"] {
            display: none !important;
        }

        /* Tab bar */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #111827 !important;
            border-radius: 8px 8px 0 0;
            gap: 0;
        }
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            color: #9ca3af !important;
            border: none !important;
            padding: 0.6rem 1.4rem !important;
            font-weight: 500;
        }
        .stTabs [aria-selected="true"] {
            color: #f59e0b !important;
            border-bottom: 2px solid #f59e0b !important;
            background-color: transparent !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: #f59e0b !important;
            color: #0a0e1a !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
        }
        .stButton > button:hover {
            background-color: #d97706 !important;
            color: #0a0e1a !important;
        }

        /* Primary button */
        .stButton > button[kind="primary"] {
            background-color: #f59e0b !important;
            color: #0a0e1a !important;
        }

        /* Secondary / cancel button */
        .stButton > button[kind="secondary"] {
            background-color: #1e2d4a !important;
            color: #f9fafb !important;
        }
        .stButton > button[kind="secondary"]:hover {
            background-color: #263d5e !important;
        }

        /* Input fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            background-color: #111827 !important;
            color: #f9fafb !important;
            border: 1px solid #1e2d4a !important;
            border-radius: 6px !important;
        }
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: #f59e0b !important;
            box-shadow: 0 0 0 2px rgba(245,158,11,0.2) !important;
        }

        /* Date input dark theme (baseweb overrides) */
        input[type="text"],
        input[type="number"],
        input[type="date"],
        .stDateInput input,
        div[data-baseweb="input"] input,
        div[data-baseweb="base-input"] input {
            background-color: #111827 !important;
            color: #f9fafb !important;
            border: 1px solid #1e2d4a !important;
            border-radius: 8px !important;
        }

        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {
            background-color: #111827 !important;
            border: 1px solid #1e2d4a !important;
        }

        /* Selectbox */
        .stSelectbox > div > div {
            background-color: #111827 !important;
            color: #f9fafb !important;
            border: 1px solid #1e2d4a !important;
            border-radius: 6px !important;
        }

        /* Radio */
        .stRadio label {
            color: #f9fafb !important;
        }

        /* Slider */
        .stSlider > div[data-baseweb="slider"] > div {
            background-color: #1e2d4a !important;
        }

        /* Dataframe */
        .stDataFrame {
            background-color: #111827 !important;
            border-radius: 8px;
            border: 1px solid #1e2d4a;
        }

        /* Dividers */
        hr {
            border-color: #1e2d4a !important;
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0a0e1a; }
        ::-webkit-scrollbar-thumb { background: #f59e0b; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #d97706; }

        /* Info / warning / success boxes */
        .stAlert {
            background-color: #111827 !important;
            border-color: #1e2d4a !important;
            color: #f9fafb !important;
        }

        /* Form containers */
        [data-testid="stForm"] {
            background-color: #111827 !important;
            border: 1px solid rgba(245,158,11,0.25) !important;
            border-radius: 10px !important;
            padding: 1rem !important;
        }

        /* Caption text */
        .stCaption, small {
            color: #9ca3af !important;
        }

        /* Toggle */
        .stToggle label {
            color: #f9fafb !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, delta=None, icon="", prefix="£"):
    """Renders a styled dark card replacing st.metric()."""
    formatted_value = f"{prefix}{value:,.2f}"

    if delta is not None:
        if delta >= 0:
            delta_html = (
                f'<div style="margin-top:8px;">'
                f'<span style="background:#064e3b;color:#10b981;padding:3px 10px;'
                f'border-radius:20px;font-size:0.78rem;font-weight:600;">'
                f'▲ {prefix}{abs(delta):,.2f}</span></div>'
            )
        else:
            delta_html = (
                f'<div style="margin-top:8px;">'
                f'<span style="background:#450a0a;color:#ef4444;padding:3px 10px;'
                f'border-radius:20px;font-size:0.78rem;font-weight:600;">'
                f'▼ {prefix}{abs(delta):,.2f}</span></div>'
            )
    else:
        delta_html = ""

    st.markdown(
        f"""
        <div style="background:#111827;border:1px solid #1e2d4a;border-radius:12px;
                    padding:24px;width:100%;box-sizing:border-box;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
                <span style="font-size:16px;line-height:1;">{icon}</span>
                <span style="color:#9ca3af;font-size:13px;font-weight:500;text-transform:uppercase;letter-spacing:0.05em;">{label}</span>
            </div>
            <div style="color:#f9fafb;font-size:1.75rem;font-weight:700;line-height:1.2;">
                {formatted_value}
            </div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_figure(fig):
    """Applies the dark navy/gold theme to any Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#f9fafb"),
        colorway=["#f59e0b", "#3b82f6", "#ef4444", "#10b981", "#8b5cf6", "#06b6d4"],
        margin=dict(l=0, r=0, t=30, b=0),
    )
    fig.update_xaxes(gridcolor="#1e2d4a", zerolinecolor="#1e2d4a")
    fig.update_yaxes(gridcolor="#1e2d4a", zerolinecolor="#1e2d4a")
    return fig


# Inject CSS immediately after page config
inject_custom_css()

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

def generate_insights(summary_text):
    """Calls Gemini with a spending summary and returns 3 plain-English insights."""
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    prompt = (
        "You are a personal finance assistant. Given this spending summary, "
        "provide 3 concise, specific insights in plain English. Each insight should "
        "be one sentence. Focus on patterns, anomalies, or actionable observations. "
        "Do not use bullet points — number them 1, 2, 3. Be direct and specific "
        f"with numbers from the data.\n\n{summary_text}"
    )
    response = model.generate_content(prompt)
    return response.text.strip()

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

# --- SIDEBAR REDESIGN ---
with st.sidebar:
    # Logo + tagline
    st.markdown(
        """
        <div style="padding:1rem 0 0.5rem 0;">
            <div style="font-size:1.6rem;font-weight:700;color:#f9fafb;font-family:'Inter',sans-serif;
                        letter-spacing:-0.5px;">
                <span style="color:#f59e0b;">◈</span>&nbsp;FinanceAI
            </div>
            <div style="font-size:0.78rem;color:#9ca3af;margin-top:2px;">Powered by Gemini</div>
        </div>
        <hr style="border:none;border-top:1px solid #f59e0b;margin:0.5rem 0 1rem 0;">
        """,
        unsafe_allow_html=True,
    )

    # Filters section label
    st.markdown(
        '<p style="color:#f59e0b;font-size:0.7rem;font-weight:700;letter-spacing:1.5px;'
        'text-transform:uppercase;margin-bottom:4px;">Filters</p>',
        unsafe_allow_html=True,
    )
    user = st.selectbox("Filter / User", ["All", "Me", "Partner", "Joint"], label_visibility="collapsed")
    demo_mode = st.toggle("Enable Demo Mode", value=False)
    st.divider()

st.markdown(
    '<h2 style="color:#f9fafb;font-weight:700;margin-bottom:0.25rem;">AI Assistant</h2>',
    unsafe_allow_html=True,
)

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
            """<div style="background:#111827;border-left:4px solid #f59e0b;padding:0.6rem 1rem;"""
            """border-radius:4px;margin-bottom:0.75rem;border:1px solid #1e2d4a;">"""
            """<strong style="color:#f59e0b;">🤖 AI Parsed — Review & Confirm</strong>&nbsp;&nbsp;"""
            """<span style="font-size:0.85rem;color:#9ca3af">Edit any field before saving.</span>"""
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
st.sidebar.markdown(
    '<p style="color:#f59e0b;font-size:0.7rem;font-weight:700;letter-spacing:1.5px;'
    'text-transform:uppercase;margin:0.5rem 0 4px 0;">Add Entry</p>',
    unsafe_allow_html=True,
)
with st.sidebar.form("expense_form"):
    st.markdown("**➕ Add Transaction**")
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

# Last synced footer
_last_synced = st.session_state.get("last_synced", datetime.now().strftime("%H:%M:%S"))
st.session_state["last_synced"] = _last_synced
st.sidebar.markdown(
    f'<p style="color:#4b5563;font-size:0.72rem;margin-top:1.5rem;padding-top:0.5rem;'
    f'border-top:1px solid #1e2d4a;">Last synced: {_last_synced}</p>',
    unsafe_allow_html=True,
)

# --- TABS LAYOUT ---
tab1, tab2 = st.tabs(["Dashboard", "Manage Data"])

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
        st.write("### Filter")
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
        with m1:
            render_metric_card("Total Income", total_income, icon="💰")
        with m2:
            render_metric_card("Total Expenses", total_expense, icon="📉")
        with m3:
            render_metric_card("Net Balance", balance, delta=balance, icon="⚖️")

        # --- AI INSIGHTS ---
        if not filtered_df.empty:
            st.divider()
            st.markdown(
                '<p style="color:#f59e0b;font-size:0.7rem;font-weight:700;letter-spacing:1.5px;'
                'text-transform:uppercase;margin-bottom:4px;">AI Insights</p>',
                unsafe_allow_html=True,
            )
            if st.button("✦ Generate Insights", key="gen_insights_btn"):
                _top_cats = (
                    filtered_df[filtered_df["type"] == "Expense"]
                    .groupby("category")["cost"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(3)
                )
                _top_cats_str = ", ".join(
                    f"{cat} (£{amt:,.2f})" for cat, amt in _top_cats.items()
                ) or "none"
                _summary = (
                    f"Date range: {start_date} to {end_date}. "
                    f"Transactions: {len(filtered_df)}. "
                    f"Total income: £{total_income:,.2f}. "
                    f"Total expenses: £{total_expense:,.2f}. "
                    f"Net balance: £{balance:,.2f}. "
                    f"Top 3 spending categories: {_top_cats_str}."
                )
                with st.spinner("Generating insights..."):
                    try:
                        insight_text = generate_insights(_summary)
                        st.session_state["ai_insights"] = insight_text
                    except Exception as e:
                        st.error(f"Gemini error: {type(e).__name__}: {str(e)}")
                        st.stop()

            if "ai_insights" in st.session_state:
                st.markdown(
                    f'<div style="background:#111827;border:1px solid #1e2d4a;border-radius:12px;'
                    f'padding:24px;margin-top:0.5rem;">'
                    f'<div style="color:#f59e0b;font-size:1rem;font-weight:700;margin-bottom:12px;">'
                    f'✦ AI Insights</div>'
                    f'<div style="color:#f9fafb;font-size:0.95rem;line-height:1.7;white-space:pre-wrap;">'
                    f'{st.session_state["ai_insights"]}</div>'
                    f'<div style="color:#4b5563;font-size:0.75rem;margin-top:12px;">'
                    f'Generated by Gemini 2.5 Flash</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.divider()
        st.subheader("Savings vs. Spending Split")

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
                style_figure(fig_pie)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expenses in this period.")

        with c2:
            st.subheader("Income vs Expense")
            grouped = filtered_df.groupby("type")['cost'].sum().reset_index()
            if not grouped.empty:
                fig_bar = px.bar(grouped, x="type", y="cost", color="type", text_auto='.2s')
                style_figure(fig_bar)
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("No data in this period.")

        # SPENDING TREND
        st.divider()
        st.subheader("Spending Trend")

        expenses_df   = filtered_df[filtered_df["type"] == "Expense"]
        daily_expense = expenses_df.groupby("date")["cost"].sum().reset_index()

        if not daily_expense.empty:
            fig_trend = px.line(daily_expense, x="date", y="cost", markers=True, title="Daily Spending Over Time")
            style_figure(fig_trend)
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("No expenses found in this date range.")

        # MONTHLY BREAKDOWN
        st.divider()
        st.subheader("Monthly Breakdown")
        _monthly = filtered_df.copy()
        _monthly["_period"] = _monthly["date"].dt.to_period("M")
        _n_months = _monthly["_period"].nunique()

        if _n_months < 2:
            st.caption(
                "Add more transactions across multiple months to see your monthly breakdown."
            )
        else:
            _inc_m  = _monthly[_monthly["type"] == "Income"].groupby("_period")["cost"].sum()
            _exp_m  = _monthly[_monthly["type"] == "Expense"].groupby("_period")["cost"].sum()
            _periods = sorted(_monthly["_period"].unique())

            _mb_rows = []
            for _p in _periods:
                _inc = float(_inc_m.get(_p, 0.0))
                _exp = float(_exp_m.get(_p, 0.0))
                _mb_rows.append({
                    "Month":    _p.strftime("%b %Y"),
                    "Income":   _inc,
                    "Expenses": _exp,
                    "Net":      _inc - _exp,
                })
            _mb_df = pd.DataFrame(_mb_rows)
            _mb_df["MoM Change (£)"] = _mb_df["Expenses"].diff()
            _mb_df["MoM (%)"]        = _mb_df["Expenses"].pct_change() * 100

            # Grouped bar chart — Income vs Expenses per month
            _melt = _mb_df.melt(
                id_vars=["Month"],
                value_vars=["Income", "Expenses"],
                var_name="Type",
                value_name="Amount",
            )
            _fig_monthly = px.bar(
                _melt,
                x="Month",
                y="Amount",
                color="Type",
                barmode="group",
                color_discrete_map={"Income": "#3b82f6", "Expenses": "#ef4444"},
                title="Monthly Income vs Expenses",
            )
            style_figure(_fig_monthly)
            st.plotly_chart(_fig_monthly, use_container_width=True)

            # Summary table — highlight net-negative months in red
            def _hl_neg_net(row):
                styles = [""] * len(row)
                net_pos = list(row.index).index("Net")
                if row["Net"] < 0:
                    styles[net_pos] = "background-color:#450a0a;color:#ef4444;"
                return styles

            _fmt = {
                "Income":         "£{:,.2f}",
                "Expenses":       "£{:,.2f}",
                "Net":            "£{:,.2f}",
                "MoM Change (£)": lambda x: f"£{x:,.2f}" if pd.notna(x) else "—",
                "MoM (%)":        lambda x: f"{x:+.1f}%" if pd.notna(x) else "—",
            }
            _styled = _mb_df.style.apply(_hl_neg_net, axis=1).format(_fmt)
            st.dataframe(_styled, hide_index=True, use_container_width=True)

        # RECENT TRANSACTIONS
        st.subheader("Recent Transactions")
        recent_items = filtered_df.sort_values(by="date", ascending=False).head(5)
        st.dataframe(
            recent_items[["date", "category", "item", "cost", "type"]],
            hide_index=True,
            use_container_width=True,
        )

with tab2:
    st.header("Manage Data")

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

        st.divider()
        st.download_button(
            label="⬇ Export to CSV",
            data=df.to_csv(index=False),
            file_name="financeai_export.csv",
            mime="text/csv",
        )
