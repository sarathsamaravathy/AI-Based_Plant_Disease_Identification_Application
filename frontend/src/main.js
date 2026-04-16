import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// Pages
import Home from './pages/Home.vue'
import DiagnosisPage from './pages/DiagnosisPage.vue'
import Results from './pages/Results.vue'
import History from './pages/History.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/diagnose', component: DiagnosisPage },
  { path: '/results/:id', component: Results },
  { path: '/history', component: History },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App)
app.use(router)
app.mount('#app')
