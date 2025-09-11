The prototype consists of:
- **Frontend (Next.js)**: A simple web page where you type a question and see a dummy answer with sources.
- **Backend (FastAPI)**: A server that accepts questions and returns dummy RAG responses (answer + sources).
- **Goal**: Run both, connect them, and practice with enhancements.

---

### Prerequisites
Before starting, ensure you have:
1. **Node.js** (v18+): Download and install from [nodejs.org](https://nodejs.org). Verify with:
   ```
   node --version
   npm --version
   ```
   - Expect: `v18.x.x` or higher for `node`, `9.x.x` or higher for `npm`.
2. **Python** (3.8+): Download and install from [python.org](https://www.python.org). Verify with:
   ```
   python --version
   ```
   - Expect: `3.8.x` or higher. On some systems, use `python3 --version`.
3. **Code Editor**: Install [VS Code](https://code.visualstudio.com) for editing files.
4. **Terminal**: Use Command Prompt (Windows), Terminal (macOS/Linux), or VS Code's built-in terminal.
5. **Git** (optional for deployment): Install from [git-scm.com](https://git-scm.com) if deploying later.

If you don’t have these, download and install them now. Restart your terminal after installation.

---

### Step 1: Set Up the Project Folders
**Goal**: Create folders for frontend and backend, install dependencies.

1. **Open a Terminal**:
   - Windows: Search for "Command Prompt" or use VS Code (Ctrl+`).
   - macOS/Linux: Open Terminal or use VS Code.

2. **Create Project Folders**:
   ```
   mkdir rag-prototype
   cd rag-prototype
   mkdir frontend backend
   ```
   - This creates a main folder `rag-prototype` with `frontend` and `backend` subfolders.

3. **Set Up Frontend (Next.js)**:
   - Navigate to frontend:
     ```
     cd frontend
     npx create-next-app@latest . --typescript --tailwind --eslint
     ```
     - Prompts:
       - Use App Router: Yes
       - Customize import alias: Yes (@/*)
       - Others: Press Enter for defaults (No for SRC folder).
     - This sets up a Next.js app with TypeScript and Tailwind CSS.
   - Install `react-spinners` for loading animation:
     ```
     npm install react-spinners
     ```
   - Verify setup:
     ```
     npm run dev
     ```
     - Open `http://localhost:3000` in a browser. You should see a Next.js welcome page.
     - Stop with Ctrl+C.

4. **Set Up Backend (FastAPI)**:
   - Navigate to backend:
     ```
     cd ../backend
     python -m venv venv
     source venv/bin/activate  # Windows: venv\Scripts\activate
     ```
     - You’ll see `(venv)` in the terminal, indicating the virtual environment is active.
   - Install dependencies:
     ```
     pip install fastapi uvicorn python-dotenv
     ```
   - Create a test `main.py`:
     ```python
     from fastapi import FastAPI
     app = FastAPI()
     @app.get("/")
     def root():
         return {"message": "Hello"}
     ```
   - Run:
     ```
     uvicorn main:app --reload
     ```
     - Open `http://localhost:8000` to see `{"message": "Hello"}`.
     - Open `http://localhost:8000/docs` to see the FastAPI Swagger UI.
     - Stop with Ctrl+C.

**Troubleshooting**:
- **Node.js errors**: Ensure Node.js is installed (`node --version`).
- **Python errors**: Use `python3` if `python` fails. Ensure Python is added to PATH during installation.
- **Port conflicts**: If `8000` or `3000` is busy, change ports (e.g., `uvicorn main:app --port 8001`).

**Explanation**:
- `frontend` holds the Next.js app (user interface).
- `backend` holds the FastAPI app (server logic).
- Virtual environment isolates Python dependencies.
- Test runs confirm setup.

---

### Step 2: Create the FastAPI Backend
**Goal**: Build a `/rag` endpoint that accepts a question and returns a dummy RAG response (answer + sources).

1. **Create Backend Files**:
   - In `backend/`, create `.env`:
     ```
     ENVIRONMENT=development
     ```
   - Replace `backend/main.py` with:
     ```python
     from fastapi import FastAPI, HTTPException
     from fastapi.middleware.cors import CORSMiddleware
     from pydantic import BaseModel
     from dotenv import load_dotenv
     import asyncio
     import logging
     import os

     # Load environment variables
     load_dotenv()

     # Set up logging
     logging.basicConfig(level=logging.INFO)
     logger = logging.getLogger(__name__)

     # Initialize FastAPI app
     app = FastAPI(title="RAG Backend")

     # Enable CORS for frontend communication
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["http://localhost:3000"],
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )

     # Pydantic models for request and response
     class QuestionRequest(BaseModel):
         question: str

     class AnswerResponse(BaseModel):
         answer: str
         sources: list[str]

     @app.post("/rag", response_model=AnswerResponse)
     async def rag_endpoint(request: QuestionRequest):
         logger.info(f"Received question: {request.question}")
         if not request.question.strip():
             logger.warning("Empty question received")
             raise HTTPException(status_code=400, detail="Question cannot be empty")
         await asyncio.sleep(1)  # Simulate RAG processing
         answer = f"This is a dummy RAG answer to: '{request.question}'."
         sources = ["Dummy Source 1: Wikipedia", "Dummy Source 2: Book"]
         logger.info("Sending response")
         return {"answer": answer, "sources": sources}

     @app.get("/")
     async def root():
         return {"message": "RAG Backend is running"}
     ```

2. **Run and Test Backend**:
   - Ensure in `backend/` with `(venv)` active:
     ```
     uvicorn main:app --reload
     ```
   - Open `http://localhost:8000/docs`.
   - Click `/rag`, then “Try it out”, enter:
     ```json
     {"question": "What is AI?"}
     ```
     - Expect: `{"answer": "This is a dummy RAG answer to: 'What is AI?'.", "sources": ["Dummy Source 1: Wikipedia", "Dummy Source 2: Book"]}`
   - Try `{"question": ""}` to see `{"detail": "Question cannot be empty"}`.
   - Check terminal for logs (e.g., `INFO:__main__:Received question: What is AI?`).

**Troubleshooting**:
- **Module not found**: Run `pip install fastapi uvicorn python-dotenv` again.
- **CORS errors**: Ensure `allow_origins` includes `http://localhost:3000`.
- **Logs not showing**: Check terminal is in `backend/` and `(venv)` is active.

**Explanation**:
- **Pydantic**: `QuestionRequest` ensures valid input; `AnswerResponse` structures output.
- **CORS**: Allows frontend to call backend.
- **Logging**: Helps debug by showing what’s happening.
- **Async**: `await asyncio.sleep` mimics real RAG delay.
- **HTTPException**: Handles errors cleanly.

**Practice**:
- Modify `answer` to include the question in a different way (e.g., `Answer: {request.question} is...`).
- Add a new source to `sources`.

---

### Step 3: Create the Next.js Frontend
**Goal**: Build a simple UI with a form to ask questions, display answers and sources, and include navigation.

1. **Update Frontend Files**:
   - Replace `frontend/app/globals.css`:
     ```css
     :root {
       --background: #ffffff;
       --foreground: #171717;
     }
     body {
       color: var(--foreground);
       background: var(--background);
       font-family: Arial, Helvetica, sans-serif;
     }
     .container {
       max-width: 600px;
       margin: 0 auto;
       padding: 20px;
     }
     .title {
       font-size: 2rem;
       color: #333;
     }
     .input {
       width: 100%;
       padding: 10px;
       margin-bottom: 10px;
       border: 1px solid #ccc;
       border-radius: 4px;
     }
     .button {
       padding: 10px 20px;
       background-color: #0070f3;
       color: white;
       border: none;
       border-radius: 4px;
       cursor: pointer;
     }
     .button:disabled {
       background-color: #ccc;
     }
     .error {
       color: red;
       margin-top: 10px;
     }
     .answer-box {
       margin-top: 20px;
       padding: 15px;
       border: 1px solid #ccc;
       border-radius: 4px;
       background-color: #f9f9f9;
     }
     .navbar {
       background-color: #f0f0f0;
       padding: 10px;
       display: flex;
       gap: 20px;
     }
     .nav-link {
       color: #0070f3;
       text-decoration: none;
     }
     .nav-link:hover {
       text-decoration: underline;
     }
     ```
   - Replace `frontend/app/layout.tsx`:
     ```tsx
     import type { Metadata } from "next";
     import { Inter } from "next/font/google";
     import "./globals.css";
     import Link from "next/link";

     const inter = Inter({ subsets: ["latin"] });

     export const metadata: Metadata = {
       title: "Q&A RAG App",
       description: "Simple RAG Prototype",
     };

     export default function RootLayout({
       children,
     }: Readonly<{
       children: React.ReactNode;
     }>) {
       return (
         <html lang="en">
           <body className={inter.className}>
             <nav className="navbar">
               <Link href="/" className="nav-link">Home</Link>
               <Link href="/about" className="nav-link">About</Link>
             </nav>
             {children}
           </body>
         </html>
       );
     }
     ```
   - Create `frontend/app/about/page.tsx`:
     ```tsx
     export default function About() {
       return (
         <div className="container">
           <h1 className="title">About This App</h1>
           <p>This is a simple Q&A RAG prototype built with Next.js and FastAPI.</p>
           <a href="/" className="nav-link">Back to Home</a>
         </div>
       );
     }
     ```
   - Replace `frontend/app/page.tsx`:
     ```tsx
     "use client";

     import { useState } from "react";
     import { ClipLoader } from "react-spinners";

     export default function Home() {
       const [question, setQuestion] = useState("");
       const [response, setResponse] = useState({ answer: "", sources: [] });
       const [isLoading, setIsLoading] = useState(false);
       const [error, setError] = useState("");

       const handleSubmit = async (e: React.FormEvent) => {
         e.preventDefault();
         setIsLoading(true);
         setError("");
         setResponse({ answer: "", sources: [] });

         try {
           const res = await fetch("http://localhost:8000/rag", {
             method: "POST",
             headers: { "Content-Type": "application/json" },
             body: JSON.stringify({ question }),
           });

           const data = await res.json();
           if (!res.ok) throw new Error(data.detail || "Something went wrong");
           setResponse(data);
           setQuestion("");
         } catch (err: any) {
           setError(err.message);
         } finally {
           setIsLoading(false);
         }
       };

       return (
         <div className="container">
           <h1 className="title">Simple Q&A RAG App</h1>
           <form onSubmit={handleSubmit}>
             <input
               type="text"
               value={question}
               onChange={(e) => setQuestion(e.target.value)}
               placeholder="Ask a question..."
               disabled={isLoading}
               className="input"
             />
             <button type="submit" disabled={isLoading} className="button">
               {isLoading ? <ClipLoader size={20} color="white" /> : "Ask"}
             </button>
           </form>
           {error && <p className="error">{error}</p>}
           {response.answer && (
             <div className="answer-box">
               <h2>Answer:</h2>
               <p>{response.answer}</p>
               <h3>Sources:</h3>
               <ul>
                 {response.sources.map((source, index) => (
                   <li key={index}>{source}</li>
                 ))}
               </ul>
             </div>
           )}
         </div>
       );
     }
     ```

2. **Run and Test Frontend**:
   - Ensure backend is running (`uvicorn main:app --reload` in `backend/`).
   - In `frontend/`:
     ```
     npm run dev
     ```
   - Open `http://localhost:3000`:
     - Type “What is AI?” and click “Ask”. Expect: Dummy answer with sources.
     - Try an empty question to see error.
     - Click “About” to navigate, then back to Home.

**Troubleshooting**:
- **CORS error**: Check browser console (F12 > Console). Ensure `allow_origins` in `main.py` includes `http://localhost:3000`.
- **Fetch error**: Verify backend is running on `http://localhost:8000`.
- **Styles not applied**: Ensure `globals.css` is correct.

**Explanation**:
- **layout.tsx**: Adds a navbar for navigation across pages.
- **page.tsx**: Main Q&A page with form, spinner, and answer display.
- **about/page.tsx**: Simple about page.
- **globals.css**: Styles make the app look clean.
- **useState**: Manages question input, response, loading, and errors.
- **fetch**: Sends questions to backend and gets responses.

**Practice**:
- Change the button text to “Submit”.
- Add a new style (e.g., change `.title` color to red in `globals.css`).

---

### Step 4: Add Question History (Frontend Enhancement)
**Goal**: Add a feature to show past questions and answers to practice state management.

1. **Update `frontend/app/page.tsx`**:
   ```tsx
   "use client";

   import { useState } from "react";
   import { ClipLoader } from "react-spinners";

   export default function Home() {
     const [question, setQuestion] = useState("");
     const [response, setResponse] = useState({ answer: "", sources: [] });
     const [history, setHistory] = useState([]); // New state for history
     const [isLoading, setIsLoading] = useState(false);
     const [error, setError] = useState("");

     const handleSubmit = async (e: React.FormEvent) => {
       e.preventDefault();
       setIsLoading(true);
       setError("");
       setResponse({ answer: "", sources: [] });

       try {
         const res = await fetch("http://localhost:8000/rag", {
           method: "POST",
           headers: { "Content-Type": "application/json" },
           body: JSON.stringify({ question }),
         });

         const data = await res.json();
         if (!res.ok) throw new Error(data.detail || "Something went wrong");
         setResponse(data);
         setHistory([...history, { question, ...data }]); // Add to history
         setQuestion("");
       } catch (err: any) {
         setError(err.message);
       } finally {
         setIsLoading(false);
       }
     };

     return (
       <div className="container">
         <h1 className="title">Simple Q&A RAG App</h1>
         <form onSubmit={handleSubmit}>
           <input
             type="text"
             value={question}
             onChange={(e) => setQuestion(e.target.value)}
             placeholder="Ask a question..."
             disabled={isLoading}
             className="input"
           />
           <button type="submit" disabled={isLoading} className="button">
             {isLoading ? <ClipLoader size={20} color="white" /> : "Ask"}
           </button>
         </form>
         {error && <p className="error">{error}</p>}
         {response.answer && (
           <div className="answer-box">
             <h2>Answer:</h2>
             <p>{response.answer}</p>
             <h3>Sources:</h3>
             <ul>
               {response.sources.map((source, index) => (
                 <li key={index}>{source}</li>
               ))}
             </ul>
           </div>
         )}
         {history.length > 0 && (
           <div className="answer-box">
             <h2>History:</h2>
             {history.map((item, index) => (
               <div key={index} style={{ marginBottom: "10px" }}>
                 <p><strong>Question:</strong> {item.question}</p>
                 <p><strong>Answer:</strong> {item.answer}</p>
               </div>
             ))}
           </div>
         )}
       </div>
     );
   }
   ```

2. **Test History**:
   - Run both servers.
   - Ask multiple questions (e.g., “What is AI?”, “What is RAG?”).
   - See history below the current answer.

**Troubleshooting**:
- **History not showing**: Check `setHistory` in `handleSubmit`.
- **Duplicate entries**: Ensure `key={index}` in the history map.

**Explanation**:
- **useState(history)**: Stores an array of past questions and answers.
- **setHistory**: Adds new entries on each successful response.
- **Rendering**: Maps history to display past interactions.

**Practice**:
- Add a “Clear History” button that calls `setHistory([])`.
- Style history entries (e.g., add a border in `globals.css`).

---

### Step 5:

### Overview
- **Goal**: Replace the dummy RAG logic in `backend/main.py` with a real RAG system using:
  - **Ollama (Mistral)**: For generating answers (LLM).
  - **Ollama (nomic-embed-text)**: For creating embeddings (to search documents).
  - **FAISS**: A local vector store to store and search document embeddings.
- **Why Local?**: You have Ollama models (`mistral:latest`, `nomic-embed-text:latest`) on your PC, so no external APIs are needed.
- **Steps**:
  1. Install dependencies (LangChain, FAISS, etc.).
  2. Set up a sample document set for RAG.
  3. Update `main.py` to use Ollama and FAISS for RAG.
  4. Run and test the backend.
  5. Practice extending the system.

This integrates with the frontend from previous steps, ensuring the Q&A app works end-to-end.

---

### Prerequisites
- **Ollama Running**: Ensure Ollama is installed and running locally. Verify by running:
  ```
  ollama list
  ```
  - You should see `mistral:latest`, `nomic-embed-text:latest`, etc.
  - Start Ollama server if not running (depends on your setup; typically `ollama serve`).
- **Python**: Already installed (3.8+).
- **Backend Setup**: From previous steps, you have `backend/` with a virtual environment (`venv`).
- **Frontend**: From previous steps, `frontend/` is set up and connects to `http://localhost:8000/rag`.

---

### Step 5: Prepare for Real RAG Integration (Local with Ollama and FAISS)

#### 5.1 Install RAG Dependencies
**Goal**: Install Python packages for LangChain, Ollama integration, and FAISS.

1. **Activate Virtual Environment**:
   - In `backend/`:
     ```
     cd rag-prototype/backend
     source venv/bin/activate  # Windows: venv\Scripts\activate
     ```

2. **Install Dependencies**:
   - Run:
     ```
     pip install langchain langchain_community faiss-cpu
     ```
   - **Packages**:
     - `langchain`: Core library for RAG.
     - `langchain_community`: Includes Ollama integration.
     - `faiss-cpu`: Local vector store (lightweight, runs on CPU).

3. **Verify Installation**:
   - Run:
     ```
     python -c "import langchain, langchain_community, faiss; print('Installed')"
     ```
   - Expect: `Installed`. If errors, re-run `pip install`.

**Troubleshooting**:
- **Module not found**: Ensure `(venv)` is active; re-run `pip install`.
- **Pip errors**: Try `pip install --force-reinstall langchain langchain_community faiss-cpu`.

**Explanation**:
- `langchain_community` provides the `Ollama` class to use your local models.
- `faiss-cpu` stores document embeddings locally, replacing Pinecone.
- No `.env` updates needed since we’re avoiding API keys.

#### 5.2 Set Up Sample Documents
**Goal**: Create a small set of documents for RAG to search.

1. **Create a Documents File**:
   - In `backend/`, create `documents.py`:
     ```python
     # Sample documents for RAG (you can expand this)
     DOCUMENTS = [
         "Artificial Intelligence (AI) is the simulation of human intelligence in machines, enabling tasks like reasoning and learning.",
         "Retrieval-Augmented Generation (RAG) combines retrieval of relevant documents with a language model to generate accurate answers.",
         "Machine learning is a subset of AI that focuses on training models to make predictions based on data."
     ]
     ```
   - These are sample texts RAG will search for relevant context.

**Explanation**:
- **Documents**: Represent the knowledge base RAG searches.
- **Practice**: You can add more documents or load from a file (e.g., text files) later.

#### 5.3 Update `main.py` for Real RAG
**Goal**: Replace dummy logic with RAG using Ollama’s `mistral` for generation, `nomic-embed-text` for embeddings, and FAISS for vector storage.

1. **Update `backend/main.py`**:
   ```python
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
   ```

2. **Explanation of Changes**:
   - **Imports**: Added `Ollama`, `OllamaEmbeddings`, `FAISS`, and `Document` from LangChain.
   - **RAG Setup**:
     - `embeddings`: Uses `nomic-embed-text` to convert text to vectors.
     - `llm`: Uses `mistral` to generate answers.
     - `vectorstore`: FAISS stores document embeddings from `DOCUMENTS`.
   - **RAG Logic**:
     - `similarity_search`: Finds top 2 relevant documents for the question.
     - `context`: Combines document texts for the LLM.
     - `prompt`: Feeds question and context to `mistral` for an answer.
     - `sources`: Returns the matched documents.
   - **Error Handling**: Catches RAG failures and logs them.
   - **No APIs**: All processing is local (Ollama and FAISS).

#### 5.4 Run and Test the Backend
1. **Start Ollama Server**:
   - Ensure Ollama is running (open a terminal and run `ollama serve` if needed).
   - Verify models:
     ```
     ollama list
     ```
     - Confirm `mistral:latest` and `nomic-embed-text:latest` are available.

2. **Run Backend**:
   - In `backend/` (with `(venv)` active):
     ```
     uvicorn main:app --reload
     ```
   - Open `http://localhost:8000/docs`.
   - Test `/rag` with:
     ```json
     {"question": "What is RAG?"}
     ```
     - Expect an answer like: `{"answer": "RAG combines retrieval of relevant documents with a language model.", "sources": ["Retrieval-Augmented Generation (RAG) combines...", "..."]}`.
   - Try `{"question": ""}` to see the empty question error.
   - Check terminal logs for `Retrieved context` and `Sending response`.

3. **Test with Frontend**:
   - Ensure frontend is running (`npm run dev` in `frontend/`).
   - Open `http://localhost:3000`, ask “What is AI?” or “What is RAG?”.
   - Verify the answer uses the sample documents and lists them as sources.

**Troubleshooting**:
- **Ollama errors**: Ensure `ollama serve` is running and models are listed (`ollama list`).
- **FAISS errors**: Reinstall `pip install faiss-cpu`.
- **Slow response**: Local models can be slow on weaker hardware; ensure your PC has enough RAM (8GB+ recommended).
- **Connection refused**: Check Ollama is running and accessible (default: `http://localhost:11434`).

**Explanation**:
- **Ollama**: Runs `mistral` for answers and `nomic-embed-text` for embeddings locally.
- **FAISS**: Stores document vectors in memory (no external service).
- **Integration**: Frontend sends questions; backend retrieves and generates answers.

#### 5.5 Practice Tasks
1. **Add More Documents**:
   - In `documents.py`, add:
     ```python
     DOCUMENTS = [
         "Artificial Intelligence (AI) is the simulation of human intelligence in machines, enabling tasks like reasoning and learning.",
         "Retrieval-Augmented Generation (RAG) combines retrieval of relevant documents with a language model to generate accurate answers.",
         "Machine learning is a subset of AI that focuses on training models to make predictions based on data.",
         "Neural networks are a type of machine learning model inspired by the human brain."
     ]
     ```
   - Restart backend, test with “What are neural networks?”.

2. **Modify Prompt**:
   - In `main.py`, change the prompt:
     ```python
     prompt = f"Question: {request.question}\nContext: {context}\nAnswer in one sentence:"
     ```
   - Test to see shorter answers.

3. **Try Another Model**:
   - Change `llm = Ollama(model="mistral")` to `llm = Ollama(model="deepseek-r1:7b")` in `main.py`.
   - Restart and test differences in answers.

**Troubleshooting**:
- **Document not found**: Ensure `documents.py` is in `backend/` and imported correctly.
- **Model errors**: Verify `deepseek-r1:7b` is listed in `ollama list`.

**Explanation**:
- **Documents**: More documents improve RAG accuracy.
- **Prompt**: Controls how `mistral` responds.
- **Model Swap**: Different models (e.g., `deepseek-r1`) may give varied results.

---

### Why This Approach?
- **Local**: Uses your Ollama models (`mistral`, `nomic-embed-text`) and FAISS, avoiding API costs.
- **Simple**: Minimal setup for learning RAG.
- **Extensible**: Add more documents or integrate with frontend history.
- **Production-Ready**: Structure supports scaling (e.g., add a file-based document loader).

---

### Next Steps
- **Extend Documents**: Load from a text file or folder instead of `DOCUMENTS`.
  - Example:
    ```python
    from langchain.document_loaders import TextLoader
    loader = TextLoader("path/to/docs.txt")
    documents = loader.load()
    ```
- **Frontend Enhancements**: Display sources with formatting (e.g., bold titles).
- **Deploy**: Follow Step 6 from the previous guide, ensuring Ollama is accessible (e.g., run on a server).

**Practice**:
- Add a new document about “Deep Learning” in `documents.py`.
- Change the prompt to include “Answer clearly and concisely.”
- Test with different questions and models.

If you hit errors (e.g., “Ollama not found”, “FAISS import error”), share the exact message and what you were doing. I can also provide code for additional features (e.g., file loading, frontend tweaks) or deployment help!

---

### Step 6: Deploy the Prototype (Optional Practice)
**Goal**: Deploy to make it accessible online.

1. **Frontend to Vercel**:
   - In `frontend/`:
     ```
     git init
     git add .
     git commit -m "Initial commit"
     ```
   - Create a GitHub repo (`rag-frontend`), push:
     ```
     git remote add origin https://github.com/your-username/rag-frontend.git
     git push -u origin main
     ```
   - Install Vercel CLI:
     ```
     npm install -g vercel
     ```
   - Deploy:
     ```
     vercel
     ```
     - Follow prompts, link to GitHub.
     - In Vercel dashboard, add `BACKEND_URL=http://localhost:8000` (update to backend URL later).
   - Visit the deployed URL (e.g., `https://rag-frontend.vercel.app`).

2. **Backend to Render**:
   - In `backend/`:
     ```
     pip freeze > requirements.txt
     git init
     git add .
     git commit -m "Initial commit"
     ```
   - Create a GitHub repo (`rag-backend`), push.
   - On [render.com](https://render.com):
     - Create a Web Service, link GitHub repo.
     - Set:
       - Runtime: Python
       - Build: `pip install -r requirements.txt`
       - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Add `.env` vars in dashboard (e.g., `ENVIRONMENT=production`).
   - Get the deployed URL (e.g., `https://rag-backend.onrender.com`).

3. **Update Frontend**:
   - In Vercel dashboard, update `BACKEND_URL` to the Render URL.
   - Redeploy: `vercel --prod`.

4. **Test Deployed App**:
   - Visit the frontend URL, ask questions, verify responses.

**Troubleshooting**:
- **CORS**: Update `main.py` `allow_origins` to include the Vercel URL.
- **Fetch errors**: Ensure `BACKEND_URL` is correct in Vercel.
- **Render slow**: Free tier may spin down; wait a minute.

**Explanation**:
- **Vercel**: Hosts Next.js, auto-scales, provides SSL.
- **Render**: Hosts FastAPI, supports Python, easy setup.
- **Env Vars**: Ensure backend URL is accessible to frontend.

**Practice**:
- Add a new endpoint in `main.py` (e.g., `@app.get("/health")`).
- Deploy only the frontend first, test with local backend.

---

### Step 7: Additional Features to Practice
**Goal**: Add more features to deepen understanding.

1. **Backend: Add API Key Authentication**:
   - Update `main.py`:
     ```python
     from fastapi import Depends, Header, HTTPException

     async def check_api_key(x_api_key: str = Header(default=None)):
         if x_api_key != "secret-key":
             raise HTTPException(status_code=401, detail="Invalid API key")
         return x_api_key

     @app.post("/rag", response_model=AnswerResponse)
     async def rag_endpoint(request: QuestionRequest, api_key: str = Depends(check_api_key)):
         # Existing code
     ```
   - Update `frontend/app/page.tsx` (in `handleSubmit`):
     ```tsx
     const res = await fetch("http://localhost:8000/rag", {
       method: "POST",
       headers: {
         "Content-Type": "application/json",
         "X-API-Key": "secret-key",
       },
       body: JSON.stringify({ question }),
     });
     ```
   - Test: Submit a question (works with correct key), remove key in browser DevTools (Network tab) to see 401 error.

2. **Frontend: Add Clear History Button**:
   - Update `frontend/app/page.tsx`, add to JSX:
     ```tsx
     {history.length > 0 && (
       <div>
         <button
           onClick={() => setHistory([])}
           className="button"
           style={{ marginTop: "10px" }}
         >
           Clear History
         </button>
         <div className="answer-box">
           <h2>History:</h2>
           {history.map((item, index) => (
             <div key={index} style={{ marginBottom: "10px" }}>
               <p><strong>Question:</strong> {item.question}</p>
               <p><strong>Answer:</strong> {item.answer}</p>
             </div>
           ))}
         </div>
       </div>
     )}
     ```
   - Test: Ask questions, click “Clear History” to reset.

**Troubleshooting**:
- **API key error**: Ensure `X-API-Key` header is sent.
- **History not clearing**: Check `setHistory([])` is called.

**Explanation**:
- **API Key**: Adds basic security to backend.
- **Clear History**: Enhances UX by resetting state.

**Practice**:
- Change the API key to a different value.
- Add a style to the history section (e.g., border in `globals.css`).

---

### Step 8: How to Run and Test Everything
**Goal**: Summarize how to run and test the entire prototype.

1. **Run Backend**:
   - In `backend/`:
     ```
     source venv/bin/activate  # Windows: venv\Scripts\activate
     uvicorn main:app --reload
     ```
   - Test: `http://localhost:8000/docs`, try `/rag`.

2. **Run Frontend**:
   - In `frontend/`:
     ```
     npm run dev
     ```
   - Test: `http://localhost:3000`, ask questions, check history, navigate to About.

3. **Full Test**:
   - Ask questions, verify answers/sources.
   - Test empty input for error.
   - Check history and clear it.
   - Use browser DevTools (F12 > Network) to see API calls.
   - Check backend terminal for logs.

4. **Optional: Deploy**:
   - Follow Step 6 for Vercel/Render.
   - Test deployed app online.

**Troubleshooting**:
- **Connection issues**: Ensure both servers run, ports are `3000` (frontend) and `8000` (backend).
- **Errors**: Check browser console and backend logs.
- **Dependencies**: Reinstall if issues (`npm install` or `pip install ...`).

---

### Step 9: Next Steps and Further Practice
- **Real RAG**: Sign up for OpenAI/Pinecone, uncomment RAG code in `main.py`, and test with real data.
- **Add Features**:
  - Backend: Log questions to a file.
  - Frontend: Add a “Copy Answer” button.
- **Testing**: Install Jest (`npm install --save-dev jest`) or pytest (`pip install pytest`) for unit tests.
- **Deploy**: Practice deployment with different platforms (e.g., Netlify for frontend, Heroku for backend).

**Practice Ideas**:
- Add a new page (e.g., `app/contact/page.tsx`).
- Modify backend to return a different dummy answer.
- Deploy only one part (frontend or backend) and test locally with the other.

---

### Why This Prototype?
- **Simple**: Minimal code to learn Next.js and FastAPI.
- **Connected**: Frontend talks to backend via API.
- **Extensible**: Ready for real RAG with LangChain.
- **Production-Ready Structure**: Folders and files mimic real apps.

If you get errors (e.g., “module not found”, “CORS”), share the exact message and what you were doing, and I’ll help! You can also ask for specific extensions (e.g., more features, tests). Practice by modifying small parts and testing!
