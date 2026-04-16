<template>
  <div class="history-container">
    <div class="history-card">
      <h2>Diagnosis History</h2>
      <p class="subtitle">View your past diagnoses and feedback</p>

      <div v-if="diagnoses.length > 0" class="history-list">
        <div v-for="diagnosis in diagnoses" :key="diagnosis.id" class="history-item">
          <div class="history-header">
            <h4>{{ diagnosis.disease_name }}</h4>
            <span :class="['severity-badge', diagnosis.severity_level]">
              {{ diagnosis.severity_level }}
            </span>
          </div>
          <p class="date">{{ formatDate(diagnosis.created_at) }}</p>
          <p class="language">Language: {{ getLanguageName(diagnosis.target_language) }}</p>
          <p class="confidence">Confidence: {{ (diagnosis.confidence_score * 100).toFixed(1) }}%</p>
          <div class="history-actions">
            <RouterLink :to="`/results/${diagnosis.id}`" class="link">View Details →</RouterLink>
          </div>
        </div>
      </div>

      <div v-else class="no-history">
        <p>No diagnoses yet. Start by creating a new diagnosis!</p>
        <RouterLink to="/diagnose" class="btn btn-primary">+ New Diagnosis</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

const diagnoses = ref([
  {
    id: '1',
    disease_name: 'Brown Spot',
    severity_level: 'medium',
    created_at: new Date().toISOString(),
    target_language: 'en',
    confidence_score: 0.92,
  },
  {
    id: '2',
    disease_name: 'Leaf Blight',
    severity_level: 'high',
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    target_language: 'hi',
    confidence_score: 0.88,
  },
])

const languages = {
  en: 'English',
  hi: 'Hindi',
  ta: 'Tamil',
  te: 'Telugu',
  ka: 'Kannada',
  ml: 'Malayalam',
  mr: 'Marathi',
  gu: 'Gujarati',
  bn: 'Bengali',
}

onMounted(() => {
  // In a real app, fetch diagnosis history from API
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

const getLanguageName = (code) => {
  return languages[code] || code
}
</script>

<style scoped>
.history-container {
  max-width: 900px;
  margin: 0 auto;
}

.history-card {
  background: white;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.history-card h2 {
  color: #667eea;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  margin-bottom: 30px;
  font-size: 16px;
}

.history-list {
  display: grid;
  gap: 15px;
}

.history-item {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  border-left: 4px solid #667eea;
  transition: all 0.3s;
}

.history-item:hover {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.history-header h4 {
  color: #667eea;
  margin: 0;
}

.severity-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.severity-badge.high {
  background: #fdd;
  color: #c33;
}

.severity-badge.medium {
  background: #ffd;
  color: #993;
}

.severity-badge.low {
  background: #dfd;
  color: #393;
}

.date, .language, .confidence {
  color: #666;
  font-size: 14px;
  margin: 5px 0;
}

.history-actions {
  margin-top: 15px;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;
}

.link:hover {
  color: #764ba2;
}

.no-history {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.btn {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 30px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover {
  background: #764ba2;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .history-card {
    padding: 20px;
  }
}
</style>
