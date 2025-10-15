import apiClient, { type ApiResponse } from './index'

// 学生信息接口
export interface StudentInfo {
  id: number
  student_id: string
  full_name: string
  email: string
  class_name: string
  enrollment_year: number
  phone?: string
  address?: string
}

// 课程信息接口
export interface CourseInfo {
  id: number
  name: string
  code: string
  teacher: string
  schedule: string
  classroom: string
  credits: number
  description?: string
  enrollment_date: string
}

// 成绩信息接口
export interface GradeInfo {
  id: number
  course: string
  course_code: string
  midterm_score?: number
  final_score?: number
  usual_score?: number
  total_score: number
  gpa: number
  semester: string
  academic_year: string
  graded_at: string
  status: string
}

// 考试信息接口
export interface ExamInfo {
  id: number
  course: string
  title: string
  exam_type: string
  date: string
  duration: number
  location: string
  max_score: number
  description?: string
}

// 仪表板数据接口
export interface StudentDashboard {
  student_info: StudentInfo
  courses: CourseInfo[]
  grades: GradeInfo[]
  upcoming_exams: ExamInfo[]
  stats: {
    total_courses: number
    total_credits: number
    average_gpa: number
  }
}

// 获取学生仪表板数据
export const getStudentDashboard = async (): Promise<StudentDashboard> => {
  const response = await apiClient.get<ApiResponse<StudentDashboard>>('/students/dashboard')
  return response.data.data
}

// 获取学生课程列表
export const getStudentCourses = async (): Promise<CourseInfo[]> => {
  const response = await apiClient.get<ApiResponse<CourseInfo[]>>('/students/courses')
  return response.data.data
}

// 获取学生成绩
export const getStudentGrades = async (semester?: string): Promise<GradeInfo[]> => {
  const params = semester ? { semester } : {}
  const response = await apiClient.get<ApiResponse<GradeInfo[]>>('/students/grades', { params })
  return response.data.data
}

// 获取学生课程表
export const getStudentSchedule = async (): Promise<any[]> => {
  const response = await apiClient.get<ApiResponse<any[]>>('/students/schedule')
  return response.data.data
}

// 获取学生考试信息
export const getStudentExams = async (): Promise<ExamInfo[]> => {
  const response = await apiClient.get<ApiResponse<ExamInfo[]>>('/students/exams')
  return response.data.data
}

// 获取学生个人信息
export const getStudentProfile = async (): Promise<StudentInfo> => {
  const response = await apiClient.get<ApiResponse<StudentInfo>>('/students/profile')
  return response.data.data
}