import streamlit as st
from urllib.parse import urlparse
from browser_client import (
    scrape_with_browser_api,
    extract_body_content,
        clean_body_content,
        split_dom_content,
    )
from parse import parse_with_openai

# Streamlit UI
st.title("Smart Scraper")

# Add app description and flow
st.markdown("""
### 📋 How This App Works

This AI-powered web scraper helps you extract specific information from any website using natural language instructions.

#### Application Flow:

1. **🌐 Enter a Website URL**  
   Paste the URL of the website you want to scrape in the input field below.

2. **🔍 Scrape the Website**  
   Click the "Scrape Website" button to fetch and clean the website's content.  
   The app will extract all visible text from the page and remove unnecessary HTML tags.

3. **👀 Review the DOM Content** *(Optional)*  
   Expand the "View DOM Content" section to see the raw extracted text from the website.

4. **💬 Describe What to Parse**  
   Enter a natural language description of what information you want to extract.  
   Examples: *"Extract all product names and prices"* or *"Get contact information"*

5. **🤖 Parse Content with AI**  
   Click "Parse Content" to let AI analyze the scraped content and extract the specific information you requested.  
   The AI will intelligently parse the content and return structured results.

---
""")

url = st.text_input("Enter Website URL", placeholder="https://www.example.com")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if not url:
        st.error("❌ Please enter a website URL")
    else:
        # Normalize and validate URL
        normalized_url = url.strip()
        parsed_url = urlparse(normalized_url)
        
        if parsed_url.scheme.lower() not in ("http", "https"):
            st.error("❌ Please enter a full URL starting with http:// or https://")
        elif not parsed_url.netloc:
            st.error("❌ Please enter a valid URL with a host (e.g., https://example.com)")
        else:
            url = normalized_url
            try:
                st.write("Scraping the website...")

                # Scrape the website
                dom_content = scrape_with_browser_api(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = clean_body_content(body_content)

                # Store the DOM content in Streamlit session state
                st.session_state.dom_content = cleaned_content

                # Display the DOM content in an expandable text box
                with st.expander("View DOM Content"):
                    st.text_area("DOM Content", cleaned_content, height=300)
            except Exception as e:
                st.error(f"❌ Error scraping the website: {str(e)}")


# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            # Parse the content with Ollama
            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_openai(dom_chunks, parse_description)
            st.write(parsed_result)

