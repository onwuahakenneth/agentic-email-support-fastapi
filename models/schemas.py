from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from typing import Annotated, Sequence, TypedDict, Literal,Union, List

class EmailClassification(TypedDict): 
    """The structure for email classification"""
    
    intent: Literal['question', 'bug', 'billing', 'feature', 'complex']
    urgency: Literal['low', 'medium', 'high', 'critical']
    topic: str
    summary: str
    
    
class EmailAgentState(TypedDict): 
    """State/Schema of the graph"""
    
    # raw email data
    email_content: str
    email_sender: str
    email_id: str
    
    
    # classification
    classification: Union[EmailClassification, None]
    
    # raw search/API results
    search_results: Union[List[str], None] # list of raw doc chunks
    customer_history: Union[dict, None] # raw customer data from CRM
    
    # generated content
    draft_response: Union[str, None]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    
    
# initial_state = {
#     "email_content": "I keep getting debited every day after a renewed my subscription. Please can you fix this?",
#     "email_sender": "customer@example.com",
#     "email_id": "email_123",
#     "messages": []
# }

initial_state = {
    "email_content": "How do I reset my password?",
    "email_sender": "customer@example.com",
    "email_id": "email_123",
    "messages": []
}