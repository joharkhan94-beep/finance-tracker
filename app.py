import streamlit as st
import google.generativeai as genai
import json
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEETS SETUP ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_google_sheet():
    """Connects to the Google Sheet using secrets."""
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], SCOPE)
        client = gspread.authorize(creds)
        return client.open("Finance Tracker").sheet1
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

st.set_page_config(page_title="Family Finance Tracker", page_icon="💰", layout="wide")
st.title("💰 Family Finance Tracker")

# --- DATABASE FUNCTIONS ---
# --- DATABASE FUNCTIONS (Google Sheets Edition) ---

def load_data():
    """Fetches all data from the Google Sheet."""
    sheet = get_google_sheet()
    if sheet:
        # Get all records as a list of dictionaries
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        # Cleanup types if data exists
        if not df.empty:
            # Convert Cost to numbers (handle potential currency symbols)
            df['Cost'] = pd.to_numeric(df['Cost'].astype(str).str.replace('£', ''), errors='coerce')
            # Convert Date to proper datetime format
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df
    return pd.DataFrame()

def ai_parse(text):
    """Sends text to Gemini and gets structured data back."""
    try:
        # 1. Setup the Brain
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-2.5-flash') # Fast & Smart

        # 2. The Prompt (Instructions)
        prompt = f"""
        You are a financial assistant. Extract transaction details from: "{text}".
        Return ONLY a JSON object with these keys:
        - "item": short description (string)
        - "amount": number (positive)
        - "category": choose strictly from [Food, Transport, Bills, Shopping, Entertainment, Health, Income]
        - "type": "Income" or "Expense"
        - "date": YYYY-MM-DD (assume today is {pd.Timestamp.now().strftime('%Y-%m-%d')} if not specified)
        """
        
        # 3. Get Response
        response = model.generate_content(prompt)
        
        # 4. Clean & Return Data
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_text)
        
    except Exception as e:
        return {"error": str(e)}

def save_data(date, category, item, cost, type_, user):
    """Appends a new row to the Google Sheet."""
    try:
        sheet = get_google_sheet()
        if sheet:
            # Convert date to string
            date_str = date.strftime("%Y-%m-%d")
            
            # Append row in the EXACT order of your Sheet columns:
            # Date | Type | Category | Item | Cost | User
            sheet.append_row([date_str, type_, category, item, float(cost), user])
            
            st.success("✅ Saved to Google Sheets!")
            # Clear cache so the new transaction shows up instantly
            st.cache_data.clear()
    except Exception as e:
        st.error(f"Error saving data: {e}")

def delete_row(row_index):
    """Deletes a specific row from Google Sheets."""
    try:
        sheet = get_google_sheet()
        if sheet:
            # Google Sheets is "1-indexed" (starts at 1)
            # Row 1 is Headers. So Index 0 in Python = Row 2 in Sheets.
            sheet_row_number = row_index + 2 
            
            sheet.delete_rows(sheet_row_number)
            
            st.toast("🗑️ Transaction Deleted!", icon="✅")
            st.cache_data.clear() # Force reload so the row disappears
    except Exception as e:
        st.error(f"Could not delete: {e}")

st.header("🤖 AI Assistant")
ai_input = st.text_input("Tell me what you spent:", placeholder="e.g., £15 on Nando's")
    
if st.button("✨ Process with AI"):
        with st.spinner("Thinking..."):
            data = ai_parse(ai_input)
            
            if "error" not in data:
                # Auto-fill the form logic would go here, but for now let's just save it!
                new_row = pd.DataFrame([{
                    "Date": data['date'],
                    "Type": data['type'],
                    "Category": data['category'],
                    "Item": data['item'],
                    "Cost": float(data['amount']),
                    "User": "AI-Added" # We can change this later
                }])
                
                # Add to Google Sheets
                sheet = get_google_sheet()
                sheet.append_row(new_row.iloc[0].tolist())
                
                st.success(f"✅ Saved: {data['item']} (£{data['amount']})")
                st.cache_data.clear() # Refresh data
                st.rerun()
            else:
                st.error(f"Error details: {data['error']}")
    
st.divider() # Adds a nice line separator
    
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
    df = load_data()
    
    if not df.empty:
        # 1. CLEAN DATA (Crucial for Google Sheets!)
        # Convert 'Cost' to numbers (remove £ symbols if any)
        df['Cost'] = pd.to_numeric(df['Cost'].astype(str).str.replace('£', ''), errors='coerce')
        # Convert 'Date' to datetime objects
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # 2. DATE FILTER
        st.write("### 🗓️ Filter")
        col_date1, col_date2 = st.columns(2)
        start_date = col_date1.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
        end_date = col_date2.date_input("End Date", value=pd.to_datetime("today"))
        
        # Apply Filter
        mask = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
        filtered_df = df[mask]
        
        # 3. METRICS
        total_income = filtered_df[filtered_df['Type'] == "Income"]['Cost'].sum()
        total_expense = filtered_df[filtered_df['Type'] == "Expense"]['Cost'].sum()
        balance = total_income - total_expense
        
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Income", f"£{total_income:,.2f}")
        m2.metric("Total Expense", f"£{total_expense:,.2f}")
        m3.metric("Net Balance", f"£{balance:,.2f}")
        
        # 4. SAVINGS GOAL (Restored!)
        st.divider()
        st.subheader("🎯 Savings Goal")
        
        # Slider for goal setting
        goal_target = st.slider("Set your Goal (£)", min_value=1000, max_value=50000, value=5000, step=500)
        
        # Calculate Progress
        if goal_target > 0:
            progress = min(max(balance / goal_target, 0.0), 1.0)
            st.progress(progress)
            st.write(f"You have saved **£{balance:,.2f}** of your **£{goal_target:,.0f}** goal!")
        
        # 5. CHARTS
        st.divider()
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Expenses by Category")
            expenses_only = filtered_df[filtered_df['Type'] == "Expense"]
            if not expenses_only.empty:
                fig_pie = px.pie(expenses_only, values='Cost', names='Category', hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No expenses in this period.")

        with c2:
            st.subheader("Income vs Expense")
            grouped = filtered_df.groupby("Type")['Cost'].sum().reset_index()
            fig_bar = px.bar(grouped, x="Type", y="Cost", color="Type", text_auto='.2s')
            st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info("Add your first transaction in the sidebar to generate data!")

with tab2:
    st.header("📝 Manage Data")
    
    # 1. Show the Data
    st.dataframe(df, use_container_width=True)
    
    # 2. Delete Section
    st.divider()
    st.subheader("🗑️ Delete a Transaction")
    
    if not df.empty:
        # Create a list of options that look like: "Index: 0 | 2024-02-08 | Coffee | £3.50"
        # We need the 'Index' to know which row to delete in Google Sheets
        delete_options = [
            f"Row {i+1}: {row['Date'].date()} - {row['Category']} - £{row['Cost']} ({row['User']})" 
            for i, row in df.iterrows()
        ]
        
        # User selects an item to delete
        selected_option = st.selectbox("Select Transaction to Remove", delete_options)
        
        # Find the index (number) of the selected item
        if st.button("Delete Selected Transaction", type="primary"):
            # Extract the index from the list selection
            index_to_delete = delete_options.index(selected_option)
            
            # Call the delete function
            delete_row(index_to_delete)
            st.rerun() # Refresh the app immediately
    else:
        st.info("No transactions to delete.")