import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel
from qdrant_client import QdrantClient, models
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import asyncio

load_dotenv() # Load environment variables from .env file

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Qdrant configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "book_content"

# Google GenAI configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

EMBEDDING_MODEL = "text-embedding-004"
GENERATION_MODEL = "gemini-2.5-flash"

# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

print(f"Qdrant Client Type: {type(qdrant_client)}")
print(f"Qdrant Client Attributes: {dir(qdrant_client)}")

# Initialize Embedding Model
embeddings_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=GEMINI_API_KEY
)

# Initialize LLM for generation
llm = ChatGoogleGenerativeAI(
    model=GENERATION_MODEL,
    google_api_key=GEMINI_API_KEY
)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Generate embedding for the user query
        query_embedding = embeddings_model.embed_query(request.query)

        # 2. Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3 # top_k=3 as per requirements
        )

        context_texts = [hit.payload["text"] for hit in search_result]

        # 3. Prepare prompt for LLM
        prompt_template = """
        You are a helpful assistant for a Docusaurus book. Answer the user's question based on the provided context only.
        use qdrant for chunk retrieval.and make detailed it and explain it .
        If the answer is not in the context,in genral qeustion, answered that.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # 4. Generate response using LLM
        full_context = "\n\n".join(context_texts)

        formatted_prompt = prompt.format(context=full_context, question=request.query)

        # Use invoke to get the full response
        response = llm.invoke(formatted_prompt)
        
        # Return as a single JSON response
        return JSONResponse(content={"response": response.content})

    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'An error occurred: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat-stream")
async def chat_stream_endpoint(request: ChatRequest):
    try:
        # 1. Generate embedding for the user query
        query_embedding = embeddings_model.embed_query(request.query)

        # 2. Retrieve relevant chunks from Qdrant
        search_result = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_embedding,
            limit=3 # top_k=3 as per requirements
        )

        context_texts = [hit.payload["text"] for hit in search_result]

        # 3. Prepare prompt for LLM
        prompt_template = """
        You are a helpful assistant for a Docusaurus book. Answer the user's question based on the provided context only.
        If the answer is not in the context, politely state that you don't have enough information.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )

        # 4. Generate response using LLM
        full_context = "\n\n".join(context_texts)

        formatted_prompt = prompt.format(context=full_context, question=request.query)

        # Use streaming instead of invoke
        async def event_generator():
            try:
                stream = llm.stream(formatted_prompt)
                for chunk in stream:
                    if chunk.content:
                        yield f"data: {chunk.content}\n\n"
            except Exception as e:
                logging.error(f'Streaming error: {e}', exc_info=True)
                yield f"data: Error during streaming: {str(e)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.error(f'An error occurred: {e}', exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/qdrant-status")
async def get_qdrant_status():
    try:
        collection_info = qdrant_client.get_collection(QDRANT_COLLECTION_NAME)
        return {
            "collection_name": QDRANT_COLLECTION_NAME,
            "status": "active",
            "point_count": collection_info.points_count
        }
    except Exception as e:
        # Log the exception for debugging
        logging.error(f"Error checking Qdrant status: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error checking Qdrant status: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
