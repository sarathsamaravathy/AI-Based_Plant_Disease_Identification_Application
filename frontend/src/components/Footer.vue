<template>
  <footer class="footer">
    <div class="footer-content">
      <p>&copy; 2026 Vector Visionaries. {{ t('footer.line1') }}</p>
      <p>{{ t('footer.line2') }}</p>
    </div>
  </footer>
</template>

<script setup>
import { useI18n } from '../i18n/useI18n'

const { t } = useI18n()
</script>

<style scoped>
.footer {
  background: #333;
  color: white;
  text-align: center;
  padding: 20px;
  font-size: 14px;
  margin-top: auto;
}

.footer-content p {
  margin: 5px 0;
}
</style>
