<script setup lang="ts">
import { ref, computed } from 'vue'

// 模拟学生数据
const studentInfo = ref({
  name: '张三',
  studentId: '2023001',
  className: '计算机科学2023-1班',
  avatar: '',
  email: 'zhangsan@student.edu.cn'
})

const courses = ref([
  { id: 1, name: '数据结构与算法', teacher: '李教授', time: '周一、三 8:00-9:30', room: 'A101', credits: 4 },
  { id: 2, name: '计算机网络', teacher: '王副教授', time: '周二、四 10:00-11:30', room: 'B203', credits: 3 },
  { id: 3, name: '操作系统原理', teacher: '张教授', time: '周一、五 14:00-15:30', room: 'C305', credits: 4 },
  { id: 4, name: '数据库系统', teacher: '陈副教授', time: '周三、五 10:00-11:30', room: 'D201', credits: 3 }
])

const grades = ref([
  { course: '数据结构与算法', midterm: 85, final: 88, usual: 90, total: 87.4, gpa: 3.7 },
  { course: '计算机网络', midterm: 82, final: 86, usual: 88, total: 85.2, gpa: 3.5 },
  { course: '操作系统原理', midterm: 78, final: 85, usual: 85, total: 82.6, gpa: 3.3 },
  { course: '数据库系统', midterm: 88, final: 92, usual: 95, total: 91.6, gpa: 4.0 }
])

const notices = ref([
  { id: 1, title: '关于期末考试安排的通知', date: '2024-01-10', urgent: true },
  { id: 2, title: '选课系统开放时间调整', date: '2024-01-08', urgent: false },
  { id: 3, title: '寒假放假通知', date: '2024-01-05', urgent: false }
])

const upcomingExams = ref([
  { course: '数据结构与算法', date: '2024-01-20', time: '09:00-11:00', room: 'A101' },
  { course: '计算机网络', date: '2024-01-22', time: '14:00-16:00', room: 'B203' },
  { course: '操作系统原理', date: '2024-01-25', time: '10:00-12:00', room: 'C305' }
])

// 计算统计数据
const totalCredits = computed(() => {
  return courses.value.reduce((sum, course) => sum + course.credits, 0)
})

const averageGPA = computed(() => {
  const total = grades.value.reduce((sum, grade) => sum + grade.gpa, 0)
  return (total / grades.value.length).toFixed(2)
})

const totalCourses = computed(() => courses.value.length)
</script>

<template>
    <!-- 欢迎信息 -->
    <div class="mb-8">
      <div class="bg-gradient-to-r from-blue-600 to-blue-700 rounded-2xl p-8 text-white">
        <h2 class="text-3xl font-bold mb-2">欢迎回来，{{ studentInfo.name }}！</h2>
        <p class="text-blue-100">今天是新的一天，继续加油学习吧！</p>
        <div class="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📚</div>
            <div class="text-2xl font-bold">{{ totalCourses }}</div>
            <div class="text-sm text-blue-100">本学期课程</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">🎯</div>
            <div class="text-2xl font-bold">{{ totalCredits }}</div>
            <div class="text-sm text-blue-100">总学分</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">⭐</div>
            <div class="text-2xl font-bold">{{ averageGPA }}</div>
            <div class="text-sm text-blue-100">平均GPA</div>
          </div>
          <div class="bg-white/20 rounded-lg p-4">
            <div class="text-3xl mb-1">📅</div>
            <div class="text-2xl font-bold">{{ upcomingExams.length }}</div>
            <div class="text-sm text-blue-100">待考科目</div>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- 课程表 -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📚</span>
              本学期课程
            </h3>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">课程名称</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">授课教师</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">上课时间</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">教室</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">学分</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="course in courses" :key="course.id" class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="py-3 px-4 font-medium text-gray-900">{{ course.name }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ course.teacher }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ course.time }}</td>
                    <td class="py-3 px-4 text-gray-600">{{ course.room }}</td>
                    <td class="py-3 px-4">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                        {{ course.credits }}学分
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 成绩概览 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden mt-6">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📊</span>
              成绩概览
            </h3>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-gray-200">
                    <th class="text-left py-3 px-4 text-sm font-medium text-gray-700">课程</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">期中</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">期末</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">平时</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">总评</th>
                    <th class="text-center py-3 px-4 text-sm font-medium text-gray-700">GPA</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="grade in grades" :key="grade.course" class="border-b border-gray-100 hover:bg-gray-50">
                    <td class="py-3 px-4 font-medium text-gray-900">{{ grade.course }}</td>
                    <td class="py-3 px-4 text-center text-gray-600">{{ grade.midterm }}</td>
                    <td class="py-3 px-4 text-center text-gray-600">{{ grade.final }}</td>
                    <td class="py-3 px-4 text-center text-gray-600">{{ grade.usual }}</td>
                    <td class="py-3 px-4 text-center">
                      <span class="font-semibold text-gray-900">{{ grade.total }}</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                      <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                        {{ grade.gpa }}
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
        <!-- 即将到来的考试 -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="p-6 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-900 flex items-center">
              <span class="text-2xl mr-2">📝</span>
              即将到来的考试
            </h3>
          </div>
          <div class="p-6">
            <div class="space-y-4">
              <div v-for="exam in upcomingExams" :key="exam.course" class="border-l-4 border-blue-500 pl-4 py-2">
                <div class="font-medium text-gray-900">{{ exam.course }}</div>
                <div class="text-sm text-gray-600 mt-1">
                  📅 {{ exam.date }} {{ exam.time }}
                </div>
                <div class="text-sm text-gray-600">
                  📍 {{ exam.room }}
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