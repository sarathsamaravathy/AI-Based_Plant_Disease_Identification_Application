import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || '/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE,
  // First inference can be slower when model/LLM is warming up.
  timeout: 120000,
})

export const diagnosisService = {
  // Upload image for diagnosis
  diagnoseImage(formData) {
    return apiClient.post('/diagnose', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // Text-based diagnosis
  diagnoseText(description, language = 'en', plantType = null) {
    return apiClient.post('/diagnose/text', null, {
      params: {
        description,
        language,
        plant_type: plantType,
      },
    })
  },

  // Retranslate existing diagnosis to a new language
  retranslateDiagnosis(diagnosisType, language, diseaseNameEn = null, plantType = null) {
    return apiClient.get('/diagnose/retranslate', {
      params: {
        diagnosis_type: diagnosisType,
        language,
        ...(diseaseNameEn ? { disease_name_en: diseaseNameEn } : {}),
        ...(plantType ? { plant_type: plantType } : {}),
      },
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
