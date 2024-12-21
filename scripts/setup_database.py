import sqlite3
import os

def setup_database():
    # データベースファイルのパス
    db_path = 'soccer_stats.db'
    
    # 既存のDBファイルを削除（if exists）
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # DBに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.executescript('''
        CREATE TABLE teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            league TEXT NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            team_id INTEGER REFERENCES teams(team_id),
            position TEXT,
            nationality TEXT,
            birth_date TEXT,
            jersey_number INTEGER
        );

        CREATE TABLE matches (
            match_id INTEGER PRIMARY KEY AUTOINCREMENT,
            home_team_id INTEGER REFERENCES teams(team_id),
            away_team_id INTEGER REFERENCES teams(team_id),
            match_date TEXT,
            season TEXT,
            competition TEXT,
            home_score INTEGER,
            away_score INTEGER
        );

        CREATE TABLE player_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER REFERENCES players(player_id),
            match_id INTEGER REFERENCES matches(match_id),
            goals INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            minutes_played INTEGER DEFAULT 0,
            xg REAL DEFAULT 0,
            shots INTEGER DEFAULT 0,
            shots_on_target INTEGER DEFAULT 0
        );

        CREATE INDEX idx_player_name ON players(name);
        CREATE INDEX idx_team_name ON teams(name);
        CREATE INDEX idx_player_team ON players(team_id);
        CREATE INDEX idx_match_teams ON matches(home_team_id, away_team_id);
        CREATE INDEX idx_player_stats_player ON player_stats(player_id);
        CREATE INDEX idx_player_stats_match ON player_stats(match_id);
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database() 