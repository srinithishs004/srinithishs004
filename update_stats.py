import urllib.request
import re
import os
import sys

username = "srinithishs004"
readme_path = os.path.join(os.path.dirname(__file__), "README.md")

# 1. Fetch contributions
contrib_url = f"https://github.com/users/{username}/contributions"
req = urllib.request.Request(contrib_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        contrib_html = response.read().decode('utf-8')
    match = re.search(r'(\d+)\s+contributions\s+in\s+the\s+last\s+year', contrib_html, re.IGNORECASE)
    contributions = match.group(1) if match else "N/A"
except Exception as e:
    print("Error getting contributions:", e)
    contributions = "N/A"

# 2. Fetch main profile stats
profile_url = f"https://github.com/{username}"
req = urllib.request.Request(profile_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response:
        profile_html = response.read().decode('utf-8')
    
    followers_match = re.search(r'<span[^>]*class="text-bold color-fg-default">([^<]+)</span>\s*followers', profile_html)
    followers = followers_match.group(1).strip() if followers_match else "N/A"

    following_match = re.search(r'<span[^>]*class="text-bold color-fg-default">([^<]+)</span>\s*following', profile_html)
    following = following_match.group(1).strip() if following_match else "N/A"

    repos_match = re.search(r'Repositories\s*<span[^>]*class="Counter"[^>]*>([^<]+)</span>', profile_html)
    repos = repos_match.group(1).strip() if repos_match else "N/A"
except Exception as e:
    print("Error getting profile stats:", e)
    followers, following, repos = "N/A", "N/A", "N/A"

print(f"Stats fetched: Contributions: {contributions}, Repos: {repos}, Followers: {followers}, Following: {following}")

# Safeguard check: Do not update README if any stats failed to fetch
if "N/A" in [contributions, repos, followers, following]:
    print("Safeguard triggered: One or more stats failed to fetch. Aborting README update to preserve existing metrics.")
    sys.exit(0)

# 3. Read README.md
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    new_stats_block = f"""<!-- START_SECTION:dynamic_stats -->
- 🌌 **Total Contributions**: **{contributions}** (in the last year)
- 📂 **Public Repositories**: **{repos}**
- 👥 **Followers**: **{followers}**
- 🤝 **Following**: **{following}**
<!-- END_SECTION:dynamic_stats -->"""

    pattern = r'<!-- START_SECTION:dynamic_stats -->.*?<!-- END_SECTION:dynamic_stats -->'
    updated_content = re.sub(pattern, new_stats_block, readme_content, flags=re.DOTALL)

    # 4. Write back to README.md
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("README.md dynamic stats successfully updated.")
else:
    print("README.md not found in the script directory.")
