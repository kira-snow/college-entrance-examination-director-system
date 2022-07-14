chcp 65001
echo call gaokao.gaokao_segment_qry('1b', '理工', 2020, 550, 5, 0) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 5501b查询结果.xls
pause