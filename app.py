import streamlit as st
import pandas as pd
import plotly.express as px
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
from utils import load_data, generate_csv, generate_excel

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Trading Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Dark Mode Toggle
# -------------------------------
dark_mode = st.sidebar.checkbox("🌙 Enable Dark Mode")
if dark_mode:
    st.markdown(
        """
        <style>
        body {
            background-color: #111827 !important;
            color: #f9fafb !important;
        }
        .navbar, .section {
            background-color: #1f2937 !important;
            color: white !important;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .footer {
            color: #aaa;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# -------------------------------
# Load authentication config
# -------------------------------
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

# -------------------------------
# Login
# -------------------------------
authenticator.login(location="main")

# -------------------------------
# Authentication Status
# -------------------------------
if st.session_state["authentication_status"] is False:
    st.error("❌ Username/password is incorrect")

elif st.session_state["authentication_status"] is None:
    st.warning("⚠️ Please enter your username and password")

elif st.session_state["authentication_status"]:
    st.markdown("""
    <div class="navbar">
        <h2>📊 Trading Dashboard</h2>
    </div>
    """, unsafe_allow_html=True)

    st.success(f"✅ Welcome *{st.session_state['name']}*")
    authenticator.logout("🔒 Logout", "sidebar")

    # -------------------------------
    # Upload Data
    # -------------------------------
    uploaded_file = st.file_uploader("Upload CSV to Replace Data", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        st.success("✅ Data loaded from uploaded file.")
    else:
        df = load_data("trading-journal.csv")
        st.info("ℹ️ Using default data.")

    # -------------------------------
    # Sidebar Filters
    # -------------------------------
    st.sidebar.header("⚙️ Filters")
    symbol_filter = (
        st.sidebar.selectbox("Symbol", ["All"] + sorted(df["Symbol"].unique()))
        if "Symbol" in df else None
    )
    type_filter = (
        st.sidebar.selectbox("Type", ["All"] + sorted(df["Type"].unique()))
        if "Type" in df else None
    )

    # Apply filters
    filtered_df = df.copy()
    if symbol_filter and symbol_filter != "All":
        filtered_df = filtered_df[filtered_df["Symbol"] == symbol_filter]
    if type_filter and type_filter != "All":
        filtered_df = filtered_df[filtered_df["Type"] == type_filter]

    # -------------------------------
    # Compute Metrics
    # -------------------------------
    st.subheader("🏠 Overview & Performance Metrics")
    col1, col2, col3, col4 = st.columns(4)

    total_trades = len(filtered_df)
    avg_profit = round(filtered_df["Profit"].mean(), 2) if "Profit" in filtered_df else "N/A"
    wins = filtered_df[filtered_df["Profit"] > 0]
    win_rate = round((len(wins) / total_trades) * 100, 2) if total_trades else 0

    mean_return = filtered_df["Profit"].mean()
    std_return = filtered_df["Profit"].std()
    sharpe_ratio = round(mean_return / std_return, 2) if std_return != 0 else "N/A"

    if not wins.empty and not filtered_df[filtered_df["Profit"] <= 0].empty:
        avg_win = wins["Profit"].mean()
        avg_loss = filtered_df[filtered_df["Profit"] <= 0]["Profit"].mean()
        risk_reward = round(abs(avg_loss) / avg_win, 2) if avg_win != 0 else "N/A"
    else:
        risk_reward = "N/A"

    expectancy = round(mean_return, 2) if "Profit" in filtered_df else "N/A"
    equity_curve = filtered_df["Profit"].cumsum()
    rolling_max = equity_curve.cummax()
    drawdown = rolling_max - equity_curve
    max_drawdown = round(drawdown.max(), 2)

    col1.metric("Total Trades", total_trades)
    col2.metric("Win Rate (%)", win_rate)
    col3.metric("Sharpe Ratio", sharpe_ratio)
    col4.metric("Risk/Reward", risk_reward)

    col5, col6 = st.columns(2)
    col5.metric("Expectancy / Trade", expectancy)
    col6.metric("Max Drawdown", max_drawdown)

    # -------------------------------
    # Tabs
    # -------------------------------
    tabs = st.tabs([
        "📈 Equity & Expectancy",
        "📊 Volatility",
        "📂 Data Table",
        "📥 Downloads"
    ])

    # 📈 Equity & Expectancy
    with tabs[0]:
        st.subheader("Equity Curve & Expectancy Over Time")
        if "Profit" in filtered_df.columns:
            fig1 = px.line(
                x=filtered_df.index,
                y=equity_curve,
                title="Equity Curve",
                template="plotly_dark" if dark_mode else "plotly"
            )
            fig2 = px.line(
                x=filtered_df.index,
                y=filtered_df["Profit"].expanding().mean(),
                title="Expectancy Over Time",
                template="plotly_dark" if dark_mode else "plotly"
            )
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)

    # 📊 Volatility
    with tabs[1]:
        st.subheader("Volatility Over Time")
        if "Profit" in filtered_df.columns:
            volatility = filtered_df["Profit"].rolling(window=5).std()
            fig3 = px.line(
                x=filtered_df.index,
                y=volatility,
                title="5-Period Rolling Volatility",
                template="plotly_dark" if dark_mode else "plotly"
            )
            st.plotly_chart(fig3, use_container_width=True)

    # 📂 Data Table
    with tabs[2]:
        st.subheader("Filtered Trades")
        st.dataframe(filtered_df, use_container_width=True)

    # 📥 Downloads
    with tabs[3]:
        st.subheader("Download Filtered Data")
        csv_data = generate_csv(filtered_df)
        excel_data = generate_excel(filtered_df)
        st.download_button(
            "Download CSV",
            csv_data,
            "filtered_report.csv",
            "text/csv"
        )
        st.download_button(
            "Download Excel",
            excel_data,
            "filtered_report.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # -------------------------------
    # Footer
    # -------------------------------
    st.markdown("""
    <div class='footer'>
    © 2025 Your Company | All rights reserved.
    </div>
    """, unsafe_allow_html=True)
