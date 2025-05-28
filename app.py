import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from prophet import Prophet
import numpy as np
import time

# Set page configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin: 0.5rem 0;
    }
    .stock-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .error-message {
        color: #dc3545;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        margin: 1rem 0;
    }
    .success-message {
        color: #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache data fetching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(symbol, start_date, end_date, interval):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Add a small delay between retries
            if attempt > 0:
                time.sleep(2)
            
            # Try to get the ticker first to validate the symbol
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            if not info or 'regularMarketPrice' not in info:
                raise ValueError(f"Invalid symbol: {symbol}")
            
            # Download data with progress=False to avoid UI issues
            data = yf.download(
                symbol,
                start=start_date,
                end=end_date,
                interval=interval,
                progress=False,
                threads=False  # Disable threading to avoid rate limits
            )
            
            if not data.empty:
                return data
            
            # If data is empty but symbol is valid, try with a shorter date range
            if attempt == max_retries - 1:
                # Try last 30 days as fallback
                fallback_start = end_date - timedelta(days=30)
                data = yf.download(
                    symbol,
                    start=fallback_start,
                    end=end_date,
                    interval=interval,
                    progress=False,
                    threads=False
                )
                if not data.empty:
                    return data
                
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            continue
    
    return pd.DataFrame()

# Cache stock info
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_info(symbol):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Validate the info
        if not info or 'regularMarketPrice' not in info:
            return {}
            
        return info
    except Exception as e:
        st.warning(f"Could not fetch detailed stock info: {str(e)}")
        return {}

# Title
st.title("📈 Stock Market Dashboard")

# Define popular stocks
POPULAR_STOCKS = {
    'Technology': {
        'AAPL': 'Apple Inc.',
        'MSFT': 'Microsoft Corporation',
        'GOOGL': 'Alphabet Inc.',
        'META': 'Meta Platforms Inc.',
        'NVDA': 'NVIDIA Corporation',
        'TSLA': 'Tesla Inc.',
        'AMZN': 'Amazon.com Inc.',
        'INTC': 'Intel Corporation'
    },
    'Finance': {
        'JPM': 'JPMorgan Chase & Co.',
        'BAC': 'Bank of America Corp.',
        'V': 'Visa Inc.',
        'MA': 'Mastercard Inc.',
        'GS': 'Goldman Sachs Group Inc.'
    },
    'Healthcare': {
        'JNJ': 'Johnson & Johnson',
        'PFE': 'Pfizer Inc.',
        'MRK': 'Merck & Co.',
        'UNH': 'UnitedHealth Group Inc.',
        'ABBV': 'AbbVie Inc.'
    },
    'Consumer': {
        'WMT': 'Walmart Inc.',
        'KO': 'Coca-Cola Co.',
        'MCD': 'McDonald\'s Corp.',
        'NKE': 'Nike Inc.',
        'SBUX': 'Starbucks Corporation'
    }
}

# Sidebar
with st.sidebar:
    st.header("Settings")
    
    # Stock selection with categories
    st.subheader("Select Stock")
    
    # Create tabs for different stock categories
    category_tabs = st.tabs(list(POPULAR_STOCKS.keys()))
    
    selected_stock = None
    for i, (category, tab) in enumerate(zip(POPULAR_STOCKS.keys(), category_tabs)):
        with tab:
            for symbol, name in POPULAR_STOCKS[category].items():
                if st.button(f"{symbol} - {name}"):
                    selected_stock = symbol
    
    # Custom stock input
    st.subheader("Or Enter Custom Stock Symbol")
    custom_symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    
    # Use selected stock or custom input
    symbol = selected_stock if selected_stock else custom_symbol
    
    # Date range selection
    st.subheader("Date Range")
    today = datetime.now()
    default_start_date = today - timedelta(days=365)
    start_date = st.date_input("Start Date", default_start_date)
    end_date = st.date_input("End Date", today)
    
    # Time interval selection
    st.subheader("Time Interval")
    interval = st.selectbox(
        "Select Interval",
        ["1d", "1wk", "1mo"],
        index=0
    )
    
    # Technical indicators selection
    st.subheader("Technical Indicators")
    show_ma = st.checkbox("Moving Averages", value=True)
    show_rsi = st.checkbox("RSI", value=True)
    show_macd = st.checkbox("MACD", value=True)
    
    # Forecasting settings
    st.subheader("Forecasting")
    forecast_days = st.slider("Forecast Days", 1, 30, 7)

# Main content
if st.sidebar.button("Analyze"):
    try:
        with st.spinner("Fetching data..."):
            # Fetch data
            data = fetch_stock_data(symbol, start_date, end_date, interval)
            
            if data.empty:
                st.error(f"No data found for {symbol}. Please check the symbol and try again.")
                st.info("Common solutions:")
                st.write("1. Verify the stock symbol is correct")
                st.write("2. Try a different date range")
                st.write("3. Check your internet connection")
                st.write("4. Try a different time interval")
                st.write("5. Try using a different stock symbol")
                
                # Add a button to try with a shorter date range
                if st.button("Try with last 30 days"):
                    new_start_date = end_date - timedelta(days=30)
                    data = fetch_stock_data(symbol, new_start_date, end_date, interval)
                    if not data.empty:
                        st.success("Successfully fetched data for the last 30 days!")
                        st.experimental_rerun()
            else:
                # Convert index to datetime if it's not already
                data.index = pd.to_datetime(data.index)
                
                # Display stock info
                stock_info = fetch_stock_info(symbol)
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    current_price = stock_info.get('currentPrice', data['Close'].iloc[-1])
                    st.metric("Current Price", f"${current_price:.2f}")
                with col2:
                    high_52w = stock_info.get('fiftyTwoWeekHigh', data['High'].max())
                    st.metric("52 Week High", f"${high_52w:.2f}")
                with col3:
                    low_52w = stock_info.get('fiftyTwoWeekLow', data['Low'].min())
                    st.metric("52 Week Low", f"${low_52w:.2f}")
                
                # Calculate indicators
                if show_ma:
                    data['MA20'] = data['Close'].rolling(window=20).mean()
                    data['MA50'] = data['Close'].rolling(window=50).mean()
                
                if show_rsi:
                    delta = data['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    data['RSI'] = 100 - (100 / (1 + rs))
                
                if show_macd:
                    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                    data['MACD'] = exp1 - exp2
                    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
                
                # Create tabs
                tab1, tab2, tab3 = st.tabs(["Price Analysis", "Technical Indicators", "Forecasting"])
                
                with tab1:
                    # Create candlestick chart
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                                    vertical_spacing=0.03,
                                    row_heights=[0.7, 0.3])
                    
                    # Candlestick chart
                    fig.add_trace(go.Candlestick(
                        x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name='OHLC'
                    ), row=1, col=1)
                    
                    # Volume chart
                    fig.add_trace(go.Bar(
                        x=data.index,
                        y=data['Volume'],
                        name='Volume'
                    ), row=2, col=1)
                    
                    # Add moving averages if selected
                    if show_ma:
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['MA20'],
                            name='MA20',
                            line=dict(color='blue')
                        ), row=1, col=1)
                        
                        fig.add_trace(go.Scatter(
                            x=data.index,
                            y=data['MA50'],
                            name='MA50',
                            line=dict(color='red')
                        ), row=1, col=1)
                    
                    fig.update_layout(
                        title=f"{symbol} Stock Price",
                        yaxis_title="Price",
                        xaxis_title="Date",
                        height=800,
                        template="plotly_white",
                        xaxis_rangeslider_visible=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Display key statistics
                    st.subheader("Key Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Open", f"${data['Open'].iloc[-1]:.2f}")
                    with col2:
                        st.metric("High", f"${data['High'].iloc[-1]:.2f}")
                    with col3:
                        st.metric("Low", f"${data['Low'].iloc[-1]:.2f}")
                    with col4:
                        st.metric("Close", f"${data['Close'].iloc[-1]:.2f}")
                
                with tab2:
                    # RSI
                    if show_rsi:
                        fig_rsi = go.Figure()
                        fig_rsi.add_trace(go.Scatter(
                            x=data.index,
                            y=data['RSI'],
                            name='RSI'
                        ))
                        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
                        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
                        fig_rsi.update_layout(
                            title="Relative Strength Index (RSI)",
                            template="plotly_white",
                            height=400
                        )
                        st.plotly_chart(fig_rsi, use_container_width=True)
                    
                    # MACD
                    if show_macd:
                        fig_macd = go.Figure()
                        fig_macd.add_trace(go.Scatter(
                            x=data.index,
                            y=data['MACD'],
                            name='MACD'
                        ))
                        fig_macd.add_trace(go.Scatter(
                            x=data.index,
                            y=data['Signal_Line'],
                            name='Signal Line'
                        ))
                        fig_macd.update_layout(
                            title="MACD",
                            template="plotly_white",
                            height=400
                        )
                        st.plotly_chart(fig_macd, use_container_width=True)
                
                with tab3:
                    st.subheader("Price Forecasting")
                    
                    try:
                        with st.spinner("Generating forecast..."):
                            # Prepare data for Prophet
                            df = pd.DataFrame()
                            df['ds'] = data.index
                            df['y'] = data['Close']
                            
                            # Remove any NaN values
                            df = df.dropna()
                            
                            # Ensure we have enough data points
                            if len(df) < 60:
                                st.error("Not enough data points for forecasting. Please select a longer date range (at least 60 days).")
                            else:
                                # Fit model with more robust settings
                                model = Prophet(
                                    yearly_seasonality=True,
                                    weekly_seasonality=True,
                                    daily_seasonality=False,
                                    changepoint_prior_scale=0.05,
                                    seasonality_prior_scale=10.0,
                                    interval_width=0.95
                                )
                                
                                # Add additional regressors if available
                                if 'Volume' in data.columns:
                                    df['volume'] = data['Volume']
                                    model.add_regressor('volume')
                                
                                # Fit the model
                                model.fit(df)
                                
                                # Make predictions
                                future = model.make_future_dataframe(periods=forecast_days, freq='D')
                                
                                # Add regressors to future dataframe if used
                                if 'Volume' in data.columns:
                                    last_volume = data['Volume'].iloc[-1]
                                    future['volume'] = last_volume
                                
                                forecast = model.predict(future)
                                
                                # Plot predictions
                                fig_forecast = go.Figure()
                                
                                # Add historical data
                                fig_forecast.add_trace(go.Scatter(
                                    x=df['ds'],
                                    y=df['y'],
                                    name='Historical',
                                    line=dict(color='blue')
                                ))
                                
                                # Add forecast
                                fig_forecast.add_trace(go.Scatter(
                                    x=forecast['ds'][-forecast_days:],
                                    y=forecast['yhat'][-forecast_days:],
                                    name='Forecast',
                                    line=dict(color='red', dash='dash')
                                ))
                                
                                # Add confidence intervals
                                fig_forecast.add_trace(go.Scatter(
                                    x=forecast['ds'][-forecast_days:],
                                    y=forecast['yhat_upper'][-forecast_days:],
                                    fill=None,
                                    mode='lines',
                                    line_color='rgba(0,100,80,0.2)',
                                    name='Upper Bound'
                                ))
                                
                                fig_forecast.add_trace(go.Scatter(
                                    x=forecast['ds'][-forecast_days:],
                                    y=forecast['yhat_lower'][-forecast_days:],
                                    fill='tonexty',
                                    mode='lines',
                                    line_color='rgba(0,100,80,0.2)',
                                    name='Lower Bound'
                                ))
                                
                                fig_forecast.update_layout(
                                    title=f"{symbol} Price Forecast",
                                    xaxis_title="Date",
                                    yaxis_title="Price",
                                    showlegend=True,
                                    template="plotly_white",
                                    height=600
                                )
                                
                                st.plotly_chart(fig_forecast, use_container_width=True)
                                
                                # Display forecast metrics
                                st.subheader("Forecast Metrics")
                                metrics_df = pd.DataFrame({
                                    'Metric': ['Forecast Start', 'Forecast End', 'Predicted Price', 'Confidence Interval'],
                                    'Value': [
                                        forecast['ds'][-forecast_days].strftime('%Y-%m-%d'),
                                        forecast['ds'][-1].strftime('%Y-%m-%d'),
                                        f"${forecast['yhat'][-1]:.2f}",
                                        f"±${(forecast['yhat_upper'][-1] - forecast['yhat_lower'][-1])/2:.2f}"
                                    ]
                                })
                                st.table(metrics_df)
                                
                                # Add forecast components
                                st.subheader("Forecast Components")
                                components = model.plot_components(forecast)
                                st.pyplot(components)
                    
                    except Exception as e:
                        st.error(f"Error in forecasting: {str(e)}")
                        st.info("Please try with a different date range or stock symbol.")
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please check your internet connection and try again.")
