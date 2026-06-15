from agents import search_agent, scraper_agent, writer_chain, critic_chain

def run_deep_research_tool(topic: str)->dict:
    state = {}
    s_agent = search_agent()
    sc_agent = scraper_agent()
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("= "*50)
    search_result = s_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Search for the latest research papers on {topic} and provide a list of relevant papers with their titles, authors, publication dates, and links to the papers."
                }
            ]
        }
    )
    state['search_result'] = search_result['messages'][-1].content
    print("\n search result \n",state['search_result'])
    print("\n"+" ="*50)
    print("step 2 - scrapper agent is working ...")
    print("= "*50)
    scrapper_result = sc_agent.invoke(
        {
            "messages":[
                {
                    "role": "user",
                    "content": f"Based on the following result about : {topic}\npick the most relative Url to scrape it for deeper information about search result : {state['search_result'][:800]}"
                }
            ]
        }
    )
    state['scraper_result'] = scrapper_result['messages'][-1].content
    print("\n scraper result \n",state['scraper_result'])
    print("\n"+" ="*50)
    print("step 3 - writer chain is working ...")
    print("= "*50)
    combin_result = (
        f"""The Web Search Result : {state['search_result']}\n\n
        The Web Scraper Result : {state['scraper_result']}\n\n"""
    )
    state['report'] = writer_chain.invoke(
        {
            "topic":topic,
            "research":combin_result
        }
    )
    print("\n Report :\n ",state['report'])
    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("= "*50)
    state['feedback'] = critic_chain.invoke(
        {
            "report":state['report']
        }
    )
    print("\n Feedback :\n ",state['feedback'])
    return state
    
    
    
    
    
if __name__ == "__main__":
    topic = input("Enter the research topic: ")
    run_deep_research_tool(topic=topic)