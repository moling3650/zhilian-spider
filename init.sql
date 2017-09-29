SET NAMES utf8;

DROP DATABASE IF EXISTS ZhiLian;

CREATE DATABASE ZhiLian;

USE ZhiLian;

GRANT SELECT, INSERT, UPDATE, DELETE ON ZhiLian.* TO 'zl'@'localhost' IDENTIFIED BY 'zl-data';

DROP TABLE IF EXISTS jobs;

CREATE TABLE jobs (
    id char(32) not null,
    职位名称 varchar(255) default null,
    职位链接 varchar(255) default null,
    公司名称 varchar(255) default null,
    公司福利 varchar(255) default null,
    职位月薪 varchar(255) default null,
    工作地点 varchar(255) default null,
    发布日期 varchar(255) default null,
    工作性质 varchar(255) default null,
    工作经验 varchar(255) default null,
    最低学历 varchar(255) default null,
    招聘人数 varchar(255) default null,
    职位类别 varchar(255) default null,
    职位描述 text,
    详细工作地点 varchar(255) default null,
    公司规模 varchar(255) default null,
    公司性质 varchar(255) default null,
    公司行业 varchar(255) default null,
    公司主页 varchar(255) default null,
    公司地址 varchar(255) default null,
    primary key(id)
) ENGINE=innodb DEFAULT CHARSET=utf8;