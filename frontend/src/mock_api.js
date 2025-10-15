// 模拟API数据，用于测试前端界面
export const mockCourses = [
  {
    id: 1,
    name: "数据结构与算法",
    code: "CS201",
    teacher: "李老师",
    credits: 4,
    classroom: "A101",
    schedule: "周一、三 8:00-9:30",
    enrolled_students: 35,
    max_students: 50,
    is_active: true,
    created_at: "2024-01-15T10:00:00",
    teacher_id: 1,
    description: "计算机科学核心课程"
  },
  {
    id: 2,
    name: "计算机网络",
    code: "CS301",
    teacher: "李老师",
    credits: 3,
    classroom: "B203",
    schedule: "周二、四 10:00-11:30",
    enrolled_students: 28,
    max_students: 40,
    is_active: true,
    created_at: "2024-01-16T14:00:00",
    teacher_id: 1,
    description: "网络原理与应用"
  },
  {
    id: 3,
    name: "操作系统原理",
    code: "CS401",
    teacher: "李老师",
    credits: 4,
    classroom: "C305",
    schedule: "周一、五 14:00-15:30",
    enrolled_students: 32,
    max_students: 45,
    is_active: true,
    created_at: "2024-01-17T09:00:00",
    teacher_id: 1,
    description: "操作系统设计与实现"
  }
];

export const mockTeachers = [
  { id: 1, full_name: "李老师", teacher_id: "T001" },
  { id: 2, full_name: "王老师", teacher_id: "T002" },
  { id: 3, full_name: "张老师", teacher_id: "T003" }
];

// 模拟API调用
export const mockApi = {
  // 获取课程列表
  getCourses: async (page = 1, pageSize = 10) => {
    await new Promise(resolve => setTimeout(resolve, 500)); // 模拟网络延迟

    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    const courses = mockCourses.slice(startIndex, endIndex);

    return {
      courses: courses,
      total: mockCourses.length,
      page: page,
      page_size: pageSize,
      total_pages: Math.ceil(mockCourses.length / pageSize)
    };
  },

  // 更新课程
  updateCourse: async (courseId, courseData) => {
    await new Promise(resolve => setTimeout(resolve, 300));

    const courseIndex = mockCourses.findIndex(c => c.id === courseId);
    if (courseIndex !== -1) {
      mockCourses[courseIndex] = { ...mockCourses[courseIndex], ...courseData };
      return { message: "Course updated successfully" };
    }
    throw new Error("Course not found");
  },

  // 切换课程状态
  toggleCourseStatus: async (courseId) => {
    await new Promise(resolve => setTimeout(resolve, 200));

    const course = mockCourses.find(c => c.id === courseId);
    if (course) {
      course.is_active = !course.is_active;
      return { message: `Course ${course.is_active ? 'activated' : 'deactivated'} successfully` };
    }
    throw new Error("Course not found");
  },

  // 获取教师列表
  getTeachers: async () => {
    await new Promise(resolve => setTimeout(resolve, 300));
    return {
      users: mockTeachers
    };
  }
};