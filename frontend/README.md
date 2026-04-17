# Frontend Development

Frontend for Plant Disease Identifier built with Vue.js 3.

## Setup

```bash
cd frontend
npm install
```

## Development

```bash
npm run dev
```

Runs at http://localhost:5173

## Build

```bash
npm run build
```

## Deploy (GitHub Pages)

GitHub Pages can host only the frontend static files. The FastAPI backend must be hosted separately (for example Render, Railway, Fly.io, or a VPS).

1. Set your backend API URL in an environment variable before building:

```bash
VITE_API_BASE=https://your-backend-domain/api/v1
```

2. Build and deploy frontend:

```bash
npm run build
```

3. Publish the generated `dist/` folder to GitHub Pages.

Important: configure backend CORS to allow your GitHub Pages domain.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.vue
│   │   └── Footer.vue
│   ├── pages/
│   │   ├── Home.vue
│   │   ├── DiagnosisPage.vue
│   │   ├── Results.vue
│   │   └── History.vue
│   ├── services/
│   │   └── api.js
│   ├── App.vue
│   └── main.js
├── public/
├── index.html
├── package.json
└── vite.config.js
```

## Features

- Image upload for disease diagnosis
- Text-based symptom description
- Multilingual support (22+ languages)
- Results with treatment recommendations
- Feedback submission
- Diagnosis history
- Local audio output
