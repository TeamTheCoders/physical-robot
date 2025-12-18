import os
import glob
from pathlib import Path
from dotenv import load_dotenv
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient, models
import uuid
import os

# Load environment variables
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = "book_content"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

EMBEDDING_MODEL = "text-embedding-004"

def load_and_chunk_documents(source_path):
    """Load documents from source path and chunk them."""
    print(f"Loading documents from {source_path}")
    
    # Find all markdown files in the source directory
    md_files = glob.glob(os.path.join(source_path, "**/*.md"), recursive=True)
    
    documents = []
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Add metadata about the source file
            documents.append({
                "content": content,
                "source": file_path
            })
    
    print(f"Loaded {len(documents)} documents")
    
    # Chunk the documents
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )
    
    chunked_docs = []
    for doc in documents:
        chunks = text_splitter.split_text(doc["content"])
        for chunk in chunks:
            chunked_docs.append({
                "text": chunk,
                "source": doc["source"]
            })
    
    print(f"Created {len(chunked_docs)} chunks")
    return chunked_docs

def initialize_qdrant_collection(client, collection_name):
    """Initialize the Qdrant collection."""
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
        )
        print(f"Collection '{collection_name}' created successfully.")
    except Exception as e:
        # Collection might already exist, that's okay
        print(f"Collection '{collection_name}' likely already exists: {e}")

def index_to_qdrant(chunked_docs, embeddings_model, client, collection_name):
    """Index the chunked documents to Qdrant."""
    print(f"Indexing {len(chunked_docs)} chunks to Qdrant...")
    
    points = []
    for i, doc in enumerate(chunked_docs):
        # Create embedding for the text
        vector = embeddings_model.embed_query(doc["text"])
        
        # Create a point for Qdrant
        point = models.PointStruct(
            id=i,  # Using index as ID, in production use UUID
            vector=vector,
            payload={
                "text": doc["text"],
                "source": doc["source"]
            }
        )
        points.append(point)
        
        # Batch insert every 100 points or at the end
        if len(points) >= 100 or i == len(chunked_docs) - 1:
            try:
                client.upsert(collection_name=collection_name, points=points)
                print(f"Indexed {min(i+1, len(chunked_docs))}/{len(chunked_docs)} documents")
                points = []  # Reset points list
            except Exception as e:
                print(f"Error indexing points: {e}")
                raise e
    
    print("Indexing completed!")

def main():
    """Main function to run the indexing process."""
    print("Starting indexing process...")
    
    # Initialize embeddings model
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GEMINI_API_KEY
    )
    
    # Initialize Qdrant client
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )
    
    # Define source path for Docusaurus docs
    source_path = "./AI-native-book/docs/"
    
    # Load and chunk documents
    chunked_docs = load_and_chunk_documents(source_path)
    
    # Initialize collection
    initialize_qdrant_collection(qdrant_client, QDRANT_COLLECTION_NAME)
    
    # Index to Qdrant
    index_to_qdrant(chunked_docs, embeddings_model, qdrant_client, QDRANT_COLLECTION_NAME)
    
    print("Indexing process completed successfully!")

if __name__ == "__main__":
    main()