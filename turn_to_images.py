import pandas
from pyecharts.charts import Map, Timeline
from pyecharts import options as opts
# 9-17 -> 8-25


def begin():
    tl = Timeline()
    return tl


def turn_to_images(excel_time, tl):
    provinces_excel_data = pandas.read_excel('../表格/case_pro_fp_{}.xlsx'.format(excel_time))
    hkmt_excel_data = pandas.read_excel('../表格/case_hkmt_{}.xlsx'.format(excel_time))
    china_data_map = Map(opts.InitOpts(width='1000px', height='800px'))

    province_name = [str(x) for x in provinces_excel_data['省份']]
    province_newconfirm = [int(x) for x in provinces_excel_data['新增确诊人数']]
    province_no_sym = [int(x) for x in provinces_excel_data['新增无症状人数']]

    # hkmt_data_name = [str(x) for x in hkmt_excel_data['省份']]
    hkmt_data_name = ['台湾', '香港', '澳门']
    hkmt_data_data = [int(x) for x in hkmt_excel_data['港澳台病例']]

    gen_newconfirm = [list(z) for z in zip(province_name, province_newconfirm)]
    gen_no_sym = [list(z) for z in zip(province_name, province_no_sym)]
    gen_hkmt_data = [list(z) for z in zip(hkmt_data_name, hkmt_data_data)]

    # 颜色配置
    pieces = [
        {'max': 1, 'color': '#FFFFF0'},
        {'min': 1, 'max': 9, 'color': '#FFE0E0'},
        {'min': 10, 'max': 99, 'color': '#FEC0C0'},
        {'min': 100, 'max': 499, 'color': '#FD9090'},
        {'min': 500, 'max': 999, 'color': '#FC6060'},
        {'min': 1000, 'max': 9999, 'color': '#FB3030'},
        {'min': 10000, 'color': '#DD0000'},
    ]
    china_data_map.add('新增确诊病例', gen_newconfirm, 'china')
    china_data_map.add('新增无症状', gen_no_sym, 'china')
    china_data_map.add('港澳台', gen_hkmt_data, 'china')
    china_data_map.set_global_opts(title_opts=opts.TitleOpts(title='全国疫情一览'),
                                   visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces))
    tl.add(china_data_map, excel_time)
    tl.add_schema(is_loop_play=True, play_interval=500)


def end(tl):
    tl.render(path='china_map_data.html')


# if __name__ == '__main__':
#     tl = begin()
#     turn_to_images('2022-08-25', tl)
#     end(tl)

