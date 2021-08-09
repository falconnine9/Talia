-- Guild tables
create table if not exists guilds (
    id bigint unsigned not null,
    prefix varchar(50) not null,
    ud_mode tinyint,
    constraint guilds_pk primary key (id)
);
create table if not exists dc (
    channel bigint unsigned not null,
    guild bigint unsigned not null,
    constraint dc_pk primary key (channel)
);
create table if not exists dco (
    pk_id bigint unsigned not null auto_increment,
    guild bigint unsigned not null,
    command varchar(50) not null,
    constraint dco_pk primary key (pk_id)
);
create table if not exists dcs (
    pk_id bigint unsigned not null auto_increment,
    guild bigint unsigned not null,
    service varchar(50) not null,
    constraint dcs_pk primary key (pk_id)
);
create table if not exists g_jobs (
    job_id bigint unsigned not null auto_increment,
    guild bigint unsigned not null,
    name varchar(75) not null,
    s_min integer unsigned not null,
    s_max integer unsigned not null,
    c_min integer not null,
    c_max integer not null,
    constraint g_jobs_pk primary key (job_id)
);
create table if not exists g_picks (
    pickaxe_id bigint unsigned not null auto_increment,
    guild bigint unsigned not null,
    name varchar(75) not null,
    speed tinyint not null,
    multiplier real not null,
    constraint g_picks_pk primary key (pickaxe_id)
);

-- User tables
create table if not exists users (
    id bigint unsigned not null auto_increment,
    guild bigint unsigned not null,
    user bigint unsigned not null,
    coins bigint unsigned not null,
    level integer unsigned not null,
    xp integer unsigned not null,
    multiplier real not null,
    commands bigint unsigned not null,
    constraint users_pk primary key (id)
);
create table if not exists u_jobs (
    user bigint unsigned not null,
    name varchar(75) not null,
    s_min integer unsigned not null,
    s_max integer unsigned not null,
    c_min integer not null,
    c_max integer not null,
    xp integer unsigned not null,
    level integer unsigned not null,
    constraint u_jobs_pk primary key (user)
);
create table if not exists u_picks (
    user bigint unsigned not null,
    name varchar(75) not null,
    speed tinyint not null,
    multiplier real not null,
    constraint u_picks_pk primary key (user)
);
create table if not exists relations (
    pk_id bigint unsigned not null auto_increment,
    user bigint unsigned not null,
    other bigint unsigned not null,
    r_type tinyint not null,
    constraint relations_pk primary key (pk_id)
);

-- Timers
create table if not exists cooldowns (
    cld_id bigint unsigned not null auto_increment,
    user bigint unsigned not null,
    time integer not null,
    constraint cooldowns_pk primary key (cld_id)
);
create table if not exists investments (
    user bigint unsigned not null,
    time integer not null,
    coins integer unsigned not null,
    failed tinyint not null,
    multi real,
    loss real,
    constraint investments_pk primary key (user)
);