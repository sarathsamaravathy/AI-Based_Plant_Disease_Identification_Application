import { computed, ref } from 'vue'
import { LANGUAGE_OPTIONS, translations } from './translations'

const STORAGE_KEY = 'plant-disease-ui-language'
const DEFAULT_LANGUAGE = 'en'

const initialLanguage = localStorage.getItem(STORAGE_KEY) || DEFAULT_LANGUAGE
const currentLanguage = ref(initialLanguage)

document.documentElement.lang = currentLanguage.value

const getValueByPath = (obj, path) => {
  return path.split('.').reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), obj)
}

export const useI18n = () => {
  const setLanguage = (code) => {
    const supported = LANGUAGE_OPTIONS.some((lang) => lang.code === code)
    const safeCode = supported ? code : DEFAULT_LANGUAGE

    currentLanguage.value = safeCode
    localStorage.setItem(STORAGE_KEY, safeCode)
    document.documentElement.lang = safeCode
  }

  const t = (key) => {
    const langPack = translations[currentLanguage.value] || translations[DEFAULT_LANGUAGE]
    const fallback = translations[DEFAULT_LANGUAGE]

    return getValueByPath(langPack, key) || getValueByPath(fallback, key) || key
  }

  const language = computed({
    get: () => currentLanguage.value,
    set: (value) => setLanguage(value),
  })

  return {
    t,
    language,
    languageOptions: LANGUAGE_OPTIONS,
    setLanguage,
  }
}
