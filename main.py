from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from documents import DOCUMENTS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="RAG Backend")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

# Initialize RAG components (runs once when server starts)
logger.info("Initializing RAG components...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = Ollama(model="mistral")
documents = [Document(page_content=doc) for doc in DOCUMENTS]
vectorstore = FAISS.from_documents(documents, embeddings)
logger.info("RAG components initialized")

@app.post("/rag", response_model=AnswerResponse)
async def rag_endpoint(request: QuestionRequest):
    logger.info(f"Received question: {request.question}")
    if not request.question.strip():
        logger.warning("Empty question received")
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Real RAG
    try:
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(request.question, k=2)
        context = "\n".join([doc.page_content for doc in docs])
        logger.info(f"Retrieved context: {context}")

        # Generate answer
        prompt = f"Question: {request.question}\nContext: {context}\nAnswer concisely:"
        answer = llm.invoke(prompt)
        sources = [doc.page_content for doc in docs]
        logger.info("Sending response")
        return {"answer": answer.strip(), "sources": sources}
    except Exception as e:
        logger.error(f"RAG error: {str(e)}")
        raise HTTPException(status_code=500, detail="RAG processing failed")

@app.get("/")
async def root():
    return {"message": "RAG Backend is running"}