create table github_repo
(
    id               int          not null auto_increment primary key,
    `name`           varchar(100) not null comment 'repo name',
    full_name        varchar(100) not null,
    private          tinyint(1)   not null, -- ture or false
    owner_id         int          not null comment 'this is a fk for github_user',
    html_url         varchar(255) not null,
    `description`    text         not null,
    fork             tinyint(1)   not null,
    url              varchar(255) not null,
    branches_url     varchar(255) not null,
    tags_url         varchar(255) not null,
    languages_url    varchar(255) not null,
    commits_url      varchar(255) not null,
    created_at       datetime     not null,
    updated_at       datetime     not null,
    pushed_at        datetime     not null,
    git_url          varchar(255) not null,
    ssh_url          varchar(255) not null,
    clone_url        varchar(255) not null,
    homepage         varchar(255) not null,
    stargazers_count int          not null,
    watchers_count   int          not null,
    forks_count      int          not null,
    `language`       varchar(100),
    archived         tinyint(1)   not null,
    disabled         tinyint(1)   not null,
    visibility       varchar(255) not null
)
    comment 'GitHub Repository';

create table guthub_repo_topic_rel
(
    id           int auto_increment primary key,
    repo_id      int                                not null,
    topic_id     int                                not null,
    topic_name   varchar(64)                        not null,
    created_time datetime default CURRENT_TIMESTAMP not null
);

create table github_topic
(
    id           int auto_increment primary key,
    topic        varchar(64)                        not null,
    created_time datetime default CURRENT_TIMESTAMP not null
);

create table github_user
(
    id         int          not null auto_increment primary key,
    login      varchar(100) not null comment 'username',
    avatar_url varchar(255) not null,
    url        varchar(255) not null,
    html_url   varchar(255) not null,
    repos_url  varchar(255) not null,
    type       varchar(20)  not null comment 'User Type',
    site_admin tinyint(1)   not null -- true or false
);

delete from guthub_repo_topic_rel where repo_id = %s