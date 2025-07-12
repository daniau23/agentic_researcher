from langchain.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os
import os

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# repo_id = "microsoft/Phi-4-mini-instruct"
# repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
# repo_id = "mistralai/Mistral-Small-24B-Instruct-2501"
repo_id = "meta-llama/Llama-3.2-3B-Instruct"

# model parameters
model_kwargs_writer = {
    "max_new_tokens": 200, # Maximum tokens to generate
    "max_length": 100, # Maximum length of input + output
    "temperature": 0.8, # Controls randomness of output
    "timeout": 6000,
}

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
    **model_kwargs_writer
    # you specify the task or not
    # You can also specify the task in the model_kwargs or within here
    # task = 'conversational',
)
chat_model = ChatHuggingFace(llm=llm)
prompt = PromptTemplate.from_template(
    "Generate an abstract for the paper titled '{input}' in the domain of {category}."
)



writer_chain = prompt | chat_model

def writer_node(state):
    result = writer_chain.invoke({"input": state.input, "category": state.category})
    return {"abstract": result.content}