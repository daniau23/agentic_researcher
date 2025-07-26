# graph_article/writer.py

"""
Writer Agent

Role:
  Generates a research abstract based on the input title and category.
"""

import os
from langchain.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
repo_id = "meta-llama/Llama-3.2-3B-Instruct"

model_kwargs_writer = {
    "max_new_tokens": 200,
    "max_length": 100,
    "temperature": 0.8,
    "timeout": 6000,
}

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    **model_kwargs_writer
)
chat_model = ChatHuggingFace(llm=llm)

prompt = PromptTemplate.from_template(
    "Generate an abstract for the paper titled '{input}' in the domain of {category}."
)

writer_chain = prompt | chat_model

def writer_node(state):
    result = writer_chain.invoke({"input": state.input, "category": state.category})
    return {"abstract": result.content}
