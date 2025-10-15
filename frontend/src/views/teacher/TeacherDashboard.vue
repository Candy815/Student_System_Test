<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟教师数据
const teacherInfo = ref({
  name: '李老师',
  teacherId: 'T001',
  department: '计算机科学系',
  title: '副教授',
  email: 'liteacher@university.edu.cn'
})

const courses = ref([
  { id: 1, name: '数据结构与算法', class: '计算机科学2023-1班', students: 45, time: '周一、三 8:00-9:30', room: 'A101', credits: 4 },
  { id: 2, name: '计算机网络', class: '计算机科学2022-2班', students: 38, time: '周二、四 10:00-11:30', room: 'B203', credits: 3 },
  { id: 3, name: '软件工程', class: '软件工程2023-1班', students: 42, time: '周三、五 14:00-15:30', room: 'C305', credits: 4 }
])

const recentGrades = ref([
  { student: '张三', course: '数据结构与算法', score: 85, date: '2024-01-10', status: '已录入' },
  { student: '李四', course: '数据结构与算法', score: 78, date: '2024-01-10', status: '已录入' },
  { student: '王五', course: '计算机网络', score: 92, date: '2024-01-09', status: '已录入' },
  { student: '赵六', course: '软件工程', score: 88, date: '2024-01-08', status: '待审核' }
])

const todaySchedule = ref([
  { course: '数据结构与算法', time: '08:00-09:30', room: 'A101', class: '计算机科学2023-1班' },
  { course: '计算机网络', time: '10:00-11:30', room: 'B203', class: '计算机科学2022-2班' }
])

const studentAttendance = ref([
  { student: '张三', total: 32, present: 30, absent: 2, rate: 93.8 },
  { student: '李四', total: 32, present: 31, absent: 1, rate: 96.9 },
  { student: '王五', total: 32, present: 28, absent: 4, rate: 87.5 },
  { student: '赵六', total: 32, present: 32, absent: 0, rate: 100.0 }
])

const notices = ref([
  { id: 1, title: '期末考试安排通知', date: '2024-01-10', urgent: true },
  { id: 2, title: '教师培训通知', date: '2024-01-08', urgent: false },
  { id: 3, title: '教学评估反馈', date: '2024-01-05', urgent: false }
])

// 计算统计数据
const totalStudents = computed(() => {
  return courses.value.reduce((sum, course) => sum + course.students, 0)
})

const averageAttendance = computed(() => {
  const rates = studentAttendance.value.map(s => s.rate)
  return (rates.reduce((sum, rate) => sum + rate, 0) / rates.length).toFixed(1)
})

const pendingGrades = computed(() => {
  return recentGrades.value.filter(grade => grade.status === '待审核').length
})

const todayClasses = computed(() => todaySchedule.value.length)

// 获取当前星期几
const getCurrentWeekday = () => {
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return weekdays[new Date().getDay()]
}
</script>

<template>
    <!-- 欢迎信息 -->
    <div class="mb-8">
      <div class="bg-gradient-to-r from-green-600 to-green-700 rounded-2xl p-8 text-white">
        <h2 class="text-3xl font-bold mb-2">欢迎回来，{{ teacherInfo.name }}！</h2>
        <p class="text-green-100">{{ getCurrentWeekday() }}，今天您有 {{ todayClasses }} 节课程</p>
        <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📚</div>
            <div class="text-2xl font-bold">{{ courses.length }}</div>
            <div class="text-sm text-green-100">授课课程</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">👥</div>
            <div class="text-2xl font-bold">{{ totalStudents }}</div>
            <div class="text-sm text-green-100">总学生数</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📈</div>
            <div class="text-2xl font-bold">{{ averageAttendance }}%</div>
            <div class="text-sm text-green-100">平均出勤率</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📊</div>
            <div class="text-2xl font-bold">{{ pendingGrades }}</div>
            <div class="text-sm text-green-100">待审成绩</div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 左侧主要内容 -->
      <div class="lg:col-span-2 space-y-6">
        <!-- 今日课程 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📅</span>
              今日课程安排 ({{ getCurrentWeekday() }})
            </h3>
          </div>
          <div class="p-6">
            <div v-if="todaySchedule.length === 0" class="text-center py-8 text-gray-500">
              <div class="text-4xl mb-2">🎉</div>
              <p>今天没有课程安排</p>
            </div>
            <div v-else class="space-y-4">
              <div v-for="schedule in todaySchedule" :key="schedule.course" class="bg-green-50 rounded-lg p-4 border-l-4 border-green-500">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="font-semibold text-gray-900 text-lg">{{ schedule.course }}</div>
                    <div class="text-gray-600 mt-1">
                      🕐 {{ schedule.time }} | 📍 {{ schedule.room }}
                    </div>
                    <div class="text-gray-600">
                      👥 {{ schedule.class }}
                    </div>
                  </div>
                  <div class="text-green-600">
                    <div class="text-2xl">✅</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 授课课程 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📚</span>
              本学期授课课程
            </h3>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">课程名称</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">班级</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">学生数</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">上课时间</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">教室</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">学分</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="course in courses" :key="course.id" class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="py-3 px-4 font-medium text-gray-900">{{ course.name }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ course.class }}</td>
                    <td class="py-3 px-4 text-center">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {{ course.students }}人
                      </span>
                    </td>
                    <td class="py-3 px-4 text-gray-600">{{ course.time }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ course.room }}</td>
                    <td class="py-3 px-4">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {{ course.credits }}学分
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
        <!-- 最近成绩录入 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📊</span>
              最近成绩录入
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <div v-for="grade in recentGrades" :key="grade.student" class="flex items-center justify-between py-2">
                <div class="flex-1">
                  <div class="font-medium text-gray-900">{{ grade.student }}</div>
                  <div class="text-sm text-gray-600">{{ grade.course }}</div>
                  <div class="text-xs text-gray-500">{{ grade.date }}</div>
                </div>
                <div class="text-right">
                  <div class="font-semibold text-lg" :class="grade.score >= 90 ? 'text-green-600' : grade.score >= 80 ? 'text-blue-600' : grade.score >= 70 ? 'text-yellow-600' : 'text-red-600'">
                    {{ grade.score }}
                  </div>
                  <div class="text-xs" :class="grade.status === '已录入' ? 'text-green-600' : 'text-orange-600'">
                    {{ grade.status }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 学生出勤情况 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">✅</span>
              学生出勤情况
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-3">
              <div v-for="student in studentAttendance" :key="student.student" class="flex items-center justify-between py-2">
                <div>
                  <div class="font-medium text-gray-900">{{ student.student }}</div>
                  <div class="text-sm text-gray-600">
                    出勤 {{ student.present }}/{{ student.total }}
                  </div>
                </div>
                <div class="text-right">
                  <div class="font-semibold" :class="student.rate >= 95 ? 'text-green-600' : student.rate >= 90 ? 'text-blue-600' : 'text-orange-600'">
                    {{ student.rate }}%
                  </div>
                  <div class="text-xs text-gray-500">
                    缺勤 {{ student.absent }}次
                  </div>
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