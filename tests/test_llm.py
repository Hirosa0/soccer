import pytest
from src.backend.llm import LLMClient

def test_extract_sql():
    llm = LLMClient()
    
    # 正常系
    content = '''Here's the SQL query:
```SQL
SELECT name, SUM(goals) as total_goals
FROM players
JOIN player_stats ON players.player_id = player_stats.player_id
GROUP BY name
ORDER BY total_goals DESC;
```'''
    expected = '''SELECT name, SUM(goals) as total_goals
FROM players
JOIN player_stats ON players.player_id = player_stats.player_id
GROUP BY name
ORDER BY total_goals DESC;'''
    
    assert llm._extract_sql(content) == expected
    
    # 異常系
    content_without_sql = "Here's some text without SQL"
    assert llm._extract_sql(content_without_sql) == ""