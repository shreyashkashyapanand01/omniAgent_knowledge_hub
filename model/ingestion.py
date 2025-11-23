import os
from langchain_community.document_loaders import PyPDFLoader, YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from model.vector_store import vector_store_instance

class IngestionManager:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=os.getenv("GROQ_API_KEY"))
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def ingest_pdf(self, file_path):
        """Ingests a PDF file: loads, splits, and stores in AstraDB."""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splits = self.text_splitter.split_documents(documents)
        vector_store_instance.add_documents(splits)
        return len(splits)

    def ingest_url(self, url):
        """Ingests a URL (YouTube or Web): loads, summarizes, and stores."""
        if "youtube.com" in url or "youtu.be" in url:
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        else:
            loader = UnstructuredURLLoader(urls=[url], ssl_verify=False)
            
        documents = loader.load()
        
        # Generate Summary
        summary = self._summarize(documents)
        
        # Store original content (split) in Vector Store
        splits = self.text_splitter.split_documents(documents)
        vector_store_instance.add_documents(splits)
        
        return {"chunks": len(splits), "summary": summary}

    def _summarize(self, docs):
        """Summarizes the content using Groq."""
        prompt_template = """
        Provide a summary of the following content in 300 words:
        Content:{text}
        """
        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
        chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt)
        return chain.run(docs)

ingestion_manager = IngestionManager()
