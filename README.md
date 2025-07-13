# 🚀 AI Startup Trend Analysis Agent

**Discover emerging trends and opportunities in your chosen startup sector.**  
This intelligent Streamlit application gathers, summarizes, and analyzes the latest news articles from the web using real-time search and the Google Gemini LLM to generate actionable startup insights.

---

## 🌟 Features

- 🔍 **Real-Time Web Search** using DuckDuckGo
- 📄 **Content Extraction** from top startup articles
- 🧠 **LLM-Powered Summarization** with Google Gemini 2.0 Flash
- 📊 **Automated Trend Report** generation (Key trends, Opportunities, Competitors, and Recommendations)
- ⚡ Built with **Streamlit** for an interactive, responsive UI


## 🧱 Tech Stack

- **Frontend:** Streamlit
- **LLM Integration:** Google Gemini (`generativeai`)
- **Search API:** DuckDuckGo Search via `ddgs`
- **Web Parsing:** BeautifulSoup & Requests
- **Logging & Status:** Python `logging` + Streamlit `st.status`

---

## 🚀 How It Works

1. **User Input:** Enter a startup sector (e.g., "AI in healthcare").
2. **News Gathering:** Top startup-related articles are fetched via DuckDuckGo.
3. **Article Extraction:** Content is extracted and cleaned using BeautifulSoup.
4. **Summarization:** Each article is summarized using Google Gemini API.
5. **Trend Analysis:** A consolidated report is generated, highlighting:
   - 🔑 Key Trends  
   - 💼 Market Opportunities  
   - 🏆 Competitive Landscape  
   - ✅ Actionable Recommendations  

---

## 📦 Installation

```bash
git clone https://github.com/faisalshahzadnadeem /ai-startup-trend-analysis.git
cd ai-startup-trend-analysis
pip install -r requirements.txt

