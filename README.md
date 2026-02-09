# Collapse/AI Doom Facebook Automation Bot

Automated Facebook page posting doom content about economic collapse, AI takeover, and societal decay from **multiple sources**.

## Features

- **45% News Articles** - Economic/AI doom news from 10+ reliable RSS sources
- **35% YouTube Videos** - Doom channel content using YouTube Data API v3 (real-time!)
- **20% Original AI Content** - Gemini generates doom analysis
- **Completely Free** - All APIs use free tiers ($0/month forever)
- **Simple & Reliable** - No OAuth complexity, just works
- **Automated** - Posts 5x per day automatically via GitHub Actions

## Content Sources

### News RSS Feeds (10+ sources)
- **Economic Doom:** ZeroHedge, Wolf Street
- **Tech/AI News:** TechCrunch, Ars Technica, The Verge, Wired
- **Business:** Business Insider, MarketWatch
- **General:** Reuters Business, BBC Business

### YouTube Channels (Data API v3)
- Michael Bordenaro (economic collapse, housing market)
- Peter Schiff (dollar collapse, inflation, debt)
- Economics Explained (economic analysis, country collapses)
- Robert Miles (AI safety, existential risk, alignment)
- David Shapiro (AI automation, job displacement, post-labor)

### Original AI Topics
- AI job displacement
- Economic collapse indicators
- US infrastructure decay
- Wealth inequality
- Mass layoffs
- Housing crisis
- Political instability

## Tech Stack

- **Python 3.11**
- **GitHub Actions** (scheduling & hosting)
- **Gemini 3 Flash Preview** (AI content generation)
- **YouTube Data API v3** (real-time video fetching)
- **Facebook Graph API v24.0** (posting)
- **News RSS Feeds** (article aggregation)

## Setup

See [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md) for enabling YouTube Data API v3 (takes 10 seconds!)

Quick version:
1. Create Facebook page + app (get FB credentials)
2. Get Gemini API key
3. **Enable YouTube Data API v3** in Google Cloud Console - CRITICAL!
4. Create GitHub repo
5. Add secrets to GitHub (just 3: FB_PAGE_ID, FB_ACCESS_TOKEN, GEMINI_API_KEY)
6. Upload files
7. Done!

**Total time:** ~15 minutes  
**Total cost:** $0/month forever

## Cost

**$0/month** - Everything uses free tiers:
- GitHub Actions: Unlimited for public repos
- Gemini API: 15 RPM, 1M requests/day free
- YouTube Data API v3: 10,000 units/day free (bot uses 15)
- Facebook API: No limits for this usage

## File Structure

```
collapse-automation/
├── collapse_automation.py       # Main bot script
├── requirements.txt             # Python dependencies
├── .gitignore                   # Protects secrets
├── .env.example                 # Template for local testing
├── .github/workflows/
│   └── collapse_automation.yml  # GitHub Actions workflow
├── SETUP_GUIDE.md              # Detailed setup instructions
└── README.md                   # This file
```

## Customization

### Change posting frequency
Edit `.github/workflows/collapse_automation.yml` cron schedule

### Adjust content mix
Edit `CONTENT_MIX` dictionary in `collapse_automation.py`:
```python
CONTENT_MIX = {
    "news": 0.70,        # 70% News
    "original": 0.30,    # 30% Original AI
}
```

### Add more news sources
Add RSS feeds to `NEWS_FEEDS` dictionary:
```python
NEWS_FEEDS = {
    "ZeroHedge": "https://www.zerohedge.com/fullrss2.xml",
    "Your New Source": "https://example.com/feed/",
}
```

### Modify post tone
Edit `system_instruction` in Gemini model calls

## Example Posts

**News Post:**
```
Amazon just announced 10,000 more warehouse layoffs while simultaneously 
expanding their robotics program. The automation tsunami isn't coming - 
it's already here.

https://techcrunch.com/...
```

**YouTube Post:**
```
Peter Schiff breaks down how the dollar is losing its reserve currency 
status as BRICS nations accelerate de-dollarization. The long-term 
consequences for American purchasing power are staggering.

https://youtube.com/watch?v=...
```

**Original AI Post:**
```
AI companies just announced another 45,000 tech layoffs this quarter 
while simultaneously bragging about record profits from automation. 
Middle-class knowledge workers are learning what factory workers 
learned 40 years ago: you are expendable.
```

## Troubleshooting

**403 Error:** App in development mode → switch to Live
**Invalid Token:** Token expired → generate new long-lived token  
**No videos:** RSS slow → bot falls back to original content
**Actions not running:** Check cron syntax (UTC timezone)

## License

MIT - Do whatever you want with it

## Credits

Built with inspiration from successful Facebook automation patterns.
Powered by Gemini 3 Flash Preview and GitHub Actions.
