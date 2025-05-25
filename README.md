# Stock-Visualization-and-Forecasting-Dashboard
   A comprehensive stock market analysis dashboard with real-time data, technical indicators, and price forecasting built with Streamlit.
## Features

- Real-time stock data from Yahoo Finance
- Interactive candlestick charts with volume analysis
- Technical indicators:
  - Moving Averages (MA20, MA50)
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
- Price forecasting using Prophet
- Multiple stock categories:
  - Technology (AAPL, MSFT, GOOGL, etc.)
  - Finance (JPM, BAC, V, etc.)
  - Healthcare (JNJ, PFE, MRK, etc.)
  - Consumer (WMT, KO, MCD, etc.)
- Custom stock symbol input
- Adjustable date ranges and intervals (daily, weekly, monthly)

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Stock-Visualization-and-Forecasting-Dashboard.git
   cd Stock-Visualization-and-Forecasting-Dashboard
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the dashboard:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a stock:
   - Choose from predefined categories
   - Or enter a custom stock symbol

2. Configure analysis:
   - Set date range
   - Choose time interval
   - Select technical indicators

3. View analysis:
   - Price Analysis tab: Candlestick chart with volume
   - Technical Indicators tab: RSI and MACD
   - Forecasting tab: Price predictions with confidence intervals

## Deployment

This dashboard is deployed on Streamlit Cloud:

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

2. Streamlit Cloud will automatically update the deployment

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- Internet connection for real-time data

## License

This project is licensed under the MIT License - see the LICENSE file for details.
