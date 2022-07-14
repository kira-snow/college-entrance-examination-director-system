CREATE DATABASE if not EXISTS gaokao;

use gaokao;

CREATE TABLE IF NOT EXISTS `schools`(
    `schoolId` varchar(10) NOT NULL,
    `name` varchar(100) NOT NULL,
    `year` varchar(10) NOT NULL,
    `level` varchar(40) NOT NULL,
    `wl` varchar(10) NOT NULL,
    `score` float NOT NULL,
    PRIMARY KEY ( `schoolId`, `year`, `level`, `wl` )
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `schoolinfo` (
  `name` varchar(100) NOT NULL,
  `province` varchar(100) NOT NULL,
  `department` varchar(100) NOT NULL,
  `type` varchar(10) NOT NULL,
  `level` varchar(10) NOT NULL,
  `yldx` char(1) DEFAULT NULL,
  `ylxk` char(1) DEFAULT NULL,
  `yjsy` char(1) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `levelLines`(
    `year` varchar(10) NOT NULL,
    `level` varchar(40) NOT NULL, -- 1a, 1a1, 1b, 2a, 2b, 2c, 专
    `wl` varchar(10) NOT NULL,    -- 文史, 理工
    `type` varchar(10) NOT NULL,  -- 常规, 艺术, 体育
    `score` float NOT NULL,
    PRIMARY KEY ( `year`, `level`, `wl`, `type` )
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `segments`(
    `year` varchar(10) NOT NULL,
    `wl` varchar(10) NOT NULL,    -- 文史, 理工
    `score` float NOT NULL,
    `ranking` int NOT NULL,
    PRIMARY KEY ( `year`, `wl`, `score` )
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

drop procedure if exists gaokao_process;
delimiter $
create procedure gaokao_process(
    in schoolId varchar(10),
    in name varchar(100),
    in year varchar(10),
    in level varchar(10),
    in wl varchar(10),
    in score float
)
begin
    insert into schools (`schoolId`, `name`, `year`, `level`, `wl`, `score`) VALUES (schoolId, name, year, level, wl, score);

end$
delimiter ;

insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2016','2c', '文史','常规',370 );
insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2016','2c', '理工','常规', 310);
insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2017','专', '文史','常规', 130);
insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2017','专', '理工','常规', 130);
insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2018','专', '文史','常规', 150);
insert into levelLines (`year`, `level`, `wl`, `type`, `score`) VALUES ('2018','专', '理工','常规', 150);