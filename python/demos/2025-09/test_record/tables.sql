create table test_record
(
    id              serial PRIMARY KEY,
    record_time     timestamp with time zone not null,
    sernum          varchar(50)              not null,
    uuttype         varchar(50)              not null,
    test_area       varchar(20)              not null,
    passfail        varchar(1)               not null check (passfail IN ('A', 'S', 'P', 'F')),
    runtime         int                      not null default 0,
    test_fail       varchar(50)              not null default '',
    test_machine    varchar(20)              not null,
    test_container  varchar(50)              not null,
    test_mode       varchar(10)              not null default 'PROD0',
    deviation       varchar(16)              not null default 'D000000',
    testr1name      varchar(50)                       default null,
    testr1          varchar(50)                       default null,
    testr2name      varchar(50)                       default null,
    testr2          varchar(50)                       default null,
    testr3name      varchar(50)                       default null,
    testr3          varchar(50)                       default null,
    first_pass_flag smallint                 not null default -1,
    created_at      TIMESTAMP WITH TIME ZONE not null DEFAULT NOW()
);

CREATE INDEX idx_test_record_calc
    ON test_record (sernum, test_area, record_time);

CREATE INDEX idx_test_record_unprocessed
    ON test_record (first_pass_flag)
    WHERE first_pass_flag = -1;


CREATE OR REPLACE FUNCTION refresh_first_pass_flag()
RETURNS VOID AS $$
BEGIN
    WITH
    -- 步骤 1: 精准找出哪些"组"有新数据
    TouchedGroups AS (
        SELECT DISTINCT sernum, test_area
        FROM test_record
        WHERE first_pass_flag = -1
    ),
    -- 步骤 2: 把这些组内的 (所有数据) 重新按业务时间排序计算
    CalculatedFlags AS (
        SELECT
            d.id,
            CASE
                WHEN ROW_NUMBER() OVER (
                    PARTITION BY d.sernum, d.test_area
                    ORDER BY d.record_time ASC
                ) = 1 THEN 1
                ELSE 0
            END AS correct_flag
        FROM test_record d
        INNER JOIN TouchedGroups tg
            ON d.sernum = tg.sernum AND d.test_area = tg.test_area
    )
    -- 步骤 3: 智能更新回主表
    UPDATE test_record d
    SET first_pass_flag = c.correct_flag
    FROM CalculatedFlags c
    WHERE d.id = c.id
      -- 只更新状态发生变化的数据！
      -- 这不仅会把 -1 变成 1 或 0，还会把因为乱序导致算错的历史 1 自动纠正为 0
      AND d.first_pass_flag IS DISTINCT FROM c.correct_flag;
END;
$$ LANGUAGE plpgsql;
