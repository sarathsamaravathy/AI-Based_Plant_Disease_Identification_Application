# AI-Based Plant Disease Identification Application

Multilingual AI-based plant disease diagnosis application using a Vue.js frontend and FastAPI backend.

## Overview

This repository contains a prototype for identifying plant diseases from leaf images or symptom descriptions. It supports multilingual output for regional Indian languages and uses a self-hosted LLM backend for reasoning.

## Technology Stack

- Frontend: Vue.js 3 + Vite
- Backend: FastAPI
- Vision: PyTorch + torchvision
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

### 1. Clone the repository

```bash
git clone https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application.git
cd AI-Based_Plant_Disease_Identification_Application
```

### 2. Prerequisites

- Python 3.11 or 3.12
- Node.js 18+
- Docker & Docker Compose (recommended)
- PostgreSQL
- Ollama service running locally for the LLM backend

### 3. Backend Setup

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

2. Upgrade packaging tools:

```bash
python -m pip install --upgrade pip setuptools wheel
```

3. Install Python dependencies:

```bash
python -m pip install --prefer-binary -r requirements.txt
```

4. If install fails with `ModuleNotFoundError: No module named 'pkg_resources'`, use the compatibility fallback:

```bash
python -m pip install "setuptools<80.10.3"
python -m pip install --prefer-binary -r requirements.txt
```

5. Copy the environment file:

```bash
cp .env.example .env
```

6. Start the backend:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at `http://localhost:8000`.

### 4. Frontend Setup

1. Change into the frontend directory:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`.

### 5. Docker Compose (Optional)

To run the full stack locally:

```bash
docker-compose up -d
```

### 6. Common Commands

- Run backend tests:

```bash
pytest tests/ -v
```

- Lint Python code:

```bash
flake8 src --max-line-length=100
```

- Format Python code:

```bash
black src --line-length=100
```

## Repository Structure

- `frontend/` — Vue.js application
- `src/` — Python backend, AI modules, API
- `data/` — datasets and sample inputs
- `models/` — pretrained model artifacts
- `tests/` — unit and integration tests
- `docker-compose.yml` — local orchestration
- `requirements.txt` — Python dependencies

## Troubleshooting

- Use Python 3.11 when possible for the most stable install experience.
- If using Python 3.12, upgrade `pip setuptools wheel` before installing dependencies.
- If you hit `pkg_resources` build failures, install `setuptools<80.10.3` and retry.

## Notes

This project is intended as a development prototype for plant disease diagnosis and requires manual validation before any production use.
