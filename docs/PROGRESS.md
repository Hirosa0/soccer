# 進捗管理

## 2024-03-XX
- プロジェクトの初期設計完了
- 基本設計書作成
- DB設計書作成
- 環境構築用ファイル作成
  - requirements.txt
  - .env
  - setup_database.py
  - insert_sample_data.py
- バックエンド基本構造の作成
  - database.py
  - llm.py

## 今後のTODO
### Phase 1: 基盤開発 [完了]
- [x] プロジェクト構造のセットアップ
- [x] SQLiteデータベースの構築
  - [x] setup_database.pyの作成
  - [x] insert_sample_data.pyの作成
  - [x] サンプルデータの作成と投入

### Phase 2: バックエンド開発 [WIP]
- [x] DB接続機能の実装
- [x] OpenAI APIとの連携
- [x] プロンプトエンジニアリングの実装
- [x] SQLジェネレーター機能の実装と統合

### Phase 3: フロントエンド開発 [完了]
- [x] Streamlitの基本UI実装
- [x] クエリ入力フォームの作成
- [x] 結果表示機能の実装
- [x] エラーハンドリングUIの実装

### Phase 4: テストと改善
- [ ] ユニットテストの作成
- [ ] 統合テストの実施
- [ ] パフォーマンス最適化