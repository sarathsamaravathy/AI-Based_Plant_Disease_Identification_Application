<template>
  <header class="header">
    <div class="header-container">
      <div class="logo">
        <h1>🌱 Plant Disease Identifier</h1>
        <p>Multilingual AI-Powered Diagnosis</p>
      </div>
      <nav class="nav">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/diagnose" class="nav-link">Diagnose</RouterLink>
        <RouterLink to="/history" class="nav-link">History</RouterLink>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo h1 {
  font-size: 28px;
  margin-bottom: 5px;
}

.logo p {
  font-size: 14px;
  opacity: 0.9;
}

.nav {
  display: flex;
  gap: 30px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
}

.nav-link:hover {
  opacity: 0.8;
}

.nav-link.router-link-active {
  border-bottom: 2px solid white;
  padding-bottom: 5px;
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    gap: 15px;
  }

  .nav {
    gap: 15px;
    font-size: 14px;
  }
}
</style>
