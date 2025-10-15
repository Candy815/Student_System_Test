#!/usr/bin/env python3

import requests
import json

# 测试课程编辑功能
def test_course_edit():
    base_url = "http://localhost:8001"

    # 测试获取课程列表
    print("1. 测试获取课程列表...")
    try:
        response = requests.get(f"{base_url}/admin/courses")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ 成功获取课程列表，共 {data['total']} 门课程")
            if data['courses']:
                course_id = data['courses'][0]['id']
                print(f"   ✓ 第一门课程ID: {course_id}")
                return course_id
            else:
                print("   ⚠ 没有课程数据")
                return None
        else:
            print(f"   ✗ 获取课程列表失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
        return None

def test_update_course(course_id):
    base_url = "http://localhost:8001"

    print(f"\n2. 测试更新课程 (ID: {course_id})...")

    # 测试数据
    update_data = {
        "name": "测试课程 - 更新",
        "credits": 4,
        "classroom": "新教室A101",
        "schedule": "周二 14:00-16:00",
        "max_students": 60
    }

    try:
        response = requests.put(
            f"{base_url}/admin/courses/{course_id}",
            json=update_data
        )

        if response.status_code == 200:
            print("   ✓ 课程更新成功")
            return True
        else:
            print(f"   ✗ 课程更新失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
        return False

def test_toggle_course_status(course_id):
    base_url = "http://localhost:8001"

    print(f"\n3. 测试切换课程状态 (ID: {course_id})...")

    try:
        response = requests.post(f"{base_url}/admin/courses/{course_id}/toggle-status")

        if response.status_code == 200:
            print("   ✓ 课程状态切换成功")
            return True
        else:
            print(f"   ✗ 课程状态切换失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ 连接失败: {e}")
        return False

if __name__ == "__main__":
    print("=== 课程编辑功能测试 ===\n")

    # 测试获取课程列表
    course_id = test_course_edit()

    if course_id:
        # 测试更新课程
        update_success = test_update_course(course_id)

        # 测试切换课程状态
        toggle_success = test_toggle_course_status(course_id)

        print(f"\n=== 测试结果 ===")
        print(f"获取课程列表: {'✓' if course_id else '✗'}")
        print(f"更新课程: {'✓' if update_success else '✗'}")
        print(f"切换课程状态: {'✓' if toggle_success else '✗'}")
    else:
        print("\n=== 测试结果 ===")
        print("无法获取课程数据，跳过其他测试")

    print("\n测试完成！")