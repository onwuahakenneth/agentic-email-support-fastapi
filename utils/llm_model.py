import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
_ = load_dotenv()

base_llm_model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY', ''),  # type: ignore
    model=os.getenv('MODEL_NAME', ''),
    name='base_llm_mode',
    temperature=0.5,)

# for classification, we want the output to always be the same for the same input
classifier_llm_model = ChatGroq(
    api_key=os.getenv('GROQ_API_KEY', ''),  # type: ignore
    model=os.getenv('MODEL_NAME', ''),
    name='base_llm_mode',
    temperature=0,)