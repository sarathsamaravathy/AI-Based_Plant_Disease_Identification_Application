<template>
  <div class="home-container">
    <div class="hero">
      <h2>{{ t('home.heroTitle') }}</h2>
      <p>{{ t('home.heroSubtitle') }}</p>
      <div class="cta-buttons">
        <RouterLink to="/diagnose" class="btn btn-primary">{{ t('home.startDiagnosis') }}</RouterLink>
        <a href="#features" class="btn btn-secondary">{{ t('home.learnMore') }}</a>
      </div>
    </div>

    <section id="features" class="features">
      <h3>{{ t('home.keyFeatures') }}</h3>
      <div class="feature-grid">
        <div class="feature-card">
          <div class="feature-icon">📸</div>
          <h4>{{ t('home.imageAnalysisTitle') }}</h4>
          <p>{{ t('home.imageAnalysisDesc') }}</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">🌍</div>
          <h4>{{ t('home.multilingualTitle') }}</h4>
          <p>{{ t('home.multilingualDesc') }}</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">💡</div>
          <h4>{{ t('home.recommendationTitle') }}</h4>
          <p>{{ t('home.recommendationDesc') }}</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">📱</div>
          <h4>{{ t('home.mobileTitle') }}</h4>
          <p>{{ t('home.mobileDesc') }}</p>
        </div>
      </div>
    </section>

    <section class="supported-diseases">
      <h3>{{ t('home.supportedDiseases') }}</h3>
      <p>{{ t('home.supportedDiseasesDesc') }}</p>
      <div class="disease-tags">
        <span class="tag">Brown Spot</span>
        <span class="tag">Leaf Blight</span>
        <span class="tag">Powdery Mildew</span>
        <span class="tag">Early Blight</span>
        <span class="tag">Late Blight</span>
        <span class="tag">Septoria Leaf Spot</span>
        <span class="tag">{{ t('home.andMore') }}</span>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useI18n } from '../i18n/useI18n'

const { t } = useI18n()
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.hero {
  background: white;
  border-radius: 10px;
  padding: 60px 40px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
}

.hero h2 {
  font-size: 42px;
  color: #667eea;
  margin-bottom: 15px;
}

.hero p {
  font-size: 18px;
  color: #666;
  margin-bottom: 30px;
}

.cta-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.btn {
  padding: 12px 30px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
  cursor: pointer;
  border: none;
  font-size: 16px;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover {
  background: #764ba2;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: transparent;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

.features, .supported-diseases {
  background: white;
  border-radius: 10px;
  padding: 40px;
  margin-bottom: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.features h3, .supported-diseases h3 {
  font-size: 32px;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.feature-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border-left: 4px solid #667eea;
}

.feature-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.feature-card h4 {
  color: #667eea;
  margin-bottom: 10px;
}

.feature-card p {
  color: #666;
  font-size: 14px;
}

.disease-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.tag {
  background: #667eea;
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .hero {
    padding: 40px 20px;
  }

  .hero h2 {
    font-size: 28px;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .features, .supported-diseases {
    padding: 20px;
  }
}
</style>
