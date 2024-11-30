import praw
import feedparser
import requests
import pandas as pd
import os
import time
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------

# Reddit API credentials
REDDIT_CLIENT_ID = ''        # Replace with your client ID
REDDIT_CLIENT_SECRET = ''  # Replace with your client secret
REDDIT_USER_AGENT = 'ContentAggregator/1.0'

# Subreddits to fetch content from
SUBREDDITS = ['devops', 'ProgrammerHumor', 'technology', 'aipromptprogramming']

# RSS feed URLs
RSS_FEEDS = [
    'https://techcrunch.com/feed/',
    'https://news.ycombinator.com/rss',
    # Add more RSS feed URLs here
]

# Keywords for filtering (optional)
KEYWORDS = ['devops', 'blockchain', 'ai', 'mlops']

# Output directories
OUTPUT_DIR = 'output'
MEME_DIR = os.path.join(OUTPUT_DIR, 'memes')

# Create output directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MEME_DIR, exist_ok=True)

# Delay between requests (in seconds)
REQUEST_DELAY = 1  # To respect rate limits and avoid overloading servers

# Today's date for file naming
TODAY = datetime.now().strftime('%Y-%m-%d')

# ----------------------------
# Reddit Content Fetching
# ----------------------------

def fetch_reddit_top_posts():
    print("Fetching top Reddit posts...")
    reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                         client_secret=REDDIT_CLIENT_SECRET,
                         user_agent=REDDIT_USER_AGENT, check_for_async=False)

    reddit_posts = []

    for subreddit_name in SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.top(limit=10):  # Fetch top ranking posts only
            if not post.stickied:
                # Fetch top comments
                post.comments.replace_more(limit=0)
                top_comments = []
                for top_level_comment in post.comments[:3]:  # Get the top 3 comments
                    top_comments.append(top_level_comment.body)

                post_type = 'Meme' if any(ext in post.url for ext in ['.jpg', '.png', '.gif']) else 'Article'
                reddit_posts.append({
                    'Title': post.title,
                    'URL': post.url,
                    'Source': f'r/{subreddit_name}',
                    'Type': post_type,
                    'Score': post.score,
                    'Top Comments': ' | '.join(top_comments)
                })
            time.sleep(REQUEST_DELAY)  # Respect Reddit's API rate limits

    return reddit_posts

# ----------------------------
# RSS Feed Content Fetching
# ----------------------------

def fetch_rss_articles():
    print("Fetching articles from RSS feeds...")
    articles = []

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        source_title = feed.feed.title if 'title' in feed.feed else 'Unknown Source'
        for entry in feed.entries[:20]:
            articles.append({
                'Title': entry.title,
                'URL': entry.link,
                'Source': source_title,
                'Type': 'Article'
            })
        time.sleep(REQUEST_DELAY)  # Avoid overloading servers

    return articles

# ----------------------------
# Hacker News Content Fetching
# ----------------------------

def fetch_hackernews_articles():
    print("Fetching articles from Hacker News...")
    top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    try:
        response = requests.get(top_stories_url)
        story_ids = response.json()[:20]
    except Exception as e:
        print(f"Error fetching Hacker News stories: {e}")
        return []

    hn_articles = []

    for story_id in story_ids:
        story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
        try:
            story = requests.get(story_url).json()
            if 'url' in story and 'title' in story:
                hn_articles.append({
                    'Title': story['title'],
                    'URL': story['url'],
                    'Source': 'Hacker News',
                    'Type': 'Article'
                })
            time.sleep(REQUEST_DELAY)  # Avoid overloading servers
        except Exception as e:
            print(f"Error fetching story ID {story_id}: {e}")
            continue

    return hn_articles

# ----------------------------
# Main Function
# ----------------------------

def main():
    # Fetch content
    reddit_posts = fetch_reddit_top_posts()
    rss_articles = fetch_rss_articles()
    hn_articles = fetch_hackernews_articles()

    # Combine all content
    all_content = reddit_posts + rss_articles + hn_articles

    # Convert to DataFrame
    df = pd.DataFrame(all_content)

    # Optional: Filter content based on keywords
    if KEYWORDS:
        keyword_pattern = '|'.join(KEYWORDS)
        df = df[df['Title'].str.contains(keyword_pattern, case=False, na=False)]

    # Save to Excel
    output_file = os.path.join(OUTPUT_DIR, f'daily_content_{TODAY}.xlsx')
    df.to_excel(output_file, index=False)
    print(f"Content saved to {output_file}")

if __name__ == '__main__':
    main()
