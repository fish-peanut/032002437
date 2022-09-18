import requests
from lxml import etree
import re
import time
import datetime

url = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27 ",
    "Cookie": "yfx_c_g_u_id_10006654=_ck22090716221713320659133618350; "
              "yfx_f_l_v_t_10006654=f_t_1662538937316__r_t_1662538937316__v_t_1662538937316__r_c_0; "
              "sVoELocvxVW0S=59vVEUPdYzZViiQJRL3OzuBKuo7wiZfNKBKnd2T"
              ".QlJkdAV6jykVnmkgDoA1bSxA3FE0yGvjRmm5dn0qMamwfTa; "
              "sVoELocvxVW0T=53SfVXCW3Yh7qqqDkma"
              ".Z4aiyHZ9XdIkPzwgpQ17TKqqLAsHlZUM1q1pke_KCzorYBxqnuE6DeVQ_NYxVaGT3o3LRelh7w8sI7Agrzv0C0GCxttt0KtlLRFQQ1 "
              ".A_1CwHhnko12KXJzcLUdN331hp8qw8kny"
              ".96LlCWOqOqkAfuIzB2mOAZxUa7B1MoQtboYtJnmCYx6h1mpoXZZJktvjm3wHde_ZNOcK88CQShMnVpuA;"
              " insert_cookie=91349450;"
              " JSESSIONID=C21F48AD6B160B83E2C69BEBB37D66C0; "
              " security_session_verify=c889cc19a59214c681f09377c14b439d "
}

link_list = []          # 存储item
url_format = 'http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_{}.shtml'


def less_time(turn_list):
    for i in range(len(turn_list)):
        turn_list[i] = str((datetime.datetime.strptime(turn_list[i], "%Y-%m-%d") + datetime.timedelta(days=-1)).date())
    return turn_list


def get_limit_num():
    response = requests.get(url=url, headers=headers).text
    ex = "<script>.*?</script>"
    result = re.findall(ex, response, re.M)[0]
    limit_num = re.findall(r'\d+', result)[0]
    # return int(limit_num)
    return 1


def spider_in_one_html(url):
    response = requests.get(url=url, headers=headers).text
    main_tree = etree.HTML(response)

    element_list = main_tree.xpath("/html/body/div[3]/div[2]/ul//a")
    time_list = main_tree.xpath("/html/body/div[3]/div[2]/ul//span/text()")

    time_list = less_time(time_list)
    for i in range(len(element_list)):
        items = {
            'link': "http://www.nhc.gov.cn/" + element_list[i].xpath("./@href")[0],
            'time': time_list[i]
            }
        link_list.append(items)


def begin_spider():
    limit_num = get_limit_num()
    for i in range(limit_num):
        time.sleep(0.5)
        if i == 0:
            spider_in_one_html(url=url)
        else:
            spider_in_one_html(url=url_format.format(i+1))
    for i in range(len(link_list)):
        if i % 40 == 0:
            time.sleep(1)
        else:
            time.sleep(0.5)
        response_inner = requests.get(url=link_list[i]['link'], headers=headers).text
        inner_tree = etree.HTML(response_inner)
        text_inner = ''.join(inner_tree.xpath('//*[@id="xw_box"]/p[1]//text() | //*[@id="xw_box"]/p[5]//text() | '
                                              '//*[@id="xw_box"]/p[7]//text()'))
        yield [text_inner, link_list[i]['time']]
    #     filename = link_list[i]['time'] + '.txt'
    #     with open(filename, 'w', encoding='utf-8') as fp:
    #         fp.write(text_inner)
    #     print(filename+' completed! ')
    # print('spider over!')
