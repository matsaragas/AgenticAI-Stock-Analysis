import serpapi
import logging
from typing import Optional, Dict, Any

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

import certifi
import os
import ssl
from dotenv import load_dotenv
from urllib.request import urlopen


logger = logging.getLogger(__name__)

load_dotenv()
retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


def fmp_income_statement(ticker: str) -> Optional[str]:
    """Hits the FMP API to retrieve the income statement information for the company with the given ticker.

    Args:
        ticker: The ticker of the company we want to access the balance sheet

    Returns:
        A formatted string with search results, or None if no results.
    """
    url = f"https://financialmodelingprep.com/stable/income-statement?symbol=AAPL&apikey={os.getenv('FMP_KEY')}"
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        return data
    except Exception as e:
        logger.error(f"fmp API request for income statement failed for {ticker}")


create_income_statement_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="Income_Statement_Agent",
    description="A simple financial analysis agent that can perform analysis on income statement trends across time",
    instruction="""You are an expert financial analyst capable to analyze the income statement in details across time. 
    
    ***Instructions***
    * Make sure you **PROVIDE DETAILED NUMBERS and PERCENTAGES** for upward and downward trends for each fundamental in the income statement
    * For each fundamental trend in the income statement explain what it means for the health of the company.
    * Try to combine fundamentals to give better insights for the financial health of the company 
    """,
    tools=[fmp_income_statement],
)

