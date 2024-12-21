import sqlite3
from datetime import datetime, timedelta

def insert_sample_data():
    conn = sqlite3.connect('soccer_stats.db')
    cursor = conn.cursor()
    
    # 5大リーグの上位チームのサンプルデータ
    cursor.executescript('''
        -- Premier League teams
        INSERT INTO teams (name, league, country) VALUES
        ('Manchester City', 'Premier League', 'England'),
        ('Arsenal', 'Premier League', 'England'),
        ('Liverpool', 'Premier League', 'England'),
        ('Tottenham', 'Premier League', 'England'),
        ('Aston Villa', 'Premier League', 'England');

        -- LaLiga teams
        INSERT INTO teams (name, league, country) VALUES
        ('Real Madrid', 'LaLiga', 'Spain'),
        ('Girona', 'LaLiga', 'Spain'),
        ('Barcelona', 'LaLiga', 'Spain'),
        ('Atletico Madrid', 'LaLiga', 'Spain'),
        ('Athletic Club', 'LaLiga', 'Spain');

        -- 注目選手のデータ
        INSERT INTO players (name, team_id, position, nationality, birth_date, jersey_number) VALUES
        ('Erling Haaland', 1, 'Forward', 'Norway', '2000-07-21', 9),
        ('Jude Bellingham', 6, 'Midfielder', 'England', '2003-06-29', 5),
        ('Mohamed Salah', 3, 'Forward', 'Egypt', '1992-06-15', 11),
        ('Vinicius Jr', 6, 'Forward', 'Brazil', '2000-07-12', 7),
        ('Robert Lewandowski', 8, 'Forward', 'Poland', '1988-08-21', 9);

        -- 最近の試合結果
        INSERT INTO matches (home_team_id, away_team_id, match_date, season, competition, home_score, away_score) VALUES
        (1, 2, '2024-03-31', '2023-24', 'Premier League', 2, 1),
        (6, 8, '2024-03-31', '2023-24', 'LaLiga', 3, 2),
        (3, 4, '2024-03-30', '2023-24', 'Premier League', 3, 1),
        (7, 9, '2024-03-30', '2023-24', 'LaLiga', 1, 1);

        -- 選手のパフォーマンス
        INSERT INTO player_stats (player_id, match_id, goals, assists, minutes_played, xg, shots, shots_on_target) VALUES
        (1, 1, 2, 0, 90, 1.8, 4, 3),  -- Haaland vs Arsenal
        (2, 2, 1, 1, 90, 0.9, 3, 2),  -- Bellingham vs Barcelona
        (3, 3, 1, 1, 90, 1.2, 5, 3),  -- Salah vs Tottenham
        (4, 2, 1, 0, 90, 0.8, 4, 2);  -- Vinicius vs Barcelona
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_sample_data() 