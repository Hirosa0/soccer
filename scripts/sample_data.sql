-- teams
INSERT INTO teams (team_name, league, country) VALUES
('Liverpool', 'Premier League', 'England'),
('Manchester City', 'Premier League', 'England'),
('Arsenal', 'Premier League', 'England'),
('Manchester United', 'Premier League', 'England'),
('Chelsea', 'Premier League', 'England');

-- players
INSERT INTO players (name, team_id, position, nationality, birth_date) VALUES
('Mohamed Salah', 1, 'Forward', 'Egypt', '1992-06-15'),
('Darwin Núñez', 1, 'Forward', 'Uruguay', '1999-06-24'),
('Virgil van Dijk', 1, 'Defender', 'Netherlands', '1991-07-08'),
('Erling Haaland', 2, 'Forward', 'Norway', '2000-07-21'),
('Kevin De Bruyne', 2, 'Midfielder', 'Belgium', '1991-06-28');

-- matches (2023-24シーズンの一部)
INSERT INTO matches (home_team_id, away_team_id, match_date, season, competition) VALUES
(1, 2, '2023-11-25', '2023-24', 'Premier League'),
(3, 1, '2023-12-23', '2023-24', 'Premier League'),
(1, 4, '2024-01-17', '2023-24', 'Premier League'),
(5, 1, '2024-01-31', '2023-24', 'Premier League');

-- player_stats
INSERT INTO player_stats (player_id, match_id, goals, assists, minutes_played) VALUES
(1, 1, 1, 1, 90),  -- Salah vs Man City
(2, 1, 2, 0, 85),  -- Núñez vs Man City
(4, 1, 1, 0, 90),  -- Haaland vs Liverpool
(1, 2, 2, 0, 90),  -- Salah vs Arsenal
(2, 3, 1, 1, 75),  -- Núñez vs Man United
(1, 4, 0, 1, 90);  -- Salah vs Chelsea

-- 他のサンプルデータ 