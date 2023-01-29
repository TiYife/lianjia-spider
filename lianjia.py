from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime
import json

now_time = datetime.datetime.now()

# header = {
#     'cookie': 'digv_extends=%7B%22utmTrackId%22%3A%2221583074%22%7D; lianjia_ssid=20ce27d2-0b3c-4fe3-bfd0-db244126430f; lianjia_uuid=f6b954f7-eede-4fa0-b8d7-c8653bb53559; UM_distinctid=176fc1543633db-0076bba923e67d-15336251-13c680-176fc15436470b; CNZZDATA1255849469=1508080472-1610546903-https%253A%252F%252Fwww.baidu.com%252F%7C1610546903; CNZZDATA1254525948=1891745129-1610546145-https%253A%252F%252Fwww.baidu.com%252F%7C1610546145; CNZZDATA1255633284=1321632851-1610545633-https%253A%252F%252Fwww.baidu.com%252F%7C1610545633; CNZZDATA1255604082=1055813061-1610543352-https%253A%252F%252Fwww.baidu.com%252F%7C1610543352; _smt_uid=5ffeff4c.443cf707; _jzqa=1.2188110743361325600.1610547021.1610547021.1610547021.1; _jzqc=1; _jzqy=1.1610547021.1610547021.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6.-; _jzqckmp=1; _qzjc=1; sajssdk_2015_cross_new_user=1; _ga=GA1.2.2079254513.1610547023; _gid=GA1.2.1673135691.1610547023; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1610547030; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22176fc154508516-03a567f6c56a1d-15336251-1296000-176fc154509a46%22%2C%22%24device_id%22%3A%22176fc154508516-03a567f6c56a1d-15336251-1296000-176fc154509a46%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wyshenzhen%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D; select_city=440300; _qzja=1.515814144.1610547021015.1610547021015.1610547021015.1610547122464.1610547177164.0.0.0.9.1; _qzjb=1.1610547021015.9.0.0.0; _qzjto=9.1.0; _jzqb=1.12.10.1610547021.1; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1610547177; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiYWJlOGU2MzFmNmRmZTI0MzM3Y2M0MTc0NmM2MWEzMjk2Yjg0ZDM5MGI0ODdjZGU2ZWE5YmMyMjhjMTMxNDE1MjVlNTlkOTE3N2QwYTFhMDk3ZjMwZTFmYTVlNGUzNTZjZjhiODQ2MjNjNmViNWViOTJkZjU2YmU0NzViY2Q4ZmMwYWRkM2MwYjFkMGQzODI3NGU5NzE2MDQ0ZmVjZTFjYWMxYTNjZjI0NWViNjdjNWI5Y2RlNWNlZmNkNjc1NDU5OGNmZTAyZTg3NDIzY2U3YWFhMjg5MDM4NmFhYzdjZDhjZTM5NzczZDBkMjVkOWY3NzhiYjMzZDcwZDVmMTllYTI2MGIwNTVmNjY5OGEyM2Y5OTUwOGJjM2I5ZGI4MTc0Yjc2ZjhhZjBkNmE4NWMxOGQ2OWU4ZWZmNzFmYWIwZDQzYjA0MGZiMWZlNGI2YzhmNmZhMTI1Y2ExMmY1YTFhOFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIyZmVjM2U2MFwifSIsInIiOiJodHRwczovL3N6LmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
# }

header = {
    # 'cookie': 'ab_jid=25468da2372c74c078e6c4a6731f34b72be6; ab_bid=e6c4a6731f34b72be70c2d74891e135ba75e; ab_sr=1.0.1_ZmZkY2YwYjFlYzJmMDhhYWIzMGQ5Nzc4N2VkZTE1ZDc4YTdkZGE1YzZjMjgwMTBmMWM0ZjRlYzM0YzNjYzFmOWM2NGVmZTUyY2Y0NzA5NGMyN2MzYThiZDhmYzM2MjNlNzkzZjllN2ExYTBjNDYyZTBiNTAxNWJiODg3ZWViNTEyNDQ3ZmE2YjBkN2NmOWI2NTMwZDE1NWNjNmIxN2I3MQ==',
    'cookie': 'select_city=110000; lianjia_ssid=b77fe47f-0fbc-4202-b869-eabddf8212bb; lianjia_uuid=bc5af399-fc43-4902-87ce-d388e8b4aeb1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1674836801; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1674913015; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22185f40d773a42-088a1e05d61e2b-c5c5429-3686400-185f40d773b117e%22%2C%22%24device_id%22%3A%22185f40d773a42-088a1e05d61e2b-c5c5429-3686400-185f40d773b117e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; sajssdk_2015_cross_new_user=1; _smt_uid=63d3fb41.26a9f58d; _jzqa=1.1182282248384110800.1674836801.1674836801.1674911816.2; _jzqc=1; _jzqckmp=1; _qzja=1.968983847.1674836801542.1674836801543.1674911816452.1674913005294.1674913015318.0.0.0.7.2; _qzjc=1; _qzjto=7.2.0; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMWI5YTdlNWVhYzBlNzk0MjYwNzZmNmY0NDU0Yzc3YzkxODBiZmEzODIyZGM5ZDY4MmU0Y2VlNTZlNzQ5ZGE2OWE3YTQ1NGFkZGM3OGJkYzQ4NzczMDUzNWI1ZDcxYmZmZDM1YjdjNmM4ODNiZmZiMzdmMjE1ZWY2MjEyYThkYjBiNzViNTAyYTVkNGRlMmU0OGY3ODc3N2E4ZDhkZGQ5YTljZGQyYTllMmIzMmM3NDg5ZDY2NTg5NjY1NDc4ZmE1OTg1ZDkxOWYyMTM2NDExZWEyNTA5YWIzYjJjZTJhYzhiMzU0YjgxZTViZDQ5YmFhYTNlYTRkZTUwYTFmMmQ1Y1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJhMWFlMWJiMlwifSIsInIiOiJodHRwczovL2JqLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=; _ga=GA1.2.1795244806.1674836804; _gid=GA1.2.1609776575.1674836804; crosSdkDT2019DeviceId=-vjpte7-oljlk7-q9okj6lrmmy2onf-fh630ejhg; login_ucid=2000000303706489; lianjia_token=2.0010dcac34786df0a10171850594cb2c9c; lianjia_token_secure=2.0010dcac34786df0a10171850594cb2c9c; security_ticket=C7lGZT5ffhdQGVDDfpFlMI3YesPKl6z6EAStaBWp+11OcDSe6WzAF3ArQH8dAJAOour0Sk3Xdr1OFqRIBG7+BaEsdbYMpnkUR1qRz+oVqafPo0D+Fupk2fwDzn/QAh5ZGHZKyX7zfo76DwpwKd7zKXXoanMLRKe2D13DyxMYcyA=; _qzjb=1.1674911816452.6.0.0.0; _jzqb=1.6.10.1674911816.1; _jzqx=1.1674911816.1674911816.1.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/.-; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

out = open('csv/lianjia_shenzhen_second_hand.csv', 'w', newline='')
csv_write = csv.writer(out, dialect='excel')

table_head = ['总价', '单价', '小区名', '位置',
    '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例', '配备电梯',
    '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件', '房协编码',
    '链接', '时间']

# regions = ['luohuqu', 'futianqu', 'nanshanqu', 'yantianqu', 'baoanqu', 'longgangqu', 'longhuaqu', 'guangmingqu', 'pingshanqu', 'dapengxinqu', 'dapengbandao']
# prices = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']

regions = ['haidianqu']
prices = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']

csv_write.writerow(table_head)

for re in regions:
    for pr in prices:
        page = 1
        # todo 代理设置
        while True:
            # url = 'https://sz.lianjia.com/ershoufang/pg' + str(page) + '/'
            # url = 'https://bj.lianjia.com/ershoufang/' + re + '/pg' + str(page) + pr + '/'
            url = 'https://bj.lianjia.com/chengjiao/' + re + '/pg' + str(page) + pr + '/'
            response = requests.get(url, headers=header)

            soup = BeautifulSoup(response.text, 'html.parser')
            page_div = soup.find('div', class_="page-box house-lst-page-box")
            page_str = page_div.attrs['page-data']
            page_obj = json.loads(page_str)
            page_total = page_obj['totalPage']

            div_item = soup.find_all('div', class_="item")
            for item in div_item:
                try:
                    write_info = []
                    a_title = item.find('a', class_="title")
                    href = a_title.get('href')
                    detail = requests.get(href, headers=header)
                    detail_soup = BeautifulSoup(detail.text, 'html.parser')
                    total_price = detail_soup.find('span', class_="total").text
                    unit_price = detail_soup.find('span', class_="unitPriceValue").text
                    write_info.append(total_price)
                    write_info.append(unit_price)

                    community = detail_soup.find('div', class_="communityName")
                    community_name = community.find(name='a', attrs={'class': 'info'}).text
                    region = community.nextSibling.text
                    if region and len(region) >= 4:
                        region = region[4:]
                    write_info.append(community_name)
                    write_info.append(region)

                    # 基本信息
                    base_info = detail_soup.find('div', class_="base").find_all(name='li')
                    for base in base_info:
                        text = base.text
                        if text and len(text) >= 4:
                            text = text[4:]
                        write_info.append(text)
                    # 交易信息
                    transaction_info = detail_soup.find('div', class_="transaction").find_all(name='li')
                    for transaction in transaction_info:
                        tr_text = transaction.text
                        if tr_text and len(tr_text) >= 4:
                            tr_text = tr_text.replace('\n', '')
                            tr_text = tr_text[4:].strip()
                        write_info.append(tr_text)
                    write_info.append(href)
                    write_info.append(now_time)
                    csv_write.writerow(write_info)
                except:
                    print(item.text)
                # todo 下一页
            if page >= page_total:
                break
            page = page + 1
            print("region: " + re + ", price: " + pr + ', page: ' + str(page))
out.close()
i = 0
