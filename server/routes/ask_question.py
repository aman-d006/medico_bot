from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
import os
from logger import logger

router=APIRouter()

@router.post("/ask/")
async def ask_question(question:str=Form(...)):
    try:
        logger.info(f"Received user question: {question}")
        pc=Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index=pc.Index(os.getenv("PINECONE_INDEX_NAME", "medical-index-v2"))
        embed_model=GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        embedded_query=embed_model.embed_query(question)
        res=index.query(vector=embedded_query, top_k=5, include_metadata=True)

        docs=[
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata={"sources": match["metadata"].get("sources", "")}
            ) for match in res["matches"]
        ]

        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents:List[Document]):
                super().__init__()
                self._docs=documents

            def get_relevant_documents(self, query:str) -> List[Document]:
                return self._docs

            # Implement the abstract method expected by BaseRetriever
            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self._docs
            
        retriever=SimpleRetriever(docs)
        chain=get_llm_chain(retriever)
        result=query_chain(chain, question)

        logger.info("Query is successful")
        return result

    except Exception as e:
        logger.exception(f"Error processing user question: {e}")
        return JSONResponse(content={"error": "Failed to process the question."}, status_code=500)