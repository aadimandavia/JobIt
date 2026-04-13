import requests

HEADERS = {
    "User-Agent": "reddit-job-board"
}

BASE_URL = "https://www.reddit.com/r/forhire+jobs+internships/new.json"

def fetch_posts(limit=200):
    posts = []
    after = None

    while len(posts) < limit:
        params = {
            "limit": 100,
            "after": after
        }

        response = requests.get(BASE_URL, headers=HEADERS, params=params)

        if response.status_code != 200:
            print("Error:", response.status_code)
            break

        data = response.json()["data"]
        children = data["children"]

        if not children:
            break

        for post in children:
            post_data = post["data"]

            posts.append({
                "title": post_data["title"],
                "url": "https://reddit.com" + post_data["permalink"],
                "created_at": post_data["created_utc"],
                "subreddit": post_data["subreddit"],
                "description": post_data.get("selftext", "")
            })

        after = data["after"]

        if after is None:
            break

    return posts[:limit]