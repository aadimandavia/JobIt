from datetime import datetime, timedelta
import requests
import time
from app.config import settings
from app.models.job import insert_job
from app.utils.filters import is_job_post
from app.utils.extractor import clean_description, is_specialized_role
from app.utils.classifier import classifier

HEADERS = {
    "User-Agent": settings.REDDIT_USER_AGENT or "reddit-job-board/1.0"
}

def fetch_search_results(query: str, max_limit: int = 100):
    """Search for jobs across all of Reddit using a keyword query."""
    posts = []
    # Fetch posts from the last week
    url = f"https://www.reddit.com/search.json?q={query}&sort=new&t=week&limit={max_limit}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            children = data.get("children", [])
            for post in children:
                post_data = post["data"]
                posts.append({
                    "title": post_data.get("title", ""),
                    "url": "https://reddit.com" + post_data.get("permalink", ""),
                    "created_at": post_data.get("created_utc", 0),
                    "subreddit": post_data.get("subreddit", "unknown"),
                    "description": clean_description(post_data.get("selftext", ""))
                })
    except Exception as e:
        print(f"[ERROR] Global search failed for '{query}': {e}")
            
    return posts

def fetch_subreddit_posts(subreddit_name: str, max_limit: int = 100):
    """Fetch recent posts from specific subreddits."""
    posts = []
    url = f"https://www.reddit.com/r/{subreddit_name}/new.json?limit={max_limit}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            children = data.get("children", [])
            for post in children:
                post_data = post["data"]
                posts.append({
                    "title": post_data.get("title", ""),
                    "url": "https://reddit.com" + post_data.get("permalink", ""),
                    "created_at": post_data.get("created_utc", 0),
                    "subreddit": post_data.get("subreddit", subreddit_name),
                    "description": clean_description(post_data.get("selftext", ""))
                })
    except Exception as e:
        print(f"[ERROR] Subreddit fetch failed for r/{subreddit_name}: {e}")
            
    return posts

def run_scraper():
    """Main entry point to fetch and process jobs from multiple sources."""
    print(f"\n[HUNTER] Starting scraper run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Subreddit Polling
    subreddits = settings.SUBREDDITS
    all_posts = fetch_subreddit_posts(subreddits, max_limit=100)
    
    # 2. Global Scouting (Niche Search)
    search_queries = [
        # Catch-all Universal Search
        '( [Hiring] OR [Offer] OR "Hiring:" OR "Job Opening" )',
        
        # Specific Niche Scouting
        '[Hiring] "data scientist"',
        '[Hiring] "machine learning"',
        '[Hiring] "ai engineer"',
        '[Hiring] "data analyst"',
        '[Hiring] "motion graphics"',
        '[Hiring] "vfx"',
        '[Hiring] "video editor"',
        '[Hiring] "animator"',
        '[Hiring] "python developer"',
        '[Hiring] "react developer"',
        '[Hiring] "backend developer"'
    ]
    
    for query in search_queries:
        print(f"[SEARCH] Scouting for: {query}")
        results = fetch_search_results(query, max_limit=50)
        all_posts.extend(results)
        time.sleep(1) # Be nice to Reddit
        
    # 3. Process and Deduplicate
    total_processed = 0
    total_inserted = 0
    seen_urls = set()
    print(f"[HUNTER] Aggregating posts... Total to scan: {len(all_posts)}")
    
    for i, post in enumerate(all_posts):
        if post["url"] in seen_urls:
            continue
        seen_urls.add(post["url"])
        
        total_processed += 1
        
        # Log progress every 20 items
        if total_processed % 20 == 0:
            print(f"[HUNTER] Progress: Analyzed {total_processed} items...")
        
        # Accuracy check: Title must pass heuristic filters AND the ML Intent model (Strict Bot Filter)
        if is_job_post(post["title"], post["description"]) and \
           classifier.predict_is_hiring(post["title"]):
            success = insert_job(post)
            if success:
                total_inserted += 1
                
    print(f"\n[SUCCESS] Scraping finished!")
    print(f"--- Total Items Analyzed: {total_processed}")
    print(f"--- New Jobs Saved:       {total_inserted}")

if __name__ == "__main__":
    run_scraper()
