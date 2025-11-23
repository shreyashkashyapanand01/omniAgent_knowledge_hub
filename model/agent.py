import os
from typing import List, TypedDict, Literal
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langchain.schema import Document
from langgraph.graph import END, StateGraph, START
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from model.vector_store import vector_store_instance

# --- Graph State ---
class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[str]

# --- Tools & LLM ---
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=os.getenv("GROQ_API_KEY"))
retriever = vector_store_instance.as_retriever()

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# --- Nodes ---
def retrieve(state):
    print("---RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def wiki_search(state):
    print("---WIKIPEDIA---")
    question = state["question"]
    docs = wiki.invoke({"query": question})
    wiki_results = Document(page_content=docs)
    return {"documents": wiki_results, "question": question}

def generate(state):
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    
    # Simple RAG generation
    if isinstance(documents, list):
        context = "\n\n".join([doc.page_content for doc in documents])
    else:
        context = documents.page_content
        
    prompt = f"Answer the question based on the context:\n\nContext: {context}\n\nQuestion: {question}"
    response = llm.invoke(prompt)
    return {"generation": response.content}

# --- Router ---
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""
    datasource: Literal["vectorstore", "wiki_search"] = Field(
        ...,
        description="Given a user question choose to route it to wikipedia or a vectorstore.",
    )

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to a vectorstore or wikipedia.
The vectorstore contains documents related to uploaded PDFs and videos.
Use the vectorstore for specific questions about that content. 
Otherwise, use wiki-search for general knowledge."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router

def route_question(state):
    print("---ROUTE QUESTION---")
    question = state["question"]
    source = question_router.invoke({"question": question})
    if source.datasource == "wiki_search":
        return "wiki_search"
    elif source.datasource == "vectorstore":
        return "vectorstore"

# --- Build Graph ---
workflow = StateGraph(GraphState)
workflow.add_node("wiki_search", wiki_search)
workflow.add_node("retrieve", retrieve)
workflow.add_node("generate", generate)

workflow.add_conditional_edges(
    START,
    route_question,
    {
        "wiki_search": "wiki_search",
        "vectorstore": "retrieve",
    },
)
workflow.add_edge("retrieve", "generate")
workflow.add_edge("wiki_search", "generate")
workflow.add_edge("generate", END)

agent_app = workflow.compile()
