# **Project Blueprint: Daily News Crossword Automation**

## **Overview**

This project is an automated system that generates a daily crossword puzzle based on financial and general news. It runs via GitHub Actions, fetches data from Alpaca, processes it with Gemini, builds a puzzle, and deploys it to GitHub Pages.

## **Architecture**

### **1\. Data Pipeline (Python)**

Located in src/, the pipeline executes sequentially:

1. **News Fetcher (news\_client.py):** Connects to Alpaca News API to fetch top headlines/summaries from the previous 24 hours.  
2. **AI Processor (ai\_client.py):** Sends news text to Google Gemini.  
   * *Prompt Strategy:* Extracts 15-25 unique, non-trivial words and generates cryptic or context-aware clues for them.  
   * *Output:* Strict JSON format.  
3. **Grid Generator (crossword\_gen.py):**  
   * Takes the list of Word/Clue pairs.  
   * Uses a "Grow from Center" algorithm to place words on a dynamic grid.  
   * Optimizes for intersection density.  
4. **Orchestrator (main.py):** Ties these steps together and writes the output to docs/data/puzzle.json.

### **2\. Frontend (HTML/JS)**

Located in docs/index.html.

* **Hosting:** GitHub Pages (serving the /docs folder).  
* **Logic:** Fetches ./data/puzzle.json on load.  
* **UI:** Renders an interactive CSS Grid based on the JSON dimensions. Checks answers locally.

### **3\. Automation (GitHub Actions)**

Located in .github/workflows/daily\_gen.yml.

* **Trigger:** Cron schedule (e.g., 8:00 AM UTC).  
* **Permissions:** Write permissions to the repo to commit the new puzzle.json.  
* **Secrets Required:**  
  * ALPACA\_API\_KEY  
  * ALPACA\_SECRET\_KEY  
  * GEMINI\_API\_KEY

## **Deployment Strategy**

1. Push this codebase.  
2. Go to Repo Settings \> Pages \> Source \= main branch, /docs folder.  
3. Add the secrets listed above in Settings \> Secrets and variables \> Actions.