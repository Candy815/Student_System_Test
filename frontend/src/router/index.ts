import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 角色选择页面（首页）
    {
      path: '/',
      name: 'roleSelect',
      component: () => import('../views/RoleSelect.vue')
    },
    // 登录页面
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue')
    },
        {
      path: '/login/student',
      name: 'studentLogin',
      component: () => import('../views/student/StudentLogin.vue')
    },
    {
      path: '/login/teacher',
      name: 'teacherLogin',
      component: () => import('../views/teacher/TeacherLogin.vue')
    },
    {
      path: '/login/admin',
      name: 'adminLogin',
      component: () => import('../views/admin/AdminLoginSimple.vue')
    },
        // 仪表板页面
    {
      path: '/dashboard',
      redirect: '/'
    },
      // 学生仪表板和子页面
    {
      path: '/dashboard/student',
      component: () => import('../components/Layout.vue'),
      meta: { requiresAuth: true, role: 'student' },
      children: [
        {
          path: '',
          name: 'studentDashboard',
          component: () => import('../views/student/StudentDashboard.vue')
        },
        {
          path: 'schedule',
          name: 'studentSchedule',
          component: () => import('../views/student/StudentSchedule.vue')
        },
        {
          path: 'grades',
          name: 'studentGrades',
          component: () => import('../views/StudentGrades.vue')
        },
        {
          path: 'courses',
          name: 'studentCourses',
          component: () => import('../views/StudentCourses.vue')
        },
        {
          path: 'exams',
          name: 'studentExams',
          component: () => import('../views/StudentExams.vue')
        },
        {
          path: 'ai-assistant',
          name: 'studentAIAssistant',
          component: () => import('../views/student/StudentAIAssistant.vue')
        },
        {
          path: 'profile',
          name: 'studentProfile',
          component: () => import('../views/StudentProfile.vue')
        }
      ]
    },
    // 教师仪表板和子页面
    {
      path: '/dashboard/teacher',
      component: () => import('../components/Layout.vue'),
      meta: { requiresAuth: true, role: 'teacher' },
      children: [
        {
          path: '',
          name: 'teacherDashboard',
          component: () => import('../views/teacher/TeacherDashboard.vue')
        },
        {
          path: 'courses',
          name: 'teacherCourses',
          component: () => import('../views/TeacherCourses.vue')
        },
        {
          path: 'grades',
          name: 'teacherGrades',
          component: () => import('../views/TeacherGrades.vue')
        },
        {
          path: 'students',
          name: 'teacherStudents',
          component: () => import('../views/TeacherStudents.vue')
        },
        {
          path: 'attendance',
          name: 'teacherAttendance',
          component: () => import('../views/TeacherAttendance.vue')
        },
        {
          path: 'friends',
          name: 'teacherFriends',
          component: () => import('../views/teacher/TeacherFriends.vue')
        },
        {
          path: 'profile',
          name: 'teacherProfile',
          component: () => import('../views/TeacherProfile.vue')
        }
      ]
    },
    // 管理员仪表板和子页面
    {
      path: '/dashboard/admin',
      component: () => import('../components/Layout.vue'),
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: '',
          name: 'adminDashboard',
          component: () => import('../views/admin/AdminDashboard.vue')
        },
        {
          path: 'users',
          name: 'adminUsers',
          component: () => import('../views/admin/AdminUsers.vue')
        },
        {
          path: 'roles',
          name: 'adminRoles',
          component: () => import('../views/admin/AdminRoles.vue')
        },
        {
          path: 'settings',
          name: 'adminSettings',
          component: () => import('../views/admin/AdminSettings.vue')
        },
        {
          path: 'analytics',
          name: 'adminAnalytics',
          component: () => import('../views/admin/AdminAnalytics.vue')
        },
        {
          path: 'logs',
          name: 'adminLogs',
          component: () => import('../views/admin/AdminLogs.vue')
        },
        {
          path: 'courses',
          name: 'adminCourses',
          component: () => import('../views/admin/AdminCourses.vue')
        }
      ]
    },
    // 404页面
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('../views/NotFound.vue')
    }
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userRole = localStorage.getItem('userRole')
  const requiresAuth = to.meta.requiresAuth as boolean
  const requiredRole = to.meta.role as string

  // 如果是404页面，直接通过
  if (to.name === 'NotFound') {
    next()
    return
  }

  // 如果页面需要认证
  if (requiresAuth) {
    if (!userRole) {
      // 未登录，重定向到首页
      next('/')
      return
    }

    if (requiredRole && userRole !== requiredRole) {
      // 角色不匹配，重定向到首页
      next('/')
      return
    }
  }

  // 如果已登录用户访问登录页面，重定向到对应的仪表板
  if (userRole && (to.path === '/' || to.path.startsWith('/login'))) {
    const dashboardPath = `/dashboard/${userRole}`
    if (to.path !== dashboardPath) {
      next(dashboardPath)
      return
    }
  }

  next()
})

export default router
