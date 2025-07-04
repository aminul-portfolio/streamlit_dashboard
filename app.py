import streamlit as st
import pandas as pd
import plotly.express as px


# 1 Load your data


df = pd.read_csv(r"trading-journal.csv")




st.title("📊 Trading Journal Dashboard")


st.header("Overview of Performance")


st.subheader("Detailed Metrics and Charts")

st.text("This dashboard helps analyze your trades.")

st.markdown("""
**Bold text**, *italic text*, and [Streamlit Docs](https://streamlit.io).
""")

st.title("🟢 1️⃣ Basic Structure & Display")
st.write("✅ Data Preview:")
st.write(df)

st.title("🟢 2️⃣ Data Display")
st.dataframe(df)
st.table(df.head(10))

win_rate = 75
previous_win_rate = 70
st.metric(label="Win Rate", value=f"{win_rate}%", delta=f"{win_rate - previous_win_rate}%")

st.title("🟢 3️⃣ User Inputs (Widgets)")

trade_type = st.selectbox("Select Trade Type", df["Type"].unique())
st.write("Selected Trade Type:", trade_type)

session = st.radio("Session", ["London", "New York", "Asia"])
st.write("Selected Session:", session)

lots = st.slider("Lot Size", min_value=0.01, max_value=5.0, step=0.01)
st.write("Selected Lot Size:", lots)

risk = st.number_input("Risk %", min_value=0.0, max_value=10.0, step=0.1)
st.write("Risk Percentage:", risk)

date_range = st.date_input("Filter Dates", [])
st.write("Selected Dates:", date_range)

st.line_chart(df["Profit"])
st.bar_chart(df["Pips"])

fig = px.line(df, x="Open", y="Profit", title="Profit Over Time")
st.plotly_chart(fig)










st.title("🟢 5️⃣ File Upload & Download")

uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded:
    df_uploaded = pd.read_csv(uploaded)
    st.dataframe(df_uploaded)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Current Data", data=csv, file_name="trading_report.csv")


st.title("🟢 6️⃣ Sidebar & Layout")

st.sidebar.header("Sidebar Filters")
symbol = st.sidebar.selectbox("Select Symbol", df["Symbol"].unique())
st.sidebar.write("Selected Symbol:", symbol)

col1, col2 = st.columns(2)
col1.metric("Total Trades", len(df))
col2.metric("Avg Profit", round(df["Profit"].mean(),2))

with st.expander("Show Raw Data"):
    st.dataframe(df)




st.title("🟢 7️⃣ State Management (st.session_state)")

if "selected_symbol" not in st.session_state:
    st.session_state.selected_symbol = "BTCUSD"

symbol = st.selectbox("Choose Symbol", ["BTCUSD", "ETHUSD"], index=["BTCUSD", "ETHUSD"].index(st.session_state.selected_symbol))

st.session_state.selected_symbol = symbol

st.write("Selected:", st.session_state.selected_symbol)





st.title("8️⃣ Tabs and Navigation")

tab1, tab2 = st.tabs(["📊 Chart View", "📈 Summary Stats"])

with tab1:
    st.plotly_chart(fig)

with tab2:
    st.table(df.describe())







st.title("9️⃣ Theming & Branding")

