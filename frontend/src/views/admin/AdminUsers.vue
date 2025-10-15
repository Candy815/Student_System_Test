<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUpgradeRequests, approveUpgrade, rejectUpgrade } from '@/api/auth'

const upgradeRequests = ref<any[]>([])
const loading = ref(true)
const processing = ref<number | null>(null)

onMounted(async () => {
  await loadUpgradeRequests()
})

const loadUpgradeRequests = async () => {
  try {
    upgradeRequests.value = await getUpgradeRequests()
  } catch (error) {
    console.error('获取升级请求失败:', error)
  } finally {
    loading.value = false
  }
}

const handleApprove = async (requestId: number) => {
  if (!confirm('确定要批准这个升级请求吗？')) return

  processing.value = requestId
  try {
    await approveUpgrade(requestId)
    await loadUpgradeRequests()
    alert('升级请求已批准')
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.message || '未知错误'))
  } finally {
    processing.value = null
  }
}

const handleReject = async (requestId: number) => {
  const reason = prompt('请输入拒绝原因:')
  if (!reason) return

  processing.value = requestId
  try {
    await rejectUpgrade(requestId, reason)
    await loadUpgradeRequests()
    alert('升级请求已拒绝')
  } catch (error: any) {
    alert('操作失败: ' + (error.response?.data?.message || '未知错误'))
  } finally {
    processing.value = null
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'pending':
      return '待审核'
    case 'approved':
      return '已通过'
    case 'rejected':
      return '已拒绝'
    default:
      return '未知状态'
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800'
    case 'approved':
      return 'bg-green-100 text-green-800'
    case 'rejected':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}
</script>

<template>
  <div class="space-y-6">
    <!-- 升级请求管理 -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-900">📋 身份升级申请管理</h2>
        <button
          @click="loadUpgradeRequests"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors duration-200"
          :disabled="loading"
        >
          {{ loading ? '加载中...' : '刷新' }}
        </button>
      </div>

      <!-- 加载状态 -->
      <div v-if="loading" class="flex justify-center items-center h-32">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>

      <!-- 空状态 -->
      <div v-else-if="upgradeRequests.length === 0" class="text-center py-12">
        <div class="text-6xl mb-4">📝</div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">暂无升级申请</h3>
        <p class="text-gray-600">当前没有待处理的身份升级申请</p>
      </div>

      <!-- 升级请求列表 -->
      <div v-else class="space-y-4">
        <div
          v-for="request in upgradeRequests"
          :key="request.id"
          class="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <div class="flex items-center space-x-4 mb-3">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ request.user?.full_name || request.user?.username }}
                </h3>
                <span :class="['px-3 py-1 rounded-full text-sm font-medium', getStatusColor(request.status)]">
                  {{ getStatusText(request.status) }}
                </span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-600">
                <div>
                  <span class="font-medium">申请身份：</span>
                  {{ request.target_role === 'student' ? '学生' : '教师' }}
                </div>
                <div>
                  <span class="font-medium">申请时间：</span>
                  {{ new Date(request.created_at).toLocaleString() }}
                </div>
                <div v-if="request.student_id">
                  <span class="font-medium">学号：</span>
                  {{ request.student_id }}
                </div>
                <div v-if="request.teacher_id">
                  <span class="font-medium">工号：</span>
                  {{ request.teacher_id }}
                </div>
                <div v-if="request.class_name">
                  <span class="font-medium">班级：</span>
                  {{ request.class_name }}
                </div>
                <div v-if="request.department">
                  <span class="font-medium">部门：</span>
                  {{ request.department }}
                </div>
              </div>

              <div v-if="request.rejection_reason" class="mt-3 p-3 bg-red-50 border border-red-200 rounded-md">
                <p class="text-sm text-red-800">
                  <strong>拒绝原因：</strong>{{ request.rejection_reason }}
                </p>
              </div>
            </div>

            <div v-if="request.status === 'pending'" class="flex space-x-2 ml-4">
              <button
                @click="handleApprove(request.id)"
                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="processing === request.id"
              >
                {{ processing === request.id ? '处理中...' : '批准' }}
              </button>
              <button
                @click="handleReject(request.id)"
                class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="processing === request.id"
              >
                {{ processing === request.id ? '处理中...' : '拒绝' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>