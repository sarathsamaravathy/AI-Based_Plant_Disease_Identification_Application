<template>
  <div class="diagnosis-container">
    <div class="diagnosis-card">
      <h2>{{ t('diagnosis.title') }}</h2>
      
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab"
          :class="['tab', { active: activeTab === tab }]"
          @click="activeTab = tab"
        >
          {{ tab === 'image' ? `📸 ${t('diagnosis.uploadImageTab')}` : `📝 ${t('diagnosis.describeSymptomsTab')}` }}
        </button>
      </div>

      <!-- Image Upload Tab -->
      <div v-if="activeTab === 'image'" class="tab-content">
        <div class="language-selector">
          <label>{{ t('diagnosis.outputLanguage') }}:</label>
          <select v-model="selectedLanguage">
            <option v-for="option in languageOptions" :key="option.code" :value="option.code">
              {{ option.nativeName }}
            </option>
          </select>
        </div>

        <div class="file-upload">
          <input
            type="file"
            id="file-input"
            ref="fileInput"
            accept="image/*"
            @change="onFileSelected"
            class="file-input"
          />
          <label class="upload-label" @click.prevent="fileInput.click()">
            <span v-if="!selectedFile">{{ t('diagnosis.uploadPrompt') }}</span>
            <span v-else>{{ selectedFile.name }}</span>
          </label>
        </div>

        <div v-if="imagePreview" class="image-preview">
          <img :src="imagePreview" alt="Preview" />
        </div>

        <div class="form-group">
          <label>{{ t('diagnosis.plantType') }}:</label>
          <input v-model="plantType" type="text" :placeholder="t('diagnosis.plantTypePlaceholder')" />
        </div>

        <button @click="diagnoseImage" :disabled="!selectedFile || loading" class="btn btn-primary">
          <span v-if="!loading">🔍 {{ t('diagnosis.analyzeImage') }}</span>
          <span v-else>⏳ {{ t('diagnosis.analyzing') }}</span>
        </button>
      </div>

      <!-- Text Tab -->
      <div v-if="activeTab === 'text'" class="tab-content">
        <div class="language-selector">
          <label>{{ t('diagnosis.outputLanguage') }}:</label>
          <select v-model="selectedLanguage">
            <option v-for="option in languageOptions" :key="option.code" :value="option.code">
              {{ option.nativeName }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>{{ t('diagnosis.describeSymptoms') }}:</label>
          <textarea
            v-model="symptoms"
            :placeholder="t('diagnosis.symptomsPlaceholder')"
            rows="5"
          ></textarea>
        </div>

        <div class="form-group">
          <label>{{ t('diagnosis.plantType') }}:</label>
          <input v-model="plantType" type="text" :placeholder="t('diagnosis.plantTypePlaceholder')" />
        </div>

        <button @click="diagnoseText" :disabled="!symptoms || loading" class="btn btn-primary">
          <span v-if="!loading">🔍 {{ t('diagnosis.getDiagnosis') }}</span>
          <span v-else>⏳ {{ t('diagnosis.analyzing') }}</span>
        </button>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { diagnosisService } from '../services/api'
import { useI18n } from '../i18n/useI18n'

const router = useRouter()
const { t, language, languageOptions } = useI18n()

const activeTab = ref('image')
const selectedLanguage = ref(language.value)
const fileInput = ref(null)
const selectedFile = ref(null)
const imagePreview = ref(null)
const plantType = ref('')
const symptoms = ref('')
const loading = ref(false)
const error = ref('')
const tabs = ['image', 'text']

watch(language, (newLanguage) => {
  selectedLanguage.value = newLanguage
})

watch(selectedLanguage, (newLanguage) => {
  language.value = newLanguage
})

const onFileSelected = (event) => {
  selectedFile.value = event.target.files[0]
  if (selectedFile.value) {
    const reader = new FileReader()
    reader.onload = (e) => {
      imagePreview.value = e.target.result
    }
    reader.readAsDataURL(selectedFile.value)
  }
}

const diagnoseImage = async () => {
  error.value = ''
  loading.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('language', selectedLanguage.value)
    if (plantType.value) {
      formData.append('plant_type', plantType.value)
    }

    const response = await diagnosisService.diagnoseImage(formData)
    router.push({ name: 'results', params: { id: response.data.diagnosis_id }, query: { ...response.data, diagnosis_type: 'image' } })
  } catch (err) {
    const detail = err?.response?.data?.detail
    error.value = Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : (detail || err.message || t('diagnosis.errorAnalyzingImage'))
  } finally {
    loading.value = false
  }
}

const diagnoseText = async () => {
  error.value = ''
  loading.value = true
  try {
    const response = await diagnosisService.diagnoseText(symptoms.value, selectedLanguage.value, plantType.value)
    router.push({ name: 'results', params: { id: response.data.diagnosis_id }, query: { ...response.data, diagnosis_type: 'text' } })
  } catch (err) {
    const detail = err?.response?.data?.detail
    error.value = Array.isArray(detail) ? detail.map((d) => d.msg).join(', ') : (detail || err.message || t('diagnosis.errorGettingDiagnosis'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.diagnosis-container {
  max-width: 800px;
  margin: 0 auto;
}

.diagnosis-card {
  background: white;
  border-radius: 10px;
  padding: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.diagnosis-card h2 {
  color: #667eea;
  margin-bottom: 30px;
  text-align: center;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  border-bottom: 2px solid #eee;
}

.tab {
  background: none;
  border: none;
  padding: 12px 20px;
  cursor: pointer;
  font-size: 16px;
  color: #999;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.tab.active {
  color: #667eea;
  border-bottom-color: #667eea;
}

.tab-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.language-selector {
  margin-bottom: 20px;
}

.language-selector label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.language-selector select,
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 14px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
}

.file-upload {
  position: relative;
  margin-bottom: 20px;
}

.file-input {
  display: none;
}

.upload-label {
  display: block;
  padding: 40px;
  border: 2px dashed #667eea;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  background: #f8f9fa;
}

.upload-label:hover {
  background: #ede9fe;
  border-color: #764ba2;
}

.image-preview {
  margin: 20px 0;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.btn {
  width: 100%;
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn:hover:not(:disabled) {
  background: #764ba2;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 15px;
  border-radius: 5px;
  margin-top: 20px;
  border-left: 4px solid #c33;
}

@media (max-width: 768px) {
  .diagnosis-card {
    padding: 20px;
  }

  .upload-label {
    padding: 30px 20px;
  }
}
</style>
