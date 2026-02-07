from dotenv import load_dotenv
import asyncio
import sys
from bs4 import BeautifulSoup
from os import environ
from playwright.sync_api import Playwright, sync_playwright

# Load environment variables from .env if present.
load_dotenv()

# Set your Browser API credentials via AUTH in .env or environment.
AUTH = environ.get("AUTH")
TARGET_URL_DEFAULT = "https://example.com"

def _scrape_with_browser_api_sync(playwright: Playwright, url: str = TARGET_URL_DEFAULT) -> str:
    if not AUTH or AUTH == "USER:PASS":
        raise Exception(
            "Provide Scraping Browsers credentials in AUTH environment variable or update the script."
        )
    print("Connecting to Browser...")
    endpoint_url = f"wss://{AUTH}@brd.superproxy.io:9222"
    browser = playwright.chromium.connect_over_cdp(endpoint_url)
    try:
        print(f"Connected! Navigating to {url}...")
        page = browser.new_page()
        client = page.context.new_cdp_session(page)
        page.goto(url, timeout=2 * 60_000)
        print("Navigated! Waiting captcha to detect and solve...")
        result = client.send(
            "Captcha.waitForSolve",
            {
                "detectTimeout": 10 * 1000,
            },
        )
        status = result.get("status")
        print(f"Captcha status: {status}")
        return page.content()
    finally:
        browser.close()


def _ensure_windows_proactor_policy() -> None:
    if sys.platform != "win32":
        return
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        # Fallback for runtimes that removed the policy helper.
        return


def scrape_with_browser_api(url: str) -> str:
    _ensure_windows_proactor_policy()
    with sync_playwright() as playwright:
        return _scrape_with_browser_api_sync(playwright, url)

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
