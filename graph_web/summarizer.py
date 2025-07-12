from langchain.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
model_kwargs = {"temperature": 0.1, 
                "max_new_tokens": 100, # Maximum tokens to generate
                "timeout": 6000}

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    **model_kwargs
)
chat_model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate.from_template(
    "Summarize the following content concisely:\n\n{content}\n\nSummary:"
)
summarize_chain = prompt | chat_model

def summarize_node(state):
    if not state.content:
        return {"summary": "No content to summarize"}
    result = summarize_chain.invoke({"content": state.content})
    return {"summary": result.content}