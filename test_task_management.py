#!/usr/bin/env python3
"""
タスク管理機能のテストスクリプト
"""

import sys
import os

# パスの設定
ROOT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
sys.path.append(SRC_DIR)

from backend.task_manager import TaskManager

def test_task_management():
    """タスク管理機能をテスト"""
    print("🧪 タスク管理機能のテスト開始...")
    
    # TaskManagerインスタンスを作成
    tm = TaskManager()
    
    # 1. タスク作成のテスト
    print("\n1️⃣ タスク作成テスト")
    task_id1 = tm.create_task("テストタスク1", "これは最初のテストタスクです", "未着手")
    task_id2 = tm.create_task("テストタスク2", "これは2番目のテストタスクです", "進行中")
    task_id3 = tm.create_task("テストタスク3", "これは3番目のテストタスクです", "完了")
    
    print(f"✅ タスク1作成成功 (ID: {task_id1})")
    print(f"✅ タスク2作成成功 (ID: {task_id2})")
    print(f"✅ タスク3作成成功 (ID: {task_id3})")
    
    # 2. 全タスク取得のテスト
    print("\n2️⃣ 全タスク取得テスト")
    all_tasks = tm.get_all_tasks()
    print(f"✅ 全タスク数: {len(all_tasks)}")
    for task in all_tasks:
        print(f"   - {task['title']} [{task['status']}]")
    
    # 3. ステータス別取得のテスト
    print("\n3️⃣ ステータス別取得テスト")
    for status in ['未着手', '進行中', '完了']:
        tasks = tm.get_tasks_by_status(status)
        print(f"✅ {status}: {len(tasks)}件")
    
    # 4. タスク統計のテスト
    print("\n4️⃣ タスク統計テスト")
    stats = tm.get_task_stats()
    for key, value in stats.items():
        print(f"✅ {key}: {value}")
    
    # 5. ステータス更新のテスト
    print("\n5️⃣ ステータス更新テスト")
    success = tm.update_task_status(task_id1, "進行中")
    if success:
        print("✅ タスク1のステータスを「進行中」に更新成功")
    else:
        print("❌ タスク1のステータス更新失敗")
    
    # 6. 更新後の確認
    print("\n6️⃣ 更新後の確認")
    updated_tasks = tm.get_tasks_by_status("進行中")
    print(f"✅ 進行中タスク数: {len(updated_tasks)}")
    
    # 7. テストデータのクリーンアップ
    print("\n7️⃣ テストデータクリーンアップ")
    for task_id in [task_id1, task_id2, task_id3]:
        success = tm.delete_task(task_id)
        if success:
            print(f"✅ タスクID {task_id} 削除成功")
        else:
            print(f"❌ タスクID {task_id} 削除失敗")
    
    print("\n🎉 全てのテストが完了しました！")

if __name__ == "__main__":
    test_task_management()