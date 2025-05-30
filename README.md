# ⚽ Soccer Stats AI - 自然言語サッカーデータ分析システム

自然言語でサッカー選手の統計データを分析できるWebアプリケーションです。OpenAI GPTを使用して自然言語をSQLクエリに変換し、サッカー選手や試合データから洞察を得ることができます。

## 🌟 主な機能

- **自然言語クエリ**: 「プレミアリーグの得点ランキングを教えて」といった自然な日本語で質問
- **AI-SQLジェネレーター**: OpenAI GPT-4を使用して自動的にSQLクエリを生成
- **サッカーデータベース**: プレミアリーグやラ・リーガの選手、チーム、試合データを管理
- **インタラクティブUI**: Streamlitによる直感的なWebインターフェース
- **結果要約機能**: AIが分析結果を自動で要約・解釈

## 🚀 クイックスタート

### 前提条件

- Python 3.8以上
- OpenAI APIキー

### インストール

1. リポジトリをクローン:
```bash
git clone https://github.com/Hirosa0/soccer.git
cd soccer
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

3. 環境変数を設定:
```bash
# .envファイルを作成してOpenAI APIキーを設定
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. データベースを初期化:
```bash
python scripts/setup_database.py
python scripts/insert_sample_data.py
```

### 実行

Streamlitアプリケーションを起動:
```bash
streamlit run src/frontend/app.py
```

Webブラウザで `http://localhost:8501` にアクセスして使用開始！

## 📊 使用例

### クエリ例

- **得点ランキング**: 「プレミアリーグの得点ランキングを教えて」
- **選手分析**: 「ハーランドの今シーズンの成績は？」
- **試合結果**: 「プレミアリーグの直近の試合結果を教えて」
- **チーム情報**: 「リバプールの選手一覧を表示して」

### 実行フロー

1. **自然言語入力** → ユーザーが日本語で質問
2. **SQL生成** → GPT-4が適切なSQLクエリを自動生成
3. **データ取得** → SQLiteデータベースからデータを取得
4. **結果表示** → 表形式で結果を表示
5. **AI要約** → 結果の要約と洞察を自動生成

## 🏗️ プロジェクト構造

```
soccer/
├── src/
│   ├── backend/           # バックエンドロジック
│   │   ├── database.py    # データベース接続・SQL実行
│   │   ├── llm.py         # OpenAI GPT連携
│   │   └── prompts.py     # プロンプトテンプレート
│   └── frontend/
│       └── app.py         # Streamlit Webアプリ
├── scripts/
│   ├── setup_database.py  # データベース初期化
│   └── insert_sample_data.py # サンプルデータ投入
├── docs/                  # 設計ドキュメント
├── tests/                 # テストファイル
└── requirements.txt       # 依存関係
```

## 🗄️ データベーススキーマ

### テーブル構造

- **players**: 選手の基本情報（名前、チーム、ポジション等）
- **teams**: チーム情報（チーム名、リーグ、国）
- **matches**: 試合情報（対戦カード、日程、結果）
- **player_stats**: 選手の試合ごとの統計（ゴール、アシスト、xG等）

### サンプルデータ

- プレミアリーグ、ラ・リーガの主要チーム
- エルリング・ハーランド、ジュード・ベリンガム、モハメド・サラー等の注目選手
- 2023-24シーズンの試合データ

## 🔧 技術スタック

- **フロントエンド**: Streamlit
- **バックエンド**: Python
- **データベース**: SQLite
- **AI/LLM**: OpenAI GPT-4
- **主要ライブラリ**: 
  - `openai` - OpenAI API連携
  - `streamlit` - Webアプリフレームワーク
  - `pandas` - データ処理
  - `python-dotenv` - 環境変数管理

## 🛠️ 開発情報

### 開発フェーズ

- [x] **Phase 1**: 基盤開発（データベース構築、環境セットアップ）
- [x] **Phase 2**: バックエンド開発（LLM連携、SQL生成機能）
- [x] **Phase 3**: フロントエンド開発（Streamlit UI、結果表示）
- [ ] **Phase 4**: テストと改善（ユニットテスト、パフォーマンス最適化）

### アーキテクチャの特徴

- **セキュリティ**: SELECT文のみ実行、読み取り専用アクセス
- **プロンプトエンジニアリング**: データベーススキーマを含む最適化されたプロンプト
- **エラーハンドリング**: LLM生成SQL、DB実行、ユーザー入力の各レベルでのエラー処理

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🤝 コントリビューション

プルリクエストやイシューを歓迎します！開発に参加したい場合は：

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチをプッシュ (`git push origin feature/AmazingFeature`)
5. プルリクエストを作成

## 📞 サポート

質問や問題がある場合は、GitHubのIssuesでお知らせください。

---

**作成者**: [Hirosa0](https://github.com/Hirosa0)