CREATE DATABASE if not EXISTS gaokao;

use gaokao;

drop procedure if exists gaokao_qry;
delimiter $
create procedure gaokao_qry(
    in _level varchar(10) character set utf8,
    in _wl varchar(10) character set utf8,
    in _score_begin float ,
    in _score_end float,
    in _year_begin int,
    in _year_end int
)
begin
    declare _year_now int;
    drop TEMPORARY TABLE IF EXISTS tempLevelLine;
    drop TABLE IF EXISTS tempResult;
    drop TEMPORARY TABLE IF EXISTS tempResultAll;

    create TEMPORARY table tempLevelLine ( select score, year from levelLines where level=_level and wl = _wl and type = '常规');

    create table tempResult(
    `schoolId` varchar(10) DEFAULT NULL,
    `name` varchar(100) NOT NULL,
    `province` varchar(100) NOT NULL,
    `department` varchar(100) NOT NULL,
    `type` varchar(10) NOT NULL,
    `yldx` char(1) DEFAULT NULL,
    `ylxk` char(1) DEFAULT NULL,
    `yjsy` char(1) DEFAULT NULL,
    `level` varchar(40) NOT NULL,
    `wl` varchar(10) NOT NULL,
    PRIMARY KEY ( `name`)
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

    create TEMPORARY table tempResultAll ( 
    select a.*, (a.score - c.score) as xiancha from schools a, tempLevelLine c 
    where a.level=_level and wl = _wl and a.score - c.score >= _score_begin and a.score - c.score <= _score_end 
    and a.year=c.year and a.year>=cast(_year_begin as char) and a.year<=cast(_year_end as char)
    order by a.score - c.score asc, a.year desc); 

    insert into tempResult(name, province, department, type, yldx, ylxk, yjsy, level, wl) 
        select b.name, province, department, type, yldx, ylxk, yjsy, _level, _wl from tempResultAll a, schoolInfo b
        where a.name = b.name 
        and not exists(select 1 from tempResult where name=a.name)
        group by a.name
        order by a.xiancha asc, a.year desc;

    set _year_now = _year_begin;
    while _year_now<=_year_end do
        set @year_now_str = cast( _year_now as char);

        set @stmt_add_str = concat('alter table tempResult add y', @year_now_str, ' float');
        prepare stmt_add FROM @stmt_add_str;
        EXECUTE stmt_add ;

        set @stmt_update_str = concat('update tempResult a, tempResultAll b set a.y', @year_now_str, ' = b.xiancha, a.schoolId = b.schoolId where a.name=b.name and b.year=', @year_now_str);
        prepare stmt_update FROM @stmt_update_str;
        EXECUTE stmt_update;

        set _year_now = _year_now+1;
    end while;

    set @stmt_select_str = concat('select * from tempResult order by y', @year_now_str, ' asc');
    prepare stmt_select FROM @stmt_select_str;
    EXECUTE stmt_select;
    -- select * from tempResult;

    drop TEMPORARY TABLE IF EXISTS tempLevelLine;
    drop TABLE IF EXISTS tempResult;
    drop TEMPORARY TABLE IF EXISTS tempResultAll;
    DEALLOCATE PREPARE stmt_add;
    DEALLOCATE PREPARE stmt_update;
    DEALLOCATE PREPARE stmt_select;
    
end$
delimiter ;

drop procedure if exists gaokao_segment_qry;
delimiter $
create procedure gaokao_segment_qry(
    in _level varchar(10) character set utf8,
    in _wl varchar(10) character set utf8,
    in _year int,
    in _score float ,
    in _score_begin float ,
    in _score_end float
)
begin
    declare _year_now int;
    declare _ranking_now int;
    drop TEMPORARY TABLE IF EXISTS tempSegments;
    drop TEMPORARY TABLE IF EXISTS tempLevelLine;
    drop TABLE IF EXISTS tempResult;
    drop TEMPORARY TABLE IF EXISTS tempResultAll;

    select ranking into _ranking_now from segments where year=cast( _year as char) and wl = _wl and score=_score;
    create TEMPORARY table tempSegments(
        `year` varchar(10) NOT NULL,
        `score` varchar(10) NOT NULL,
        PRIMARY KEY ( `year`)
        )ENGINE=MyISAM DEFAULT CHARSET=utf8;

    set _year_now = 2016;
    while _year_now<=_year-1 do
        set @year_now_str = cast( _year_now as char);

        insert into tempSegments(score, year)
        select score, year from segments
        where wl = _wl 
        and ranking>=_ranking_now 
        and year=@year_now_str
        order by ranking limit 1;

        set _year_now = _year_now+1;
    end while;

    create TEMPORARY table tempLevelLine ( select score, year from levelLines where level=_level and wl = _wl and type = '常规');

    create table tempResult(
    `schoolId` varchar(10) DEFAULT NULL,
    `name` varchar(100) NOT NULL,
    `province` varchar(100) NOT NULL,
    `department` varchar(100) NOT NULL,
    `type` varchar(10) NOT NULL,
    `yldx` char(1) DEFAULT NULL,
    `ylxk` char(1) DEFAULT NULL,
    `yjsy` char(1) DEFAULT NULL,
    `level` varchar(40) NOT NULL,
    `wl` varchar(10) NOT NULL,
    PRIMARY KEY ( `name`)
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

    create TEMPORARY table tempResultAll ( 
    select a.*, (a.score - c.score) as xiancha from schools a, tempLevelLine c, tempSegments d 
    where a.level=_level and wl = _wl 
    and a.score >= d.score - _score_begin 
    and a.score <= d.score + _score_end 
    and a.year=c.year 
    and a.year=d.year
    order by a.score - c.score asc, a.year desc); 

    insert into tempResult(name, province, department, type, yldx, ylxk, yjsy, level, wl) 
        select b.name, province, department, type, yldx, ylxk, yjsy, _level, _wl from tempResultAll a, schoolInfo b
        where a.name = b.name 
        and not exists(select 1 from tempResult where name=a.name)
        group by a.name
        order by a.xiancha asc, a.year desc;

    set _year_now = 2016;
    while _year_now<=_year-1 do
        set @year_now_str = cast( _year_now as char);

        set @stmt_add_str = concat('alter table tempResult add y', @year_now_str, ' float');
        prepare stmt_add FROM @stmt_add_str;
        EXECUTE stmt_add ;

        set @stmt_update_str = concat('update tempResult a, tempResultAll b set a.y', @year_now_str, ' = b.xiancha, a.schoolId = b.schoolId where a.name=b.name and b.year=', @year_now_str);
        prepare stmt_update FROM @stmt_update_str;
        EXECUTE stmt_update;

        set _year_now = _year_now+1;
    end while;

    set @stmt_select_str = concat('select * from tempResult order by y', @year_now_str, ' asc');
    prepare stmt_select FROM @stmt_select_str;
    EXECUTE stmt_select;
    -- select * from tempResult;

    drop TEMPORARY TABLE IF EXISTS tempLevelLine;
    drop TABLE IF EXISTS tempResult;
    drop TEMPORARY TABLE IF EXISTS tempResultAll;
    DEALLOCATE PREPARE stmt_add;
    DEALLOCATE PREPARE stmt_update;
    DEALLOCATE PREPARE stmt_select;
    
end$
delimiter ;

drop procedure if exists gaokao_qry_all;
delimiter $
create procedure gaokao_qry_all(
    in _level varchar(10) character set utf8,
    in _wl varchar(10) character set utf8,
    in _year_begin int,
    in _year_end int
)
begin
    declare _year_now int;
    drop TABLE IF EXISTS tempResult;

    create table tempResult(
    `schoolId` varchar(10) NOT NULL,
    `name` varchar(100) NOT NULL,
    PRIMARY KEY ( `schoolId`,`name`)
    )ENGINE=MyISAM DEFAULT CHARSET=utf8;

    insert into tempResult(schoolId, name) 
        select schoolId, name from schools
        where level=_level and wl=_wl and year=cast( _year_end as char);

    set _year_now = _year_begin;
    while _year_now<=_year_end do
        set @year_now_str = cast( _year_now as char);

        set @stmt_add_str = concat('alter table tempResult add y', @year_now_str, ' float');
        prepare stmt_add FROM @stmt_add_str;
        EXECUTE stmt_add ;

        set @stmt_update_str = concat('update tempResult a, schools b set a.y', @year_now_str, ' = b.score where a.name=b.name and a.schoolId=b.schoolId and b.level=''', _level, ''' and b.wl=''', _wl, ''' and b.year=''', @year_now_str, '''');
        prepare stmt_update FROM @stmt_update_str;
        EXECUTE stmt_update;

        set _year_now = _year_now+1;
    end while;

    set @stmt_select_str = concat('select * from tempResult order by y', @year_now_str, ' asc');
    prepare stmt_select FROM @stmt_select_str;
    EXECUTE stmt_select;
    -- select * from tempResult;

    drop TABLE IF EXISTS tempResult;
    DEALLOCATE PREPARE stmt_add;
    DEALLOCATE PREPARE stmt_update;
    DEALLOCATE PREPARE stmt_select;
    
end$
delimiter ;