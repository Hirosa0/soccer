DB_SCHEMA = """
テーブル構造:
1. players (player_id, name, team_id, position, nationality, birth_date, jersey_number)
   - 選手の基本情報を管理
   - team_idはteamsテーブルを参照
   - positionは'Forward', 'Midfielder', 'Defender', 'Goalkeeper'のいずれか
   - jersey_numberは背番号

2. teams (team_id, name, league, country)
   - チームの基本情報を管理
   - leagueは'Premier League', 'LaLiga'等のリーグ名
   - countryは国名

3. matches (match_id, home_team_id, away_team_id, match_date, season, competition, home_score, away_score)
   - 試合情報を管理
   - home_team_id, away_team_idはteamsテーブルを参照
   - seasonは'2023-24'等のシーズン表記
   - competitionは'Premier League'等の大会名
   - home_score, away_scoreは得点

4. player_stats (stat_id, player_id, match_id, goals, assists, minutes_played, xg, shots, shots_on_target)
   - 選手の試合ごとの統計情報
   - player_idはplayersテーブルを参照
   - match_idはmatchesテーブルを参照
   - xgは期待得点
   - shotsは総シュート数
   - shots_on_targetはシュートのうち枠内に入った数

クエリ例:
1. プレミアリーグの得点ランキング:
```sql
SELECT p.name, t.name as team, SUM(ps.goals) as total_goals
FROM players p
JOIN teams t ON p.team_id = t.team_id
JOIN player_stats ps ON p.player_id = ps.player_id
JOIN matches m ON ps.match_id = m.match_id
WHERE t.league = 'Premier League'
AND m.season = '2023-24'
GROUP BY p.player_id, p.name, t.name
ORDER BY total_goals DESC;
```

2. 特定選手の直近の試合成績:
```sql
SELECT m.match_date, t_home.name as home_team, t_away.name as away_team,
       m.home_score, m.away_score, ps.goals, ps.assists, ps.xg
FROM matches m
JOIN teams t_home ON m.home_team_id = t_home.team_id
JOIN teams t_away ON m.away_team_id = t_away.team_id
JOIN player_stats ps ON m.match_id = ps.match_id
JOIN players p ON ps.player_id = p.player_id
WHERE p.name = 'Erling Haaland'
ORDER BY m.match_date DESC
LIMIT 5;
```

注意事項:
1. SELECT文のみを生成してください
2. 複雑なJOINが必要な場合は適切に結合してください
3. 集計関数（SUM, COUNT等）を適切に使用してください
4. 必要に応じてサブクエリを使用してください
5. 結果は読みやすい順序でソートしてください
6. テーブル名とカラム名は必ずスキーマに存在するものを使用してください
7. 日付形式は'YYYY-MM-DD'を使用してください
"""

USER_PROMPT_TEMPLATE = """
以下の質問に対するSQLクエリを生成してください：
{user_query}

必ず```sql```で囲んでSQLクエリのみを出力してください。
"""