from dotenv import load_dotenv
import asyncio
import sys
from bs4 import BeautifulSoup
from os import environ
from playwright.async_api import async_playwright

# Load environment variables from .env if present.
load_dotenv()

# Set your Browser API credentials via AUTH in .env or environment.
AUTH = environ.get("AUTH")
TARGET_URL_DEFAULT = "https://example.com"

async def _scrape_with_browser_api(url: str = TARGET_URL_DEFAULT) -> str:
    if not AUTH or AUTH == "USER:PASS":
        raise Exception(
            "Set your Browser API credentials in AUTH env var or in .env."
        )

    print("Connecting to Browser API...")
    endpoint_url = f"wss://{AUTH}@brd.superproxy.io:9222"

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(endpoint_url)
        try:
            page = await browser.new_page()
            await page.goto(url, timeout=2 * 60_000)
            html = await page.content()
            return html
        finally:
            await browser.close()

def scrape_with_browser_api(url: str) -> str:
    """Sync wrapper so Streamlit can call it easily."""
    # For Windows, we need to use ProactorEventLoop for subprocess support
    if sys.platform == "win32":
        # Create a new ProactorEventLoop
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        return loop.run_until_complete(_scrape_with_browser_api(url))
    finally:
        loop.close()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
