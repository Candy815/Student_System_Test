import { createPinia } from 'pinia'
import { useAuthStore } from '../stores/auth'

export const setupAuth = (app: any) => {
  const pinia = createPinia()
  app.use(pinia)

  // 初始化auth store
  const authStore = useAuthStore()
  authStore.initializeAuth()

  console.log('🔐 Auth plugin initialized')
}

// 为TypeScript准备的类型声明
declare module '@vue/runtime-core' {
  interface ComponentCustomProperties {
    $auth: typeof useAuthStore
  }
}