import uuid
from rich.console import Console
from rich.markdown import Markdown
from langgraph.types import Command
from src.models.schemas import initial_state
from src.orchestrator.agent import AgentBuilder
from src.models.schemas import EmailClassification
from langchain_core.runnables import RunnableConfig

def main(): 
    console = Console()
    
    builder = AgentBuilder()
    agent = builder.createAgent()
    
    config: RunnableConfig = {'configurable': {'thread_id': str(uuid.uuid4())}}
    response = agent.invoke(initial_state, config=config) # type: ignore
    
    console.print(f"state: {response}")
    edited_response = "Dear Customer,\n\n We sincerely apologize for the double charge. I've initiated an immediate refund... \n\n Best regards,"
    
    is_interrupted = response.get('__interrupt__')
    
    if is_interrupted:
        action = response['__interrupt__'][0].value['action']
        
        user_response = input(f"""
        {action}
        
        CUSTOMER: 
        
        content:
        -------------------------- 
        
        {response['email_content']}
        
        --------------------------
        email: {response['email_sender']}
        email id: {response['email_id']}
        
        
        SuMMARY: 
        -------------------------
        {response['classification']['summary']}
        -------------------------
        
        INITIAL EMAIL DRAFT: 
        
        =========================
        
        # {response.get('draft_response', 'No draft yet. Start typing response here')}
        
        =========================
        
        
        """)
        
        human_response = Command(
            resume={
                'approved': True,
                'edited_response': user_response
            }
        )
        
        # we resume execution
        # result = agent.invoke(human_response, config)
        agent.invoke(human_response, config)
    
    else: 
        console.print(Markdown(response['draft_response']))
    # console.print(f"FINAL DRAFT:\n\n {result['draft_response']}")

if __name__ == '__main__': 
    main()