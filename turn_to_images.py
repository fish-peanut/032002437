"""
    turn_to_images文件, 主要负责将excel表格生成可视化图像,

    这里选取中国地图的模板进行可视化实现,

    使用时需先使用begin()函数初始化图像,

    最后要使用end()函数关闭, 进行主要操作的是turn_to_images()函数,

    需要的参数就是excel表格的时间(通过时间寻找表格),和begin()返回的实例化对象
"""
import pandas
from pyecharts.charts import Map, Timeline, Grid, Bar
from pyecharts import options as opts


def begin():      # 初始化tl对象
    tl = Timeline()
    return tl


def turn_to_images(excel_time, tl):       # 进行主要的操作,负责将数据载入图像
    # 数据读取
    provinces_excel_data = pandas.read_excel('./table/case_pro_fp_{}.xlsx'.format(excel_time))
    hkmt_excel_data = pandas.read_excel('./table/case_hkmt_{}.xlsx'.format(excel_time))

    # 实例化map对象
    china_data_map = Map(opts.InitOpts(width='1000px', height='800px'))

    # 解析出要使用的数据
    province_name = [str(x) for x in provinces_excel_data['省份']]
    province_newconfirm = [int(x) for x in provinces_excel_data['新增确诊人数']]
    province_no_sym = [int(x) for x in provinces_excel_data['新增无症状人数']]

    local_case_no_sym = sum(province_no_sym)
    local_case_newconfirm = sum(province_newconfirm)

    # hkmt_data_name = [str(x) for x in hkmt_excel_data['省份']]
    hkmt_data_name = ['台湾', '香港', '澳门']
    hkmt_data_data = [int(x) for x in hkmt_excel_data['港澳台病例']]

    # 生成图像需要的数据类型
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

    # 将数据载入图像
    china_data_map.add('新增确诊病例', gen_newconfirm, 'china')
    china_data_map.add('新增无症状', gen_no_sym, 'china')
    china_data_map.add('港澳台', gen_hkmt_data, 'china')
    china_data_map.set_global_opts(title_opts=opts.TitleOpts(title=f'全国疫情一览\n大陆新增无症状人数:{local_case_no_sym}\n大陆新增确诊人数:{local_case_newconfirm}'),
                                   visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces))

    # 将图像载入tl模块
    tl.add(china_data_map, excel_time)
    tl.add_schema(is_loop_play=True, play_interval=500)


def end(tl):               # 保存数据
    tl.render(path='china_map_data.html')


# if __name__ == '__main__':
#     tl = begin()
#     turn_to_images('2022-08-25', tl)
#     end(tl)

