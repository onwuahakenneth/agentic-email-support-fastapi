from langchain_core.prompts import PromptTemplate

email_classification_promptTemplate = PromptTemplate.from_template(
    """
    Analyze this customer email and classify it: 
    
    Email: {email_content}
    From: {email_sender}
    
    Provide classification including intent, urgency, topic, and a summary.
    """
)


draft_response_promptTemplate = PromptTemplate.from_template(
    """
    Draft a response to this customer email: 
    
    Email: {email_content}
    
    Email intent: {email_intent}
    Urgency level: {email_urgency}
    
    Context:
    {context}
    
    Guidelines: 
    - Be professional and helpful
    - Address their specific concern
    - Use the provided documentation when relevant
    - Email draft should only contain the email - starting wih the subject part.
    - DO NOT add extra text that is not meant for the customer.
    - Use a generic salutation - 'Dear Customer,'
    - DO NOT include name after the closure.
    """
)
