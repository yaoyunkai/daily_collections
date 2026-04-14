1. trigger
只适用于数据严格按序到达的情况。

CREATE TABLE first_seen_tracker
(
    sernum    VARCHAR(100),
    test_area VARCHAR(100),
    PRIMARY KEY (sernum, test_area)
);

create table test_record
(
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
    first_pass_flag boolean                  not null,
    created_at      TIMESTAMP WITH TIME ZONE not null DEFAULT NOW()
);

-- 1. 创建触发器执行函数
CREATE OR REPLACE FUNCTION set_first_flag()
    RETURNS TRIGGER AS
$$
DECLARE
    inserted_id INT;
BEGIN
    -- 尝试向辅助表插入。如果已存在，则什么都不做；如果成功，返回 1
    INSERT INTO first_seen_tracker (sernum, test_area)
    VALUES (NEW.sernum, NEW.test_area)
    ON CONFLICT (sernum, test_area) DO NOTHING
    RETURNING 1 INTO inserted_id;

    -- 根据返回值极速判断
    IF inserted_id = 1 THEN
        NEW.first_flag := TRUE;
    ELSE
        NEW.first_flag := FALSE;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 2. 将触发器绑定到主表
CREATE TRIGGER trg_before_insert_test_record
    BEFORE INSERT
    ON test_record
    FOR EACH ROW
EXECUTE FUNCTION set_first_flag();


CREATE INDEX idx_test_record_created_at_brin
    ON test_record USING BRIN (record_time);


=================================================================================
=================================================================================
=================================================================================
=================================================================================


2. corn 定时任务。

数据有可能延迟的情况下。
附带额外的record_time, 每隔一段时间执行去更新 first_pass_flag.
超过30分钟的插入失败。


CREATE TABLE demo_record (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sernum VARCHAR(100) NOT NULL,
    test_area VARCHAR(100) NOT NULL,
    result CHAR(1) CHECK (result IN ('P', 'F')),
    record_time TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    -- 使用 SMALLINT: -1=未处理, 1=True, 0=False
    first_flag SMALLINT NOT NULL DEFAULT -1
);

-- 核心复合索引：加速定时任务的查询和排序
CREATE INDEX idx_demo_record_calc
ON demo_record (sernum, test_area, record_time);

-- 专门为 -1 建立一个“部分索引”(Partial Index)，极大加速定时任务抓取未处理数据的速度
CREATE INDEX idx_demo_record_unprocessed
ON demo_record (first_flag)
WHERE first_flag = -1;


CREATE OR REPLACE FUNCTION refresh_first_flag()
RETURNS VOID AS $$
BEGIN
    WITH
    -- 步骤 1：精准找出哪些“组”有新数据
    TouchedGroups AS (
        SELECT DISTINCT sernum, test_area
        FROM demo_record
        WHERE first_flag = -1
    ),
    -- 步骤 2：把这些组内的【所有数据】重新按业务时间排序计算
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
        FROM demo_record d
        INNER JOIN TouchedGroups tg
            ON d.sernum = tg.sernum AND d.test_area = tg.test_area
    )
    -- 步骤 3：智能更新回主表
    UPDATE demo_record d
    SET first_flag = c.correct_flag
    FROM CalculatedFlags c
    WHERE d.id = c.id
      -- 【极其重要】只更新状态发生变化的数据！
      -- 这不仅会把 -1 变成 1 或 0，还会把因为乱序导致算错的历史 1 自动纠正为 0
      AND d.first_flag IS DISTINCT FROM c.correct_flag;

END;
$$ LANGUAGE plpgsql;


CREATE EXTENSION pg_cron;
-- 每 5 分钟执行一次
SELECT cron.schedule('refresh_flag_job', '*/5 * * * *', 'SELECT refresh_first_flag();');

