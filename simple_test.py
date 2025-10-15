#!/usr/bin/env python3

import requests
import json

def test_api():
    base_url = "http://localhost:8001"

    print("=== 测试课程编辑功能 ===")

    # 测试获取课程列表
    try:
        response = requests.get(f"{base_url}/admin/courses")
        if response.status_code == 200:
            data = response.json()
            print(f"成功获取课程列表: {data['total']} 门课程")
            if data['courses']:
                course = data['courses'][0]
                print(f"示例课程: {course['name']} (ID: {course['id']})")
                return course['id']
        else:
            print(f"获取课程列表失败: {response.status_code}")
    except Exception as e:
        print(f"连接失败: {e}")

    return None

if __name__ == "__main__":
    course_id = test_api()
    if course_id:
        print(f"可以测试的课程ID: {course_id}")
    else:
        print("没有可测试的课程")