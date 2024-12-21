import streamlit as st
import sys
import os
import sqlite3
import subprocess

# パスの設定
FRONTEND_DIR = os.path.dirname(__file__)  # frontend
SRC_DIR = os.path.dirname(FRONTEND_DIR)   # src
ROOT_DIR = os.path.dirname(SRC_DIR)       # kyoya-soccer

# Pythonパスに追加
sys.path.append(SRC_DIR)      # srcディレクトリを追加
sys.path.append(ROOT_DIR)     # プロジェクトルートを追加

from backend.llm import LLMClient
from backend.database import execute_sql

# データベースパスの設定
DB_PATH = os.path.join(ROOT_DIR, 'soccer_stats.db')

def init_database():
    """データベースの初期化とサンプルデータの投入"""
    if not os.path.exists(DB_PATH):
        st.warning("データベースを初期化しています...")
        try:
            subprocess.run(['python', os.path.join(ROOT_DIR, 'scripts', 'setup_database.py')], check=True)
            subprocess.run(['python', os.path.join(ROOT_DIR, 'scripts', 'insert_sample_data.py')], check=True)
            st.success("データベースの初期化が完了しました！")
        except Exception as e:
            st.error(f"データベースの初期化に失敗しました: {str(e)}")
            st.stop()

def get_result_summary(query: str, results: list, columns: list) -> str:
    """結果の要約を生成"""
    llm = LLMClient()
    # 結果をテキスト形式に変換
    result_text = "結果:\n"
    for row in results:
        result_text += ", ".join([f"{col}: {val}" for col, val in zip(columns, row)]) + "\n"
    
    # 要約を生成するプロンプト
    prompt = f"""
質問: {query}

{result_text}

この結果について、以下の点を含めて簡潔に説明してください：
1. 主要なデータポイント
2. 特筆すべき点や傾向
3. データの解釈

回答は3-4文程度でまとめてください。
"""
    
    summary = llm.generate_summary(prompt)
    return summary

def main():
    init_database()
    
    st.title("⚽ サッカー選手データ分析")
    
    # サイドバーにクエリ例を表示
    st.sidebar.header("クエリ例")
    example_queries = [
        "プレミアリーグの得点ランキングを教えて",
        "ハーランドの今シーズンの成績は？",
        "プレミアリーグの直近の試合結果を教えて",
        "リバプールの選手一覧を表示して"
    ]
    for query in example_queries:
        if st.sidebar.button(query):
            st.session_state.query = query
    
    # メインエリアにクエリ入力フォーム
    query = st.text_area(
        "質問を入力してください",
        value=st.session_state.get("query", ""),
        height=100
    )
    
    if st.button("分析実行") or query != st.session_state.get("query", ""):
        st.session_state.query = query
        if query:
            try:
                # LLMでSQLを生成
                llm = LLMClient()
                sql = llm.generate_sql(query)
                
                # 生成されたSQLを表示
                with st.expander("生成されたSQL"):
                    st.code(sql, language="sql")
                
                # SQLを実行して結果を表示
                columns, results = execute_sql(sql)
                if results:
                    st.dataframe(
                        [dict(zip(columns, row)) for row in results]
                    )
                    
                    # 結果の要約を表示
                    with st.spinner("分析結果を要約しています..."):
                        summary = get_result_summary(query, results, columns)
                        st.write("### 分析結果")
                        st.write(summary)
                else:
                    st.info("データが見つかりませんでした")
                    
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")

if __name__ == "__main__":
    main() 