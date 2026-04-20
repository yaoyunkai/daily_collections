CREATE TABLE test_record
(
    id              SERIAL                                     NOT NULL,
    record_time     TIMESTAMP WITH TIME ZONE                   NOT NULL,
    sernum          VARCHAR(50)                                NOT NULL,
    uuttype         VARCHAR(50)                                NOT NULL,
    test_area       VARCHAR(20)                                NOT NULL,
    passfail        VARCHAR(10)                                NOT NULL,
    runtime         INTEGER                                    NOT NULL,
    test_fail       VARCHAR(50)              DEFAULT ''        NOT NULL,
    test_machine    VARCHAR(20)                                NOT NULL,
    test_container  VARCHAR(50)                                NOT NULL,
    test_mode       VARCHAR(10)              DEFAULT 'PROD0'   NOT NULL,
    deviation       VARCHAR(16)              DEFAULT 'D000000' NOT NULL,
    testr1name      VARCHAR(50),
    testr1          VARCHAR(50),
    testr2name      VARCHAR(50),
    testr2          VARCHAR(50),
    testr3name      VARCHAR(50),
    testr3          VARCHAR(50),
    first_pass_flag BOOLEAN,
    synced_at       TIMESTAMP WITH TIME ZONE,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT now()     NOT NULL,
    PRIMARY KEY (id)
);

-- 针对这个特定的表，调低触发 Autovacuum 的阈值，让数据库更勤快地清理这张表。
-- ALTER TABLE test_record SET (
--     autovacuum_vacuum_scale_factor = 0.02, -- 当表里有 2% 的死元组时就触发清理 (默认是 20%)
--     autovacuum_analyze_scale_factor = 0.01
-- );

CREATE INDEX idx_test_record_window ON test_record (sernum, test_area, record_time);
CREATE INDEX idx_test_record_unsynced ON test_record (sernum, test_area) WHERE synced_at IS NULL;

CREATE OR REPLACE FUNCTION refresh_first_pass_flag()
RETURNS VOID AS $$
BEGIN
    IF NOT pg_try_advisory_xact_lock(98765) THEN
        RAISE NOTICE 'Previous refresh task is still running. Skipping this run.';
        RETURN;
    END IF;

    WITH
    TouchedGroups AS (
        -- 步骤1：找出所有包含“未计算数据”的产品和测试区域组合
        SELECT DISTINCT sernum, test_area
        FROM test_record
        WHERE synced_at IS NULL
    ),
    CalculatedFlags AS (
        SELECT
            d.id,
            CASE
                -- 只有当状态不是 'start' 且排名第一时，才算作首次测试
                WHEN d.passfail != 'start' AND ROW_NUMBER() OVER (
                    PARTITION BY d.sernum, d.test_area
                    -- 过滤掉 start 记录参与排名
                    -- (注：这里使用 FILTER 或在 WHERE 中过滤，具体取决于你是否希望 start 记录也被打上 synced_at 标签)
                    ORDER BY CASE WHEN d.passfail = 'start' THEN 1 ELSE 0 END, d.record_time ASC
                ) = 1 THEN TRUE
                ELSE FALSE
            END AS correct_flag
        FROM test_record d
        INNER JOIN TouchedGroups tg
            ON d.sernum = tg.sernum AND d.test_area = tg.test_area
    )
    -- 步骤3：将计算结果和同步时间更新回主表
    UPDATE test_record d
    SET
        first_pass_flag = c.correct_flag,
        synced_at = NOW()
    FROM CalculatedFlags c
    WHERE d.id = c.id
      AND (
          d.synced_at IS NULL
          OR d.first_pass_flag IS DISTINCT FROM c.correct_flag
      );
END;
$$ LANGUAGE plpgsql;
