from openai import OpenAI
import os
from dotenv import load_dotenv
import re
from .prompts import DB_SCHEMA, USER_PROMPT_TEMPLATE

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"

    def generate_sql(self, user_query: str) -> str:
        """ユーザーの質問からSQLクエリを生成"""
        messages = [
            {"role": "system", "content": DB_SCHEMA},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(user_query=user_query)}
        ]

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.0  # より決定論的な出力に
            )
            sql = self._extract_sql(response.choices[0].message.content)
            return sql
        except Exception as e:
            raise Exception(f"SQLの生成に失敗しました: {str(e)}")

    def _extract_sql(self, content: str) -> str:
        """レスポンスからSQLクエリを抽出"""
        # SQLブロックを探す
        sql_match = re.search(r'```sql\n(.*?)```', content, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()
        
        # バッククォートのみの場合
        sql_match = re.search(r'`(.*?)`', content, re.DOTALL)
        if sql_match:
            return sql_match.group(1).strip()
        
        # SQLブロックがない場合は空文字を返す
        return ""

    def validate_sql(self, sql: str) -> bool:
        """生成されたSQLの基本的な検証"""
        # 基本的なバリデーション
        sql_lower = sql.lower()
        
        # SELECT文で始まることを確認
        if not sql_lower.strip().startswith('select'):
            return False
        
        # 禁止されたSQL文を含まないことを確認
        forbidden = ['insert', 'update', 'delete', 'drop', 'truncate', 'alter']
        if any(word in sql_lower for word in forbidden):
            return False
        
        # テーブル名の存在確認
        required_tables = ['players', 'teams', 'matches', 'player_stats']
        if not any(table in sql_lower for table in required_tables):
            return False
        
        return True

    def generate_summary(self, prompt: str) -> str:
        """分析結果の要約を生成"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7  # より自然な文章生成のため
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"要約の生成に失敗しました: {str(e)}")