# AI Web Scraper 🤖🌐

An intelligent web scraping application that combines the power of AI language models with advanced browser automation to extract and parse web content. Built with Streamlit for an intuitive user interface, this tool allows you to scrape websites and intelligently extract specific information using natural language queries.

## ✨ Features

- **Smart Web Scraping**: Uses Playwright with BrightData's Browser API to scrape modern web pages, including JavaScript-rendered content
- **AI-Powered Parsing**: Leverages OpenAI's GPT models or local Ollama models to intelligently extract specific information from scraped content
- **Natural Language Queries**: Simply describe what you want to extract in plain English
- **Clean Content Extraction**: Automatically removes scripts, styles, and unnecessary HTML to focus on meaningful content
- **Interactive UI**: Built with Streamlit for a user-friendly, web-based interface
- **Chunked Processing**: Handles large web pages by intelligently splitting content into processable chunks

## 🔧 Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- BrightData Browser API credentials ([Sign up here](https://brightdata.com/))
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- (Optional) Ollama installed locally for offline AI processing

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/apadlo/ai-web-scrapper.git
   cd ai-web-scrapper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with your API credentials:

```env
# BrightData Browser API credentials
AUTH=YOUR_USERNAME:YOUR_PASSWORD

# OpenAI API Key
OPENAI_API_KEY=your-openai-api-key-here
```

**Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## 🚀 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Scrape a website**
   - Enter the URL of the website you want to scrape
   - Click "Scrape Website"
   - Wait for the content to be extracted and cleaned

3. **Parse content with AI**
   - Once scraping is complete, describe what information you want to extract
   - For example: "Extract all product names and prices" or "Find all email addresses"
   - Click "Parse Content"
   - The AI will process the content and return only the information you requested

## 📁 Project Structure

```
ai-web-scrapper/
├── app.py              # Main Streamlit application
├── browser_client.py   # Web scraping with Playwright & BrightData
├── parse.py           # AI parsing using OpenAI or Ollama
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (not in repo)
└── README.md         # This file
```

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/)**: Interactive web UI framework
- **[Playwright](https://playwright.dev/python/)**: Browser automation for web scraping
- **[BrightData](https://brightdata.com/)**: Proxy and browser automation infrastructure
- **[OpenAI GPT](https://openai.com/)**: Advanced language model for content parsing
- **[Ollama](https://ollama.ai/)**: Local AI model alternative (optional)
- **[LangChain](https://www.langchain.com/)**: LLM application framework
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)**: HTML parsing and cleaning

## 💡 Example Use Cases

- Extract product information from e-commerce sites
- Gather contact information from business directories
- Collect article titles and summaries from news sites
- Extract structured data from unstructured web content
- Monitor competitor websites for specific information

## 🔒 Security Notes

- Always keep your API credentials secure in the `.env` file
- Never commit sensitive credentials to version control
- Be mindful of website terms of service when scraping
- Respect robots.txt and rate limits

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Always ensure you have permission to scrape websites and comply with their terms of service and robots.txt files.
