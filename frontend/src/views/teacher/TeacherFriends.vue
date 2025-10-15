<script setup lang="ts">
import { computed } from 'vue'
import FriendManager from '../../components/FriendManager.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 计算属性
const userInfo = computed(() => authStore.userInfo || {})
</script>

<template>
  <div class="teacher-friends-page">
    <!-- 页面标题 -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">好友管理</h1>
      <p class="text-gray-600">
        管理您的好友列表，添加新的好友联系
      </p>
    </div>

    <!-- 好友管理组件 -->
    <FriendManager />
  </div>
</template>

<style scoped>
.teacher-friends-page {
  min-height: 100vh;
  background: #f9fafb;
  padding: 2rem 0;
}
</style>