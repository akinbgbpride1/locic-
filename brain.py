from src.tools.market_data import MarketDataTool
from src.tools.scraper import WebScraperTool
from src.memory.storage import VirtualMemoryStore

class InvestmentAgent:
    def __init__(self):
        self.market = MarketDataTool()
        self.scraper = WebScraperTool()
        self.memory = VirtualMemoryStore()
        self.knowledge = self.memory.load("agent_state", default={})

    def research_company(self, ticker: str, website_url: str):
        """Fetches market data AND scrapes the website."""
        print(f"Researching {ticker}...")
        
        # 1. Get financial data
        financials = self.market.get_financial_summary(ticker)
        
        # 2. Scrape website content
        web_content = self.scraper.get_text_from_url(website_url)
        
        # 3. Store both
        self.knowledge[ticker] = {
            "financials": financials,
            "web_summary": web_content[:2000] # Save first 2000 chars
        }
        self.memory.save("agent_state", self.knowledge)
        return f"Completed research on {ticker}."