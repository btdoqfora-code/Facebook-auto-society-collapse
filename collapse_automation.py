#!/usr/bin/env python3
"""
Collapse/AI Doom Facebook Automation Bot
Multi-source aggregation: News RSS + YouTube (Data API v3) + Original AI posts
"""

import os
import random
import re
import requests
import feedparser
import google.generativeai as genai
from googleapiclient.discovery import build
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

# YouTube Channel IDs (using UU prefix for uploads playlist)
# Note: Convert UC (channel) to UU (uploads) to get latest videos
YOUTUBE_CHANNELS = {
    "Michael Bordenaro": "UUdxGqN9_aBisOJHzIRTGLfg",  # Economic collapse, housing
    "Peter Schiff": "UUIjuLiLHdFxYtFmWlbTGQRQ",  # Economic doom, dollar collapse
    "Economics Explained": "UUZ4AMrDcNrfy3X6nsU8-rPg",  # Economic analysis
    "Robert Miles AI Safety": "UULB7AzTwc6VFZrBsO2ucBMg",  # AI safety, existential risk
    "David Shapiro": "UUvKRFNawVcuz4b9ihUTApCg",  # AI automation, post-labor
}

# News RSS Feeds
NEWS_FEEDS = {
    # Economic Doom
    "ZeroHedge": "https://www.zerohedge.com/fullrss2.xml",
    "Wolf Street": "https://wolfstreet.com/feed/",
    
    # Tech/AI
    "TechCrunch": "https://techcrunch.com/feed/",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Wired": "https://www.wired.com/feed/rss",
    
    # Business/Economics
    "Business Insider": "https://www.businessinsider.com/rss",
    "MarketWatch": "https://www.marketwatch.com/rss/topstories",
    
    # General News
    "Reuters Business": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
    "BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
}

# Content mix probabilities (must sum to 1.0)
CONTENT_MIX = {
    "news": 0.45,        # 45% News articles (reliable RSS feeds)
    "youtube": 0.35,     # 35% YouTube videos (Data API v3 - now enabled!)
    "original": 0.20,    # 20% Original AI posts (always works)
}



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
            print(f"  Fetching from {source_name}...")
            feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print(f"  ⚠️  {source_name} has no entries")
                continue
            
            relevant_count = 0
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
                    relevant_count += 1
            
            print(f"  ✓ Found {relevant_count} relevant articles from {source_name}")
        
        except Exception as e:
            print(f"  ✗ Error fetching {source_name}: {e}")
            continue
    
    print(f"\nTotal relevant articles: {len(all_articles)}")
    
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
    """Fetch recent videos from doom YouTube channels using YouTube Data API v3"""
    try:
        # Build YouTube API client using same key as Gemini
        youtube = build('youtube', 'v3', developerKey=GEMINI_API_KEY)
        
        all_videos = []
        
        for channel_name, playlist_id in YOUTUBE_CHANNELS.items():
            try:
                print(f"  Fetching from {channel_name}...")
                
                # Get latest videos from uploads playlist (UU...)
                request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=5  # Get 5 most recent videos
                )
                response = request.execute()
                
                # Handle empty response
                if not response.get('items'):
                    print(f"  ⚠️  {channel_name} returned empty list")
                    continue
                
                for item in response['items']:
                    snippet = item['snippet']
                    video_id = snippet['resourceId']['videoId']
                    
                    all_videos.append({
                        "channel": channel_name,
                        "title": snippet['title'],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "published": snippet['publishedAt']
                    })
                
                print(f"  ✓ Got {len(response['items'])} videos from {channel_name}")
            
            except Exception as e:
                print(f"  ✗ Error fetching from {channel_name}: {e}")
                continue
        
        print(f"\nTotal videos found: {len(all_videos)}")
        
        if not all_videos:
            return None
        
        return random.choice(all_videos)
    
    except Exception as e:
        print(f"YouTube API error: {e}")
        print("  → Make sure YouTube Data API v3 is enabled in Google Cloud Console")
        return None



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
    
    # Extract URL from message if present (for link previews)
    link_url = None
    lines = message.split('\n')
    for line in lines:
        if line.strip().startswith('http'):
            link_url = line.strip()
            # Remove the URL from message since we'll use it as 'link' parameter
            message = message.replace(line, '').strip()
            break
    
    payload = {
        "message": message,
        "access_token": FB_ACCESS_TOKEN
    }
    
    # Add link parameter for previews
    if link_url:
        payload["link"] = link_url
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print(f"✅ Posted successfully!")
        print(f"Preview: {message[:100]}...")
        if link_url:
            print(f"Link: {link_url}")
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
    
    print(f"\n🎲 Random selection: {rand:.3f} → Content type: {content_type}")
    print(f"   Mix: News {CONTENT_MIX['news']*100:.0f}% | YouTube {CONTENT_MIX['youtube']*100:.0f}% | Original {CONTENT_MIX['original']*100:.0f}%")
    
    post_content = None
    
    # Generate content based on selected type
    if content_type == "news":
        print("\n📰 Generating NEWS POST...")
        article = get_news_articles()
        
        if article:
            print(f"Selected article: {article['source']} - '{article['title']}'")
            post_content = generate_news_post(article)
        else:
            print("⚠️ No relevant news found, falling back to original post")
            content_type = "original"
    
    elif content_type == "youtube":
        print("\n📺 Generating YOUTUBE POST (Data API v3)...")
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

