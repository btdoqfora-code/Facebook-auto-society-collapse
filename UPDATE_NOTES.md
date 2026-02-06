# Updates Made to Collapse Automation Bot

## Date: February 6, 2026

### Changes Made:

1. **Updated Gemini Model** (CRITICAL FIX)
   - Changed from `gemini-2.0-flash-exp` to `gemini-3-flash-preview`
   - Updated in all 4 functions that use Gemini:
     - `generate_reddit_post()`
     - `generate_news_post()`
     - `generate_video_post()`
     - `generate_original_post()`

2. **Facebook Graph API Version** (Already Correct)
   - Confirmed using v24.0 in the `post_to_facebook()` function
   - URL: `https://graph.facebook.com/v24.0/{FB_PAGE_ID}/feed`
   - This is the correct endpoint for posting text updates

3. **Documentation Updates**
   - Updated README.md to reference Gemini 3 Flash Preview
   - Updated SETUP_GUIDE.md to reference Gemini 3 Flash Preview

4. **Additional Files Created**
   - `.gitignore` - Protects your .env file from being uploaded to GitHub
   - `.env.example` - Template for local testing setup

### Your Page Configuration:

Your Page ID: **960131433852420**
Correct endpoint: `https://graph.facebook.com/v24.0/960131433852420/feed`

### Next Steps:

1. Upload all these files to your GitHub repository
2. Make sure your GitHub secrets are set:
   - `FB_PAGE_ID` = 960131433852420
   - `FB_ACCESS_TOKEN` = your long-lived token
   - `GEMINI_API_KEY` = your Gemini API key

3. Ensure your Facebook app is in **Live mode** (not Development)

4. Test by manually triggering the GitHub Action

### Files to Upload to GitHub:

1. `collapse_automation.py` (main script - UPDATED)
2. `requirements.txt` (dependencies)
3. `collapse_automation.yml` (goes in `.github/workflows/` folder)
4. `README.md` (documentation - UPDATED)
5. `SETUP_GUIDE.md` (setup instructions - UPDATED)
6. `.gitignore` (protects secrets - NEW)
7. `.env.example` (template for local testing - NEW)

### Troubleshooting Reminder:

If you see "Post is empty" error:
- This usually means the message parameter is blank
- Check GitHub Actions logs to see what content was generated
- Make sure Gemini API key is valid and working

If you see 403 error:
- App must be in Live mode (not Development)
- Check that token has `pages_manage_posts` permission

If token expires:
- Generate new long-lived token every 60 days
- Update the `FB_ACCESS_TOKEN` secret in GitHub
