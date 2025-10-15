import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './styles/main.css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

console.log('🎯 main.ts started')

const app = createApp(App)
const pinia = createPinia()

console.log('📦 Setting up Pinia')
app.use(pinia)

console.log('🛣️ Setting up Router')
app.use(router)

console.log('🔐 Initializing Auth Store')
// 初始化auth store
const authStore = useAuthStore()
authStore.initializeAuth()

console.log('🚀 Mounting app')
app.mount('#app')
console.log('✅ App mounted')
