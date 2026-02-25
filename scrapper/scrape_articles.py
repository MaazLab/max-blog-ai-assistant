import asyncio
import re
from urllib.parse import urljoin
from pathlib import Path

from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
from markdownify import markdownify as md


BASE_URL = "https://maximilian-schwarzmueller.com"
ARTICLES_URL = f"{BASE_URL}/articles"

# Project root (parent of scrapper folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "articles"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ----------------------------
# Utility: Clean Filename
# ----------------------------
def clean_filename(title: str) -> str:
    title = title.strip().lower()
    title = re.sub(r"[^\w\s-]", "", title)
    title = re.sub(r"\s+", "-", title)
    return title


# ----------------------------
# Extract Article Links
# ----------------------------
async def extract_article_links(crawler):
    result = await crawler.arun(url=ARTICLES_URL)

    if not result.success:
        print("❌ Failed to load articles page")
        return []

    soup = BeautifulSoup(result.html, "html.parser")

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("/articles/") and href != "/articles":
            links.add(urljoin(BASE_URL, href))

    print(f"✅ Found {len(links)} articles")
    return list(links)


# ----------------------------
# Extract Clean Article HTML
# ----------------------------
def extract_clean_article_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("article")
    if not article:
        return ""

    # Remove unwanted structural elements
    for tag in article.find_all(["nav", "footer", "aside"]):
        tag.decompose()

    # Remove promotional course blocks
    for link in article.find_all("a"):
        href = link.get("href", "")
        if "acad.link" in href:
            link.decompose()

    # Remove duplicate H1 (we store in frontmatter)
    h1 = article.find("h1")
    if h1:
        h1.decompose()

    # Convert cleaned HTML → Markdown
    markdown_content = md(
        str(article),
        heading_style="ATX"
    )

    return markdown_content.strip()


# ----------------------------
# Scrape Single Article
# ----------------------------
async def scrape_article(crawler, url):
    result = await crawler.arun(url=url)

    if not result.success:
        print(f"❌ Failed to scrape: {url}")
        return None

    soup = BeautifulSoup(result.html, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

    date_tag = soup.find("time")
    published_date = date_tag.get_text(strip=True) if date_tag else ""

    clean_markdown = extract_clean_article_markdown(result.html)

    return {
        "title": title,
        "date": published_date,
        "content": clean_markdown,
        "url": url,
    }


# ----------------------------
# Save MDX File
# ----------------------------
def write_mdx(article_data):
    filename = OUTPUT_DIR / f"{clean_filename(article_data['title'])}.mdx"

    frontmatter = f"""---
title: "{article_data['title']}"
date: "{article_data['date']}"
source: "{article_data['url']}"
---

"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(frontmatter)
        f.write(article_data["content"])

    print(f"📄 Saved: {filename.name}")


# ----------------------------
# Main
# ----------------------------
async def main():
    async with AsyncWebCrawler() as crawler:
        article_links = await extract_article_links(crawler)

        for idx, link in enumerate(article_links, start=1):
            print(f"[{idx}/{len(article_links)}] Scraping: {link}")

            article_data = await scrape_article(crawler, link)
            if article_data and article_data["content"]:
                write_mdx(article_data)

    print("🎉 Clean articles saved in /articles folder")


if __name__ == "__main__":
    asyncio.run(main())