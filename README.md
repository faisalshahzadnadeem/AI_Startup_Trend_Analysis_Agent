# AI_Startup_Trend_Analysis_Agent
A Streamlit application that analyzes emerging trends and opportunities in your chosen startup sector using Google Gemini and web scraping.
Features

Real-time News Collection: Gathers recent articles from trusted sources using DuckDuckGo search.
Content Extraction: Extracts meaningful content from articles using BeautifulSoup.
AI-Powered Summarization: Summarizes articles with Google Gemini for concise insights.
Trend Analysis: Generates a detailed report on key trends, market opportunities, competitive landscape, and actionable recommendations.
User-Friendly Interface: Built with Streamlit for an interactive and intuitive experience.

Prerequisites

Python 3.8+
Google Gemini API Key (obtain from Google AI Studio)
Internet connection for web scraping and API calls

Installation

Clone the repository:
git clone https://github.com/faisalshahzadnadeem /ai-startup-trend-analysis.git
cd ai-startup-trend-analysis


Install dependencies:
pip install -r requirements.txt


Run the application:
streamlit run app.py



Usage

Open the app in your browser (typically at http://localhost:8501).
Enter your Google Gemini API key in the sidebar.
Input a startup sector (e.g., "AI in Healthcare") in the text box.
Click "Generate Analysis" to fetch, summarize, and analyze articles.
View the article summaries and a comprehensive trend report.

Requirements
See requirements.txt for the full list of dependencies.
File Structure

app.py: Main application script containing the Streamlit app and logic.
requirements.txt: Python dependencies required to run the app.
README.md: This file, providing an overview and setup instructions.

Notes

The app uses DuckDuckGo for news collection and filters out low-quality domains.
Summaries are limited to 100 words for brevity.
Maximum of 5 articles are analyzed to ensure quick results.
Ensure a valid Gemini API key is provided for summarization and trend analysis.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.
License
This project is licensed under the MIT License.
