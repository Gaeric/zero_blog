-- schema.sql
-- initialization database
drop database if exists zero_blog;

create database zero_blog;

use zero_blog;

grant insert, delete, update, select on zero_blog.* to 'zero_blog'@'localhost' identified by 'zero_blog';

create table users (
  `id` varchar(50) not null,
  `email` varchar(50) not null,
  `passwd` varchar(50) not null,
  `admin` bool not null,
  `name` varchar(50) not null,
  `image` varchar(50) not null,
  `create_at` real not null,
  unique key `idx_eamil` (`email`),
  key `idx_create_at` (`create_at`),
  primary key (`id`)
  ) engine=innodb default charset=utf8;

create table blogs (
  `id` varchar(50) not null,
  `user_id` varchar(50) not null,
  `user_name` varchar(50) not null,
  `user_image` varchar(500) not null,
  `name` varchar(50) not null,
  `summary` varchar(200) not null,
  `content` mediumtext not null,
  `create_at` real not null,
  key `id_create_at` (`create_at`),
  primary key (`id`)
  ) engine=innodb default charset=utf8;

create table coments (
  `id` varchar(50) not null,
  `blog_id` varchar(50) not null,
  `user_id` varchar(50) not null,
  `user_name` varchar(50) not null,
  `user_image` varchar(500) not null,
  `content` mediumtext not null,
  `create_at` real not null,
  key `idx_create_at` (`create_at`),
  primary key (`id`)
  ) engine=innodb default charset=utf8;
