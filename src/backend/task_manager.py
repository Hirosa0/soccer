"""
タスク管理機能のバックエンド
"""

import sqlite3
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import os

# データベースパスの設定
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'soccer_stats.db')

class TaskManager:
    """タスク管理クラス"""
    
    VALID_STATUSES = ['未着手', '進行中', '完了']
    
    def __init__(self):
        self.db_path = DB_PATH
        self._init_tasks_table()
    
    def _init_tasks_table(self):
        """tasksテーブルの初期化"""
        conn = sqlite3.connect(self.db_path)
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
        except Exception as e:
            print(f"テーブル初期化エラー: {str(e)}")
            conn.rollback()
        finally:
            conn.close()
    
    def create_task(self, title: str, description: str = "", status: str = "未着手") -> int:
        """新しいタスクを作成"""
        if status not in self.VALID_STATUSES:
            raise ValueError(f"無効なステータス: {status}. 有効な値: {self.VALID_STATUSES}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO tasks (title, description, status, created_at, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            ''', (title, description, status))
            
            task_id = cursor.lastrowid
            conn.commit()
            return task_id
        finally:
            conn.close()
    
    def get_all_tasks(self) -> List[Dict]:
        """全てのタスクを取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT task_id, title, description, status, created_at, updated_at
                FROM tasks
                ORDER BY created_at DESC
            ''')
            
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in results]
        finally:
            conn.close()
    
    def get_tasks_by_status(self, status: str) -> List[Dict]:
        """ステータス別でタスクを取得"""
        if status not in self.VALID_STATUSES:
            raise ValueError(f"無効なステータス: {status}. 有効な値: {self.VALID_STATUSES}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT task_id, title, description, status, created_at, updated_at
                FROM tasks
                WHERE status = ?
                ORDER BY created_at DESC
            ''', (status,))
            
            columns = [description[0] for description in cursor.description]
            results = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in results]
        finally:
            conn.close()
    
    def update_task_status(self, task_id: int, new_status: str) -> bool:
        """タスクのステータスを更新"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"無効なステータス: {new_status}. 有効な値: {self.VALID_STATUSES}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE tasks 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE task_id = ?
            ''', (new_status, task_id))
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
        finally:
            conn.close()
    
    def update_task(self, task_id: int, title: str = None, description: str = None, status: str = None) -> bool:
        """タスクの情報を更新（部分更新対応）"""
        if status and status not in self.VALID_STATUSES:
            raise ValueError(f"無効なステータス: {status}. 有効な値: {self.VALID_STATUSES}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # 更新するフィールドを動的に構築
            update_fields = []
            params = []
            
            if title is not None:
                update_fields.append("title = ?")
                params.append(title)
            
            if description is not None:
                update_fields.append("description = ?")
                params.append(description)
            
            if status is not None:
                update_fields.append("status = ?")
                params.append(status)
            
            if not update_fields:
                return False  # 更新するフィールドがない
            
            update_fields.append("updated_at = CURRENT_TIMESTAMP")
            params.append(task_id)
            
            sql = f"UPDATE tasks SET {', '.join(update_fields)} WHERE task_id = ?"
            cursor.execute(sql, params)
            
            success = cursor.rowcount > 0
            conn.commit()
            return success
        finally:
            conn.close()
    
    def delete_task(self, task_id: int) -> bool:
        """タスクを削除"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM tasks WHERE task_id = ?', (task_id,))
            success = cursor.rowcount > 0
            conn.commit()
            return success
        finally:
            conn.close()
    
    def get_task_stats(self) -> Dict[str, int]:
        """タスクの統計情報を取得"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT status, COUNT(*) as count
                FROM tasks
                GROUP BY status
            ''')
            
            stats = {status: 0 for status in self.VALID_STATUSES}
            results = cursor.fetchall()
            
            for status, count in results:
                stats[status] = count
            
            stats['合計'] = sum(stats.values())
            return stats
        finally:
            conn.close()