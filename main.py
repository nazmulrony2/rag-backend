from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from documents import DOCUMENTS  # Assuming this is your sample docs file

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
class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]  # Full conversation history

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

# Initialize RAG components (runs once when server starts)
logger.info("Initializing RAG components...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = Ollama(model="mistral:latest")
documents = [Document(page_content=doc) for doc in DOCUMENTS]
vectorstore = FAISS.from_documents(documents, embeddings)
logger.info("RAG components initialized")

@app.post("/rag", response_model=AnswerResponse)
async def rag_endpoint(request: ChatRequest):
    if not request.messages or not request.messages[-1].content.strip():
        logger.warning("Empty or invalid message received")
        raise HTTPException(status_code=400, detail="Last message cannot be empty")

    last_message = request.messages[-1].content
    logger.info(f"Received last message: {last_message}")

    # Real RAG
    try:
        # Retrieve relevant documents based on the last user message
        docs = vectorstore.similarity_search(last_message, k=2)
        context = "\n".join([doc.page_content for doc in docs])
        logger.info(f"Retrieved context: {context}")

        # Build prompt with full history and context
        history_str = "\n".join([f"{msg.role}: {msg.content}" for msg in request.messages])
        prompt = f"History:\n{history_str}\nContext: {context}\nAssistant: Respond concisely based on the history and context:"

        # Generate answer
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