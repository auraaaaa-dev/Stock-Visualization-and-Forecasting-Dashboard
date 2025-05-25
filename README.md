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

## Making Changes

### Adding New Features
1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the code

3. Test your changes locally:
   ```bash
   streamlit run app.py
   ```

4. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request on GitHub

### Updating Dependencies
1. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```

2. Test the updated dependencies:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

3. Commit the changes:
   ```bash
   git add requirements.txt
   git commit -m "Update dependencies"
   git push
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

## Troubleshooting

Common issues and solutions:

1. **No data found for symbol**:
   - Check if the stock symbol is correct
   - Try a different date range
   - Verify internet connection

2. **Forecasting errors**:
   - Ensure at least 60 days of historical data
   - Try a different stock symbol
   - Reduce forecast days

3. **Installation issues**:
   - Make sure Python 3.8+ is installed
   - Try creating a new virtual environment
   - Update pip: `python -m pip install --upgrade pip`

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt
- Internet connection for real-time data

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
