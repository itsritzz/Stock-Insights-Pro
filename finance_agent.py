import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Agent 1: For web search
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    role="Search the web for information and print sources",
    tools=[DuckDuckGoTools()],
    instructions="ALWAYS include sources and provide relevant news.",
    show_tool_calls=True,
    markdown=True,
)

# Agent 2: To access financial data
finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    role="Get financial data",
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# To assign roles based on the task to different agents
agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["First, get analyst recommendation for the stock user has asked for, Use tables to display data",
                  "Then fetch the latest news for the given stock"],
    show_tool_calls=False,
    markdown=True,
)

# Page configuration with custom theme
st.set_page_config(
    page_title="Stock Insights Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main gradient background */
    .main {
        background: linear-gradient(135deg, #f0f5ff 0%, #e6f0ff 100%);
    }

    /* Container styling */
    .css-1d391kg, .css-1r6slb0 {
        background: linear-gradient(to right, rgba(230, 240, 255, 0.7), rgba(240, 245, 255, 0.7));
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border: 1px solid rgba(200, 220, 250, 0.5);
    }

    /* Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
    }

    h1 {
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        margin-bottom: 1.5rem !important;
        text-align: center;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6, #0ea5e9);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #0284c7);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }

    /* Select box and text input */
    .stSelectbox > div, .stTextInput > div:first-child {
        border-radius: 8px;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }

    .stSelectbox > div:hover, .stTextInput > div:first-child:hover {
        border: 1px solid rgba(59, 130, 246, 0.7);
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #3b82f6 !important;
    }

    /* Tables */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
        border: none !important;
    }

    .dataframe th {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
        color: white;
        font-weight: 500;
        text-align: center !important;
        border: none !important;
    }

    .dataframe td {
        background-color: rgba(240, 245, 255, 0.7);
        color: #2c3e50;
        text-align: left !important;
        border: none !important;
        border-bottom: 1px solid rgba(59, 130, 246, 0.1) !important;
    }

    /* Card layout */
    .card {
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: #2c3e50;
    }

    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    }

    /* Dashboard metrics */
    .metric-card {
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        background: linear-gradient(145deg, #f0f5ff, #e6f0ff);
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 10px 0;
        background: linear-gradient(90deg, #2563eb, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: linear-gradient(90deg, rgba(240, 245, 255, 0.9), rgba(230, 240, 255, 0.9));
        font-size: 12px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #64748b;
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(59, 130, 246, 0.1);
        z-index: 999;
    }

    .footer a {
        color: #3b82f6;
        text-decoration: none;
        margin: 0 8px;
        transition: color 0.3s ease;
    }

    .footer a:hover {
        color: #2563eb;
        text-decoration: underline;
    }

    /* Sidebar */
    .css-6qob1r {
        background: linear-gradient(to bottom, #e6f0ff, #f0f5ff);
        border-right: 1px solid rgba(59, 130, 246, 0.1);
    }

    /* Improve readability for markdown content */
    .markdown-text-container {
        line-height: 1.7;
        color: #2c3e50;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f0f5ff;
    }

    ::-webkit-scrollbar-thumb {
        background: #93c5fd;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #60a5fa;
    }

    /* Divider */
    hr {
        margin: 2rem 0;
        border: 0;
        height: 1px;
        background-image: linear-gradient(to right, rgba(59, 130, 246, 0), rgba(59, 130, 246, 0.5), rgba(59, 130, 246, 0));
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/stocks-growth.png", width=80)
    st.title("Navigation")

    st.markdown("---")
    page = st.radio("", ["Dashboard", "About", "Help"])

    st.markdown("---")
    st.subheader("Market Overview")

    # Mock market data
    col1, col2 = st.columns(2)
    with col1:
        st.metric("S&P 500", "5,218.24", "+0.43%")
    with col2:
        st.metric("NASDAQ", "16,389.37", "+0.21%")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("DOW", "39,126.84", "-0.12%")
    with col2:
        st.metric("VIX", "15.82", "+2.14%")

    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%B %d, %Y %H:%M')}")

# Main content
if page == "Dashboard":
    # Header with animations
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 30px 0;">
        <h1>📈 Stock Insights Pro</h1>
        <p style="font-size: 1.2rem; color: #94a3b8; margin-top: -15px;">
            Advanced AI-Powered Financial Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">AI-Powered Analysis</div>
            <div class="metric-value">Real-Time</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Data Sources</div>
            <div class="metric-value">Multiple</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Analyst Insights</div>
            <div class="metric-value">Curated</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stock selection area with improved layout
    st.markdown("""
    <div class="card">
        <h2 style="font-size: 1.5rem; margin-bottom: 15px;">Select Your Stock</h2>
        <p style="color: #94a3b8; margin-bottom: 20px;">
            Choose a stock from our popular selections or enter a custom symbol to get analyst recommendations and the latest news.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        # Popular stocks with logos
        popular_stocks = ["NVDA", "AAPL", "TSLA", "MSFT", "AMZN", "GOOG", "META", "AMD"]
        selected_stock = st.selectbox("Choose a popular stock:", popular_stocks)

    with col2:
        # Option for manual entry
        manual_stock = st.text_input("Or enter a custom symbol:")

    # Determine stock to use
    stock_to_use = manual_stock.strip().upper() if manual_stock else selected_stock

    # More prominent button
    if st.button(f"📊 Analyze {stock_to_use}"):
        # Show fancy loader
        with st.spinner(f"🔍 Analyzing {stock_to_use}... Please wait while our AI examines market data and news"):
            try:
                # Create tabs for organized display
                tab1, tab2 = st.tabs(["📈 Analysis Results", "⚙️ Technical Details"])

                with tab1:
                    # Get the response from the agent team
                    response = agent_team.run(
                        f"Provide analyst recommendations and also share the latest news from the web for {stock_to_use}",
                        stream=False)

                    if response:
                        # Success message
                        st.success(f"✅ Analysis for {stock_to_use} completed successfully!")

                        # Create a container with styling
                        st.markdown(f"""
                        <div class="card">
                            <h2 style="font-size: 1.8rem; margin-bottom: 20px;">
                                {stock_to_use} - Analyst Insights & Market News
                            </h2>
                            <div class="markdown-text-container">
                                {response.content}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.error("❌ No data received. Please try again.")

                with tab2:
                    st.markdown("""
                    <div class="card">
                        <h3>Technical Implementation</h3>
                        <p>This analysis is powered by a multi-agent system using the Agno framework and LLama 3.3 language model via Groq:</p>
                        <ul>
                            <li>Financial Agent: Retrieves real-time stock data and analyst recommendations</li>
                            <li>Web Agent: Searches for latest news and market sentiment</li>
                            <li>Orchestration: Coordinates the analysis pipeline for comprehensive results</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div class="card">
                        <h3>Data Sources</h3>
                        <ul>
                            <li>Yahoo Finance API: Real-time market data</li>
                            <li>Web Search: Latest news and market analysis</li>
                            <li>Analyst Ratings: Professional market evaluations</li>
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"⚠️ Error analyzing {stock_to_use}: {e}")
                st.info("Please try again or select a different stock symbol.")

    # Additional informative section
    st.markdown("---")

    st.markdown("""
    <div class="card">
        <h2 style="font-size: 1.5rem; margin-bottom: 15px;">How It Works</h2>
        <p style="color: #e2e8f0;">
            Our AI-powered platform combines real-time financial data with the latest market news to deliver comprehensive stock insights. The analysis includes:
        </p>
        <ul style="color: #e2e8f0;">
            <li><strong>Analyst Recommendations:</strong> Professional ratings and price targets</li>
            <li><strong>Latest News:</strong> Recent developments that might impact the stock</li>
            <li><strong>Market Sentiment:</strong> Overall analyst and market perspective</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif page == "About":
    st.title("About Stock Insights Pro")

    st.markdown("""
    <div class="card">
        <h2>Project Overview</h2>
        <p>Stock Insights Pro is an AI-powered financial analysis platform that combines cutting-edge language models with financial data tools to provide comprehensive stock insights.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Key Features")
    st.markdown("""
    - Real-time analyst recommendations
    - Latest news and market sentiment analysis
    - Multi-agent architecture for specialized information gathering
    - User-friendly interface with detailed visualizations
    """)

    st.subheader("Technology Stack")
    st.markdown("""
    - Frontend: Streamlit with custom CSS
    - AI Framework: Agno with Groq LLM integration
    - Data Sources: Yahoo Finance, DuckDuckGo search
    - Language Model: Llama 3.3 70B Versatile
    """)

elif page == "Help":
    st.title("Help & FAQ")

    st.markdown("""
    <div class="card">
        <h3>How to Use</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    1. Select a stock from the dropdown menu or enter a custom symbol
    2. Click the "Analyze" button to generate insights
    3. View the results in the Analysis tab
    4. Check the Technical Details tab for information about the data sources
    """)

    st.subheader("Frequently Asked Questions")

    expander1 = st.expander("How accurate are the recommendations?")
    expander1.write(
        "The recommendations are sourced from professional analysts and aggregated by our system. They represent expert opinions but should not be taken as financial advice.")

    expander2 = st.expander("How often is the data updated?")
    expander2.write(
        "Stock data and analyst recommendations are retrieved in real-time when you request an analysis. News is gathered from the most recent available sources.")

    expander3 = st.expander("Can I analyze international stocks?")
    expander3.write(
        "Yes, you can enter any valid stock symbol that is available on Yahoo Finance, including international stocks.")

    expander4 = st.expander("Is there a limit to how many analyses I can run?")
    expander4.write(
        "There are no hard limits, but please be considerate with usage to ensure service availability for all users.")

# Footer with social links
st.markdown("""
<div class="footer">
    2025 © Developed with ❤️ by Ritesh Kumar Singh. All rights reserved.
    <br>
    <a href="https://itsritz.my.canva.site" target="_blank">Portfolio</a> |
    <a href="https://www.linkedin.com/in/ritesh001/" target="_blank">LinkedIn</a> | 
    <a href="https://github.com/itsritzz" target="_blank">GitHub</a> 
</div>
""", unsafe_allow_html=True)