drop database if exists sqldb;
create database sqldb;
use sqldb;

grant select, insert, update, delete on sqldb.* to 'mysqldb'@'localhost'
    identified by 'mysqldb';

create table users (
    `id` int(11) not null AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1 ;