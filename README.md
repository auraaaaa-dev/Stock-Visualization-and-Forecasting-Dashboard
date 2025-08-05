# 📈 Stock Market Dashboard

A comprehensive stock market analysis and forecasting dashboard built with Streamlit, featuring real-time data from Alpha Vantage API.

## 🚀 Features

- **Real-time Stock Data**: Get live stock prices and historical data
- **Interactive Charts**: Candlestick charts with volume analysis
- **Technical Indicators**: RSI, MACD, Moving Averages
- **Price Forecasting**: AI-powered price predictions using Prophet
- **Beautiful UI**: Modern, responsive design with custom styling
- **Multiple Timeframes**: Daily, weekly, and monthly data views

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd stock-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Alpha Vantage API Key**
   - Go to [Alpha Vantage](https://www.alphavantage.co/)
   - Sign up for a free API key
   - Copy your API key

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📊 Usage

1. **Enter API Key**: Paste your Alpha Vantage API key in the sidebar
2. **Select Stock**: Choose from popular stocks or enter a custom symbol
3. **Set Date Range**: Select your desired time period
4. **Choose Indicators**: Toggle technical indicators on/off
5. **Analyze**: Click "Analyze" to generate charts and forecasts

## 🎯 Supported Stocks

### Technology
- AAPL (Apple Inc.)
- MSFT (Microsoft Corporation)
- GOOGL (Alphabet Inc.)
- META (Meta Platforms Inc.)
- NVDA (NVIDIA Corporation)
- TSLA (Tesla Inc.)
- AMZN (Amazon.com Inc.)
- INTC (Intel Corporation)

### Finance
- JPM (JPMorgan Chase & Co.)
- BAC (Bank of America Corp.)
- V (Visa Inc.)
- MA (Mastercard Inc.)
- GS (Goldman Sachs Group Inc.)

### Healthcare
- JNJ (Johnson & Johnson)
- PFE (Pfizer Inc.)
- MRK (Merck & Co.)
- UNH (UnitedHealth Group Inc.)
- ABBV (AbbVie Inc.)

### Consumer
- WMT (Walmart Inc.)
- KO (Coca-Cola Co.)
- MCD (McDonald's Corp.)
- NKE (Nike Inc.)
- SBUX (Starbucks Corporation)

## 🚀 Deployment on Render

1. **Connect your GitHub repository to Render**
2. **Set environment variables**:
   - `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key
3. **Deploy**: Render will automatically deploy your app

### Start Command for Render:
```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

## 📦 Dependencies

- **streamlit==1.32.0**: Web framework
- **pandas==2.2.0**: Data manipulation
- **plotly==5.18.0**: Interactive charts
- **prophet==1.1.4**: Time series forecasting
- **numpy==1.26.3**: Numerical computing
- **requests==2.31.0**: HTTP requests
- **matplotlib>=3.7.0**: Plotting library
- **scipy>=1.11.0**: Scientific computing

## 🔧 Configuration Files

- **app.py**: Main application file
- **requirements.txt**: Python dependencies
- **render.yaml**: Render deployment configuration
- **packages.txt**: System dependencies for Render
- **.gitignore**: Git ignore rules

## 📈 API Rate Limits

- **Free Alpha Vantage API**: 5 requests per minute, 500 per day
- **Premium API**: Higher limits available

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. Stock market predictions are not guaranteed and should not be used as financial advice. Always consult with a qualified financial advisor before making investment decisions.
