<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  searchUsers,
  sendFriendRequest,
  getSentRequests,
  getReceivedRequests,
  acceptFriendRequest,
  rejectFriendRequest,
  getFriends,
  removeFriend,
  type UserSearchResponse,
  type FriendRequest,
  type Friend
} from '../api/friends'

// 响应式数据
const searchQuery = ref('')
const searchResults = ref<UserSearchResponse[]>([])
const friends = ref<Friend[]>([])
const sentRequests = ref<FriendRequest[]>([])
const receivedRequests = ref<FriendRequest[]>([])
const activeTab = ref('friends')

// 加载状态
const loading = reactive({
  search: false,
  friends: false,
  requests: false
})

// 计算属性
const hasPendingRequests = computed(() => receivedRequests.value.length > 0)

// 搜索用户
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }

  loading.search = true
  try {
    searchResults.value = await searchUsers(searchQuery.value.trim())
  } catch (error: any) {
    ElMessage.error(error.message || '搜索用户失败')
  } finally {
    loading.search = false
  }
}

// 发送好友请求
const handleSendRequest = async (user: UserSearchResponse) => {
  try {
    await sendFriendRequest({ receiver_id: user.id })
    ElMessage.success('好友请求已发送')
    searchQuery.value = ''
    searchResults.value = []
    loadSentRequests()
  } catch (error: any) {
    ElMessage.error(error.message || '发送好友请求失败')
  }
}

// 接受好友请求
const handleAcceptRequest = async (request: FriendRequest) => {
  try {
    await acceptFriendRequest(request.id)
    ElMessage.success('已接受好友请求')
    loadReceivedRequests()
    loadFriends()
  } catch (error: any) {
    ElMessage.error(error.message || '接受好友请求失败')
  }
}

// 拒绝好友请求
const handleRejectRequest = async (request: FriendRequest) => {
  try {
    await rejectFriendRequest(request.id)
    ElMessage.success('已拒绝好友请求')
    loadReceivedRequests()
  } catch (error: any) {
    ElMessage.error(error.message || '拒绝好友请求失败')
  }
}

// 删除好友
const handleRemoveFriend = async (friend: Friend) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除好友 ${friend.name} 吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await removeFriend(friend.user_id)
    ElMessage.success('好友已删除')
    loadFriends()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除好友失败')
    }
  }
}

// 加载好友列表
const loadFriends = async () => {
  loading.friends = true
  try {
    friends.value = await getFriends()
  } catch (error: any) {
    ElMessage.error(error.message || '加载好友列表失败')
  } finally {
    loading.friends = false
  }
}

// 加载发送的好友请求
const loadSentRequests = async () => {
  try {
    sentRequests.value = await getSentRequests()
  } catch (error: any) {
    console.error('加载发送的好友请求失败:', error)
  }
}

// 加载收到的好友请求
const loadReceivedRequests = async () => {
  loading.requests = true
  try {
    receivedRequests.value = await getReceivedRequests()
  } catch (error: any) {
    ElMessage.error(error.message || '加载好友请求失败')
  } finally {
    loading.requests = false
  }
}

// 获取角色图标
const getRoleIcon = (role: string) => {
  switch (role) {
    case 'student': return '👨‍🎓'
    case 'teacher': return '👨‍🏫'
    case 'admin': return '👨‍💼'
    default: return '👤'
  }
}

// 获取角色名称
const getRoleName = (role: string) => {
  switch (role) {
    case 'student': return '学生'
    case 'teacher': return '教师'
    case 'admin': return '管理员'
    default: return '用户'
  }
}

// 获取状态标签类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'accepted': return 'success'
    case 'rejected': return 'danger'
    case 'pending': return 'warning'
    default: return 'info'
  }
}

// 获取状态名称
const getStatusName = (status: string) => {
  switch (status) {
    case 'accepted': return '已接受'
    case 'rejected': return '已拒绝'
    case 'pending': return '待处理'
    default: return '未知'
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadFriends()
  loadSentRequests()
  loadReceivedRequests()
})
</script>

<template>
  <div class="friend-manager">
    <!-- 搜索区域 -->
    <div class="search-section mb-6">
      <div class="flex gap-2">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户（用户名、姓名、邮箱）"
          class="flex-1"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button :loading="loading.search" @click="handleSearch">
              🔍 搜索
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- 搜索结果 -->
      <div v-if="searchResults.length > 0" class="mt-4">
        <h3 class="text-lg font-semibold mb-3">搜索结果</h3>
        <div class="space-y-2">
          <div
            v-for="user in searchResults"
            :key="user.id"
            class="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between"
          >
            <div class="flex items-center space-x-3">
              <div class="text-2xl">{{ getRoleIcon(user.role) }}</div>
              <div>
                <div class="font-semibold">{{ user.name }}</div>
                <div class="text-sm text-gray-600">
                  {{ getRoleName(user.role) }} • {{ user.email }}
                </div>
                <div v-if="user.student_id" class="text-xs text-gray-500">
                  学号: {{ user.student_id }}
                </div>
                <div v-if="user.teacher_id" class="text-xs text-gray-500">
                  工号: {{ user.teacher_id }}
                </div>
                <div v-if="user.department" class="text-xs text-gray-500">
                  部门: {{ user.department }}
                </div>
              </div>
            </div>
            <el-button
              type="primary"
              size="small"
              @click="handleSendRequest(user)"
            >
              添加好友
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 标签页 -->
    <el-tabs v-model="activeTab" class="friend-tabs">
      <!-- 好友列表 -->
      <el-tab-pane label="我的好友" name="friends">
        <div v-if="loading.friends" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <div class="mt-2">加载中...</div>
        </div>
        <div v-else-if="friends.length === 0" class="text-center py-8 text-gray-500">
          <div class="text-4xl mb-2">👥</div>
          <p>还没有好友，快去搜索添加吧！</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="friend in friends"
            :key="friend.id"
            class="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between"
          >
            <div class="flex items-center space-x-3">
              <div class="text-2xl">{{ getRoleIcon(friend.role) }}</div>
              <div>
                <div class="font-semibold">{{ friend.name }}</div>
                <div class="text-sm text-gray-600">
                  {{ getRoleName(friend.role) }} • {{ friend.email }}
                </div>
                <div v-if="friend.student_id" class="text-xs text-gray-500">
                  学号: {{ friend.student_id }}
                  <span v-if="friend.class_name">• {{ friend.class_name }}</span>
                </div>
                <div v-if="friend.teacher_id" class="text-xs text-gray-500">
                  工号: {{ friend.teacher_id }}
                  <span v-if="friend.department">• {{ friend.department }}</span>
                  <span v-if="friend.title">• {{ friend.title }}</span>
                </div>
                <div class="text-xs text-gray-400">
                  好友于: {{ new Date(friend.friendship_since).toLocaleDateString() }}
                </div>
              </div>
            </div>
            <el-button
              type="danger"
              size="small"
              @click="handleRemoveFriend(friend)"
            >
              删除好友
            </el-button>
          </div>
        </div>
      </el-tab-pane>

      <!-- 收到的好友请求 -->
      <el-tab-pane label="好友请求" name="requests">
        <el-badge v-if="hasPendingRequests" :value="receivedRequests.length" class="ml-2">
          <span>收到的好友请求</span>
        </el-badge>
        <span v-else>收到的好友请求</span>

        <div v-if="loading.requests" class="text-center py-8">
          <div class="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <div class="mt-2">加载中...</div>
        </div>
        <div v-else-if="receivedRequests.length === 0" class="text-center py-8 text-gray-500">
          <div class="text-4xl mb-2">📭</div>
          <p>暂无待处理的好友请求</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="request in receivedRequests"
            :key="request.id"
            class="bg-white border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="text-2xl">{{ getRoleIcon(request.sender_role) }}</div>
                <div>
                  <div class="font-semibold">{{ request.sender_name }}</div>
                  <div class="text-sm text-gray-600">
                    {{ getRoleName(request.sender_role) }} • {{ new Date(request.created_at).toLocaleDateString() }}
                  </div>
                </div>
              </div>
              <el-tag :type="getStatusType(request.status)">
                {{ getStatusName(request.status) }}
              </el-tag>
            </div>

            <div v-if="request.message" class="mb-3 p-2 bg-gray-50 rounded text-sm">
              {{ request.message }}
            </div>

            <div class="flex gap-2">
              <el-button
                type="success"
                size="small"
                @click="handleAcceptRequest(request)"
              >
                接受
              </el-button>
              <el-button
                type="danger"
                size="small"
                @click="handleRejectRequest(request)"
              >
                拒绝
              </el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- 发送的好友请求 -->
      <el-tab-pane label="已发送请求" name="sent">
        <div v-if="sentRequests.length === 0" class="text-center py-8 text-gray-500">
          <div class="text-4xl mb-2">📤</div>
          <p>暂无已发送的好友请求</p>
        </div>
        <div v-else class="space-y-3">
          <div
            v-for="request in sentRequests"
            :key="request.id"
            class="bg-white border border-gray-200 rounded-lg p-4"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center space-x-3">
                <div class="text-2xl">{{ getRoleIcon(request.receiver_role) }}</div>
                <div>
                  <div class="font-semibold">{{ request.receiver_name }}</div>
                  <div class="text-sm text-gray-600">
                    {{ getRoleName(request.receiver_role) }} • {{ new Date(request.created_at).toLocaleDateString() }}
                  </div>
                </div>
              </div>
              <el-tag :type="getStatusType(request.status)">
                {{ getStatusName(request.status) }}
              </el-tag>
            </div>

            <div v-if="request.message" class="p-2 bg-gray-50 rounded text-sm">
              {{ request.message }}
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
.friend-manager {
  max-width: 800px;
  margin: 0 auto;
}

.search-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 0.5rem;
}

.friend-tabs :deep(.el-tabs__content) {
  padding-top: 1rem;
}

:deep(.el-badge__content) {
  top: -5px;
  right: -10px;
}
</style>