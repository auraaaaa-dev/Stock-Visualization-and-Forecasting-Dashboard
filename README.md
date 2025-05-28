# Stock-Visualization-and-Forecasting-Dashboard
  A comprehensive stock market dashboard built with Streamlit and Alpha Vantage API.

## Features

- Real-time stock data visualization
- Technical indicators (MA, RSI, MACD)
- Price forecasting using Prophet
- Interactive charts and analysis
- Multiple time intervals (daily, weekly, monthly)

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd stock-dashboard
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Get an Alpha Vantage API key:
   - Go to https://www.alphavantage.co/
   - Sign up for a free API key
   - Create a `.streamlit/secrets.toml` file with:
   ```toml
   ALPHA_VANTAGE_API_KEY = "your_api_key_here"
   ```

5. Run the app:
```bash
streamlit run app.py
```

## Deployment

### Local Development
- Run `streamlit run app.py`
- Access the app at http://localhost:8501

### Render Deployment
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Add your Alpha Vantage API key in the environment variables
4. Deploy!

## Environment Variables

- `ALPHA_VANTAGE_API_KEY`: Your Alpha Vantage API key
- `PORT`: Port number for the web service (default: 10000)

## Dependencies

- streamlit==1.32.0
- pandas==2.2.0
- plotly==5.18.0
- prophet==1.1.5
- numpy==1.26.3
- requests==2.31.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
