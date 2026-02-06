#!/usr/bin/env python3
"""
Collapse/AI Doom Facebook Automation Bot
Multi-source aggregation: Reddit + News RSS + YouTube + Original AI posts
"""

import os
import random
import re
import requests
import feedparser
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# YouTube Channel RSS Feeds
YOUTUBE_CHANNELS = {
    "Michael Bordenaro": "https://www.youtube.com/feeds/videos.xml?channel_id=UCdxGqN9_aBisOJHzIRTGLfg",
    "Peter Schiff": "https://www.youtube.com/feeds/videos.xml?channel_id=UCIjuLiLHdFxYtFmWlbTGQRQ",
    "Economics Explained": "https://www.youtube.com/feeds/videos.xml?channel_id=UCZ4AMrDcNrfy3X6nsU8-rPg",
    "Robert Miles AI Safety": "https://www.youtube.com/feeds/videos.xml?channel_id=UCLB7AzTwc6VFZrBsO2ucBMg",
    "David Shapiro": "https://www.youtube.com/feeds/videos.xml?channel_id=UCvKRFNawVcuz4b9ihUTApCg",
}

# Reddit Subreddits (doom-focused)
REDDIT_SUBREDDITS = [
    "collapse",
    "lostgeneration",
    "antiwork",
    "ABoringDystopia",
    "Futurology",
]

# News RSS Feeds
NEWS_FEEDS = {
    "ZeroHedge": "https://www.zerohedge.com/fullrss2.xml",
    "Wolf Street": "https://wolfstreet.com/feed/",
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
}

# Content mix probabilities (must sum to 1.0)
CONTENT_MIX = {
    "reddit": 0.30,      # 30% Reddit posts
    "news": 0.30,        # 30% News articles
    "youtube": 0.20,     # 20% YouTube videos
    "original": 0.20,    # 20% Original AI posts
}


def get_reddit_posts():
    """Fetch top posts from collapse-related subreddits"""
    all_posts = []
    
    for subreddit in REDDIT_SUBREDDITS:
        try:
            # Reddit JSON feed (top posts from last 24 hours)
            url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=10"
            headers = {"User-Agent": "Mozilla/5.0 (collapse-bot/1.0)"}
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue
            
            data = response.json()
            
            for post in data.get("data", {}).get("children", []):
                post_data = post.get("data", {})
                
                # Filter out stickied posts, deleted, removed
                if post_data.get("stickied") or post_data.get("removed"):
                    continue
                
                # Only include posts with decent engagement
                if post_data.get("score", 0) < 50:
                    continue
                
                all_posts.append({
                    "subreddit": subreddit,
                    "title": post_data.get("title", ""),
                    "url": f"https://reddit.com{post_data.get('permalink', '')}",
                    "score": post_data.get("score", 0),
                    "selftext": post_data.get("selftext", "")[:500],  # First 500 chars
                })
        
        except Exception as e:
            print(f"Error fetching r/{subreddit}: {e}")
            continue
    
    if not all_posts:
        return None
    
    # Return a random high-scoring post
    return random.choice(sorted(all_posts, key=lambda x: x["score"], reverse=True)[:20])


def get_news_articles():
    """Fetch recent news from RSS feeds, filtered for collapse/AI relevance"""
    all_articles = []
    
    # Keywords that indicate doom-relevant content
    relevance_keywords = [
        "layoff", "recession", "collapse", "crisis", "inflation", "debt",
        "unemployment", "AI", "automation", "replace", "workers", "jobs",
        "housing", "market crash", "downturn", "decline", "bankrupt",
        "failure", "shutdown", "cut", "economic", "dystopia"
    ]
    
    for source_name, rss_url in NEWS_FEEDS.items():
        try:
            feed = feedparser.parse(rss_url)
            
            for entry in feed.entries[:15]:  # Check last 15 articles
                title = entry.title.lower()
                summary = entry.get("summary", "").lower()
                
                # Check if article is doom-relevant
                is_relevant = any(keyword in title or keyword in summary 
                                 for keyword in relevance_keywords)
                
                if is_relevant:
                    all_articles.append({
                        "source": source_name,
                        "title": entry.title,
                        "url": entry.link,
                        "summary": entry.get("summary", "")[:300],
                        "published": entry.get("published", "Unknown date")
                    })
        
        except Exception as e:
            print(f"Error fetching {source_name}: {e}")
            continue
    
    if not all_articles:
        return None
    
    return random.choice(all_articles)


def clean_ai_response(text):
    """Remove common AI preambles and formatting artifacts"""
    # Remove preambles like "Here's a post about...", "Sure! Here's...", etc.
    preamble_patterns = [
        r"^Here'?s? (?:a |an |the )?(?:post|caption|text|content|update).*?[:\n]",
        r"^Sure[,!]? .*?[:\n]",
        r"^I'(?:ve|ll) .*?[:\n]",
        r"^(?:Based on|Given).*?[:\n]",
        r"^This (?:post|content).*?[:\n]",
    ]
    
    for pattern in preamble_patterns:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Remove markdown formatting
    text = text.replace("**", "").replace("__", "")
    
    # Remove extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    
    return text


def get_youtube_videos():
    """Fetch recent videos from doom YouTube channels"""
    all_videos = []
    
    for channel_name, rss_url in YOUTUBE_CHANNELS.items():
        try:
            feed = feedparser.parse(rss_url)
            # Get the 5 most recent videos from each channel
            for entry in feed.entries[:5]:
                all_videos.append({
                    "channel": channel_name,
                    "title": entry.title,
                    "url": entry.link,
                    "published": entry.published if hasattr(entry, 'published') else "Unknown date"
                })
        except Exception as e:
            print(f"Error fetching from {channel_name}: {e}")
            continue
    
    if not all_videos:
        return None
    
    return random.choice(all_videos)


def generate_reddit_post(reddit_data):
    """Use Gemini to create commentary about a Reddit post"""
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="""You are a social media manager for a collapse/AI doom awareness page.
        Your audience is interested in economic collapse, AI takeover, and US decline.
        
        Generate engaging Facebook posts about Reddit discussions. The post should:
        - Be 2-4 sentences of commentary
        - Highlight why the Reddit discussion is important/alarming
        - Use a direct, serious tone (not sensational or clickbaity)
        - NOT include the Reddit link (that will be added separately)
        - NOT use emojis
        - NOT start with preambles like "Here's a post" or "Check out"
        - Reference the subreddit naturally (e.g., "r/collapse is discussing...")
        
        Example good post:
        "r/collapse found data showing 40% of recent college grads are working jobs that don't require a degree. The credential inflation trap is real, and we're sacrificing an entire generation to it."
        """
    )
    
    prompt = f"""Create a Facebook post about this Reddit discussion:

Subreddit: r/{reddit_data['subreddit']}
Title: {reddit_data['title']}
Upvotes: {reddit_data['score']}

Write ONLY the post text, nothing else."""
    
    response = model.generate_content(prompt)
    post_text = clean_ai_response(response.text)
    
    # Add the Reddit link at the end
    full_post = f"{post_text}\n\n{reddit_data['url']}"
    
    return full_post


def generate_news_post(article):
    """Use Gemini to create commentary about a news article"""
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="""You are a social media manager for a collapse/AI doom awareness page.
        Your audience is interested in economic collapse, AI takeover, and US decline.
        
        Generate engaging Facebook posts about news articles. The post should:
        - Be 2-4 sentences of analysis
        - Highlight the doom/collapse implications
        - Use a direct, serious tone (not sensational)
        - NOT include the article link (that will be added separately)
        - NOT use emojis
        - NOT start with preambles
        
        Example good post:
        "Amazon just announced 10,000 more warehouse layoffs while simultaneously expanding their robotics program. The automation tsunami isn't coming - it's already here."
        """
    )
    
    prompt = f"""Create a Facebook post about this news article:

Source: {article['source']}
Title: {article['title']}
Summary: {article['summary']}

Write ONLY the post text, nothing else."""
    
    response = model.generate_content(prompt)
    post_text = clean_ai_response(response.text)
    
    # Add the article link at the end
    full_post = f"{post_text}\n\n{article['url']}"
    
    return full_post


def generate_video_post(video):
    """Use Gemini to create commentary about a doom YouTube video"""
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="""You are a social media manager for a collapse/AI doom awareness page. 
        Your audience is interested in economic collapse, AI takeover, and US decline.
        
        Generate engaging Facebook posts about YouTube videos. The post should:
        - Be 2-4 sentences of commentary
        - Highlight why the video is alarming/important
        - Use a direct, serious tone (not sensational or clickbaity)
        - NOT include the video link (that will be added separately)
        - NOT use emojis
        - NOT start with preambles like "Here's a post" or "Check out"
        
        Example good post:
        "Michael Bordenaro breaks down new data showing real unemployment is nearly double the official rate. The gap between reality and government statistics has never been wider."
        """
    )
    
    prompt = f"""Create a Facebook post about this YouTube video:

Title: {video['title']}
Channel: {video['channel']}

Write ONLY the post text, nothing else."""
    
    response = model.generate_content(prompt)
    post_text = clean_ai_response(response.text)
    
    # Add the video link at the end
    full_post = f"{post_text}\n\n{video['url']}"
    
    return full_post


def generate_original_post():
    """Use Gemini to create original doom content"""
    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        system_instruction="""You are a social media manager for a collapse/AI doom awareness page.
        Your audience is interested in economic collapse, AI displacement, societal decay, and US decline.
        
        Create original Facebook posts about:
        - Economic indicators (job losses, inflation, debt, layoffs)
        - AI replacing workers / automation anxiety
        - Signs of societal breakdown (infrastructure failures, political instability)
        - US geopolitical decline
        - Wealth inequality and corporate greed
        
        Posts should:
        - Be 3-5 sentences
        - Include specific data points or recent examples when possible
        - Have a serious, observational tone (not sensational)
        - NOT use emojis
        - NOT end with questions or calls to action
        - Read like informed commentary, not panic
        
        Example:
        "AI companies just announced another 45,000 tech layoffs this quarter while simultaneously bragging about record profits from automation. Middle-class knowledge workers are learning what factory workers learned 40 years ago: you are expendable. The only difference is this time there's no other industry to absorb the displaced."
        """
    )
    
    # Topic variety
    topics = [
        "AI job displacement and automation",
        "Economic collapse indicators and recession fears",
        "US infrastructure decay and systemic failures",
        "Wealth inequality and corporate profits vs worker wages",
        "Government dysfunction and political instability",
        "Mass layoffs in tech and white-collar sectors",
        "Housing market unaffordability and homelessness",
        "Healthcare system collapse and medical debt",
        "Student loan crisis and generational wealth gap",
        "Climate disasters and economic disruption"
    ]
    
    topic = random.choice(topics)
    prompt = f"Create a Facebook post about: {topic}\n\nWrite ONLY the post text, nothing else."
    
    response = model.generate_content(prompt)
    post_text = clean_ai_response(response.text)
    
    return post_text


def post_to_facebook(message):
    """Post text content to Facebook page"""
    url = f"https://graph.facebook.com/v24.0/{FB_PAGE_ID}/feed"
    
    payload = {
        "message": message,
        "access_token": FB_ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print(f"✅ Posted successfully!")
        print(f"Preview: {message[:100]}...")
        return True
    else:
        print(f"❌ Error posting to Facebook: {response.status_code}")
        print(f"Response: {response.text}")
        return False


def main():
    print("=" * 60)
    print("COLLAPSE/AI DOOM FACEBOOK BOT - MULTI-SOURCE")
    print(f"Running at: {datetime.now()}")
    print("=" * 60)
    
    # Choose content type based on probabilities
    rand = random.random()
    cumulative = 0
    content_type = None
    
    for ctype, probability in CONTENT_MIX.items():
        cumulative += probability
        if rand < cumulative:
            content_type = ctype
            break
    
    post_content = None
    
    # Generate content based on selected type
    if content_type == "reddit":
        print("\n🔴 Generating REDDIT POST...")
        reddit_data = get_reddit_posts()
        
        if reddit_data:
            print(f"Selected post: r/{reddit_data['subreddit']} - '{reddit_data['title']}' ({reddit_data['score']} upvotes)")
            post_content = generate_reddit_post(reddit_data)
        else:
            print("⚠️ No Reddit posts found, falling back to original post")
            content_type = "original"
    
    elif content_type == "news":
        print("\n📰 Generating NEWS POST...")
        article = get_news_articles()
        
        if article:
            print(f"Selected article: {article['source']} - '{article['title']}'")
            post_content = generate_news_post(article)
        else:
            print("⚠️ No relevant news found, falling back to original post")
            content_type = "original"
    
    elif content_type == "youtube":
        print("\n📺 Generating YOUTUBE POST...")
        video = get_youtube_videos()
        
        if video:
            print(f"Selected video: '{video['title']}' from {video['channel']}")
            post_content = generate_video_post(video)
        else:
            print("⚠️ No videos found, falling back to original post")
            content_type = "original"
    
    # Fallback or explicit original content
    if content_type == "original" or post_content is None:
        print("\n✍️ Generating ORIGINAL POST...")
        post_content = generate_original_post()
    
    print(f"\n📝 Generated content:\n{post_content}\n")
    
    # Post to Facebook
    success = post_to_facebook(post_content)
    
    if success:
        print("\n🎉 Bot run completed successfully!")
    else:
        print("\n💥 Bot run failed!")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
