create table github_repo
(
    id               int          not null auto_increment primary key,
    `name`           varchar(100) not null comment 'repo name',
    full_name        varchar(100) not null,
    private          tinyint(1)   not null, -- ture or false

    owner_id         int          not null comment 'this is a fk for github_user',
    owner_login      varchar(100) not null,
    owner_html_url   varchar(255) not null,

    html_url         varchar(255) not null,
    `description`    text         not null,
    fork             tinyint(1)   not null,
    url              varchar(255) not null,
    languages_url    varchar(255) not null,
    created_at       datetime     not null,
    updated_at       datetime     not null,
    pushed_at        datetime     not null,
    ssh_url          varchar(255) not null,
    clone_url        varchar(255) not null,
    homepage         varchar(255) not null,
    stargazers_count int          not null,
    watchers_count   int          not null,
    forks_count      int          not null,
    `language`       varchar(100) not null,
    archived         tinyint(1)   not null,
    disabled         tinyint(1)   not null,
    visibility       varchar(255) not null,

    create_time      datetime     not null default current_timestamp,
    update_time      datetime     not null default current_timestamp on update current_timestamp
) comment 'GitHub Repository';

create table github_user
(
    id          int          not null auto_increment primary key,
    login       varchar(100) not null comment 'username',
    avatar_url  varchar(255) not null,
    url         varchar(255) not null,
    html_url    varchar(255) not null,
    repos_url   varchar(255) not null,
    type        varchar(20)  not null comment 'User Type',
    site_admin  tinyint(1)   not null, -- true or false

    create_time datetime     not null default current_timestamp,
    update_time datetime     not null default current_timestamp on update current_timestamp
);

create table github_repo_topic_rel
(
    repo_id     int                                not null,
    topic_name  varchar(64)                        not null,
    create_time datetime default CURRENT_TIMESTAMP not null,
    primary key (repo_id, topic_name)
) comment 'Repo and Topic Relationship';
