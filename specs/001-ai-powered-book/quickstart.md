# Quickstart Guide: AI-Powered Book Enhancement

## Overview
This guide provides a quick setup and usage guide for the AI-Powered Book Enhancement feature. It covers how to set up the development environment, run the application locally, and use the key features.

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.8+ for backend development
- Access to Google Gemini API
- Qdrant vector database (local instance or cloud)
- Git for version control

## Setting up the Development Environment

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-book-project
```

### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Google Gemini API key and other configurations
```

### 3. Frontend Setup (Docusaurus)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

### 4. Qdrant Vector Database Setup
```bash
# Option 1: Local Docker container
docker run -p 6333:6333 -p 6334:6334 -v ./qdrant_storage:/qdrant/storage:z qdrant/qdrant

# Option 2: Cloud instance
# Create account at qdrant.cloud and configure connection details in backend
```

## Running the Application Locally

### 1. Start the Backend
```bash
cd backend
# Activate virtual environment if not already done
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Start the FastAPI server
uvicorn main:app --reload --port 8000
```

### 2. Index the Book Content
```bash
# In the backend directory with the virtual environment activated
python indexing_script.py
```

### 3. Start the Frontend
```bash
cd frontend
npm start
# or
yarn start
```

The application will be available at `http://localhost:3000` with the AI backend at `http://localhost:8000`.

## Key Features Usage

### 1. Browsing Book Content
- Navigate through the sidebar using the 13-week course structure
- Access modules and weekly breakdowns as specified in hackathon.md
- Use the search feature in the top navigation bar

### 2. Using the AI Chat Interface
- Locate the chat widget in the bottom-right corner of the page
- Type questions about the book content in the input field
- The AI will provide answers based solely on the book content
- Responses will reference specific sections when possible

### 3. Bookmarking Sections
- When viewing a section you want to save, click the bookmark icon
- Access your bookmarks using the bookmark menu in the navigation
- Bookmarks are stored in browser's local storage

## API Usage Examples

### Querying the AI
```bash
curl -X POST "http://localhost:8000/v1/ai/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain the concept of ROS 2 from Module 1",
    "session_id": "session-123"
  }'
```

### Searching Content
```bash
curl -X GET "http://localhost:8000/v1/content/search?q=ROS%202&limit=5"
```

### Getting Content by Section
```bash
curl -X GET "http://localhost:8000/v1/content/section-1-id"
```

## Testing the Application

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
# or
yarn test
```

## Deployment

### Building for Production
```bash
# Frontend
cd frontend
npm run build
# or
yarn build

# Backend (follow your deployment platform's requirements)
```

## Troubleshooting

### Common Issues
- **AI responses taking too long**: Check Google Gemini API connection and rate limits
- **Content not showing**: Verify that indexing_script.py was run after content updates
- **Chat widget not appearing**: Check that the React chat component is properly integrated
- **Qdrant connection errors**: Verify Qdrant service is running and connection details are correct

### Environment Variables
Ensure all required environment variables are set:
- `GEMINI_API_KEY`: Google Gemini API key
- `QDRANT_URL`: URL of the Qdrant instance
- `QDRANT_API_KEY`: Qdrant API key (if applicable)
- `ENVIRONMENT`: Set to "development", "staging", or "production"