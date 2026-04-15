# AI-Based Plant Disease Identification Application

Multilingual AI-based plant disease diagnosis application using a Vue.js frontend and FastAPI backend.

## Overview

This repository contains a simplified prototype for identifying plant diseases using image and symptom inputs. The system supports multilingual output for regional Indian languages and uses a self-hosted LLM backend for reasoning.

## Technology Stack

- Frontend: Vue.js 3 + Vite
- Backend: FastAPI
- Model inference: PyTorch / torchvision
- Database: PostgreSQL
- Vector store: Chroma (local)
- LLM orchestration: Ollama
- MLOps: MLflow (local tracking)

## Features

- Upload leaf images for disease diagnosis
- Text-based symptom reporting
- Multilingual result formatting
- Feedback capture for model improvement
- Docker Compose orchestration for local development

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker + Docker Compose
- PostgreSQL
- Ollama service running locally

### Setup Backend

1. Copy `.env.example` to `.env`
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend locally:

```bash
uvicorn src.api.main:app --reload
```

### Setup Frontend

1. Change into the frontend directory:

```bash
cd frontend
```

2. Install npm dependencies:

```bash
npm install
```

3. Start the frontend dev server:

```bash
npm run dev
```

### Docker Compose

Start the full stack with:

```bash
docker-compose up -d
```

## Repository Structure

- `src/` - Python backend and AI modules
- `frontend/` - Vue.js application
- `data/` - Dataset and storage placeholders
- `models/` - Model artifacts
- `tests/` - Unit and integration tests
- `docs/` - Architecture and deployment documentation

## Notes

This repository is a working scaffold for plant disease identification and is intended for local development and prototype evaluation.
