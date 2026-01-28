try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json
import os
import ssl
from dotenv import load_dotenv


from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types


retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

load_dotenv()

def get_jsonparsed_data(ticker: str):
    """Hits the FMP API to retrieve the balance information for the company with the given ticker.

    Args:
        ticker: The ticker of the company we want to access the balance sheet

    Returns:
        A formatted string with search results, or None if no results.
    """

    url = (f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={os.getenv('fmp_key')}")
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    return data #json.loads(data)


#url = (f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol=AAPL&apikey={os.getenv('fmp_key')}")
#print(get_jsonparsed_data("AAPL"))




print("✅ summarizer_agent created.")

root_agent = Agent(
    name="helpful_financial_assistant",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple financial analysis agent that can perform analysis on balance sheet trends across time",
    instruction="""You are an expert financial analyst capable to analyze the balance sheet in details. 
    
    ***Instructions***
    * Make sure you provide detailed numbers and percentages for upward and downward trends for each fundamental in the balance sheet
    * For each fundamental trend in the balance sheet explain what it means for the health of the company.
    * Try to combine fundamentals to give better insights for the financial health of the company 
    """,
    tools=[get_jsonparsed_data],
)

runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug("analyze the balance sheet trends for Apple company and give insights for the health of the company")
    print(response)

import asyncio
asyncio.run(main())
