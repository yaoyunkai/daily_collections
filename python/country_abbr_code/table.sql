create table country_abbr_code
(
    id           int auto_increment primary key,
    code2        char(2)     not null,
    code3        char(3)     not null,
    num_code     char(3)     not null comment '数字代码',
    zh_name      varchar(64) not null,
    en_name      varchar(64) not null,
    en_full_name varchar(64) not null
)
    comment 'ISO 3166-1';

insert into country_abbr_code (zh_name, en_name, en_full_name, code2, code3, num_code)
values ('', '', '', '', '', '')
