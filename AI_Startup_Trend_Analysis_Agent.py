import streamlit as st
import google.generativeai as genai
from ddgs import DDGS  # Updated import
import requests
from bs4 import BeautifulSoup
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit app setup
st.set_page_config(page_title="AI Startup Trend Analysis", layout="wide")
st.title("🚀 AI Startup Trend Analysis Agent")
st.caption("Discover emerging trends and opportunities in your chosen startup sector.")

# Configuration
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
MAX_ARTICLES = 5
SUMMARY_LENGTH = 100

# Initialize Gemini model
def init_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {str(e)}")
        return None

# Improved web content extraction
def extract_content(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()
        
        # Try to find main content
        for tag in ['article', 'main', 'div.article-content', 'div.content']:
            content = soup.find(tag)
            if content:
                return content.get_text(separator='\n', strip=True)
        
        return soup.get_text(separator='\n', strip=True)[:5000]
    except Exception as e:
        logger.warning(f"Content extraction failed for {url}: {str(e)}")
        return None

# News collection with domain filtering
def collect_news(topic, language='en'):
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(
                f"{topic} startup news site:.com",
                region='wt-wt',
                safesearch='off',
                max_results=MAX_ARTICLES * 2  # Get extra to filter
            ):
                if not any(d in r['href'] for d in ['zhihu.com', 'weixin.qq.com']):
                    results.append(r)
                    if len(results) >= MAX_ARTICLES:
                        break
        
        return [{"title": r["title"], "url": r["href"]} for r in results]
    except Exception as e:
        logger.error(f"News collection failed: {str(e)}")
        return []

# Article summarization
def summarize_article(url, content, model, topic):
    try:
        prompt = f"""
        Summarize this article about {topic} in {SUMMARY_LENGTH} words or less, 
        focusing on key insights relevant to startups and entrepreneurs:
        
        {content[:3000]}
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        return f"Summary unavailable: {str(e)}"

# Main analysis function
def run_analysis(topic, model):
    with st.status("Analyzing startup trends...") as status:
        try:
            # Step 1: Collect news
            st.write("🔍 Searching for relevant articles...")
            articles = collect_news(topic)
            
            if not articles:
                st.error("No suitable articles found. Try a different topic.")
                return
            
            # Step 2: Process articles
            st.write("📝 Analyzing articles...")
            results = []
            
            for article in articles:
                content = extract_content(article["url"])
                
                if not content:
                    logger.warning(f"Skipping article: {article['url']}")
                    continue
                
                summary = summarize_article(
                    article["url"], 
                    content, 
                    model, 
                    topic
                )
                
                results.append({
                    "title": article["title"],
                    "url": article["url"],
                    "summary": summary
                })
            
            # Display results
            st.subheader("📰 Article Summaries")
            for result in results:
                st.markdown(f"### {result['title']}")
                st.markdown(result['summary'])
                st.markdown(f"[Read original article]({result['url']})")
                st.divider()
            
            # Step 3: Generate trend report
            if results:
                st.write("📊 Generating trend report...")
                report = generate_trend_report(results, model, topic)
                st.subheader("📈 Startup Trend Analysis Report")
                st.markdown(report)
                status.update(label="Analysis complete!", state="complete")
            else:
                st.warning("No valid articles could be analyzed")
                status.update(label="Analysis incomplete", state="error")
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            logger.exception("Analysis error")
            status.update(label="Analysis failed", state="error")

# Trend report generation
def generate_trend_report(articles, model, topic):
    article_text = "\n\n".join(
        f"**{a['title']}**\n{a['summary']}\nURL: {a['url']}" 
        for a in articles
    )
    
    prompt = f"""
    Analyze these {topic} articles and provide:
    
    1. **Key Trends** (3-5 bullet points)
    2. **Market Opportunities** (specific areas for innovation)
    3. **Competitive Landscape** (major players and gaps)
    4. **Actionable Recommendations** (for startups)
    
    Articles:
    {article_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Trend analysis failed: {str(e)}"

# UI Components
gemini_api_key = st.sidebar.text_input("Enter Google Gemini API Key", type="password")
topic = st.text_input("Enter startup sector:", placeholder="e.g., AI in Healthcare")

if st.button("Generate Analysis", type="primary"):
    if not gemini_api_key or not topic:
        st.warning("Please enter both API key and topic")
    else:
        model = init_gemini(gemini_api_key)
        if model:
            run_analysis(topic, model)

