import os
from dotenv import load_dotenv
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    DuckDuckGoSearchResults,
    BraveSearch,
    JinaSearch,
    MojeekSearch,
    YouSearchTool,
)
from langchain_community.utilities import (
    GoogleSerperAPIWrapper,
    SearxSearchWrapper,
    BingSearchAPIWrapper,
    SearchApiAPIWrapper,
    SerpAPIWrapper,
    YouSearchAPIWrapper,
    GoogleSearchAPIWrapper,
)
from langchain_tavily import TavilySearch, TavilyExtract
from exa_py import Exa
from smolagents import Tool, DuckDuckGoSearchTool, VisitWebpageTool

load_dotenv()

# Langchain tools
# tavily_search_tool = Tool.from_langchain(
#     TavilySearch(tavily_api_key=os.getenv("TAVILY_API_KEY"))
# )  # error
# tavily_extract_tool = Tool.from_langchain(
#     TavilyExtract(tavily_api_key=os.getenv("TAVILY_API_KEY"))
# )  # error
duckduckgo_search_run_tool = Tool.from_langchain(
    DuckDuckGoSearchRun(
        name="duckduckgo_search_run",
    )
)
duckduckgo_search_results_tool = Tool.from_langchain(
    DuckDuckGoSearchResults(
        name="duckduckgo_search_results",
    )
)

# Built-in tools
duckduckgo_search_tool = DuckDuckGoSearchTool(
    max_results=25,
    headers=None,
    proxy=None,
    timeout=10,
    verify=True,
)
visit_webpage_tool = VisitWebpageTool(max_output_length=40000)
