import xlwt
import openpyxl
import pandas as pd

list_e = []


def turn_to_excels(list_e, data_time):
    case_province = pd.DataFrame(list(list_e[0].values()), columns=['省份', '新增确诊人数', '新增无症状人数'])
    case_hkmt_fp = pd.DataFrame(list(list_e[1].items()), columns=['省份', '港澳台病例'])

    case_province.fillna(0, inplace=True)
    case_hkmt_fp.fillna(0, inplace=True)

    case_province.to_excel(f'../表格/case_pro_fp_{data_time}.xlsx', encoding='utf-8', index=False)
    case_hkmt_fp.to_excel(f'../表格/case_hkmt_{data_time}.xlsx', encoding='utf-8', index=False)

    print('over!')
