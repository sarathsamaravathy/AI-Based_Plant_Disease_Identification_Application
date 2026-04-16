<template>
  <div class="results-container">
    <div class="results-card">
      <h2>Diagnosis Results</h2>
      
      <div v-if="diagnosis" class="diagnosis-results">
        <!-- Disease Info -->
        <div class="disease-info">
          <div class="disease-header">
            <h3>{{ diagnosis.disease_name }}</h3>
            <span :class="['severity-badge', diagnosis.severity_level]">
              {{ diagnosis.severity_level.toUpperCase() }}
            </span>
          </div>
          <div class="confidence">
            <span>Confidence: {{ (diagnosis.confidence_score * 100).toFixed(1) }}%</span>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: (diagnosis.confidence_score * 100) + '%' }"></div>
            </div>
          </div>
        </div>

        <!-- Symptoms -->
        <div v-if="diagnosis.symptoms" class="section">
          <h4>🔍 Symptoms Detected</h4>
          <ul class="symptom-list">
            <li v-for="(symptom, idx) in diagnosis.symptoms" :key="idx">{{ symptom }}</li>
          </ul>
        </div>

        <!-- Treatment Recommendations -->
        <div class="section">
          <h4>💊 Treatment Recommendations</h4>
          <ol class="recommendation-list">
            <li v-for="(rec, idx) in diagnosis.treatment_recommendations" :key="idx">
              {{ rec }}
            </li>
          </ol>
        </div>

        <!-- Preventive Measures -->
        <div class="section">
          <h4>🛡️ Preventive Measures</h4>
          <ul class="prevention-list">
            <li v-for="(prev, idx) in diagnosis.preventive_measures" :key="idx">
              {{ prev }}
            </li>
          </ul>
        </div>

        <!-- Farmer Explanation -->
        <div class="explanation">
          <h4>📖 Farmer-Friendly Explanation</h4>
          <p>{{ diagnosis.farmer_friendly_explanation }}</p>
        </div>

        <!-- Audio -->
        <div v-if="diagnosis.audio_available" class="audio-section">
          <h4>🔊 Audio Output</h4>
          <button @click="playAudio" class="btn-audio">▶️ Play Audio</button>
        </div>

        <!-- Feedback Form -->
        <div class="feedback-section">
          <h4>📝 Was this diagnosis helpful?</h4>
          <div class="feedback-form">
            <div class="feedback-group">
              <label>
                <input type="radio" v-model="feedback.diagnosis_correct" :value="true" />
                Diagnosis is correct
              </label>
              <label>
                <input type="radio" v-model="feedback.diagnosis_correct" :value="false" />
                Diagnosis is incorrect
              </label>
            </div>

            <div class="feedback-group">
              <label>
                <input type="radio" v-model="feedback.recommendation_helpful" :value="true" />
                Recommendations helpful
              </label>
              <label>
                <input type="radio" v-model="feedback.recommendation_helpful" :value="false" />
                Recommendations not helpful
              </label>
            </div>

            <div class="form-group">
              <label>Additional Notes:</label>
              <textarea v-model="feedback.user_notes" placeholder="Any additional feedback..." rows="3"></textarea>
            </div>

            <button @click="submitFeedback" :disabled="feedbackLoading" class="btn btn-primary">
              {{ feedbackLoading ? '⏳ Submitting...' : '✓ Submit Feedback' }}
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="actions">
          <RouterLink to="/diagnose" class="btn btn-secondary">↶ New Diagnosis</RouterLink>
          <RouterLink to="/history" class="btn btn-secondary">📋 View History</RouterLink>
        </div>
      </div>

      <div v-else class="loading">
        ⏳ Loading results...
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { diagnosisService } from '../services/api'

const route = useRoute()
const diagnosis = ref(route.query)
const feedbackLoading = ref(false)
const feedback = ref({
  diagnosis_correct: null,
  recommendation_helpful: null,
  user_notes: '',
})

onMounted(() => {
  // Load diagnosis data if needed
  // In a real app, you'd fetch this from the API using the diagnosis ID
})

const playAudio = () => {
  alert('Audio playback would be implemented here')
}

const submitFeedback = async () => {
  feedbackLoading.value = true
  try {
    await diagnosisService.submitFeedback(route.params.id, feedback.value)
    alert('✓ Feedback submitted successfully!')
    feedback.value = {
      diagnosis_correct: null,
      recommendation_helpful: null,
      user_notes: '',
    }
  } catch (err) {
    alert('Error submitting feedback: ' + err.message)
  } finally {
    feedbackLoading.value = false
  }
}
</script>

<style scoped>
.results-container {
  max-width: 900px;
  margin: 0 auto;
}

.results-card {
  background: white;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #667eea;
}

.disease-info {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border-left: 4px solid #667eea;
}

.disease-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.disease-header h3 {
  color: #667eea;
  font-size: 28px;
}

.severity-badge {
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 14px;
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

.confidence {
  margin-top: 15px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #ddd;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 8px;
}

.progress-fill {
  height: 100%;
  background: #667eea;
  transition: width 0.3s;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.section h4 {
  color: #667eea;
  margin-bottom: 15px;
  font-size: 18px;
}

.symptom-list, .prevention-list {
  margin-left: 20px;
}

.symptom-list li, .prevention-list li {
  margin-bottom: 10px;
  color: #333;
}

.recommendation-list {
  margin-left: 20px;
}

.recommendation-list li {
  margin-bottom: 12px;
  color: #333;
  line-height: 1.6;
}

.explanation {
  background: #ede9fe;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border-left: 4px solid #764ba2;
}

.explanation h4 {
  color: #667eea;
  margin-bottom: 15px;
}

.explanation p {
  color: #333;
  line-height: 1.6;
}

.audio-section {
  background: #f0f7ff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.audio-section h4 {
  color: #667eea;
  margin-bottom: 15px;
}

.btn-audio {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-audio:hover {
  background: #764ba2;
}

.feedback-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  border-left: 4px solid #667eea;
}

.feedback-section h4 {
  color: #667eea;
  margin-bottom: 15px;
}

.feedback-form {
  margin-top: 15px;
}

.feedback-group {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.feedback-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn {
  flex: 1;
  padding: 12px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  text-decoration: none;
  text-align: center;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #764ba2;
}

.btn-secondary {
  background: #f8f9fa;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

@media (max-width: 768px) {
  .results-card {
    padding: 20px;
  }

  .disease-header {
    flex-direction: column;
    align-items: flex-start;
  }

  .actions {
    flex-direction: column;
  }
}
</style>
