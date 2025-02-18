from langgraph.graph import END, StateGraph, START

def create_workflow(agent_state):

    from .nodes import search_node, online_appearance_node, summarization_node

    workflow = StateGraph(agent_state)
    
    workflow.add_node("search", search_node)
    workflow.add_node("online_ap", online_appearance_node)
    workflow.add_node("summarization", summarization_node)

    workflow.add_edge(START, "search")
    workflow.add_edge("search", "online_ap")
    workflow.add_edge("online_ap", "summarization")
    workflow.add_edge("summarization", END)

    app = workflow.compile()

    return app
