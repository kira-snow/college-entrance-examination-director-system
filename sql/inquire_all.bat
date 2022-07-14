chcp 65001
echo call gaokao.gaokao_qry_all('1a', '理工',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020理工1a.xls
echo call gaokao.gaokao_qry_all('1a', '文史',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020文史1a.xls
echo call gaokao.gaokao_qry_all('1b', '理工',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020理工1b.xls
echo call gaokao.gaokao_qry_all('1b', '文史',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020文史1b.xls
echo call gaokao.gaokao_qry_all('1a1', '理工',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020理工1a1.xls
echo call gaokao.gaokao_qry_all('1a1', '文史',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020文史1a1.xls
echo call gaokao.gaokao_qry_all('2a', '理工',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020理工2a.xls
echo call gaokao.gaokao_qry_all('2a', '文史',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020文史2a.xls
echo call gaokao.gaokao_qry_all('2b', '理工',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020理工2b.xls
echo call gaokao.gaokao_qry_all('2b', '文史',2016, 2020) | mysql -uroot -p123456 | iconv -f utf-8 -t gb2312 > 2020文史2b.xls
pause