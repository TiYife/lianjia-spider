from bs4 import BeautifulSoup
import requests
import csv
import time
import datetime
import json

now_time = datetime.datetime.now()

header = {
    'cookie': 'select_city=110000; lianjia_ssid=b77fe47f-0fbc-4202-b869-eabddf8212bb; lianjia_uuid=bc5af399-fc43-4902-87ce-d388e8b4aeb1; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1674836801; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1674918099; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22185f40d773a42-088a1e05d61e2b-c5c5429-3686400-185f40d773b117e%22%2C%22%24device_id%22%3A%22185f40d773a42-088a1e05d61e2b-c5c5429-3686400-185f40d773b117e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; sajssdk_2015_cross_new_user=1; _smt_uid=63d3fb41.26a9f58d; _jzqa=1.1182282248384110800.1674836801.1674911816.1674917982.3; _jzqc=1; _jzqckmp=1; _ga=GA1.2.1795244806.1674836804; _gid=GA1.2.1609776575.1674836804; crosSdkDT2019DeviceId=-vjpte7-oljlk7-q9okj6lrmmy2onf-fh630ejhg; _jzqx=1.1674911816.1674911816.1.jzqsr=clogin%2Elianjia%2Ecom|jzqct=/.-; _jzqb=1.6.10.1674917982.1; _gat=1; _gat_past=1; _gat_global=1; _gat_new_global=1; _gat_dianpu_agent=1; login_ucid=2000000303706489; lianjia_token=2.001176941d79c7c88800dbbd2c66cd76eb; lianjia_token_secure=2.001176941d79c7c88800dbbd2c66cd76eb; security_ticket=HUguQh5tRAbO0GF0lAeGR/4PWOYlVsTHpUvu/w3gHaT8DYTdnPw5Lrek9OLP7UOI4OPxWQt8skNiFPEiaAcfcj0JGswqaJ4azxx59MUgtRH3Qg73E3m9WHoIdjCdPaWidvADYCGDHLZT3DeCgeOKxTEbtmyyQQeHcV+cCkjJWLk=',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

out = open('csv/ershoufang.csv', 'w', newline='')
csv_write = csv.writer(out, dialect='excel')
#
# table_head = ['总价', '单价', '小区名', '位置',
#     '房屋户型', '所在楼层', '建筑面积', '户型结构', '套内面积', '建筑类型', '房屋朝向', '建筑结构', '装修情况', '梯户比例', '配备电梯',
#     '挂牌时间', '交易权属', '上次交易', '房屋用途', '房屋年限', '产权所属', '抵押信息', '房本备件', '房协编码',
#     '链接', '时间']
#
# # regions = ['luohuqu', 'futianqu', 'nanshanqu', 'yantianqu', 'baoanqu', 'longgangqu', 'longhuaqu', 'guangmingqu', 'pingshanqu', 'dapengxinqu', 'dapengbandao']
# # prices = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
#
# regions = ['haidianqu']
# prices = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
#
# csv_write.writerow(table_head)
#
# for re in regions:
#     for pr in prices:
#         page = 1
#         # todo 代理设置
#         while True:
#             # url = 'https://sz.lianjia.com/ershoufang/pg' + str(page) + '/'
#             # url = 'https://bj.lianjia.com/ershoufang/' + re + '/pg' + str(page) + pr + '/'
#             url = 'https://bj.lianjia.com/ershoufang/' + re + '/pg' + str(page) + pr + '/'
#
#             page = page + 1
#             print("region: " + re + ", price: " + pr + ', page: ' + str(page))
# out.close()
# i = 0

# class ErShouSpider:
#    def __init__(self):

price_low = 450
price_high = 520


def search_region(in_region):
    page = 1
    price = price_low
    while price < price_high:
        while True:
            url = generate_url(in_region, page, price, price + 5)
            if not parse_page(url, page):
                break
            page += 1
        price += 5


def generate_url(in_region, in_page, in_price_low, in_price_high):
    return 'https://bj.lianjia.com/chengjiao/' + in_region + '/pg' + str(in_page) + 'bp' + str(in_price_low) + 'ep' + str(in_price_high) + '/'
    # return 'https://bj.lianjia.com/ershoufang/' + in_region + '/pg' + str(in_page) + 'bp' + str(in_price_low) + 'ep' + str(in_price_high) + '/'


def parse_page(in_url, in_page):
    response = requests.get(in_url, headers=header)

    soup = BeautifulSoup(response.text, 'html.parser')
    page_div = soup.find('div', class_="page-box house-lst-page-box")
    page_str = page_div.attrs['page-data']
    page_obj = json.loads(page_str)
    page_total = page_obj['totalPage']

    if in_page >= page_total:
        return False

    div_item = soup.find_all('div', class_="info")
    if len(div_item) == 0:
        return False

    for item in div_item:
        try:
            write_info = []
            a_title = item.find('div', class_="title")
            href = a_title.find('a').get('href')
            detail = requests.get(href, headers=header)
            detail_soup = BeautifulSoup(detail.text, 'html.parser')

            # total_price = detail_soup.find('span', class_="total").text
            # unit_price = detail_soup.find('span', class_="unitPriceValue").text
            # write_info.append(total_price)
            # write_info.append(unit_price)

            # community = detail_soup.find('div', class_="communityName")
            # community_name = community.find(name='a', attrs={'class': 'info'}).text
            # region = community.nextSibling.text
            # if region and len(region) >= 4:
            #     region = region[4:]
            # write_info.append(community_name)
            # write_info.append(region)

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

    return True


if __name__ == '__main__':
    region = 'qinghe11'
    search_region(region)