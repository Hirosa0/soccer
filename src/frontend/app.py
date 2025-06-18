import streamlit as st
import sys
import os
import sqlite3
import subprocess
from datetime import datetime

# パスの設定
FRONTEND_DIR = os.path.dirname(__file__)  # frontend
SRC_DIR = os.path.dirname(FRONTEND_DIR)   # src
ROOT_DIR = os.path.dirname(SRC_DIR)       # kyoya-soccer

# Pythonパスに追加
sys.path.append(SRC_DIR)      # srcディレクトリを追加
sys.path.append(ROOT_DIR)     # プロジェクトルートを追加

from backend.llm import LLMClient
from backend.database import execute_sql
from backend.task_manager import TaskManager

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

def render_task_management():
    """タスク管理画面をレンダリング"""
    st.header("📋 タスク管理")
    
    # TaskManagerのインスタンスを作成
    task_manager = TaskManager()
    
    # タスク統計を表示
    stats = task_manager.get_task_stats()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("未着手", stats['未着手'])
    with col2:
        st.metric("進行中", stats['進行中'])
    with col3:
        st.metric("完了", stats['完了'])
    with col4:
        st.metric("合計", stats['合計'])
    
    st.divider()
    
    # 新しいタスクを作成するフォーム
    with st.expander("➕ 新しいタスクを作成", expanded=False):
        with st.form("create_task_form"):
            new_title = st.text_input("タスクタイトル", placeholder="例: データベース設計の見直し")
            new_description = st.text_area("説明（任意）", placeholder="タスクの詳細説明...")
            new_status = st.selectbox("初期ステータス", ["未着手", "進行中", "完了"], index=0)
            
            if st.form_submit_button("タスクを作成"):
                if new_title.strip():
                    try:
                        task_id = task_manager.create_task(new_title.strip(), new_description.strip(), new_status)
                        st.success(f"✅ タスク「{new_title}」を作成しました（ID: {task_id}）")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ タスクの作成に失敗しました: {str(e)}")
                else:
                    st.warning("⚠️ タスクタイトルを入力してください")
    
    # ステータス別表示の選択肢
    view_option = st.radio(
        "表示方法を選択",
        ["全て", "未着手", "進行中", "完了"],
        horizontal=True
    )
    
    # タスク一覧を取得
    if view_option == "全て":
        tasks = task_manager.get_all_tasks()
    else:
        tasks = task_manager.get_tasks_by_status(view_option)
    
    if not tasks:
        st.info(f"📝 {view_option}のタスクはありません")
        return
    
    # タスク一覧を表示
    st.subheader(f"タスク一覧 ({view_option})")
    
    for task in tasks:
        with st.container():
            col1, col2, col3 = st.columns([6, 2, 2])
            
            with col1:
                # タスクタイトルとステータスのスタイリング
                status_color = {
                    "未着手": "🔴",
                    "進行中": "🟡", 
                    "完了": "🟢"
                }
                
                st.write(f"{status_color[task['status']]} **{task['title']}**")
                if task['description']:
                    st.write(f"_{task['description']}_")
                st.caption(f"作成: {task['created_at']} | 更新: {task['updated_at']}")
            
            with col2:
                # ステータス変更
                current_status = task['status']
                new_status = st.selectbox(
                    "ステータス", 
                    ["未着手", "進行中", "完了"],
                    index=["未着手", "進行中", "完了"].index(current_status),
                    key=f"status_{task['task_id']}"
                )
                
                if new_status != current_status:
                    if task_manager.update_task_status(task['task_id'], new_status):
                        st.success(f"✅ ステータスを「{new_status}」に更新しました")
                        st.rerun()
                    else:
                        st.error("❌ ステータスの更新に失敗しました")
            
            with col3:
                # タスク削除ボタン
                if st.button("🗑️ 削除", key=f"delete_{task['task_id']}", help="タスクを削除"):
                    if task_manager.delete_task(task['task_id']):
                        st.success("✅ タスクを削除しました")
                        st.rerun()
                    else:
                        st.error("❌ タスクの削除に失敗しました")
        
        st.divider()

def render_soccer_analysis():
    """サッカー分析画面をレンダリング"""
    st.header("⚽ サッカー選手データ分析")
    
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

def main():
    init_database()
    
    st.set_page_config(
        page_title="Soccer Stats & Task Manager",
        page_icon="⚽",
        layout="wide"
    )
    
    st.title("⚽ Soccer Stats & Task Manager")
    st.markdown("**サッカー選手データ分析** と **タスク管理** を統合したWebアプリケーション")
    
    # タブを作成
    tab1, tab2 = st.tabs(["⚽ サッカー分析", "📋 タスク管理"])
    
    with tab1:
        render_soccer_analysis()
    
    with tab2:
        render_task_management()

if __name__ == "__main__":
    main() 