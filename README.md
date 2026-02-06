# Collapse/AI Doom Facebook Automation Bot

Automated Facebook page posting doom content about economic collapse, AI takeover, and societal decay from **multiple sources**.

## Features

- **30% Reddit Posts** - Top discussions from r/collapse, r/antiwork, r/lostgeneration, etc.
- **30% News Articles** - Economic/AI doom news from ZeroHedge, Wolf Street, TechCrunch, etc.
- **20% YouTube Videos** - Doom channel content with AI commentary
- **20% Original AI Content** - Gemini generates doom analysis
- **Completely Free** - Runs on GitHub Actions (no server needed)
- **Automated** - Posts 5x per day automatically

## Content Sources

### Reddit Subreddits
- r/collapse (societal collapse discussions)
- r/lostgeneration (economic despair)
- r/antiwork (worker exploitation, layoffs)
- r/ABoringDystopia (late-stage capitalism)
- r/Futurology (AI takeover concerns)

### News RSS Feeds
- ZeroHedge (economic doom, market analysis)
- Wolf Street (housing bubble, debt, inflation)
- TechCrunch (tech layoffs, AI news)
- Ars Technica (AI developments)

### YouTube Channels
- Michael Bordenaro (economic collapse, jobs)
- Peter Schiff (dollar collapse, inflation, debt)
- Economics Explained (economic analysis)
- Robert Miles (AI safety, existential risk)
- David Shapiro (AI automation, job displacement)

### Original Topics
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
- **Gemini 2.0 Flash** (AI content generation)
- **Facebook Graph API** (posting)
- **YouTube RSS** (video aggregation)

## Setup

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete step-by-step instructions.

Quick version:
1. Create Facebook page + app
2. Get API tokens (Facebook + Gemini)
3. Create GitHub repo
4. Add secrets
5. Upload files
6. Done!

## Cost

**$0/month** - Everything uses free tiers:
- GitHub Actions: Unlimited for public repos
- Gemini API: 15 RPM, 1M requests/day free
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
    "reddit": 0.30,      # 30% Reddit
    "news": 0.30,        # 30% News
    "youtube": 0.20,     # 20% YouTube
    "original": 0.20,    # 20% Original AI
}
```

### Add more subreddits
Add to `REDDIT_SUBREDDITS` list in `collapse_automation.py`

### Add more news sources
Add RSS feeds to `NEWS_FEEDS` dictionary

### Add YouTube channels
Add to `YOUTUBE_CHANNELS` dictionary with channel RSS URL

### Modify post tone
Edit `system_instruction` in Gemini model calls

## Example Posts

**Reddit Post:**
```
r/collapse found data showing 40% of recent college grads are working 
jobs that don't require a degree. The credential inflation trap is real, 
and we're sacrificing an entire generation to it.

https://reddit.com/r/collapse/...
```

**News Post:**
```
Amazon just announced 10,000 more warehouse layoffs while simultaneously 
expanding their robotics program. The automation tsunami isn't coming - 
it's already here.

https://techcrunch.com/...
```

**Video Post:**
```
Michael Bordenaro breaks down new data showing real unemployment 
is nearly double the official rate. The gap between reality and 
government statistics has never been wider.

https://youtube.com/watch?v=...
```

**Original Post:**
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
Powered by Gemini 2.0 Flash and GitHub Actions.
