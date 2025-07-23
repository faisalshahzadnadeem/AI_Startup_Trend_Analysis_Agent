import streamlit as st
import requests
from bs4 import BeautifulSoup
import logging
from ddgs import DDGS
from crewai import Agent, Task, Crew
from crewai_tools import tool
import google.generativeai as genai

# --- Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Streamlit Setup ---
st.set_page_config(page_title="AI Startup Trend Analysis (CrewAI)", layout="wide")
st.title("🚀 AI Startup Trend Analysis (CrewAI Agent)")
st.caption("Automated multi-step trend research using CrewAI agents.")

# --- Config ---
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
MAX_ARTICLES = 5
SUMMARY_LENGTH = 100

# --- Initialize Gemini ---
def init_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"Gemini init failed: {e}")
        return None

# --- CrewAI Tools ---
@tool("collect_news")
def collect_news_tool(topic: str) -> list:
    """Search startup news articles for a topic using DuckDuckGo."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(f"{topic} startup news site:.com", region='wt-wt',
                               safesearch='off', max_results=MAX_ARTICLES * 2):
                if not any(d in r['href'] for d in ['zhihu.com', 'weixin.qq.com']):
                    results.append({"title": r["title"], "url": r["href"]})
                    if len(results) >= MAX_ARTICLES:
                        break
        return results
    except Exception as e:
        logger.error(f"News collection failed: {e}")
        return []

@tool("extract_content")
def extract_content_tool(url: str) -> str:
    """Extracts readable text content from a webpage."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for el in soup(['script', 'style', 'nav', 'footer']):
            el.decompose()
        for tag in ['article', 'main', 'div.article-content', 'div.content']:
            content = soup.find(tag)
            if content:
                return content.get_text(separator='\n', strip=True)
        return soup.get_text(separator='\n', strip=True)[:5000]
    except Exception as e:
        logger.warning(f"Extraction failed for {url}: {e}")
        return ""

# --- CrewAI Agent ---
def build_startup_trend_agent(model):
    return Agent(
        role="Startup Trend Analyst",
        goal="Find and analyze the latest startup sector trends.",
        backstory="An AI assistant specialized in web research and summarization for entrepreneurs.",
        tools=[collect_news_tool, extract_content_tool],
        llm=model,
        verbose=True
    )

# --- Task Pipeline ---
def create_tasks(agent, topic):
    return [
        Task(
            description=f"Search for the top {MAX_ARTICLES} news articles about {topic} startups.",
            agent=agent,
            expected_output="List of articles (title + URL)."
        ),
        Task(
            description="Extract readable content from each article.",
            agent=agent,
            expected_output="Clean text for each article."
        ),
        Task(
            description=f"Summarize each article in under {SUMMARY_LENGTH} words, focusing on key trends.",
            agent=agent,
            expected_output="Concise summaries for each article."
        ),
        Task(
            description=f"""
            Analyze all summaries and produce:
            1. Key Trends (3-5 points)
            2. Market Opportunities
            3. Competitive Landscape
            4. Actionable Recommendations for startups in {topic}.
            """,
            agent=agent,
            expected_output="Structured trend analysis report."
        )
    ]

# --- Run CrewAI ---
def run_crew_analysis(topic, model):
    agent = build_startup_trend_agent(model)
    tasks = create_tasks(agent, topic)
    crew = Crew(agents=[agent], tasks=tasks, verbose=True)

    with st.status("Running CrewAI pipeline...") as status:
        try:
            result = crew.kickoff()
            status.update(label="Analysis complete!", state="complete")
            return result
        except Exception as e:
            status.update(label="Analysis failed", state="error")
            st.error(f"Error: {e}")
            logger.exception(e)
            return None

# --- UI ---
api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
topic = st.text_input("Enter startup sector:", placeholder="e.g., AI in Healthcare")

if st.button("Run CrewAI Trend Analysis", type="primary"):
    if not api_key or not topic:
        st.warning("Enter API key and topic.")
    else:
        model = init_gemini(api_key)
        if model:
            result = run_crew_analysis(topic, model)
            if result:
                st.subheader("📊 Startup Trend Analysis Report")
                st.markdown(result)
