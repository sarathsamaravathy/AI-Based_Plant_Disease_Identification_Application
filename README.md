# AI-Based Plant Disease Identification Application

A multilingual AI-powered application for identifying plant diseases from leaf images or symptom descriptions. Built with Vue.js frontend and FastAPI backend, supporting 22 Indian languages.

## Features

- 🖼️ **Image-based diagnosis**: Upload leaf images for disease detection
- 📝 **Text-based reporting**: Describe symptoms in natural language
- 🌍 **Multilingual support**: Results in 22 Indian languages (Hindi, Tamil, Telugu, etc.)
- 🤖 **AI-powered reasoning**: Uses self-hosted LLMs via Ollama
- 📊 **Feedback system**: Collect user feedback for model improvement
- 🐳 **Docker support**: Easy deployment with Docker Compose
- 📈 **MLOps tracking**: MLflow integration for experiment tracking

## Prerequisites

Before installing, ensure you have the following:

- **Python 3.11 or 3.12** (3.12 recommended for latest features)
- **Node.js 18+** (for frontend development)
- **PostgreSQL** (for data storage)
- **Ollama** (for local LLM inference)
- **Git** (for cloning the repository)
- **Docker & Docker Compose** (optional, for containerized deployment)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application.git
cd AI-Based_Plant_Disease_Identification_Application
```

### Step 2: Set Up PostgreSQL Database

1. Install PostgreSQL if not already installed
2. Create a database named `plant_disease_db`
3. Note the connection details (host, port, username, password)

### Step 3: Set Up Ollama (LLM Backend)

1. Install Ollama from [ollama.ai](https://ollama.ai)
2. Pull the required model:

```bash
ollama pull llama2  # or any supported model
```

3. Start Ollama service:

```bash
ollama serve
```

### Step 4: Backend Setup

1. **Create virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Upgrade packaging tools:**

   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

4. **Install Python dependencies:**

   ```bash
   python -m pip install --prefer-binary -r requirements.txt
   ```

   > **Note:** If you encounter `ModuleNotFoundError: No module named 'pkg_resources'`, use this fallback:
   > ```bash
   > python -m pip install "setuptools<80.10.3"
   > python -m pip install --prefer-binary -r requirements.txt
   > ```

5. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your database and Ollama settings.

6. **Start the backend server:**

   ```bash
   uvicorn src.api.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

### Step 5: Frontend Setup

> **Note:** The frontend runs on Node.js and doesn't require the Python virtual environment. Keep your backend terminal running with the activated venv.

1. **Open a new terminal** and navigate to the project directory:

   ```bash
   cd AI-Based_Plant_Disease_Identification_Application
   ```

2. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

3. **Install Node.js dependencies:**

   ```bash
   npm install
   ```

4. **Start the development server:**

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`.

### Step 6: Alternative - Docker Setup (Optional)

If you prefer using Docker:

```bash
docker-compose up -d
```

This will start all services (backend, frontend, database, Ollama) in containers.

## Usage

1. Open your browser and go to `http://localhost:5173`
2. Upload a leaf image or describe symptoms
3. Select your preferred language
4. Get AI-powered disease diagnosis with treatment suggestions

## Testing

### Backend Tests

```bash
# Activate virtual environment first
pytest tests/ -v --cov=src
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Development Commands

- **Lint Python code:** `flake8 src --max-line-length=100`
- **Format Python code:** `black src --line-length=100`
- **Lint frontend:** `cd frontend && npm run lint`
- **Format frontend:** `cd frontend && npm run format`

## Troubleshooting

### Common Issues

1. **Python 3.12 installation issues:**
   - Upgrade pip/setuptools: `python -m pip install --upgrade pip setuptools wheel`
   - Use `--prefer-binary` flag for installations

2. **Database connection errors:**
   - Ensure PostgreSQL is running
   - Check `.env` file for correct database credentials

3. **Ollama not responding:**
   - Verify Ollama service is running: `ollama serve`
   - Check model is pulled: `ollama list`

4. **Port conflicts:**
   - Backend: Change port in `uvicorn` command
   - Frontend: Check `vite.config.js` for port settings

5. **Memory issues:**
   - Reduce batch sizes in model configurations
   - Use smaller models if available

### Getting Help

- Check the [Issues](https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application/issues) page
- Review the [Wiki](https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application/wiki) for detailed guides

## Repository Structure

```
├── frontend/          # Vue.js application
├── src/              # Python backend code
│   ├── api/          # FastAPI routes
│   ├── database/     # Database models and connections
│   ├── vision/       # Computer vision modules
│   ├── llm/          # LLM integration
│   └── multilingual/ # Translation and TTS
├── data/             # Sample datasets
├── models/           # Pretrained model artifacts
├── tests/            # Unit and integration tests
├── docker-compose.yml # Container orchestration
└── requirements.txt  # Python dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and add tests
4. Run tests: `pytest tests/ -v`
5. Commit changes: `git commit -am 'Add your feature'`
6. Push to branch: `git push origin feature/your-feature`
7. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- PlantVillage dataset for training data
- AI4Bharat for Indic language models
- Meta for Llama models via Ollama

## Troubleshooting

- Use Python 3.11 when possible for the most stable install experience.
- If using Python 3.12, upgrade `pip setuptools wheel` before installing dependencies.
- If you hit `pkg_resources` build failures, install `setuptools<80.10.3` and retry.

## Notes

This project is intended as a development prototype for plant disease diagnosis and requires manual validation before any production use.
