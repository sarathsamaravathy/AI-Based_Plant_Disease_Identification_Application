# AI-Based Plant Disease Identification Application

A multilingual AI-powered application for identifying plant diseases from leaf images or symptom descriptions. Built with Vue.js frontend and FastAPI backend, supporting 22 Indian languages.

## Features

- 🖼️ **Image-based diagnosis**: Upload leaf images for disease detection
- 📝 **Text-based reporting**: Describe symptoms in natural language
- 🌍 **Multilingual UI**: The entire interface (nav, labels, buttons, forms) switches language instantly — supports English, हिन्दी, தமிழ், తెలుగు, and 5 more Indian languages. Language preference is saved automatically.
- 🌐 **Multilingual AI output**: Diagnosis results delivered in 22 Indian languages (Hindi, Tamil, Telugu, etc.)
- 🤖 **AI-powered reasoning**: Uses self-hosted LLMs via Ollama
- 📊 **Feedback system**: Collect user feedback for model improvement
- 🐳 **Docker support**: Easy deployment with Docker Compose
- 📈 **MLOps tracking**: MLflow integration for experiment tracking

## Prerequisites

Before installing, ensure you have the following:

- **Python 3.11 or 3.12** (tested successfully on Python 3.127)
- **Node.js 18+** (for frontend development)
- **PostgreSQL** (for data storage)
- **Ollama** (for local LLM inference)
- **Git** (for cloning the repository)
- **Docker & Docker Compose** (optional, for containerized deployment)

### Windows Docker requirement (important)

If you want to run with Docker on Windows, install and start Docker Desktop first.

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Open Docker Desktop and wait until it shows Engine running.
3. In PowerShell, verify Docker server is reachable:

```bash
docker info
```

If `docker info` shows a pipe error like `dockerDesktopLinuxEngine`, Docker Desktop/WSL is not running yet.

## Installation
https://git-scm.com/install/windows (Git installation)
### Step 1: Clone the Repository

```bash
git clone https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application.git
```
```bash
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
ollama pull llama3  # or any supported model
```

3. Start Ollama service:

```bash
ollama serve
#or if its already running ->
ollama run llama3
```

### Step 4: Backend Setup

1. **Create virtual environment:**
   Install Python 3.12.7
   open a new terminal
```bash
cd AI-Based_Plant_Disease_Identification_Application
```
   ```bash
   #cd to your python 3.12 directory(eg: C:\Users\sarat\AppData\Local\Programs\Python\Python312)
   python -m venv venv
   ```

3. **Activate virtual environment:**

   - **Windows:**
     ```bash
     cd AI-Based_Plant_Disease_Identification_Application
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Upgrade packaging tools:**

   ```bash
   python -m pip install --upgrade pip setuptools wheel
   ```

5. **Install Python dependencies:**

   ```bash
   python -m pip install --prefer-binary -r requirements.txt
   ```

   > **Note:** If you encounter `ModuleNotFoundError: No module named 'pkg_resources'`, use this fallback:
   > ```bash
   > python -m pip install "setuptools<80.10.3"
   > python -m pip install --prefer-binary -r requirements.txt
   > ```

6. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your database and Ollama settings.

7. **Start the backend server:**

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

> If you still see the default Vite welcome page, make sure you are opening the diagnosis route. Use the app by clicking **Start Diagnosis** or visiting:
>
> ```bash
> http://localhost:5173/diagnose
> ```
>
> On the diagnosis page, the **Output Language** selector is available for both image and symptom-based diagnosis.

### Step 6: Alternative - Docker Setup (Optional)

If you prefer using Docker on Windows, use the following sequence:

1. Open Docker Desktop and confirm it is running.
2. From the project root, build and start the stack:

```bash
docker compose up --build
```

3. Pull the LLM model inside the Ollama container (first run only):

```bash
docker exec -it plant-disease-ollama ollama pull llama2
```

4. Open the app and API docs:

```bash
http://localhost
http://localhost:8000/docs
```

This starts backend, frontend, PostgreSQL, Ollama, and MLflow in containers.

If Docker still fails to start on Windows, check WSL:

```bash
wsl --status
wsl -l -v
```

## Usage

1. Open your browser and go to `http://localhost:5173`
2. **Select your interface language** using the dropdown in the top-right of the header — the whole UI switches instantly. Your choice is saved for future visits.
3. Upload a leaf image or describe symptoms
4. Optionally change the **Output Language** on the diagnosis page if you want AI results in a different language
5. Get AI-powered disease diagnosis with treatment suggestions

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

5. **Docker Desktop Linux engine not found:**
   - Start Docker Desktop and wait for Engine running
   - Run `docker info` and confirm a `Server` section appears
   - If needed, verify WSL: `wsl --status` and `wsl -l -v`

5. **Memory issues:**
   - Reduce batch sizes in model configurations
   - Use smaller models if available

### Getting Help

- Check the [Issues](https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application/issues) page
- Review the [Wiki](https://github.com/sarathsamaravathy/AI-Based_Plant_Disease_Identification_Application/wiki) for detailed guides

## Repository Structure

```
├── frontend/          # Vue.js application
│   └── src/i18n/      # UI translation packs (EN, HI, TA, TE + 5 fallback languages)
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

## Full Project Documentation

A comprehensive project document is available in the repository:

- `Project_Documentation.rtf` — contains explanations of backend code, frontend flow, multilingual handling, dataset assumptions, training notes, and viva-ready details.
