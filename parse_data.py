from lxml import etree
import re

provinces1 = ['河北', '山西', '辽宁', '吉林', '黑龙江', '江苏', '浙江', '安徽', '福建', '江西', '山东',
              '河南', '湖北', '湖南', '广东', '海南', '四川', '贵州', '云南', '陕西', '甘肃', '青海',
              '北京', '天津', '上海', '重庆', '内蒙古', '广西', '西藏', '宁夏', '新疆', ]
provinces2 = ['台湾地区', '香港特别行政区', '澳门特别行政区']


#  统计中国大陆每日本土新增确诊人数及新增无症状感染人数
#  统计所有省份包括港澳台每日本土新增确诊人数及新增无症状感染人数


def parse_provinces(data):
    HongKong_case = '香港特别行政区(\d+)例'
    Macao_case = '澳门特别行政区(\d+)例'
    taiwan_case = '台湾地区(\d+)例'
    new_sym = '本土病例(\d+)例'
    new_no_sym = '本土(\d+)例'
    provinces_dic_case = {}
    provinces_hkmt_dic = {}

    data_list = data.split('本土')
    provinces_index_1 = data_list[1].find('（')
    provinces_index_2 = data_list[1].find('）')
    sym_data = data_list[1][provinces_index_1 + 1:provinces_index_2]
    # print(sym_data)

    provinces_index_1 = data_list[2].find('（')
    provinces_index_2 = data_list[2].find('）')
    no_sym_data = data_list[2][provinces_index_1 + 1:provinces_index_2]
    # print(no_sym_data)

    hkmt_data = data_list[2][provinces_index_2:-1]
    # print(hkmt_data)

    # 31 个省
    for pros in provinces1:
        # 新增确诊
        case_num_1 = 0
        pro_find_list = re.findall(pros + r'(\d+)例', sym_data, re.M)
        if len(pro_find_list) != 0:
            case_num_1 = pro_find_list[0]

        # 新增无症状
        case_num_2 = 0
        pro_find_list = re.findall(pros + r'(\d+)例', no_sym_data, re.M)
        if len(pro_find_list) != 0:
            case_num_2 = pro_find_list[0]
        provinces_dic_case[pros] = (pros, int(case_num_1), int(case_num_2))

    # 港澳台地区
    for pros in provinces2:
        case_num_3 = 0
        pro_find_list = re.findall(pros + r'(\d+)例', hkmt_data, re.M)
        if len(pro_find_list) != 0:
            case_num_3 = pro_find_list[0]
        if case_num_3 != 0:
            provinces_hkmt_dic[pros] = int(case_num_3)

    list_case = [provinces_dic_case, provinces_hkmt_dic]

    return list_case

    # print(provinces_dic_sym)
    # print(provinces_dic_no_sym)
    # print(provinces_hkmt_dic)

# if __name__ == '__main__':
#     fp = open('./8.txt', 'r', encoding='utf-8')
#     data = fp.read()
#     parse_provinces(data)
#     fp.close()
