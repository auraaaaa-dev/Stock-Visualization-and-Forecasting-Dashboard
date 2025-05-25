import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from prophet import Prophet
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

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
        # Fetch data
        data = yf.download(symbol, start=start_date, end=end_date, interval=interval)

        if data.empty:
            st.error(f"No data found for {symbol}. Please check the symbol and try again.")
        else:
            # Convert index to datetime if it's not already
            data.index = pd.to_datetime(data.index)

            # Calculate indicators
            if show_ma:
                data['MA20'] = data['Close'].rolling(window=20).mean()
                data['MA50'] = data['Close'].rolling(window=50).mean()

            if show_rsi:
                # Calculate RSI manually
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                data['RSI'] = 100 - (100 / (1 + rs))

            if show_macd:
                # Calculate MACD manually
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
                    height=800
                )

                st.plotly_chart(fig, use_container_width=True)

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
                    fig_rsi.update_layout(title="Relative Strength Index (RSI)")
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
                    fig_macd.update_layout(title="MACD")
                    st.plotly_chart(fig_macd, use_container_width=True)

            with tab3:
                st.subheader("Price Forecasting")

                try:
                    # Prepare data for Prophet
                    df = pd.DataFrame()
                    df['ds'] = data.index
                    df['y'] = data['Close']

                    # Remove any NaN values
                    df = df.dropna()

                    # Ensure we have enough data points
                    if len(df) < 60:  # Increased minimum data points
                        st.error("Not enough data points for forecasting. Please select a longer date range (at least 60 days).")
                    else:
                        # Fit model with more robust settings
                        model = Prophet(
                            yearly_seasonality=True,
                            weekly_seasonality=True,
                            daily_seasonality=False,
                            changepoint_prior_scale=0.05,
                            seasonality_prior_scale=10.0,
                            interval_width=0.95  # Increased confidence interval
                        )

                        # Add additional regressors if available
                        if 'Volume' in data.columns:
                            df['volume'] = data['Volume']
                            model.add_regressor('volume')

                        # Fit the model with error handling
                        try:
                            model.fit(df)
                            
                            # Make predictions
                            future = model.make_future_dataframe(periods=forecast_days, freq='D')

                            # Add regressors to future dataframe if used
                            if 'Volume' in data.columns:
                                # Use the last known volume for future predictions
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
                                showlegend=True
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

                        except Exception as model_error:
                            st.error(f"Error in model fitting: {str(model_error)}")
                            st.info("Try these solutions:")
                            st.write("1. Select a longer date range (at least 60 days)")
                            st.write("2. Try a different stock symbol")
                            st.write("3. Reduce the forecast days")

                except Exception as e:
                    st.error(f"Error in forecasting: {str(e)}")
                    st.info("Please try with a different date range or stock symbol.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
