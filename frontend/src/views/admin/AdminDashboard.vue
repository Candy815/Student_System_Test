<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟系统统计数据
const systemStats = ref({
  totalUsers: 2156,
  activeUsers: 1823,
  totalStudents: 1956,
  totalTeachers: 156,
  totalCourses: 89,
  totalDepartments: 12
})

const recentActivities = ref([
  { id: 1, user: '张三', action: '登录系统', time: '2024-01-10 14:30', role: '学生', status: 'success' },
  { id: 2, user: '李老师', action: '录入成绩', time: '2024-01-10 13:45', role: '教师', status: 'success' },
  { id: 3, user: '系统', action: '数据备份', time: '2024-01-10 12:00', role: '系统', status: 'success' },
  { id: 4, user: '王五', action: '修改密码失败', time: '2024-01-10 11:30', role: '学生', status: 'error' },
  { id: 5, user: '管理员', action: '更新用户权限', time: '2024-01-10 10:15', role: '管理员', status: 'success' }
])

const userGrowthData = ref([
  { month: '2023-07', students: 1800, teachers: 140 },
  { month: '2023-08', students: 1820, teachers: 142 },
  { month: '2023-09', students: 1850, teachers: 145 },
  { month: '2023-10', students: 1880, teachers: 148 },
  { month: '2023-11', students: 1910, teachers: 150 },
  { month: '2023-12', students: 1956, teachers: 156 }
])

const systemStatus = ref([
  { service: '用户服务', status: '正常', uptime: '99.9%', response: '12ms' },
  { service: '数据库服务', status: '正常', uptime: '99.8%', response: '8ms' },
  { service: '文件服务', status: '正常', uptime: '99.7%', response: '45ms' },
  { service: '邮件服务', status: '警告', uptime: '98.5%', response: '120ms' },
  { service: '缓存服务', status: '正常', uptime: '99.9%', response: '2ms' }
])

const securityAlerts = ref([
  { id: 1, type: 'high', title: '检测到异常登录尝试', count: 5, time: '最近1小时' },
  { id: 2, type: 'medium', title: '用户密码重置异常', count: 3, time: '最近24小时' },
  { id: 3, type: 'low', title: '系统性能警告', count: 1, time: '最近12小时' }
])

const notices = ref([
  { id: 1, title: '系统维护通知：本周六凌晨2-4点', date: '2024-01-10', urgent: true },
  { id: 2, title: '新功能发布：成绩分析模块', date: '2024-01-08', urgent: false },
  { id: 3, title: '安全更新提醒', date: '2024-01-05', urgent: false }
])

// 计算统计数据
const activeRate = computed(() => {
  return ((systemStats.value.activeUsers / systemStats.value.totalUsers) * 100).toFixed(1)
})

const recentNewStudents = computed(() => {
  const lastMonth = userGrowthData.value[userGrowthData.value.length - 1]
  const prevMonth = userGrowthData.value[userGrowthData.value.length - 2]
  return lastMonth.students - prevMonth.students
})

const recentNewTeachers = computed(() => {
  const lastMonth = userGrowthData.value[userGrowthData.value.length - 1]
  const prevMonth = userGrowthData.value[userGrowthData.value.length - 2]
  return lastMonth.teachers - prevMonth.teachers
})

const criticalAlerts = computed(() => {
  return securityAlerts.value.filter(alert => alert.type === 'high').length
})

const normalServices = computed(() => {
  return systemStatus.value.filter(service => service.status === '正常').length
})
</script>

<template>
    <!-- 欢迎信息 -->
    <div class="mb-8">
      <div class="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl p-8 text-white">
        <h2 class="text-3xl font-bold mb-2">管理员控制台</h2>
        <p class="text-purple-100">系统运行正常，当前在线用户 {{ systemStats.activeUsers }} 人</p>
        <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">👥</div>
            <div class="text-2xl font-bold">{{ systemStats.totalUsers }}</div>
            <div class="text-sm text-purple-100">总用户数</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📈</div>
            <div class="text-2xl font-bold">{{ activeRate }}%</div>
            <div class="text-sm text-purple-100">活跃率</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📚</div>
            <div class="text-2xl font-bold">{{ systemStats.totalCourses }}</div>
            <div class="text-sm text-purple-100">课程数量</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">⚠️</div>
            <div class="text-2xl font-bold">{{ criticalAlerts }}</div>
            <div class="text-sm text-purple-100">安全警告</div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧主要内容 -->
      <div class="lg:col-span-2 space-y-6">
        <!-- 系统状态 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">🖥️</span>
              系统服务状态
            </h3>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-for="service in systemStatus" :key="service.service" class="border rounded-lg p-4"
                   :class="service.status === '正常' ? 'border-green-200 bg-green-50' : 'border-yellow-200 bg-yellow-50'">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-medium text-gray-900">{{ service.service }}</div>
                    <div class="text-sm text-gray-600 mt-1">
                      响应时间: {{ service.response }}
                    </div>
                  </div>
                  <div class="flex items-center">
                    <div class="w-3 h-3 rounded-full mr-2"
                         :class="service.status === '正常' ? 'bg-green-500' : 'bg-yellow-500'"></div>
                    <span class="text-sm font-medium"
                          :class="service.status === '正常' ? 'text-green-600' : 'text-yellow-600'">
                      {{ service.status }}
                    </span>
                  </div>
                </div>
                <div class="mt-2 text-xs text-gray-500">
                  正常运行时间: {{ service.uptime }}
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 用户增长趋势 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📊</span>
              用户增长趋势
            </h3>
          </div>
          <div class="p-6">
            <div class="mb-4">
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-blue-50 rounded-lg p-4">
                  <div class="text-sm text-blue-600">本月新增学生</div>
                  <div class="text-2xl font-bold text-blue-700">+{{ recentNewStudents }}</div>
                </div>
                <div class="bg-green-50 rounded-lg p-4">
                  <div class="text-sm text-green-600">本月新增教师</div>
                  <div class="text-2xl font-bold text-green-700">+{{ recentNewTeachers }}</div>
                </div>
              </div>
            </div>

            <!-- 简化的图表展示 -->
            <div class="space-y-3">
              <div v-for="data in userGrowthData" :key="data.month" class="flex items-center">
                <div class="w-24 text-sm text-gray-600">{{ data.month }}</div>
                <div class="flex-1">
                  <div class="flex items-center">
                    <div class="flex-1 bg-gray-200 rounded-full h-6 mr-2">
                      <div class="bg-blue-500 h-6 rounded-full flex items-center justify-center text-xs text-white"
                           :style="`width: ${(data.students / 2000) * 100}%`">
                        {{ data.students }}
                      </div>
                    </div>
                    <div class="bg-gray-200 rounded-full h-6 w-20">
                      <div class="bg-green-500 h-6 rounded-full flex items-center justify-center text-xs text-white"
                           :style="`width: ${(data.teachers / 200) * 100}%`">
                        {{ data.teachers }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-4 flex items-center space-x-4 text-sm">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
                <span class="text-gray-600">学生</span>
              </div>
              <div class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                <span class="text-gray-600">教师</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 最近活动 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📝</span>
              系统活动日志
            </h3>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">用户</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">操作</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">角色</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">时间</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">状态</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="activity in recentActivities" :key="activity.id" class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="py-3 px-4 font-medium text-gray-900">{{ activity.user }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ activity.action }}</td>
                    <td class="py-3 px-4">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                        {{ activity.role }}
                      </span>
                    </td>
                    <td class="py-3 px-4 text-gray-600">{{ activity.time }}</td>
                    <td class="py-3 px-4">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                            :class="activity.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                        {{ activity.status === 'success' ? '成功' : '失败' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧信息栏 -->
      <div class="space-y-6">
        <!-- 安全警告 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">🚨</span>
              安全警告
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="alert in securityAlerts" :key="alert.id"
                   class="border-l-4 p-4 rounded-lg"
                   :class="alert.type === 'high' ? 'border-red-500 bg-red-50' :
                           alert.type === 'medium' ? 'border-yellow-500 bg-yellow-50' : 'border-blue-500 bg-blue-50'">
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <div class="font-medium text-gray-900">{{ alert.title }}</div>
                    <div class="text-sm text-gray-600 mt-1">
                      发生次数: {{ alert.count }} | {{ alert.time }}
                    </div>
                  </div>
                  <div class="w-2 h-2 rounded-full"
                       :class="alert.type === 'high' ? 'bg-red-500' :
                               alert.type === 'medium' ? 'bg-yellow-500' : 'bg-blue-500'"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 快速统计 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📈</span>
              用户分布
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div>
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-600">学生</span>
                  <span class="text-sm font-medium text-gray-900">{{ systemStats.totalStudents }}人</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full"
                       :style="`width: ${(systemStats.totalStudents / systemStats.totalUsers) * 100}%`"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-600">教师</span>
                  <span class="text-sm font-medium text-gray-900">{{ systemStats.totalTeachers }}人</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-green-600 h-2 rounded-full"
                       :style="`width: ${(systemStats.totalTeachers / systemStats.totalUsers) * 100}%`"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between items-center mb-1">
                  <span class="text-sm text-gray-600">管理员</span>
                  <span class="text-sm font-medium text-gray-900">
                    {{ systemStats.totalUsers - systemStats.totalStudents - systemStats.totalTeachers }}人
                  </span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-purple-600 h-2 rounded-full"
                       :style="`width: ${((systemStats.totalUsers - systemStats.totalStudents - systemStats.totalTeachers) / systemStats.totalUsers) * 100}%`"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 系统通知 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">🔔</span>
              系统通知
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="notice in notices" :key="notice.id" class="hover:bg-gray-50 p-3 rounded-lg cursor-pointer">
                <div class="flex items-start">
                  <div class="flex-1">
                    <div class="flex items-center">
                      <div v-if="notice.urgent" class="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                      <div class="font-medium text-gray-900">{{ notice.title }}</div>
                    </div>
                    <div class="text-sm text-gray-600 mt-1">{{ notice.date }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
/* 自定义样式 */
</style>