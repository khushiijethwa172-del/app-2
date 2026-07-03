# ==========================================================
# AI Insurance Claim Fraud Detection &
# Global Insurance Stock Market Dashboard
# Developed using Streamlit + Yahoo Finance + Plotly
# ==========================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="🛡️ AI Insurance Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Poppins',sans-serif;
}

.main{
    background:#F8FAFC;
}

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.title{
    font-size:42px;
    font-weight:bold;
    color:#0F172A;
}

.metric-card{
    background:white;
    border-radius:15px;
    padding:20px;
    border:1px solid #E2E8F0;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
}

.metric-title{
    color:#64748B;
    font-size:14px;
}

.metric-value{
    font-size:32px;
    font-weight:bold;
    color:#1E293B;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""",unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.markdown(
"""
<div class="title">
🛡️ AI Insurance Claim Fraud Detection &
Global Insurance Stock Market Dashboard
</div>
""",
unsafe_allow_html=True
)

st.write(
"""
This dashboard provides

✅ Live Global Insurance Stock Market

✅ Fraud Claim Analytics

✅ Risk Insights

✅ Interactive Charts

✅ Premium Dashboard UI
"""
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("⚙ Dashboard Settings")

companies={
    "Berkshire Hathaway":"BRK-B",
    "AIG":"AIG",
    "Allianz":"ALV.DE",
    "MetLife":"MET",
    "Prudential":"PRU",
    "Ping An":"2318.HK",
    "AXA":"CS.PA"
}

company=st.sidebar.selectbox(
    "Select Insurance Company",
    list(companies.keys())
)

ticker=companies[company]

period=st.sidebar.selectbox(
    "Select Time Period",
    [
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("Live Yahoo Finance Data")

# ---------------- FETCH STOCK ----------------

@st.cache_data
def load_stock(symbol,period):

    stock=yf.Ticker(symbol)

    hist=stock.history(period=period)

    info=stock.info

    return hist,info

try:

    history,info=load_stock(ticker,period)

    if history.empty:

        st.error("No Stock Data Available")

        st.stop()

except Exception as e:

    st.error(e)

    st.stop()
  # ---------------- LIVE STOCK METRICS ----------------

current_price = info.get("regularMarketPrice", history["Close"].iloc[-1])

previous_close = info.get(
    "regularMarketPreviousClose",
    history["Close"].iloc[-2] if len(history) > 1 else current_price
)

currency = info.get("currency", "USD")

market_cap = info.get("marketCap", 0)

pe_ratio = info.get("trailingPE", None)

day_high = info.get("dayHigh", current_price)

day_low = info.get("dayLow", current_price)

change = current_price - previous_close

change_percent = (change / previous_close) * 100 if previous_close else 0

col1,col2,col3,col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Current Price",
        f"{current_price:.2f} {currency}",
        f"{change:.2f} ({change_percent:.2f}%)"
    )

with col2:

    if market_cap:

        st.metric(
            "🏢 Market Cap",
            f"{market_cap/1e9:.2f} B"
        )

    else:

        st.metric(
            "🏢 Market Cap",
            "N/A"
        )

with col3:

    if pe_ratio:

        st.metric(
            "📊 P/E Ratio",
            f"{pe_ratio:.2f}"
        )

    else:

        st.metric(
            "📊 P/E Ratio",
            "N/A"
        )

with col4:

    st.metric(
        "📈 Day Range",
        f"{day_low:.2f} - {day_high:.2f}"
    )

st.markdown("---")

# ---------------- STOCK CHART ----------------

history = history.reset_index()

fig = go.Figure()

fig.add_trace(

    go.Scatter(

        x=history["Date"],

        y=history["Close"],

        mode="lines",

        name="Closing Price",

        line=dict(width=3,color="#2563EB")

    )

)

fig.update_layout(

    title=f"{company} Stock Price",

    template="plotly_white",

    height=550,

    hovermode="x unified",

    xaxis_title="Date",

    yaxis_title=f"Price ({currency})"

)

st.plotly_chart(fig,use_container_width=True)

# ---------------- EXTRA INFORMATION ----------------

st.subheader("📊 Company Information")

left,right = st.columns(2)

with left:

    st.write("**Company Name** :",info.get("longName","N/A"))

    st.write("**Sector** :",info.get("sector","N/A"))

    st.write("**Industry** :",info.get("industry","N/A"))

    st.write("**Country** :",info.get("country","N/A"))

with right:

    st.write("**Website** :",info.get("website","N/A"))

    st.write("**Employees** :",info.get("fullTimeEmployees","N/A"))

    st.write("**52 Week High** :",info.get("fiftyTwoWeekHigh","N/A"))

    st.write("**52 Week Low** :",info.get("fiftyTwoWeekLow","N/A"))

st.markdown("---")
# ---------------- AI INSURANCE FRAUD DATASET ----------------

st.header("🕵 AI Insurance Claim Fraud Analytics")

@st.cache_data
def load_fraud_data():

    np.random.seed(42)

    size = 500

    df = pd.DataFrame({

        "Claim ID":[f"CLM{i}" for i in range(1,size+1)],

        "Age":np.random.randint(18,70,size),

        "Vehicle Claim Amount":np.random.randint(2000,90000,size),

        "Incident Severity":np.random.choice(
            ["Minor","Major","Total Loss","Trivial"],
            size
        ),

        "Vehicle Type":np.random.choice(
            ["SUV","Sedan","Truck","Bike"],
            size
        ),

        "Police Report":np.random.choice(
            ["Yes","No"],
            size
        ),

        "Witness Present":np.random.choice(
            ["Yes","No"],
            size
        ),

        "Fraud Reported":np.random.choice(
            ["Fraud","Genuine"],
            size,
            p=[0.28,0.72]
        )

    })

    return df


fraud_df = load_fraud_data()

st.subheader("Insurance Claims Dataset")

st.dataframe(
    fraud_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ---------------- FILTER ----------------

st.subheader("🎯 Filter Claims")

c1,c2 = st.columns(2)

with c1:

    severity = st.selectbox(

        "Incident Severity",

        ["All"]+list(fraud_df["Incident Severity"].unique())

    )

with c2:

    status = st.selectbox(

        "Fraud Status",

        ["All"]+list(fraud_df["Fraud Reported"].unique())

    )

filtered = fraud_df.copy()

if severity!="All":

    filtered = filtered[
        filtered["Incident Severity"]==severity
    ]

if status!="All":

    filtered = filtered[
        filtered["Fraud Reported"]==status
    ]

st.dataframe(

    filtered,

    use_container_width=True,

    hide_index=True

)

st.markdown("---")

# ---------------- KPI ----------------

total_claims = len(filtered)

fraud_cases = len(

    filtered[
        filtered["Fraud Reported"]=="Fraud"
    ]

)

genuine_cases = total_claims-fraud_cases

fraud_rate = (fraud_cases/total_claims)*100 if total_claims else 0

a,b,c,d = st.columns(4)

a.metric("📄 Total Claims",total_claims)

b.metric("🚨 Fraud Cases",fraud_cases)

c.metric("✅ Genuine",genuine_cases)

d.metric("⚠ Fraud Rate",f"{fraud_rate:.2f}%")

st.markdown("---")

# ---------------- PIE CHART ----------------

pie = px.pie(

    filtered,

    names="Fraud Reported",

    title="Fraud vs Genuine Claims",

    hole=.45,

    color="Fraud Reported"

)

st.plotly_chart(

    pie,

    use_container_width=True

)

# ---------------- BAR CHART ----------------

bar = px.bar(

    filtered,

    x="Incident Severity",

    color="Fraud Reported",

    barmode="group",

    title="Incident Severity Analysis"

)

st.plotly_chart(

    bar,

    use_container_width=True

)

# ---------------- VEHICLE CLAIM ----------------

hist = px.histogram(

    filtered,

    x="Vehicle Claim Amount",

    nbins=30,

    title="Vehicle Claim Amount Distribution"

)

st.plotly_chart(

    hist,

    use_container_width=True

)

# ---------------- SCATTER ----------------

scatter = px.scatter(

    filtered,

    x="Age",

    y="Vehicle Claim Amount",

    color="Fraud Reported",

    size="Vehicle Claim Amount",

    title="Fraud Detection Scatter Plot"

)

st.plotly_chart(

    scatter,

    use_container_width=True
)

st.download_button(

    "📥 Download Dataset",

    filtered.to_csv(index=False),

    "Insurance_Fraud_Dataset.csv",

    "text/csv"

)

st.markdown("---")

st.success("✅ AI Insurance Claim Fraud Analytics Completed Successfully")

st.caption("Developed using Streamlit • Plotly • Yahoo Finance • Pandas • NumPy")
