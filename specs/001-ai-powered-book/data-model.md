# Data Model: AI-Powered Book Enhancement

## Overview
This document describes the data models for the AI-Powered Book Enhancement feature, focusing on how content is structured, accessed, and related to AI responses.

## Core Entities

### Book Content
- **Name**: Book Content
- **Fields**: 
  - id: String (unique identifier for each content section)
  - title: String (title of the section/module/week)
  - content: Text (the actual book content)
  - type: Enum (module, week, lesson, exercise, objective, assessment)
  - module_id: String (reference to parent module)
  - week_number: Integer (for weekly breakdown in 13-week course)
  - order_index: Integer (sequence within parent container)
  - created_date: DateTime
  - updated_date: DateTime
  - metadata: JSON (additional content attributes)
- **Relationships**: Parent-child relationships with modules, weeks, and sub-sections
- **Validation rules**: Content and title are required fields
- **State transitions**: N/A (content is static once published)

### AI Query
- **Name**: AI Query
- **Fields**:
  - id: String (unique identifier for each query)
  - query_text: Text (the user's question)
  - timestamp: DateTime (when the query was made)
  - user_session_id: String (to track queries in current session)
  - source_content_ids: Array[String] (content IDs referenced by the AI response)
  - query_type: Enum (factual, conceptual, application, navigation)
- **Relationships**: Related to Book Content (one-to-many: AI responses can reference multiple content sections)
- **Validation rules**: query_text is required
- **State transitions**: N/A (queries are immutable once stored)

### AI Response
- **Name**: AI Response
- **Fields**:
  - id: String (unique identifier for each response)
  - response_text: Text (the AI's answer)
  - timestamp: DateTime (when the response was generated)
  - ai_query_id: String (reference to the original query)
  - referenced_content_ids: Array[String] (IDs of content sections referenced in response)
  - confidence_score: Float (confidence level of the response, 0-1)
  - response_metadata: JSON (additional response attributes, like tokens used)
- **Relationships**: Linked to AI Query (many-to-one) and Book Content (many-to-many)
- **Validation rules**: response_text and ai_query_id are required
- **State transitions**: N/A (responses are immutable once generated)

### Bookmarked Section
- **Name**: Bookmarked Section
- **Fields**:
  - id: String (unique identifier)
  - section_id: String (reference to the book content section)
  - section_title: String (title of the bookmarked section)
  - url_path: String (URL to access the section)
  - bookmark_date: DateTime (when it was bookmarked)
  - user_session_id: String (browser session identifier)
- **Relationships**: Related to Book Content (many-to-one)
- **Validation rules**: section_id, section_title, and user_session_id are required
- **State transitions**: Can be removed (deleted) by user
- **Notes**: Stored in browser's local storage, not on server

### Module
- **Name**: Module
- **Fields**:
  - id: String (unique identifier for the module)
  - title: String (the name of the module)
  - description: Text (brief overview of the module)
  - module_number: Integer (Module 1, 2, 3, or 4 as per hackathon.md)
  - learning_objectives: Array[Text] (list of learning objectives)
  - weeks_count: Integer (number of weeks in the module)
  - content_sections: Array[String] (IDs of content sections in the module)
  - prerequisites: Array[String] (IDs of prerequisite modules)
- **Relationships**: Contains multiple Book Content items; may have prerequisites to other Modules
- **Validation rules**: title is required
- **State transitions**: N/A (modules are static)

### Weekly Breakdown
- **Name**: Weekly Breakdown
- **Fields**:
  - id: String (unique identifier)
  - module_id: String (reference to parent module)
  - week_number: Integer (1-13 for the 13-week course)
  - title: String (title of the week)
  - content_summary: Text (summary of the week's content)
  - learning_goals: Array[Text] (specific goals for the week)
  - assignments: Array[Text] (assignments or exercises for the week)
- **Relationships**: Belongs to a Module; contains multiple Book Content items
- **Validation rules**: module_id, week_number, and title are required
- **State transitions**: N/A (weekly breakdows are static)