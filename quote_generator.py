import random
import requests

class QuoteGenerator:
    def __init__(self):
        self.FALLBACK_QUOTES = {
            "motivation": [
                {"text": "Success is not final, failure is not fatal: it is the courage to continue that counts."},
                {"text": "The only way to do great work is to love what you do."},
                {"text": "Don't watch the clock; do what it does. Keep going."}
            ],
            "wisdom": [
                {"text": "The only true wisdom is in knowing you know nothing."},
                {"text": "The journey of a thousand miles begins with one step."},
                {"text": "What you think, you become."}
            ],
            "happiness": [
                {"text": "Happiness is not something ready made. It comes from your own actions."},
                {"text": "The purpose of our lives is to be happy."},
                {"text": "Happiness is when what you think, what you say, and what you do are in harmony."}
            ],
            "life": [
                {"text": "Life is what happens while you are busy making other plans."},
                {"text": "Life is really simple, but we insist on making it complicated."},
                {"text": "In the end, it is not the years in your life that count. It is the life in your years."}
            ]
        }

    def fetch_quote(self, category):
        """Fetch a quote from API or fallback to local quotes if API fails"""
        try:
            response = requests.get("https://zenquotes.io/api/random", timeout=5, verify=False)
            if response.status_code == 200:
                quote = response.json()[0]
                return {
                    'text': quote['q'],
                    'category': category
                }
        except Exception as e:
            print(f"API Error: {e}")
            print("Using fallback quotes...")
        
        # Use fallback quotes if API fails
        if category in self.FALLBACK_QUOTES:
            quote = random.choice(self.FALLBACK_QUOTES[category])
            quote['category'] = category
            return quote
        
        # If category not in fallback, use a random category
        random_category = random.choice(list(self.FALLBACK_QUOTES.keys()))
        quote = random.choice(self.FALLBACK_QUOTES[random_category])
        quote['category'] = random_category
        return quote