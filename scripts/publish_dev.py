#!/usr/bin/env python3
"""
Publishes or drafts the Hacktoberfest Week 1 blog post to DEV (dev.to).
Usage:
    python3 scripts/publish_dev.py [--publish] [--api-key YOUR_DEV_KEY]

If --publish is passed, the article is published live; otherwise, it is saved as an unpublished draft on DEV.
"""

import os
import sys
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env
load_dotenv(Path(__file__).parent.parent / ".env")

DEV_API_URL = "https://dev.to/api/articles"
BLOG_POST_PATH = Path(__file__).parent.parent / "BLOG_POST.md"

def parse_frontmatter_and_body(content: str):
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    
    frontmatter_str = parts[1].strip()
    body = parts[2].strip()
    
    meta = {}
    for line in frontmatter_str.split("\n"):
        line = line.strip()
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k == "tags":
                meta[k] = [t.strip() for t in v.split(",") if t.strip()]
            elif k == "published":
                meta[k] = v.lower() in ("true", "1", "yes")
            else:
                meta[k] = v
    return meta, body

def main():
    parser = argparse.ArgumentParser(description="Publish Chadodoro blog post to DEV (dev.to)")
    parser.add_argument("--api-key", help="DEV.to API Key (or set DEV_API_KEY in .env)")
    parser.add_argument("--publish", action="store_true", help="Publish immediately (defaults to unpublished draft)")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("DEV_API_KEY") or os.getenv("DEV_TOKEN")

    if not api_key:
        print("\n❌ No DEV.to API key found.")
        print("To publish via API:")
        print("1. Log in to https://dev.to")
        print("2. Go to Settings -> Extensions: https://dev.to/settings/extensions")
        print("3. Generate a DEV Community API Key")
        print("4. Run:\n   python3 scripts/publish_dev.py --api-key YOUR_KEY\n   or add DEV_API_KEY=\"...\" to your .env file.\n")
        print("Alternatively, copy the contents of BLOG_POST.md directly into https://dev.to/new\n")
        sys.exit(1)

    if not BLOG_POST_PATH.exists():
        print(f"❌ Error: {BLOG_POST_PATH} not found.")
        sys.exit(1)

    with open(BLOG_POST_PATH, "r", encoding="utf-8") as f:
        raw_text = f.read()

    meta, body = parse_frontmatter_and_body(raw_text)

    title = meta.get("title", "Chadodoro: The Stoic GigaChad Pomodoro Coach That Forces You to Touch Physical Grass")
    tags = meta.get("tags", ["devchallenge", "hf26challenge", "elevenlabs", "opensource"])
    canonical_url = meta.get("canonical_url", "https://chadodoro.ntsd.dev/")
    cover_image = meta.get("cover_image")
    published = args.publish or meta.get("published", False)

    payload = {
        "article": {
            "title": title,
            "body_markdown": body,
            "published": published,
            "tags": tags,
            "canonical_url": canonical_url,
        }
    }
    if cover_image:
        payload["article"]["main_image"] = cover_image

    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "User-Agent": "Chadodoro-Publisher/1.0"
    }

    print(f"\n📡 Sending article to DEV ({'PUBLISHED' if published else 'DRAFT'})...")
    res = requests.post(DEV_API_URL, json=payload, headers=headers, timeout=20)

    if res.status_code in (200, 201):
        data = res.json()
        print("\n✅ Successfully created DEV article!")
        print(f"Title: {data.get('title')}")
        print(f"URL: {data.get('url')}")
        print(f"Edit URL: https://dev.to/{data.get('user', {}).get('username', 'dashboard')}/{data.get('slug', '')}/edit")
    else:
        print(f"\n❌ Error from DEV API ({res.status_code}):")
        print(res.text)
        sys.exit(1)

if __name__ == "__main__":
    main()
