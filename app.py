import streamlit as st
import yfinance as yf
import pandas as pd
from backtesting import Backtest
from strategies.buy_hold import BuyHold
from strategies.sma_crossover import SmaCross
from strategies.rsi_strategy import RsiStrategy

# App title
st.title("📈 Backtest Trading Strategies")

# Sidebar options
ticker = st.sidebar.text_input("Ticker", "AAPL")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

strategy_name = st.sidebar.selectbox(
    "Strategy",
    ("Buy & Hold", "SMA Crossover", "RSI Strategy")
)

# Fetch data
@st.cache_data
def get_data(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, group_by='ticker')
    
    # Flatten multi-index if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(0)  # Drop the ticker level
    
    df.dropna(inplace=True)
    #st.write("Columns in data:", df.columns.tolist())

    return df

df = get_data(ticker, start_date, end_date)

# Run backtest
strategy_map = {
    "Buy & Hold": BuyHold,
    "SMA Crossover": SmaCross,
    "RSI Strategy": RsiStrategy
}

if st.button("Run Backtest"):
    if df.empty:
        st.warning("No data found for the selected ticker and date range.")
    else:
        bt = Backtest(df, strategy_map[strategy_name], cash=10000, commission=.002)
        stats = bt.run()
        st.subheader("📊 Strategy Results")
        st.write(stats)
        st.subheader("📉 Equity Curve")
        from bokeh.plotting import figure
        st.bokeh_chart(bt.plot(), use_container_width=True)