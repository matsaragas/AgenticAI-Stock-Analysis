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


def fmp_cashflow_statement(ticker: str) -> Optional[str]:
    """Hits the FMP API to retrieve the cash flow information for the company with the given ticker.

    Args:
        ticker: The ticker of the company we want to access the balance sheet

    Returns:
        A formatted string with search results, or None if no results.
    """
    url = (f"https://financialmodelingprep.com/stable/cash-flow-statement-as-reported?symbol={ticker}&apikey={os.getenv('FMP_KEY')}")
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        return data
    except Exception as e:
        logger.error(f"fmp API request for cash flow statement informaation failed for {ticker}")


create_cashflow_statement_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="Cash_Flow_Agent",
    description="A simple financial analysis agent that can perform analysis on cash flow statement trends across time",
    instruction="""You are an expert financial analyst capable to analyze the cash flow business in details. 
    
    ***Instructions***
    * Make sure you provide detailed numbers and percentages for upward and downward trends for each fundamental in the cash flow statement
    * For each fundamental trend in the cash flow statement, explain what it means for the health of the company.
    * Try to combine fundamentals to give better insights for the financial health of the company 
    """,
    tools=[fmp_cashflow_statement],
)

