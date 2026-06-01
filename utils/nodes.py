from langgraph.graph import END
from typing import Literal, Union
from langgraph.types import Command, interrupt
from langchain_core.messages import HumanMessage
from src.models.schemas import EmailAgentState, EmailClassification
from src.utils.llm_model import base_llm_model, classifier_llm_model
from src.prompts.prompt_templates import email_classification_promptTemplate, draft_response_promptTemplate


def read_email_node(state: EmailAgentState) -> EmailAgentState:
    """Extracts and parses email content"""

    # type: ignore
    return {'messages': [HumanMessage(content=f"Processing email: {state['email_content']}")]}


def classify_intent_node(state: EmailAgentState) -> Command[Literal['search_documentation', 'human_review', 'draft_response', 'bug_tracking']]:
    """Use LLM model to classify email content intent and urgency, then route accordingly"""

    # create a structure LLM that returns EmailClassification object
    structured_llm = classifier_llm_model.with_structured_output(
        EmailClassification)  # type: ignore

    # we also format the prompt on-demand, not stored in state

    classification_prompt = email_classification_promptTemplate.format(
        email_content=state['email_content'],
        email_sender=state['email_sender'],
    )

    # get the structured response
    classification: EmailClassification = structured_llm.invoke(
        classification_prompt)  # type: ignore

    # route to next node based on classification result
    intent = classification['intent']
    urgency = classification['urgency']

    if intent == 'billing' or urgency == "critical":
        goto = 'human_review'
    elif intent in ['question', 'feature']:
        goto = 'search_documentation'
    elif intent == "bug":
        goto = 'bug_tracking',
    else:
        goto = 'draft_response'

    return Command(
        update={'classification': classification},
        goto=goto
    )


def search_documentation(state: EmailAgentState) -> Command[Literal['draft_response']]:
    """search knowledge base for relevant information or context"""

    # build search query from classification channel of the graph's state
    classification = state['classification']
    # type: ignore
    query = f"{classification.get('intent', '')} {classification.get('topic', '')}"

    try:
        # implement search logic
        # store raw results, not formatted text

        search_results = [
            "Reset password via Settings > Security > Change Password",
            "Password must be at least 12 characters",
            "Include uppercase, lowercase, numbers, and symbols"
        ]

    except Exception as e:
        # for recoverable search errors, store error and continue
        search_results = [f"Search temporarily unavailable: {str(e)}"]

    return Command(
        update={'search_results'},
        goto='draft_response'
    )


def bug_tracking(state: EmailAgentState) -> Command[Literal['draft_response']]:
    """create or update bug tracking ticket"""

    # create a ticket in bug tracking system
    ticket_id = 'BUG-12345#'  # usually created via API

    return Command(
        update={
            'search_results': [f"Bug ticket {ticket_id} created"],
            'current_step': 'bug_tracked'
        },
        goto='draft_response'
    )


def draft_response(state: EmailAgentState) -> Command[Literal['human_review', 'send_reply']]:
    """generates a response using context and route based on email's `intent` and `urgency`"""

    classification = state.get('classification', {})

    # format context from raw state data on demand
    context_sections = []

    if state.get('search_results'):
        # format search results for the prompt
        formatted_docs = "\n\n".join(
            f"- {doc}" for doc in state['search_results'])
        context_sections.append(f"Relevant documentation: \n{formatted_docs}")

    if state.get('customer_history'):
        # format customer history data for the prompt
        context_sections.append(
            f"Customer tier: {state['customer_history'].get('tier', 'standard')}"
        )

    # we build the prompt with formatted context
    draft_prompt = draft_response_promptTemplate.format(
        email_content=state['email_content'],
        email_intent=classification.get('intent', 'unknown'),
        email_urgency=classification.get('urgency', 'unknown'),
        context=chr(10).join(context_sections)
    )

    response = base_llm_model.invoke(draft_prompt)

    # determine if a human review is needed based on urgency and intent
    urgency = classification.get('urgency')
    intent = classification.get('intent')

    needs_review = urgency in ['high', 'critical'] or intent == 'complex'

    # route to appropriate next node
    goto = 'human_review' if needs_review else 'send_reply'

    return Command(
        update={'draft_response': response.content},
        goto=goto
    )


def human_review(state: EmailAgentState) -> Command[Literal['send_reply', END]]:
    """pause for human review using interrupt and route based on decision/action of the human"""

    classification = state.get('classification', {})

    # NOTE interrupt() must come first - any code b4 it will re-run on resume
    human_decision = interrupt({
        "email_id": state.get('email_id', ''),
        "original_email": state.get('email_content', ''),
        "draft_response": state.get('draft_response', ''),
        "urgency": classification.get('urgency'),
        "intent": classification.get('intent'),
        "action": "Please review and approve/edit this response"
    })
    
    # we now process the human's decision
    if human_decision.get('approved'): 
        return Command(
            update={'draft_response': human_decision.get('edited_response', state.get('draft_response', ''))},
            goto='send_reply'
        )
    else: 
        # rejection means human will handle the email response directly
        return Command(update={}, goto=END)
    
    
def send_reply(state: EmailAgentState) -> dict: 
    """send the email response"""
    
    # here, we can integrate with email service
    print(f"\n\n-------------------------\nSending reply to {state['email_sender']}\n\n {state['draft_response'][:100]}...\n-------------------------")
    
    return {}
    