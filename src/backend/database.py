import sqlite3
from typing import List, Tuple
import os

# プロジェクトのルートディレクトリを取得
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIR, 'soccer_stats.db')

def execute_sql(sql: str) -> Tuple[List[str], List[tuple]]:
    """SQLを実行して結果を返す"""
    conn = sqlite3.connect(DB_PATH)  # 絶対パスを使用
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        return columns, results
    finally:
        conn.close()