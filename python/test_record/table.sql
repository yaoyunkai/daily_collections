CREATE TABLE `test_record`
(
    `id`             int                                    NOT NULL AUTO_INCREMENT COMMENT '主键',
    `tst_id`         datetime                               NOT NULL COMMENT 'Test ID\n\nunique togther with sernum',
    `bf_status`      tinyint                                NOT NULL COMMENT 'back flush status:\n\n0 - no back flush\n1- back flush status with *',
    `record_time`    datetime                               NOT NULL COMMENT 'Record Time: Pass time',
    `sernum`         varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Serial Number \n\nupper case, length 40',
    `uuttype`        varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'UUT Type\n\nlength 40, upper case',
    `area`           varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Area\n\nupper case, length 20',
    `test_result`    char(1) COLLATE utf8mb4_general_ci     NOT NULL COMMENT 'final test result\n\noptional: \nP - passed\nF - failed\nA - adt sampling\nS - start ',
    `run_time`       int                                    NOT NULL DEFAULT '0' COMMENT 'Total Run time, unit is second',
    `test_failure`   varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'if test result is F, the column record test failed\n\nupper case',
    `test_server`    varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Machine\n\nlower case',
    `test_container` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Container\n\nlength 50, no modify',
    `test_mode`      varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Mode:\n\nupper case\n^((DEBUG)[1-8]|(PROD|FA|PROTO|GPS)[0-8]|(CDOFA)[0-7]|MCVT)$',
    `username`       varchar(35) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test start username',
    `deviation`      varchar(16) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Deviation Number',
    `testr1name`     varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 1 name',
    `testr1`         varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 1',
    `testr2name`     varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 2 name',
    `testr2`         varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 2',
    `create_time`    datetime                               NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The record create time in DB',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci COMMENT ='Test Record';

/*
将first_pass 用视图保存起来。


*/
CREATE VIEW first_pass_record AS
SELECT t1.*
FROM test_record t1
         INNER JOIN
     (SELECT MIN(record_time) AS earliest_time,
             sernum,
             area
      FROM test_record
      GROUP BY sernum, area) t2 ON t1.record_time = t2.earliest_time
         AND t1.sernum = t2.sernum
         AND t1.area = t2.area;


select uuttype,
       area,
       sum(IF(test_result = 'P', 1, 0))         as 'pass_count',
       sum(IF(test_result = 'F', 1, 0))         as 'pass_count',
       sum(IF(test_result in ('P', 'F'), 1, 0)) as 'total_count'
from first_pass_record
group by uuttype, area;


SELECT distinct sernum
FROM first_pass_record t1
where exists(select * from first_pass_record t2 where t1.sernum = t2.sernum and t2.test_result = 'F');

SELECT uuttype, count(distinct sernum) as 'pass_count'
FROM first_pass_record t1
where not exists(select * from first_pass_record t2 where t1.sernum = t2.sernum and t2.test_result = 'F')
group by uuttype;


SELECT uuttype,
       COUNT(DISTINCT sernum) AS total_count,
       SUM(CASE WHEN all_pass = 1 THEN 1 ELSE 0 END) AS pass_count,
       SUM(CASE WHEN only_one_fail = 1 THEN 1 ELSE 0 END) AS fail_count
FROM (
  SELECT sernum, uuttype,
         MAX(CASE WHEN area = 'PCBFT' AND test_result = 'P' THEN 1 ELSE 0 END) AS ft_pass,
         MAX(CASE WHEN area = 'PCB2C' AND test_result = 'P' THEN 1 ELSE 0 END) AS c_pass,
         MAX(CASE WHEN area = 'PCBST' AND test_result = 'P' THEN 1 ELSE 0 END) AS st_pass,
         MAX(CASE WHEN area = 'PCBFT' AND test_result = 'F' THEN 1 ELSE 0 END) AS ft_fail,
         MAX(CASE WHEN area = 'PCB2C' AND test_result = 'F' THEN 1 ELSE 0 END) AS c_fail,
         MAX(CASE WHEN area = 'PCBST' AND test_result = 'F' THEN 1 ELSE 0 END) AS st_fail,
         IF(ft_fail + c_fail + st_fail = 1 AND ft_pass + c_pass + st_pass = 0, 1, 0) AS only_one_fail,
         IF(ft_fail + c_fail + st_fail = 0 AND ft_pass + c_pass + st_pass = 3, 1, 0) AS all_pass
  FROM demo3.first_pass_record
  GROUP BY sernum, uuttype
) AS uut_summary
GROUP BY uuttype;
