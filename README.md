# Code Assessment for Full-Stack Python Engineer

## Overview

This repository contains the code assessment for a full-stack Python engineer. The tasks involve creating a FastAPI application with SQLAlchemy ORM model for a SQLite database. The application includes routes for managing reviews and tags, and Pytest test cases to ensure correctness.

## Task Completion

### Database Setup

1. SQLite database named `reviews` with tables:
   - `reviews` with columns: `id`, `text`, `is_tagged`
   - `tags` with columns: `id`, `name`
   - `review_tag` with columns: `id`, `is_ai_tag`, `tag_id`
   - `review_review_tags` with columns: `id`, `review_id`, `review_tag_id`

### FastAPI Application

2. Implemented FastAPI application with OpenAPI compliant routes:
   - `POST /reviews/{review_id}/tags`: Adds a tag to the specified review.
   - `GET /reviews`: Returns a paginated list of reviews with associated tag information.
   - `POST /tags`: Creates a new tag.
   - `DELETE /tags/{tag_id}`: Deletes a tag and associated `review_tag`.

### Testing

3. Pytest test cases for each route and data associations:
   - Use the following commands to run tests and check coverage:
     ```bash
     virtualenv venv
     source venv/bin/activate  # On Windows, use venv\Scripts\activate
     uvicorn main:app --reload
     coverage run -m pytest test/test_review_routes.py
     coverage report -m
     ```

## Instructions

1. To start the code assessment, fork this repository.
2. Create a pull request to the repository (access share via email).
command -git clone https://github.com/srinivaskstpl/Code-Assessment-for-Full-Stack-Python-Engineer.git

3. Added `Nicky(lele9112@163.com)` and `Terry(wh9112@gmail.com)` as collaborators to repository for code review.
4. Leave a comment on the pull request with the following information:
   ```markdown
   Name:
   Email:
   Application channel: Linkedin/UpWork/Yodo1 official website
   Position:
   ```

Thanks for your time and effort! If you have any questions, feel free to reach out to the provided contacts.