import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

export const diagnosisService = {
  // Upload image for diagnosis
  diagnoseImage(formData, language = 'en') {
    return apiClient.post('/diagnose', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      params: { language },
    })
  },

  // Text-based diagnosis
  diagnoseText(description, language = 'en', plantType = null) {
    return apiClient.post('/diagnose/text', {
      description,
      language,
      plant_type: plantType,
    })
  },

  // Get supported languages
  getLanguages() {
    return apiClient.get('/languages')
  },

  // Submit feedback
  submitFeedback(diagnosisId, feedback) {
    return apiClient.post('/feedback', {
      diagnosis_id: diagnosisId,
      ...feedback,
    })
  },

  // Health check
  healthCheck() {
    return apiClient.get('/health')
  },
}

export default apiClient
