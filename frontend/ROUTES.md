# 路由连接说明

## 🎯 项目路由结构

### 公共路由
- `/` - 角色选择页面 (RoleSelect.vue)
- `/login` - 重定向到首页
- `/login/student` - 学生登录页面
- `/login/teacher` - 教师登录页面
- `/login/admin` - 管理员登录页面

### 学生路由 (需要 student 角色)
- `/dashboard/student` - 学生仪表板
- `/dashboard/student/schedule` - 个人课表
- `/dashboard/student/grades` - 成绩查询
- `/dashboard/student/courses` - 选课系统
- `/dashboard/student/exams` - 考试安排
- `/dashboard/student/profile` - 个人信息

### 教师路由 (需要 teacher 角色)
- `/dashboard/teacher` - 教师仪表板
- `/dashboard/teacher/courses` - 课程管理
- `/dashboard/teacher/grades` - 成绩录入
- `/dashboard/teacher/students` - 学生名单
- `/dashboard/teacher/attendance` - 考勤管理
- `/dashboard/teacher/profile` - 个人中心

### 管理员路由 (需要 admin 角色)
- `/dashboard/admin` - 管理员仪表板

### 其他路由
- `/:pathMatch(.*)*` - 404页面 (NotFound.vue)

## 🔐 路由守卫

1. **认证检查**: 需要认证的页面会检查用户是否已登录
2. **角色权限**: 检查用户角色是否匹配页面要求
3. **自动重定向**:
   - 未登录用户访问受保护页面会重定向到首页
   - 已登录用户访问登录页面会重定向到对应仪表板
   - 角色不匹配会重定向到首页

## 📝 测试方法

### 1. 首页测试
- 访问: http://localhost:5173/
- 应显示角色选择页面

### 2. 登录测试
- 学生登录: 2023001 / student123
- 教师登录: T001 / teacher123
- 管理员登录: admin / admin123

### 3. 路由跳转测试
登录后可以测试以下路由跳转：

**学生路由:**
- http://localhost:5173/dashboard/student/schedule
- http://localhost:5173/dashboard/student/grades
- http://localhost:5173/dashboard/student/courses
- http://localhost:5173/dashboard/student/exams
- http://localhost:5173/dashboard/student/profile

**教师路由:**
- http://localhost:5173/dashboard/teacher/courses
- http://localhost:5173/dashboard/teacher/grades
- http://localhost:5173/dashboard/teacher/students
- http://localhost:5173/dashboard/teacher/attendance
- http://localhost:5173/dashboard/teacher/profile

### 4. 权限测试
- 未登录时直接访问受保护页面应重定向到首页
- 学生角色访问教师或管理员路由应重定向到首页
- 教师角色访问学生或管理员路由应重定向到首页

### 5. 404测试
- 访问不存在的路由: http://localhost:5173/unknown-page
- 应显示404页面

## 🎨 组件连接状态

### ✅ 已连接的组件
- ✅ RoleSelect.vue ↔ `/`
- ✅ StudentLogin.vue ↔ `/login/student`
- ✅ TeacherLogin.vue ↔ `/login/teacher`
- ✅ AdminLogin.vue ↔ `/login/admin`
- ✅ StudentDashboard.vue ↔ `/dashboard/student`
- ✅ TeacherDashboard.vue ↔ `/dashboard/teacher`
- ✅ AdminDashboard.vue ↔ `/dashboard/admin`
- ✅ StudentSchedule.vue ↔ `/dashboard/student/schedule`
- ✅ StudentGrades.vue ↔ `/dashboard/student/grades`
- ✅ StudentCourses.vue ↔ `/dashboard/student/courses`
- ✅ StudentExams.vue ↔ `/dashboard/student/exams`
- ✅ StudentProfile.vue ↔ `/dashboard/student/profile`
- ✅ TeacherCourses.vue ↔ `/dashboard/teacher/courses`
- ✅ TeacherGrades.vue ↔ `/dashboard/teacher/grades`
- ✅ TeacherStudents.vue ↔ `/dashboard/teacher/students`
- ✅ TeacherAttendance.vue ↔ `/dashboard/teacher/attendance`
- ✅ TeacherProfile.vue ↔ `/dashboard/teacher/profile`
- ✅ NotFound.vue ↔ `/:pathMatch(.*)*`

### 🎯 布局组件
- 所有Dashboard和子页面都使用 Layout.vue 组件
- 登录页面使用独立布局

所有路由都已正确连接到对应的Vue组件，系统可以正常运行！