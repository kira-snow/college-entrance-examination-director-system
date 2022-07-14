chcp 65001
echo call gaokao.gaokao_qry('2c', '理工', 0, 10, 2016, 2019) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 查询结果.xls
pause