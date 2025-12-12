import requests

class NewsClient:
    def __init__(self, api_key, secret_key):
        if not api_key or not secret_key:
            raise ValueError("Alpaca API credentials are required.")
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = "https://data.alpaca.markets/v1beta1/news"

    def fetch_news(self, limit=20):
        """
        Fetches the latest news from Alpaca and returns a single combined string
        of headlines and summaries.
        """
        print("Fetching news from Alpaca...")
        
        headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.secret_key
        }
        
        # Get last 24 hours of news implicitly by fetching latest 'limit' articles
        params = {
            "limit": limit,
            "include_content": "true" # Retrieve summary/content if available
        }
        
        try:
            response = requests.get(self.url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"Alpaca Error {response.status_code}: {response.text}")
                return ""
            
            data = response.json()
            articles = data.get('news', [])
            
            if not articles:
                print("No articles found.")
                return ""

            # Combine headlines and summaries into one large text blob for the AI
            text_blob = ""
            for article in articles:
                headline = article.get('headline', '')
                summary = article.get('summary', '')
                text_blob += f"{headline}. {summary} "
            
            return text_blob
            
        except Exception as e:
            print(f"Connection Error: {e}")
            return ""