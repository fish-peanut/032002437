""""
    turn_to_excels文件, 主要负责将传进来的数据进行解析,

    并生成excel表格, 需要的参数有(数据列表,时间)
"""
import pandas as pd


def turn_to_excels(list_e, data_time):
    # 数据读取
    case_province = pd.DataFrame(list(list_e[0].values()), columns=['省份', '新增确诊人数', '新增无症状人数'])
    case_hkmt_fp = pd.DataFrame(list(list_e[1].items()), columns=['省份', '港澳台病例'])

    # 对空的格子填充处理
    case_province.fillna(0, inplace=True)
    case_hkmt_fp.fillna(0, inplace=True)

    # 存储表格
    case_province.to_excel(f'./table/case_pro_fp_{data_time}.xlsx', encoding='utf-8', index=False)
    case_hkmt_fp.to_excel(f'./table/case_hkmt_{data_time}.xlsx', encoding='utf-8', index=False)

    print('{} over!'.format(data_time))
