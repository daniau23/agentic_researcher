from langchain.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import os
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# repo_id = "microsoft/Phi-4-mini-instruct"
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
# repo_id = "mistralai/Mistral-Small-24B-Instruct-2501"
# repo_id = "meta-llama/Llama-3.2-3B-Instruct"

# model parameters
model_kwargs_critic = {
    "max_new_tokens": 5, # Maximum tokens to generate
    "temperature": 0.1, # Controls randomness of output
    "timeout": 6000,
    # "task":'conversational'
}

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token = HUGGINGFACEHUB_API_TOKEN,
    **model_kwargs_critic
)
chat_model = ChatHuggingFace(llm=llm)
prompt = PromptTemplate.from_template(
    "You are a strict research reviewer. Review the abstract:\n\n{abstract}\n\nRespond with 'ACCEPTED' or 'REJECTED'."
)
critic_chain = prompt | chat_model

def critic_node(state):
    result = critic_chain.invoke({"abstract": state.abstract})
    critique = result.content.strip().upper()
    return {"critique": critique}