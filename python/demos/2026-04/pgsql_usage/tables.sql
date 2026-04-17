/*
tables DDL

*/


create table person
(
    id         serial                   not null primary key,
    name       char varying(50)         not null,
    gender     smallint                 not null,
    birthday   date,
    created_at timestamp with time zone not null default now()
);

create table post
(
    id         serial                   not null primary key,
    person_id  integer references person (id),
    tags       varchar(20)[]            not null default '{}',
    title      varchar(100)             not null,
    content    text,
    status     smallint                 not null,
    created_at timestamp with time zone not null default now()
);