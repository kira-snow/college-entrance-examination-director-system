# -*- coding: utf-8 -*-
import scrapy
import traceback
import os
import re
import copy
from gaokaospider.items import GaokaospiderItem, LinespiderItem, SchoolInfoItem,SegmentsItem
from gaokaospider.settings import LEVEL_DICT,WL_DICT,YEARS_START,SCHOOL_INFO
from openpyxl import Workbook

class BenkeSpider(scrapy.Spider):
    name = 'benke'

    def start_requests(self):
        url = 'http://www.sxkszx.cn/news/ptgk/index.html'
        yield scrapy.Request(url, callback=self.parse)
        if SCHOOL_INFO:
            url='https://gaokao.chsi.com.cn/sch/search.do?searchType=1&start=0'
            yield scrapy.Request(url, callback=self.parse_school_info_all)

    def parse(self, response):
        ## //*[@id="table1"]/tbody/tr[2]/td/table[2]/tbody/tr[12]/td[1]/a/span 山西省2019年普通高校招生专科（高职）理工类院校投档线 山西省2014年普通高校招生本科第二批A类院校投档线 山西省2014年普通高校招生专科院校（理工类）投档线 山西省2020年普通高校招生第一批本科A1类院校投档线
        self.logger.info("Get page: " + response.url)
        for tr in response.xpath('//span[re:test(text(),"山西省\d{4}年普通高校招生.*院校投档线")]'):
            title = tr.xpath('./text()').get()
            self.logger.info("Find title: " + title)
            # if not re.search(r'A1',title):
            #     continue
            year = int(re.search(r'\d{4}', title).group() )
            if year > YEARS_START-1:
                try:
                    href = tr.xpath('../@href').get()
                    href = 'http://www.sxkszx.cn'+href
                    yield scrapy.Request(href, callback=self.parse_xian) 
                except Exception as e:
                    self.logger.error(traceback.format_exc())
        ## 山西省2019年普通高校招生本科录取最低控制分数线(不含二C）公告
        # 我省2019年普通高校招生第二批本科C类院校最低控制分数线划定
        # 我省2019年普通高校招生专科（高职）录取最低控制分数线划定
        for tr in response.xpath('//span[re:test(text(),".*省\d{4}年普通高校招生.*最低控制分数线")]'):
            title = tr.xpath('./text()').get()
            self.logger.info("Find title: " + title)
            year = int(re.search(r'\d{4}', title).group() )
            if year > YEARS_START-1:
                try:
                    href = tr.xpath('../@href').get()
                    href = 'http://www.sxkszx.cn'+href
                    yield scrapy.Request(href, callback=self.parse_line) 
                except Exception as e:
                    self.logger.error(traceback.format_exc())
        # 2020年山西省普通高考成绩分段统计表
        # 2017年山西省高考成绩分段统计表
        # 2016年山西省高考成绩分段统计表
        for tr in response.xpath('//span[re:test(text(),"\d{4}年山西省.*高考成绩分段统计表")]'):
            title = tr.xpath('./text()').get()
            self.logger.info("Find title: " + title)
            year = int(re.search(r'\d{4}', title).group() )
            if year > YEARS_START-1:
                try:
                    href = tr.xpath('../@href').get()
                    href = 'http://www.sxkszx.cn'+href
                    yield scrapy.Request(href, callback=self.parse_segment) 
                except Exception as e:
                    self.logger.error(traceback.format_exc())
        ## 时间 //*[@id="table1"]/tbody/tr[2]/td/table[2]/tbody/tr[60]/td[2]
        year_label = response.xpath('//td[re:test(text(),"\[\d{4}年\d{1,2}月\d{1,2}日\]")]/text()').getall()[-1]
        if year_label:
            year = re.search(r'\d{4}', year_label).group()
            if int(year)>YEARS_START-1:
                ## 下一页//*[@id="table1"]/tbody/tr[2]/td/div/a[36]
                index_label = response.url.split("/")[-1].split(".")[0]
                if index_label == 'index':
                    next_url = 'http://www.sxkszx.cn/news/ptgk/index_2.html'
                else:
                    index = int(re.search(r'\d+$', index_label).group())
                    next_url = 'http://www.sxkszx.cn/news/ptgk/index_' + str(index+1) + '.html'
                yield scrapy.Request(next_url, callback=self.parse) 

    def parse_xian(self, response):
        ## //*[@id="NewsTitle"] 山西省2019年普通高校招生专科（高职）理工类院校投档线 山西省2019年普通高校招生第二批本科A类院校投档线 山西省2019年普通高校招生本科第二批A类院校投档线
        title = response.xpath('//h1[@id="NewsTitle"]/text()').get()
        self.logger.info("Get title: " + title)
        year = re.search(r'\d{4}', title).group()
        benke_en = re.search(r'本科',title)
        zhuan_en = re.search(r'专科',title)
        guantong_en = re.search(r'高本贯通',title)
        if benke_en:
            piyi_en = re.search(r'第一批',title)
            if piyi_en:
                lev1b = re.search(r'B',title)
                lev1a = re.search(r'A类',title)
                lev1a1 = re.search(r'A1',title)
                if lev1b:
                    level = LEVEL_DICT['1b']
                elif lev1a:
                    level = LEVEL_DICT['1a']
                elif lev1a1:
                    level = LEVEL_DICT['1a1']
            else:
                lev2a = re.search(r'A',title)
                lev2b = re.search(r'B',title)
                lev2c = re.search(r'C',title)
                if lev2a:
                    level = LEVEL_DICT['2a']
                elif lev2b:
                    level = LEVEL_DICT['2b']
                elif lev2c:
                    level = LEVEL_DICT['2c']
        elif zhuan_en:
            level = LEVEL_DICT['专']
        elif guantong_en:
            level = LEVEL_DICT['高本贯通']
        # self.logger.info("Get year: " + year+ ', ' + str(level) )
        if zhuan_en:
            ## //*[@id="newsbody_class"]/div[2]/table/tbody/tr[1]/td[1]/div/strong/span
            # self.logger.info(response.xpath('//span[re:test(text(),"院校代码")]/../../../../../tr')[1].get())
            item_all = response.xpath('//span[re:test(text(),"代码")]/../../../../../tr')[1:]
            try:
                item = GaokaospiderItem()
                item['level'] = level
                item['year'] = int(year)
                item['wl'] = WL_DICT[item_all[1].xpath('./td[3]/div/span/text()').get()]
                for tr in item_all:       
                    ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[2]/td[1]/div/span
                    item['id'] = int(tr.xpath('./td[1]/div/span/text()').get())
                    ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[2]/td[2]/div/span
                    item['school'] = ''
                    for school_name in tr.xpath('./td[2]/div/span'):
                        item['school'] = item['school'] + school_name.xpath('./text()').get()
                    item['score'] = int(float(tr.xpath('./td[5]/div/span/text()').get()))
                    # self.logger.info(item )
                    yield item
            except Exception as e:
                self.logger.error("url=" + response.url + "\n" + traceback.format_exc())
        elif benke_en:
            for item_first in response.xpath('//span[re:test(text(),"院校代码")]'): ## 院校
                item_all = item_first.xpath('../../../../../tr')[1:]
                try:
                    item = GaokaospiderItem()
                    item['level'] = level
                    item['year'] = int(year)
                    item['wl'] = WL_DICT[item_all[1].xpath('./td[3]/div/span/text()').get()]
                    for tr in item_all:       
                        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[2]/td[1]/div/span
                        item['id'] = int(tr.xpath('./td[1]/div/span/text()').get())
                        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[2]/td[2]/div/span
                        item['school'] = ''
                        for school_name in tr.xpath('./td[2]/div/span'):
                            item['school'] = item['school'] + school_name.xpath('./text()').get()
                        item['score'] = int(float(tr.xpath('./td[5]/div/span/text()').get()))
                        # self.logger.info(item )
                        yield item
                except Exception as e:
                    self.logger.error("url=" + response.url + "\n" + traceback.format_exc())
                    
    def parse_line(self, response):
        ## //*[@id="newsbody_class"]/div[5]
        ## /html/body/div[2]/table/tbody/tr[2]/td/div/div/div/div/div[2]/div[3]/div[5]/strong/span
        ## //*[@id="newsbody_class"]/div[5]/strong/span
        ## //*[@id="newsbody_class"]/div[5]/span[2] 518
        ## //*[@id="newsbody_class"]/div[5]/span[4] 460
        ## //*[@id="newsbody_class"]/div[6]/span[2] 
        # //*[@id="newsbody_class"]/div[6]/span[2]
        title = response.xpath('//h1[@id="NewsTitle"]/text()').get()
        ## 山西省2019年普通高校招生本科录取最低控制分数线(不含二C）公告
        # 我省2019年普通高校招生第二批本科C类院校最低控制分数线划
        # 我省2019年普通高校招生专科（高职）录取最低控制分数线划定
        self.logger.info("Get title: " + title)
        year = re.search(r'\d{4}', title).group()
        self.logger.info("year: " + year)
        try:
            if re.search(r'不含二C', title):
                ws_all = response.xpath('//*[@id="newsbody_class"]/div[5]')
                lg_all = response.xpath('//*[@id="newsbody_class"]/div[6]')
                item = LinespiderItem()
                item['year'] = int(year)
                item['type'] = '常规'
                item['level'] = '1'
                item['wl'] = '文史'
                item['score'] = ws_all.xpath('./span[2]/text()').get()
                yield copy.deepcopy(item)
                item['level'] = '2'
                item['score'] = ws_all.xpath('./span[4]/text()').get()
                yield copy.deepcopy(item)
                item['wl'] = '理工'
                item['level'] = '1'
                item['score'] = lg_all.xpath('./span[2]/text()').get()
                yield copy.deepcopy(item)
                item['level'] = '2'
                item['score'] = lg_all.xpath('./span[4]/text()').get()
                yield copy.deepcopy(item)
            elif re.search(r'第二批本科C类院校', title):
                # //*[@id="newsbody_class"]/div[3]/span[2]   文史
                # //*[@id="newsbody_class"]/div[3]/span
                # //*[@id="newsbody_class"]/div[3]/font
                # //*[@id="newsbody_class"]/div[4]/span[2]   理工
                item = LinespiderItem()
                item['year'] = int(year)
                item['type'] = '常规'
                item['level'] = '2c'
                item['wl'] = '文史'
                item['score'] = response.xpath('//*[@id="newsbody_class"]/div[3]/span[2]/text()').get()
                yield copy.deepcopy(item)
                item['wl'] = '理工'
                item['score'] = response.xpath('//*[@id="newsbody_class"]/div[4]/span[2]/text()').get()
                yield copy.deepcopy(item)
            elif re.search(r'专科', title):
                # //*[@id="newsbody_class"]/div[3]/span[2]  文史
                # //*[@id="newsbody_class"]/div[4]/span[2]  理工
                item = LinespiderItem()
                item['year'] = int(year)
                item['type'] = '常规'
                item['level'] = '专'
                item['wl'] = '文史'
                item['score'] = response.xpath('//*[@id="newsbody_class"]/div[3]/span[2]/text()').get()
                yield copy.deepcopy(item)
                item['wl'] = '理工'
                item['score'] = response.xpath('//*[@id="newsbody_class"]/div[4]/span[2]/text()').get()
                yield copy.deepcopy(item)

        except Exception as e:
            self.logger.error(traceback.format_exc())

    def parse_segment(self, response):
        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[3]/td[1]/div/span 641
        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[3]/td[3]/div/span 12
        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[3]/td[5]/div/span 554
        ## //*[@id="newsbody_class"]/div[3]/table/tbody/tr[3]/td[7]/div/span 4099
        ## //*[@id="newsbody_class"]/div[6]/table/tbody/tr[3]/td[1]/div/span 696
        title = response.xpath('//h1[@id="NewsTitle"]/text()').get()
        self.logger.info("Get title: " + title)
        year = re.search(r'\d{4}', title).group()
        self.logger.info("year: " + year)
        index=1
        for table in response.xpath('//table[@border="1"]'):
            if index==1:
                wl='文史'
            elif index==2:
                wl='理工'
            for tr in table.xpath('./tbody/tr')[1:]:
                try:
                    item = SegmentsItem()
                    item['year'] = int(year)
                    item['wl'] = wl
                    item['score'] = tr.xpath('./td[1]/div/span/text()').get()
                    item['ranking'] = tr.xpath('./td[3]/div/span/text()').get()
                    yield copy.deepcopy(item)
                    if item['year']>=2019:
                        item['score'] = tr.xpath('./td[5]/div/span/text()').get()
                        item['ranking'] = tr.xpath('./td[7]/div/span/text()').get()
                        if item['score']:
                            yield copy.deepcopy(item)
                    else:
                        item['score'] = tr.xpath('./td[4]/div/span/text()').get()
                        item['ranking'] = tr.xpath('./td[6]/div/span/text()').get()
                        if item['score']:
                            yield copy.deepcopy(item)
                except Exception as e:
                    self.logger.error(traceback.format_exc())
            index=index+1
                            
    def parse_school_info_all(self, response):
        self.logger.info("Get page: " + response.url + ', encoding:' + response.encoding)
        response.body.decode(response.encoding)
        # with open('test.html','w', encoding=response.encoding) as f:
        #     f.write(response.text)
        # self.logger.info("-------------- h1 : " + str(response.xpath('//h1/text()').get()))
        # /html/body/div[2]/div[3]/div/table/tbody/tr[2]
        for tr in response.css('table').css('tr')[1:]:  ##xpath('//table/tbody/tr')[1:]:
            try:
                item = SchoolInfoItem()
                item['name'] = self.get_name(tr.xpath('./td[1]'))
                item['province'] = tr.xpath('./td[2]/text()').get().strip()
                item['department'] = tr.xpath('./td[3]/text()').get().strip()
                item['type'] = tr.xpath('./td[4]/text()').get().strip()
                item['level'] = tr.xpath('./td[5]/text()').get().strip().strip('"')
                item['yldx'] = self.if_has(tr.xpath('./td[6]'))
                item['ylxk'] = self.if_has(tr.xpath('./td[7]'))
                item['yjsy'] = self.if_has(tr.xpath('./td[8]'))
                # print('name:'+item['name']+', province'+item['province']+
                # ',department:'+item['department']+', type'+item['type']+
                # ',level:'+item['level']+', yldx'+item['yldx']+
                # ',ylxk:'+item['ylxk']+', yjsy'+item['yjsy'])
                yield item
            except Exception as e:
                self.logger.error(traceback.format_exc())
        ## /html/body/div[2]/div[3]/div/div/div/form/ul/li[@class="lip selected"]/following-sibling::li[1]
        # /a/@href
        next_li = response.xpath('//li[@class="lip selected"]/following-sibling::li[@class="lip "]')
        if next_li:
            # print('next url: ' + next_li.xpath('./a/@href').get())
            next_url = 'https://gaokao.chsi.com.cn' + next_li[0].xpath('./a/@href').get()
            yield scrapy.Request(next_url, callback=self.parse_school_info_all) 

    def if_has(self, response):
        try:
            ttxt = response.xpath('./i/text()').get().strip()
            if ttxt:
                return '1'
            else:
                return '0'
        except Exception as e:
            return '0'
            
    def get_name(self, response):
        try:
            ttxt = response.xpath('./a/text()').get().strip()
            return ttxt
        except Exception as e:
            return response.xpath('./text()').get().strip()

