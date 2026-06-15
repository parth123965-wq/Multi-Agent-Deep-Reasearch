from tavily import TavilyClient
from langchain.tools import tool
import os
from rich import print 
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
load_dotenv()

tavil = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_search(query:str)->str:
    """
        Search the web for recent information and return search results.Return the title, url and a snippet of the content for each result.
    """
    result = tavil.search(query=query,max_results=5)
    output = []
    for i in result['results']:
        output.append(
            f"""
                Title: {i['title']}
                Url: {i['url']}
                Snippet: {i['content'][:300]}\n
            """
        )    
    return "\n----\n".join(output)    


@tool
def get_scapper(url:str)->str:
    """
        Scrape the content of a webpage and return the text.
    """
    try:
        response = requests.get(url,timeout=15,headers={
            "User-Agent": "Mozilla/5.0"
        })
        response.raise_for_status()
        soup = BeautifulSoup(response.text,"html.parser")
        for i in soup(["script","style","nav","footer","header","aside","noscript","form","svg"]):
            i.decompose()
        return soup.get_text(separator=" ",strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"