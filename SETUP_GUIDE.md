# Collapse/AI Doom Facebook Automation - Setup Guide

## Quick Overview

This bot automatically posts to your Facebook page with content from **multiple sources**:
- **30% Reddit** - Top posts from r/collapse, r/antiwork, r/lostgeneration, etc.
- **30% News** - Economic/AI doom articles from ZeroHedge, Wolf Street, TechCrunch, etc.
- **20% YouTube** - Doom channel videos with AI commentary
- **20% Original AI** - Gemini generates collapse analysis

Runs **5 times per day** via GitHub Actions (completely free).

---

## Step 1: Create Your Facebook Page

1. Go to Facebook and create a new page for your collapse content
2. Name it something like:
   - "American Decline Watch"
   - "Collapse Chronicles"
   - "Economic Doom Tracker"
   - (or whatever you want!)

3. Note down your **Page ID**:
   - Go to your page
   - Click "About"
   - Scroll down to find the Page ID (long number)

---

## Step 2: Get Facebook Access Token

### A. Create Facebook App

1. Go to https://developers.facebook.com/apps/
2. Click **"Create App"**
3. Select **"Business"** as app type
4. Fill in:
   - App Name: "Collapse Bot" (or similar)
   - Contact Email: Your email
5. Click **"Create App"**

### B. Add Facebook Login Product

1. In your app dashboard, scroll to **"Add Products"**
2. Find **"Facebook Login"** and click **"Set Up"**
3. Choose **"Web"** platform
4. Enter any URL like `https://localhost` (doesn't matter for API access)

### C. Generate Page Access Token

1. In left sidebar, go to **Tools → Graph API Explorer**
2. In "User or Page" dropdown, select **"Get Page Access Token"**
3. Select your collapse page
4. Grant permissions: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`
5. Copy the **Access Token** (starts with `EAAA...`)

### D. Make Token Long-Lived (60 days)

**Option 1: Use Graph API Explorer**
1. In Graph API Explorer, click the ℹ️ icon next to Access Token
2. Click **"Open in Access Token Tool"**
3. Click **"Extend Access Token"**
4. Copy the new long-lived token

**Option 2: Use URL method**
```
https://graph.facebook.com/v24.0/oauth/access_token?
grant_type=fb_exchange_token&
client_id=YOUR_APP_ID&
client_secret=YOUR_APP_SECRET&
fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
```

### E. Switch App to LIVE Mode

⚠️ **CRITICAL STEP** - Without this, posts won't work!

1. In your app dashboard, top-right corner
2. Toggle switch from **"Development"** to **"Live"**
3. Confirm the switch

---

## Step 3: Get Gemini API Key

1. Go to https://aistudio.google.com/apikey
2. Click **"Create API Key"**
3. Copy the key (starts with `AIza...`)

**Note:** Gemini 3 Flash Preview has generous free tier (15 RPM, 1M requests/day)

---

## Step 4: Set Up GitHub Repository

### A. Create Repository

1. Go to https://github.com/new
2. Repository name: `collapse-automation` (or any name)
3. Choose **Public**
4. Click **"Create repository"**

### B. Add Secrets

1. In your repository, go to **Settings → Secrets and variables → Actions**
2. Click **"New repository secret"** and add:

   **Secret 1:**
   - Name: `FB_PAGE_ID`
   - Value: Your Facebook page ID

   **Secret 2:**
   - Name: `FB_ACCESS_TOKEN`
   - Value: Your Facebook page access token

   **Secret 3:**
   - Name: `GEMINI_API_KEY`
   - Value: Your Gemini API key

---

## Step 5: Upload Files to GitHub

You'll upload 4 files:

### 1. collapse_automation.py
- The main Python script (provided)

### 2. requirements.txt
- Python dependencies (provided)

### 3. .gitignore
- Protects your local .env from being uploaded (provided)

### 4. .github/workflows/collapse_automation.yml
- GitHub Actions workflow file (provided)

**Upload via GitHub Web Interface:**

1. Go to your repository
2. Click **"Add file" → "Upload files"**
3. Drag and drop:
   - `collapse_automation.py`
   - `requirements.txt`
   - `.gitignore`

4. For the workflow file:
   - Create folder structure: Click **"Add file" → "Create new file"**
   - Type: `.github/workflows/collapse_automation.yml`
   - Paste the workflow YAML content
   - Commit

5. Commit all files with message: "Initial bot setup"

---

## Step 6: Test the Bot

### Manual Test

1. Go to **Actions** tab in your repository
2. Click **"Collapse Bot Automation"** workflow
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 30-60 seconds
5. Check your Facebook page for new post!

### Check Logs

1. Click on the workflow run
2. Click **"post-content"**
3. View logs to see what was posted

---

## Customization Options

### Change Posting Frequency

Edit `.github/workflows/collapse_automation.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours (4x/day)
  - cron: '0 0,8,16 * * *'  # 3x/day (midnight, 8am, 4pm UTC)
```

### Adjust Content Mix

Edit `CONTENT_MIX` dictionary in `collapse_automation.py`:

```python
CONTENT_MIX = {
    "reddit": 0.50,      # 50% Reddit posts
    "news": 0.30,        # 30% News articles
    "youtube": 0.10,     # 10% YouTube videos
    "original": 0.10,    # 10% Original AI posts
}
# Must sum to 1.0
```

### Add More Subreddits

Edit `REDDIT_SUBREDDITS` list in `collapse_automation.py`:

```python
REDDIT_SUBREDDITS = [
    "collapse",
    "lostgeneration",
    "antiwork",
    "preppers",              # Add new subreddit
    "LateStageCapitalism",   # Add new subreddit
]
```

### Add More News Sources

Add RSS feeds to `NEWS_FEEDS` dictionary:

```python
NEWS_FEEDS = {
    "ZeroHedge": "https://www.zerohedge.com/fullrss2.xml",
    "Your New Source": "https://example.com/feed/",
}
```

### Add More YouTube Channels

Edit `YOUTUBE_CHANNELS` dictionary in `collapse_automation.py`:

```python
YOUTUBE_CHANNELS = {
    "Michael Bordenaro": "https://www.youtube.com/feeds/videos.xml?channel_id=UCdxGqN9_aBisOJHzIRTGLfg",
    "Your New Channel": "https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID_HERE",
}
```

To find a channel ID:
1. Go to the channel
2. View page source (Ctrl+U)
3. Search for `"channelId"`

### Modify Post Tone

Edit the `system_instruction` in `generate_video_post()` or `generate_original_post()` functions.

---

## Troubleshooting

### "Error 403: This endpoint requires the 'pages_manage_posts' permission"
→ Your app is in Development mode. Switch to Live mode in app dashboard.

### "Invalid OAuth access token"
→ Token expired (60-day limit). Generate a new long-lived token.

### "No videos found"
→ YouTube RSS feeds might be slow. The bot will fall back to original posts.

### GitHub Actions not running
→ Check cron syntax. Remember it's in UTC timezone.

### Posts look too "AI-y"
→ Tweak the `system_instruction` prompts to be more specific about tone.

---

## Local Testing (Optional)

If you want to test on your computer:

1. Create `.env` file (copy from `.env.example`)
2. Fill in your actual credentials
3. Run: `python collapse_automation.py`

**Important:** Never upload `.env` to GitHub! (It's in `.gitignore`)

---

## Content Sources Currently Configured

### Reddit Subreddits:
1. **r/collapse** - Societal collapse discussions
2. **r/lostgeneration** - Economic despair, generational wealth gap
3. **r/antiwork** - Worker exploitation, layoff stories
4. **r/ABoringDystopia** - Late-stage capitalism critique
5. **r/Futurology** - AI takeover concerns

### News RSS Feeds:
1. **ZeroHedge** - Economic doom, market crashes, alternative finance
2. **Wolf Street** - Housing bubble, inflation, debt crisis
3. **TechCrunch** - Tech layoffs, AI announcements
4. **Ars Technica** - AI developments, technology news

### YouTube Channels:
1. **Michael Bordenaro** - Housing market collapse, job losses
2. **Peter Schiff** - Economic doom, dollar collapse, inflation
3. **Economics Explained** - Economic analysis, country collapses
4. **Robert Miles** - AI safety, existential risk, alignment
5. **David Shapiro** - AI automation, job displacement, post-labor

---

## What Happens When It Runs

1. Bot randomly selects content type based on probabilities:
   - 30% chance: Reddit post
   - 30% chance: News article
   - 20% chance: YouTube video
   - 20% chance: Original AI post

2. **If Reddit post:**
   - Fetches top posts (50+ upvotes) from collapse subreddits
   - Gemini generates commentary about the discussion
   - Posts to Facebook with Reddit link

3. **If News article:**
   - Parses RSS feeds from news sources
   - Filters for doom-relevant keywords (layoffs, AI, recession, etc.)
   - Gemini analyzes the article
   - Posts to Facebook with article link

4. **If YouTube video:**
   - Randomly selects from 5 most recent videos across all channels
   - Gemini generates commentary about the video
   - Posts to Facebook with video link

5. **If Original post:**
   - Gemini generates doom content about random topic
   - Posts to Facebook (no external link)

6. Logs success/failure

---

## Free Tier Limits

- **GitHub Actions:** Unlimited for public repos ✅
- **Gemini API:** 15 requests/min, 1M requests/day ✅
- **Facebook API:** No practical limit for this usage ✅

**Total cost: $0/month** 🎉

---

## Tips

- Check your Facebook page after first manual test
- Monitor GitHub Actions logs to see what's being posted
- Token expires in 60 days - set a calendar reminder to renew
- You can disable the bot by pausing the GitHub Action workflow

---

## Need Help?

- Check GitHub Actions logs for error messages
- Most issues are: wrong secrets, app in dev mode, or expired token
- You can always manually trigger a test run to debug

---

**You're all set! The bot will now run automatically 5x per day.** 🚀
