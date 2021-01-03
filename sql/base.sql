CREATE DATABASE IF NOT EXISTS euroleague_players;

CREATE TABLE player_info(
	player varchar(50) not null,
    height decimal(3,2),
    position enum('Guard', 'Forward', 'Center'),
    year_born int,
    nationality varchar(30)
);

CREATE TABLE box_score(
	Player varchar(50) not null, G int, MP decimal(3,1), FG decimal(3,1), FGA decimal(3,1), `FG%` int, 3P decimal(3,1), 3PA decimal(3,1), `3P%` int, 2P decimal(3,1),
    2PA decimal(3,1), `2P%` int, FT decimal(3,1), FTA decimal(3,1), `FT%` int, ORB decimal(3,1), DRB decimal(3,1), TRB decimal(3,1),
    AST decimal(3,1), STL decimal(2,1), BLK decimal(2,1), TOV decimal(2,1), PF decimal(2,1), PTS decimal(3,1),
    Team varchar(45), Season int
);

CREATE TABLE play_by_play(
	Player varchar(50) not null, CODETEAM varchar(5), Season int, T2A_j int, T2A_e int, T3A_j int, T3A_e int, TLA_j int, TLA_e int,
    DREB_j int, DREB_t int, OREB_j int, OREB_t int, TO_j int, TO_e int
);


CREATE TABLE shot_chart(
	Player varchar(50) not null, TEAM varchar(5), Season int, Games int, C3R int, C3R_A int, E3R int, E3R_A int, Ce3R int, Ce3R_A int, 
Ce3L int, Ce3L_A int, E3L int, E3L_A int, C3L int, C3L_A int, MBR int, MBR_A int, MER int, MER_A int, MEL int, MEL_A int, 
MBL int, MBL_A int, PR int, PR_A int, PC int, PC_A int, PL int, PL_A int
);

select CONCAT(Player, Season) as id, Player, Season, Games, C3R/Games, C3R_A/Games, E3R/Games, E3R_A/Games, Ce3R/Games, Ce3R_A/Games,
Ce3L/Games, Ce3L_A/Games, E3L/Games, E3L_A/Games, C3L/Games, C3L_A/Games, MBR/Games, MBR_A/Games, MER/Games,
MER_A/Games, MEL/Games, MEL_A/Games, MBL/Games, MBL_A/Games, PR/Games, PR_A/Games, PC/Games, PC_A/Games,
PL/Games, PL_A/Games 
from shot_chart;

select CONCAT(Player, Season) as id, Player, Team, Season, MP as minutes, (2P*2)/2PA as PPT2, (3P*3)/3PA as PPT3, (2P*2)/2PA + (3P*3)/3PA as PPT, 
(TOV*100)/(FGA + FTA*0.44 + AST + TOV) as '%TO', (AST*100)/(FGA + FTA*0.44 + AST + TOV) as '%Ass', FT/FGA as FrTL 
from box_score;

select CONCAT(Player, Season) as id, Player, Season, (T2A_j*100)/T2A_e as '%T2 Abs', (T3A_j*100)/T3A_e as '%T3 Abs',
(T2A_j + T3A_j + TLA_j*0.44 + TO_j - OREB_j)*100/(T2A_e + T3A_e + TLA_e*0.44 + TO_e - OREB_t) as '%Poss Abs',
(DREB_j*100)/DREB_t as '%DReb', (OREB_j*100)/OREB_t as '%OReb'
from play_by_play;


CREATE VIEW stats as (
	select CONCAT(bs.Player, bs.Season) as id, bs.Player, bs.Team, bs.Season, bs.G AS Games, MP as minutes, IFNULL((2P*2)/2PA,0) as PPT2, IFNULL((3P*3)/3PA,0) as PPT3, 
	IFNULL((2P*2)/2PA + (3P*3)/IFNULL(3PA,0),0) as PPT, IFNULL((TOV*100)/(FGA + FTA*0.44 + AST + TOV),0) as '%TO', IFNULL((AST*100)/(FGA + FTA*0.44 + AST + TOV),0) as '%Ass', IFNULL(FT/FGA,0) as FrTL,
	IFNULL((T2A_j*100)/T2A_e,0) as '%T2 Abs', IFNULL((T3A_j*100)/T3A_e,0) as '%T3 Abs',
	IFNULL((T2A_j + T3A_j + TLA_j*0.44 + TO_j - OREB_j)*100/(T2A_e + T3A_e + TLA_e*0.44 + TO_e - OREB_t),0) as '%Poss Abs',
	IFNULL((DREB_j*100)/DREB_t,0) as '%DReb', IFNULL((OREB_j*100)/OREB_t,0) as '%OReb',
	IFNULL(C3R/Games,0) as C3R, IFNULL(C3R_A/Games,0) as C3R_A, IFNULL(E3R/Games,0) as E3R, IFNULL(E3R_A/Games,0) as E3R_A, IFNULL(Ce3R/Games,0) as Ce3R, IFNULL(Ce3R_A/Games,0) as Ce3R_A, IFNULL(Ce3L/Games,0) as Ce3L, 
	IFNULL(Ce3L_A/Games,0) as Ce3L_A, IFNULL(E3L/Games,0) as E3L, IFNULL(E3L_A/Games,0) as E3L_A, IFNULL(C3L/Games,0) as C3L, IFNULL(C3L_A/Games,0) as C3L_A, IFNULL(MBR/Games,0) as MBR, IFNULL(MBR_A/Games,0) as MBR_A, IFNULL(MER/Games,0) as MER,
	IFNULL(MER_A/Games,0) as MER_A, IFNULL(MEL/Games,0) as MEL, IFNULL(MEL_A/Games,0) as MEL_A, IFNULL(MBL/Games,0) as MBL, IFNULL(MBL_A/Games,0) as MBL_A, IFNULL(PR/Games,0) as PR, IFNULL(PR_A/Games,0) as PR_A, IFNULL(PC/Games,0) as PC, 
	IFNULL(PC_A/Games,0) as PC_A, IFNULL(PL/Games,0) as PL, IFNULL(PL_A/Games,0) as PL_A 
	from box_score as bs
	left join play_by_play as pbp
		on CONCAT(bs.Player, bs.Season) = CONCAT(pbp.Player, pbp.Season)
	left join shot_chart as sc
		on CONCAT(bs.Player, bs.Season) = CONCAT(sc.Player, sc.Season)
);

select distinct s.player
from stats s
left join player_info p
	on s.player = p.player
where Games>5 and minutes>5 and height is null
