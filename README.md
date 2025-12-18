# AI-Powered Book Enhancement

A comprehensive AI-powered book with integrated chatbot that uses RAG (Retrieval-Augmented Generation) to answer questions about the book's content.

## Features

- Interactive AI chat interface integrated into the Docusaurus book
- RAG (Retrieval-Augmented Generation) for accurate answers based on book content
- Responsive design for all devices
- Content indexing for efficient information retrieval
- Context-aware responses based on relevant sections

## Prerequisites

- Python 3.8+
- Node.js 18+ (for Docusaurus frontend)
- Qdrant vector database
- Google Gemini API key

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   
   Then edit `.env` and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your-gemini-api-key-here
   ```

4. Start the Qdrant database (either locally or use cloud instance):
   - For local setup using Docker:
     ```bash
     docker run -p 6333:6333 -p 6334:6334 -v ./qdrant_storage:/qdrant/storage:z qdrant/qdrant
     ```

5. Run the content indexing script to load book content:
   ```bash
   python src/indexing_script.py
   ```

6. Start the backend server:
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup (AI-native-book)

1. Navigate to the frontend directory:
   ```bash
   cd AI-native-book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Endpoints

- `POST /v1/ai/query` - Submit a question about the book content
- `GET /v1/ai/response/{response_id}` - Retrieve details of a specific AI response

## Architecture

- **Frontend**: Docusaurus 3.x with React-based ChatWidget component
- **Backend**: FastAPI with services for AI integration, RAG functionality, and database operations
- **AI Service**: Google Gemini for intelligent responses
- **Database**: Qdrant vector database for document indexing
- **Embeddings**: Sentence Transformers for content vectorization

## Troubleshooting

1. If you see mock responses in the chatbot, ensure all dependencies are installed:
   ```bash
   pip install sentence-transformers google-generativeai qdrant-client
   ```

2. Make sure your GEMINI_API_KEY is properly set in the .env file

3. Verify Qdrant database is running and accessible

## Development

The implementation follows these architectural principles:
- Separate backend API and frontend components
- RAG (Retrieval-Augmented Generation) for accurate responses
- Proper separation of concerns with dedicated services
- Environment-based configuration
- Error handling and fallback responses

## Production Deployment

For production deployment:
1. Use environment variables for all sensitive information
2. Implement proper authentication if required
3. Set up a production-grade Qdrant instance
4. Configure proper CORS settings
5. Optimize performance and implement caching as needed