CREATE TABLE IF NOT EXISTS new_matches
(
    game_id         BIGINT PRIMARY KEY,
    game_start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    game_duration   INTEGER                     NOT NULL,
    queue_id        INTEGER                     NOT NULL,
    game_end_result VARCHAR(64)                 NOT NULL DEFAULT ''
);

/*

game_version for matches


*/

COMMENT ON TABLE new_matches IS '比赛记录';
COMMENT ON COLUMN new_matches.queue_id IS '队列ID（如排位赛、匹配赛等）';
COMMENT ON COLUMN new_matches.game_end_result IS '游戏结束时的状态';

-- 参与者信息
CREATE TABLE IF NOT EXISTS new_participants
(
    id                  SERIAL PRIMARY KEY,
    participant_idx     INTEGER      NOT NULL, -- 召唤师位置
    game_id             BIGINT       NOT NULL REFERENCES new_matches (game_id),
    summoner_id         BIGINT       NOT NULL,
    nick                VARCHAR(100) NOT NULL,
    team_id             INTEGER      NOT NULL,
    champion_id         INTEGER      NOT NULL,
    spell0_id           INTEGER      NOT NULL,
    spell1_id           INTEGER      NOT NULL,
    win                 BOOLEAN      NOT NULL,

    item0_id            INTEGER      NOT NULL,
    item1_id            INTEGER      NOT NULL,
    item2_id            INTEGER      NOT NULL,
    item3_id            INTEGER      NOT NULL,
    item4_id            INTEGER      NOT NULL,
    item5_id            INTEGER      NOT NULL,
    item6_id            INTEGER      NOT NULL,
    perk0_id            INTEGER      NOT NULL,
    perk1_id            INTEGER      NOT NULL,

    kills               INTEGER      NOT NULL,
    deaths              INTEGER      NOT NULL,
    assists             INTEGER      NOT NULL,
    gold_earned         INTEGER      NOT NULL,
    damage_to_champions INTEGER      NOT NULL,
    damage_total        INTEGER      NOT NULL,
    damage_taken        INTEGER      NOT NULL
);


/*
Query SQLs

*/

select game_id, summoner_id, win
from new_participants
where game_id in (select game_id from new_participants where summoner_id = 4100826724)
  and summoner_id != 4100826724