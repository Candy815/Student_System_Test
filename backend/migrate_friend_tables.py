#!/usr/bin/env python3
"""
数据库迁移脚本 - 添加好友功能相关表
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base
from database import DATABASE_URL

def create_friend_tables():
    """创建好友功能相关表"""
    engine = create_engine(DATABASE_URL)

    # 创建新的表
    print("正在创建好友功能相关表...")

    # 检查表是否已存在
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('friend_requests', 'friendships')"))
        existing_tables = [row[0] for row in result.fetchall()]

        if 'friend_requests' not in existing_tables:
            print("创建 friend_requests 表...")
            conn.execute(text("""
                CREATE TABLE friend_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sender_id INTEGER NOT NULL,
                    receiver_id INTEGER NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    message TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (sender_id) REFERENCES users (id),
                    FOREIGN KEY (receiver_id) REFERENCES users (id),
                    UNIQUE(sender_id, receiver_id)
                )
            """))
            print("✅ friend_requests 表创建成功")
        else:
            print("⚠️ friend_requests 表已存在")

        if 'friendships' not in existing_tables:
            print("创建 friendships 表...")
            conn.execute(text("""
                CREATE TABLE friendships (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user1_id INTEGER NOT NULL,
                    user2_id INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active',
                    FOREIGN KEY (user1_id) REFERENCES users (id),
                    FOREIGN KEY (user2_id) REFERENCES users (id),
                    UNIQUE(user1_id, user2_id)
                )
            """))
            print("✅ friendships 表创建成功")
        else:
            print("⚠️ friendships 表已存在")

        # 插入一些测试数据
        print("正在插入测试数据...")
        conn.execute(text("""
            INSERT OR IGNORE INTO friend_requests (sender_id, receiver_id, status, message)
            VALUES (2, 1, 'pending', '您好，希望与您成为好友，方便交流教学经验')
        """))

        conn.commit()
        print("✅ 测试数据插入完成")

if __name__ == "__main__":
    try:
        create_friend_tables()
        print("\n🎉 数据库迁移完成！")
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        sys.exit(1)