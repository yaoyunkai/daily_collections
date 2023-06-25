"""
Test record tables

sqlalchemy
fastapi
restframework
django ORM
MySQL

--------------------------------------

create table demo3.all_test_record
(
    tid          int auto_increment comment '数据库主键' primary key,
    tst_id       datetime    not null comment 'Test Id',
    record_time  datetime    not null comment 'test record time',
    sernum       varchar(40) not null comment '序列号',
    uuttype      varchar(40) not null comment 'UUTTYPE',
    test_area    varchar(20) not null comment '测试工站',
    test_result  char        not null comment '最终测试结果: S: Start A: ADT Sampling P: Passed F: Failed',
    run_time     int         not null comment '测试所用时间(单位:秒)',
    failure_item varchar(50) not null comment '测试failure item',
    machine      varchar(20) not null comment '测试服务器',
    container    varchar(40) not null comment '测试容器',
    test_user    varchar(35) not null comment '开始测试的用户/员工',
    test_mode    varchar(10) not null comment '测试模式: PROD: 生产模式 DEBUG: 调试模式',
    deviation    varchar(16) not null comment 'Deviation',
    testr1name   varchar(50) not null comment 'TE String Name 1',
    testr1       varchar(50) not null comment 'TE String 1',
    testr2name   varchar(50) not null comment 'TE String Name 2',
    testr2       varchar(50) not null comment 'TE String 2',
    testr3name   varchar(50) not null comment 'TE String Name 3',
    testr3       varchar(50) not null comment 'TE String 3'
)
    comment '测试记录';




"""
