import yfinance as yf
import pandas as pd

class MarketDataTool:
    def __init__(self):
        pass

    def get_price(self, ticker: str) -> float:
        """Fetches the current price of a stock."""
        stock = yf.Ticker(ticker)
        # Using fast_info for better performance
        return stock.fast_info['last_price']

    def get_history(self, ticker: str, period: str = "1mo") -> pd.DataFrame:
        """Fetches historical OHLCV data."""
        stock = yf.Ticker(ticker)
        return stock.history(period=period)

    def get_financial_summary(self, ticker: str) -> dict:
        """Fetches key metrics for the AI to analyze."""
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "symbol": ticker,
            "pe_ratio": info.get("trailingPE"),
            "market_cap": info.get("marketCap"),
            "dividend_yield": info.get("dividendYield"),
            "52_week_high": info.get("fiftyTwoWeekHigh")
        }