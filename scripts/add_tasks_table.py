#!/usr/bin/env python3
"""
タスク管理テーブルを追加するマイグレーションスクリプト
"""

import sqlite3
import os

# データベースパスを設定
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'soccer_stats.db')

def add_tasks_table():
    """tasksテーブルを作成"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # tasksテーブルの作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                status VARCHAR(20) NOT NULL DEFAULT '未着手',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT chk_status CHECK (status IN ('未着手', '進行中', '完了'))
            )
        ''')
        
        # インデックスの作成
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_task_status ON tasks(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_task_created ON tasks(created_at)')
        
        conn.commit()
        print("✅ tasksテーブルが正常に作成されました")
        
        # 既存のテーブル確認
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 データベース内のテーブル: {[table[0] for table in tables]}")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_tasks_table()