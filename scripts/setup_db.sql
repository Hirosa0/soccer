-- データベース作成
CREATE DATABASE soccer_stats;

\c soccer_stats;

-- テーブル作成
CREATE TABLE teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    league VARCHAR(100),
    country VARCHAR(100)
);

CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    team_id INTEGER REFERENCES teams(team_id),
    position VARCHAR(50),
    nationality VARCHAR(100),
    birth_date DATE
);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    home_team_id INTEGER REFERENCES teams(team_id),
    away_team_id INTEGER REFERENCES teams(team_id),
    match_date DATE,
    season VARCHAR(9),
    competition VARCHAR(100)
);

CREATE TABLE player_stats (
    stat_id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(player_id),
    match_id INTEGER REFERENCES matches(match_id),
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    minutes_played INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0
);

-- インデックス作成
CREATE INDEX idx_player_team ON players(team_id);
CREATE INDEX idx_match_teams ON matches(home_team_id, away_team_id);
CREATE INDEX idx_player_stats_player ON player_stats(player_id);
CREATE INDEX idx_player_stats_match ON player_stats(match_id);

-- テーブル作成（プロジェクト設計書のSQL文を実行） 