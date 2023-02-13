CREATE TABLE `test_record` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `tst_id` datetime NOT NULL COMMENT 'Test ID\n\nunique togther with sernum',
  `bf_status` tinyint NOT NULL COMMENT 'back flush status:\n\n0 - no back flush\n1- back flush status with *',
  `record_time` datetime NOT NULL COMMENT 'Record Time: Pass time',
  `sernum` varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Serial Number \n\nupper case, length 40',
  `uuttype` varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'UUT Type\n\nlength 40, upper case',
  `area` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Area\n\nupper case, length 20',
  `test_result` char(1) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'final test result\n\noptional: \nP - passed\nF - failed\nA - adt sampling\nS - start ',
  `run_time` int NOT NULL DEFAULT '0' COMMENT 'Total Run time, unit is second',
  `test_failure` varchar(40) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'if test result is F, the column record test failed\n\nupper case',
  `test_server` varchar(20) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Machine\n\nlower case',
  `test_container` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Container\n\nlength 50, no modify',
  `test_mode` varchar(10) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test Mode:\n\nupper case\n^((DEBUG)[1-8]|(PROD|FA|PROTO|GPS)[0-8]|(CDOFA)[0-7]|MCVT)$',
  `username` varchar(35) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Test start username',
  `deviation` varchar(16) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'Deviation Number',
  `testr1name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 1 name',
  `testr1` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 1',
  `testr2name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 2 name',
  `testr2` varchar(64) COLLATE utf8mb4_general_ci NOT NULL COMMENT 'TE String 2',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'The record create time in DB',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Test Record';


select * from test_record where area = 'PCB2C' and record_time between '2021-10-01 00:00:00' and '2021-10-05 23:59:59';