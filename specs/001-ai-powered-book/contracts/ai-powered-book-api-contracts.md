# API Contracts: AI-Powered Book Enhancement

## Overview
This document defines the API contracts for the AI-Powered Book Enhancement feature based on the functional requirements. All endpoints are designed to support the 13-week course structure specified in the feature requirements.

## Base URL
`https://api.ai-powered-book.com/v1` (or local equivalent during development)

## Content Endpoints

### Get All Book Content
- **Endpoint**: `GET /content`
- **Description**: Retrieve all book content organized according to the 13-week course structure
- **Authentication**: None required
- **Query Parameters**: 
  - `module` (optional): Filter by module number
  - `week` (optional): Filter by week number
- **Response**:
  ```json
  {
    "modules": [
      {
        "id": "module-1",
        "title": "Module Title",
        "module_number": 1,
        "weeks": [
          {
            "week_number": 1,
            "title": "Week Title",
            "content_sections": [
              {
                "id": "section-1",
                "title": "Section Title",
                "url_path": "/module-1/week-1/section-1",
                "content_preview": "Brief preview of content"
              }
            ]
          }
        ]
      }
    ]
  }
  ```

### Get Content by Section ID
- **Endpoint**: `GET /content/{section_id}`
- **Description**: Retrieve specific book content section
- **Authentication**: None required
- **Path Parameters**: 
  - `section_id` (required): Unique identifier for the content section
- **Response**:
  ```json
  {
    "id": "section-1",
    "title": "Section Title",
    "content": "Full content of the section...",
    "module_id": "module-1",
    "week_number": 1,
    "type": "lesson",
    "order_index": 1,
    "metadata": {}
  }
  ```

### Search Content
- **Endpoint**: `GET /content/search`
- **Description**: Search for specific topics or keywords within the book content
- **Authentication**: None required
- **Query Parameters**:
  - `q` (required): Search query
  - `limit` (optional): Maximum number of results (default: 10)
- **Response**:
  ```json
  {
    "query": "search term",
    "results": [
      {
        "id": "section-1",
        "title": "Section Title",
        "url_path": "/module-1/week-1/section-1",
        "content_preview": "Preview of content containing search term...",
        "relevance_score": 0.95
      }
    ],
    "total_results": 5
  }
  ```

## AI Interaction Endpoints

### Submit AI Query
- **Endpoint**: `POST /ai/query`
- **Description**: Submit a question about the book content to the AI
- **Authentication**: None required
- **Request Body**:
  ```json
  {
    "query": "What is ROS 2?",
    "session_id": "unique-session-identifier",
    "context": {
      "current_section_id": "section-1",
      "current_module": "module-1",
      "current_week": 1
    }
  }
  ```
- **Response**:
  ```json
  {
    "response_id": "response-123",
    "query": "What is ROS 2?",
    "answer": "ROS 2 (Robot Operating System 2) is the next generation robotics middleware...",
    "referenced_sections": [
      {
        "id": "section-1",
        "title": "Introduction to ROS 2",
        "url_path": "/module-1/week-1/section-1"
      }
    ],
    "confidence_score": 0.92,
    "timestamp": "2024-12-18T10:30:00Z"
  }
  ```

### Get AI Response Details
- **Endpoint**: `GET /ai/response/{response_id}`
- **Description**: Retrieve details of a specific AI response
- **Authentication**: None required
- **Path Parameters**:
  - `response_id` (required): Unique identifier for the AI response
- **Response**:
  ```json
  {
    "response_id": "response-123",
    "original_query": "What is ROS 2?",
    "answer": "ROS 2 (Robot Operating System 2) is the next generation robotics middleware...",
    "referenced_sections": [
      {
        "id": "section-1",
        "title": "Introduction to ROS 2",
        "url_path": "/module-1/week-1/section-1",
        "content_snippet": "ROS 2 provides a collection of libraries and tools..."
      }
    ],
    "confidence_score": 0.92,
    "timestamp": "2024-12-18T10:30:00Z"
  }
  ```

## User Interaction Endpoints

### Bookmark Section
- **Endpoint**: `POST /bookmarks`
- **Description**: Create a bookmark for a specific book section
- **Authentication**: Browser session only (no server authentication)
- **Request Body**:
  ```json
  {
    "section_id": "section-1",
    "section_title": "Introduction to ROS 2",
    "url_path": "/module-1/week-1/section-1",
    "session_id": "unique-session-identifier"
  }
  ```
- **Response**:
  ```json
  {
    "bookmark_id": "bookmark-456",
    "section_id": "section-1",
    "section_title": "Introduction to ROS 2",
    "url_path": "/module-1/week-1/section-1",
    "bookmark_date": "2024-12-18T10:30:00Z"
  }
  ```

### Get Bookmarks
- **Endpoint**: `GET /bookmarks`
- **Description**: Retrieve all bookmarks for the current session
- **Authentication**: Browser session only (no server authentication)
- **Query Parameters**:
  - `session_id` (required): User's browser session identifier
- **Response**:
  ```json
  {
    "bookmarks": [
      {
        "bookmark_id": "bookmark-456",
        "section_id": "section-1",
        "section_title": "Introduction to ROS 2",
        "url_path": "/module-1/week-1/section-1",
        "bookmark_date": "2024-12-18T10:30:00Z"
      }
    ]
  }
  ```

### Delete Bookmark
- **Endpoint**: `DELETE /bookmarks/{bookmark_id}`
- **Description**: Remove a specific bookmark
- **Authentication**: Browser session only (no server authentication)
- **Path Parameters**:
  - `bookmark_id` (required): Unique identifier for the bookmark
- **Response**: 204 No Content

## Error Responses

All endpoints follow standard HTTP error conventions:

- `400 Bad Request`: Request validation failed
- `404 Not Found`: Requested resource doesn't exist
- `500 Internal Server Error`: Server encountered an error
- `503 Service Unavailable`: AI service temporarily unavailable

Error response format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details if applicable"
  }
}
```