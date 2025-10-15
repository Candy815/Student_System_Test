<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'
import ErrorBoundary from './components/ErrorBoundary.vue'

const authStore = useAuthStore()

console.log('🚀 App.vue setup started')

onMounted(() => {
  console.log('📌 App.vue onMounted called')
  // 应用初始化时设置默认学生身份
  authStore.initializeAuth()
})
</script>

<template>
  <ErrorBoundary>
    <RouterView />
  </ErrorBoundary>
</template>

<style scoped>
</style>
