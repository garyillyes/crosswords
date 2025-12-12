import os
import json
import datetime
from news_client import NewsClient
from ai_client import AIClient
from crossword_gen import CrosswordGenerator

# --- Config ---
ALPACA_KEY = os.environ.get("ALPACA_API_KEY")
ALPACA_SECRET = os.environ.get("ALPACA_SECRET_KEY")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

def main():
    # 1. Initialize Clients
    try:
        news_client = NewsClient(ALPACA_KEY, ALPACA_SECRET)
        ai_client = AIClient(GEMINI_KEY)
        generator = CrosswordGenerator()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # 2. Get Data
    news_text = news_client.fetch_news(limit=25)
    if not news_text:
        print("No news text retrieved. Aborting.")
        return

    # 3. Process AI
    word_data = ai_client.extract_words(news_text)
    
    # Deduplicate based on word
    seen = set()
    unique_data = []
    for item in word_data:
        w = item.get('word', '').upper().strip()
        if w and w not in seen and w.isalpha():
            item['word'] = w
            unique_data.append(item)
            seen.add(w)
            
    print(f"Extracted {len(unique_data)} valid unique words.")
    
    if len(unique_data) < 5:
        print("Not enough words generated to build a puzzle.")
        return

    # 4. Generate Grid
    puzzle = generator.generate(unique_data)
    
    if not puzzle:
        print("Failed to generate a valid grid layout.")
        return

    # Add metadata
    puzzle['generated_at_utc'] = datetime.datetime.utcnow().isoformat()
    puzzle['title'] = f"Daily News Crossword: {datetime.date.today()}"

    # 5. Save
    output_path = "docs/data/puzzle.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(puzzle, f, indent=2)
    
    print(f"Success! Puzzle saved to {output_path}")

if __name__ == "__main__":
    main()