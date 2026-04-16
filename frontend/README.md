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
