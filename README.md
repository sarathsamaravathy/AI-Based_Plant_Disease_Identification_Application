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

**Recommended:** Python 3.11, or Python 3.12 with updated packaging tools.

- Python 3.11 or 3.12
- Node.js 18+
- Docker + Docker Compose
- PostgreSQL
- Ollama service running locally

> **Troubleshooting:**
> If you use Python 3.12 and see errors during dependency install, first upgrade packaging tools and prefer binary wheels. If a package build still fails because it imports `pkg_resources`, use the compatibility fallback below.

### Setup Backend

1. Copy `.env.example` to `.env`

2. Upgrade pip, setuptools, and wheel:

```bash
python -m pip install --upgrade pip setuptools wheel
```

3. Install Python dependencies, preferring binary wheels:

```bash
python -m pip install --prefer-binary -r requirements.txt
```

4. If the install still fails with `ModuleNotFoundError: No module named 'pkg_resources'`, use:

```bash
python -m pip install "setuptools<80.10.3"
python -m pip install --prefer-binary -r requirements.txt
```

5. Start the backend locally:

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
