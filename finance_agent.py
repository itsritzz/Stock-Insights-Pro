import os  # Provides functions to interact with the operating system, such as managing environment variables or file paths.
from dotenv import load_dotenv  # Loads environment variables from a .env file into the system's environment, useful for managing sensitive credentials.
import streamlit as st # Imports Streamlit

from agno.agent import Agent  # Represents a framework-specific agent.
from agno.models.groq import Groq  # Groq model module, for leveraging specific machine learning models or tools in Phi.
from agno.tools.yfinance import YFinanceTools  # Provides tools to access and manipulate financial data from Yahoo Finance.
from agno.tools.duckduckgo import DuckDuckGoTools  # Enables querying DuckDuckGo search engine for retrieving search results programmatically.

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Agent 1: For web search
web_agent = Agent(
    name= "Web Agent",
    model= Groq(id="llama-3.3-70b-versatile"),
    role= "Search the web for information and print sources",
    # tools=[GoogleSearch()],
    tools=[DuckDuckGoTools()],
    instructions="ALWAYS include sources and provide relevant news.",
    show_tool_calls=False,
    # debug_mode=True,
    markdown=True,
)

# Agent 2: To access financial data
finance_agent = Agent(
    name="Finance Agent",
    model= Groq(id="llama-3.3-70b-versatile"),
    role = "Get financial data",
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    # tools=[YFinanceTools(enable_all=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=False,
    # debug_mode=True,
    markdown=True,
)

# To assisgn roles based on the task to different agents
agent_team = Agent(
    team=[web_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["First, get analyst recommendation for the stock user has asked for,Use tables to display data",
                  "Then fetch the latest news for the given stock"],
    show_tool_calls=False,
    # debug_mode=True,
    markdown=True,
)
# agent_team.print_response("Provide analyst recommendations and also share the latest news from the web for NVDA", stream=True)

# Streamlit UI
st.set_page_config(page_title="Stock Insights", layout="centered")
st.title("📈 Stock Insights Dashboard")

st.write(
    "Select a stock from the dropdown or enter a stock symbol manually to get **analyst recommendations** and the **latest news**.")

# Stock selection dropdown
popular_stocks = ["NVDA", "AAPL", "TSLA", "MSFT"]
selected_stock = st.selectbox("Choose a stock:", popular_stocks)

# Option for manual entry
manual_stock = st.text_input("Or enter a stock symbol (e.g., AMZN, GOOG):")

# Determine stock to use
stock_to_use = manual_stock.strip().upper() if manual_stock else selected_stock

# Fetch data when button is clicked
if st.button("Get Insights"):
    with st.spinner("Fetching data..."):
        try:
            response = agent_team.run(f"Provide analyst recommendations and also share the latest news from the web for {stock_to_use}", stream=False)

            if response:
                st.subheader("🔍 Analyst Recommendations & News")
                st.markdown(response.content)  # `.content` contains the text response
            else:
                st.error("❌ No data received. Please try again.")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")