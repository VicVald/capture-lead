from .state import AgentState
import serpapi
from tavily import TavilyClient
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

def search_node(state: AgentState) -> AgentState:
    """This node receive the niche and locations to return a list of possible leads"""
    print("=== Searching for leads ===")
    niche = state['niche']
    locations = state['locations']
    limit_per_location = state['limit_per_location']
    
    client = serpapi.Client(api_key=os.getenv("SERPAPI_KEY"))

    leads_information = []
    
    for location in locations:
        results = client.search(
            q=niche,
            engine="google_local",
            type="search",
            gl="br",
            hl="pt",
            location=location,
            zoom=15
        )

        for result in results['local_results']:
            if result['position'] > limit_per_location:
                break
            # Get will handle the case where the key is not present and assign a default value to the variable
            name = result.get('title', "No name found")
            phone = result.get('phone', "No phone found")
            website = [link for link in result.get('links', {}).values() if 'https://www.google.com/maps' not in link]
            address = results.get('search_parameters', {}).get('location_used', "No address found")

            lead = {
                "name": name,
                "phone": phone,
                "website": website,
                "address": address,
            }
            leads_information.append(lead)
    
    state['final_sheet'] = leads_information

    return state

#Can be add a new node to condition when use or not tavily search

def online_appearance_node(state: AgentState) -> AgentState:
    """This node receive the final_sheet with the leads and search for the online appearance of the leads"""
    print("=== Searching for aditional information ===")
    leads = state['final_sheet']
    tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    online_appearances = []

    for lead in leads:
        search_results = tavily.search(query=lead['name'], limit=5)


        for result in search_results['results']:
            online_appearances.append(
                {
                'title': result['title'],
                'url': result['url'],
                'content': result['content']
                }
            )

    state['online_appearance'] = online_appearances

    return state

def summarization_node(state:AgentState) -> AgentState:
    """This node receive the final_sheet with the leads and search for the online appearance of the leads"""
    print("=== Summarizing information ===")

    llm = ChatGroq(model= "llama-3.1-8b-instant",api_key=os.getenv("GROQ_API_KEY"))

    #Can be add a niche in template to, to give a more specific suggestion

    prompt = PromptTemplate(
        input_variables=["web_search", "lead_info", "role"],
        template="""
        Use the content: {web_search} and the businesses information: {lead_info}   
        To summarize the online appearance of the businesses.
        And provide a suggestion on how a {role} can help them improve their online presence.
        Be succint and answer in Brazillian Portuguese.
        """
        )
    
    summary_list = []

    role = state['role']
    for lead, online_ap in zip(state['final_sheet'], state['online_appearance']):
        
        lead_info = lead
        web_search = online_ap
    
        messages = SystemMessage(content=prompt.format(web_search=web_search, lead_info=lead_info, role=role))

        answer = llm.invoke([messages]).content.strip()
        summary_list.append(answer)

    for i, lead in enumerate(state['final_sheet']):
        lead['summary'] = summary_list[i]

    return state