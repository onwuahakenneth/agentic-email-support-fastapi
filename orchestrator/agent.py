
import os
from langchain_groq import ChatGroq
from src.utils.llm_model import base_llm_model
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from src.models.schemas import EmailAgentState, EmailClassification
from src.prompts.prompt_templates import email_classification_promptTemplate
from src.utils.nodes import read_email_node, classify_intent_node, search_documentation, bug_tracking, draft_response, human_review, send_reply


class AgentBuilder:
    def __init__(self, llm_model: ChatGroq = base_llm_model) -> None:
        self.llm_model = llm_model

    def createAgent(self):

        builder = StateGraph(EmailAgentState)
        builder.add_node('read_email_node', read_email_node)
        builder.add_node('classify_intent_node', classify_intent_node)
        builder.add_node('search_documentation', search_documentation)
        builder.add_node('bug_tracking', bug_tracking)
        builder.add_node('draft_response', draft_response)
        builder.add_node('human_review', human_review)
        builder.add_node('send_reply', send_reply)

        builder.add_edge('read_email_node', 'classify_intent_node')
        builder.add_edge(START, 'read_email_node')
        builder.add_edge('send_reply', END)

        checkpointer = InMemorySaver()
        graph = builder.compile(checkpointer=checkpointer)

        # save graph image for visualization
        output_dir = os.path.join(os.path.dirname( __file__), '..', '..', 'outputs')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'graph.png')
        
        with open(output_path, 'wb') as _file: 
            graph_image_bytes = graph.get_graph().draw_mermaid_png()
            _file.write(graph_image_bytes)

        
        return graph
    

