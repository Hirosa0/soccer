import sys
import os
import sqlite3
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.backend.llm import LLMClient

def execute_sql(sql: str) -> list:
    """SQLを実行して結果を返す"""
    conn = sqlite3.connect('soccer_stats.db')
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        columns = [description[0] for description in cursor.description]
        results = cursor.fetchall()
        return columns, results
    finally:
        conn.close()

def process_query(llm: LLMClient, query: str):
    """クエリを処理して結果を表示"""
    print(f"\n質問: {query}")
    print("\n生成されたSQL:")
    sql = llm.generate_sql(query)
    print(sql)
    print("\n実行結果:")
    
    try:
        columns, results = execute_sql(sql)
        if results:
            print(", ".join(columns))
            for row in results:
                print(row)
        else:
            print("データが見つかりませんでした")
    except Exception as e:
        print(f"エラー: {str(e)}")

def main():
    llm = LLMClient()
    
    # テストしたいクエリのリスト
    queries = [
        "プレミアリーグでハーランドは何ゴール決めていますか？",
        "プレミアリーグの得点ランキングを教えて",
        "プレミアリーグの直近の試合結果を教えて",
        "ハーランドの今シーズンの詳細な成績を教えて（ゴール、アシスト、xG）"
    ]
    
    # 各クエリを実行
    for query in queries:
        process_query(llm, query)

if __name__ == "__main__":
    main()