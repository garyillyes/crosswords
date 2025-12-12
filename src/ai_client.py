import json
import google.generativeai as genai

class AIClient:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("Gemini API Key is required for AI processing.")
        
        genai.configure(api_key=api_key)
        # using Flash for speed and efficiency on large text blocks
        DIGEST_MODEL = "gemini-2.5-flash-preview-09-2025"

        self.model = genai.GenerativeModel(DIGEST_MODEL)

    def extract_words(self, text_blob):
        """
        Sends the news text to Gemini to extract a bag of words and generate clues.
        Returns a list of dictionaries: [{'word': '...', 'clue': '...'}, ...]
        """
        print("Sending text to Gemini for extraction...")
        
        prompt = f"""
        Analyze the following news text. 
        1. Extract 25 unique, distinct words that are relevant to the news or general vocabulary found in the text.
        2. Words must be between 3 and 10 letters long.
        3. No spaces, no hyphens, no special characters.
        4. For each word, write a crossword clue. The clue should be witty, cryptic, or fact-based relative to the news.
        5. Return ONLY valid JSON in this format:
        [
          {{"word": "MARKET", "clue": "Place where stocks are traded"}},
          ...
        ]
        
        TEXT:
        {text_blob[:12000]} 
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            data = json.loads(response.text)
            
            # Basic validation
            if isinstance(data, list):
                return data
            else:
                print("AI returned unexpected format (not a list).")
                return []
                
        except Exception as e:
            print(f"Gemini Error: {e}")
            return []