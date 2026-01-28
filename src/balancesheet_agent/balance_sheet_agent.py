import serpapi
import logging
from typing import Optional, Dict, Any

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

import certifi
import json
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


def fmp_balance_sheet(ticker: str) -> Optional[str]:
    """Hits the FMP API to retrieve the balance information for the company with the given ticker.

    Args:
        ticker: The ticker of the company we want to access the balance sheet

    Returns:
        A formatted string with search results, or None if no results.
    """
    url = (f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol={ticker}&apikey={os.getenv('FMP_KEY')}")
    try:
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
    except Exception as e:
        logger.error(f"fmp API request for balance sheet informaation failed for {company}")

    serpapi_params = {
        "engine": "google",
        "api_key": os.getenv('SERPAPI_KEY')
    }
    try:
        search = serpapi.search({
            **serpapi_params,
            "q": query,
            "num": 5,
        })
    except Exception as e:
        logger.error(f"SerpAPI request failed for query '{query}': {e}", exc_info=True)
        return f"Search failed due to an internal error. Query: '{query}'"


    # Validate response structure
    if not isinstance(search, Dict):
        logger.error(f"Unexpected SerpAPI response type: {type(search)} for query '{query}'")
        return f"Unexpected response format from search API."

    results = search["organic_results"]
    if not results:
        logger.warning(f"No search results found for query '{query}'")
        return f"No results found for query: '{query}'. Try a different search."

    contexts = "\n---\n".join(
        ["\n".join([x["title"], x["snippet"], x["link"]]) for x in results]
    )
    return contexts


create_search_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="Google_Search_Agent",
    description="An agent to search google and retrieve information relevant to user's queries",
    instruction="""You are a Google search assistant. You search the web using google and retrieve information that 
     is relevant to user's queries. Your primary function is to utilize the provided tools to retrieve information 
     in response to user queries. Ensure that all responses include the detailed output from the tools used and are 
     formatted in Markdown""",
    tools=[fmp_balance_sheet],
)

