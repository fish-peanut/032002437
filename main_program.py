""""
    此为主函数，负责调度各个模块开始工作,

    运行并完成爬取数据,解析数据,生成excel表格,生成可视化图像的工作

    各个模块的功能,可以阅读各个模块的注释(在每个模块代码文件的首部).

    目录中的china_map_data.html为爬取24天的展示示例,

    若要获取所有天数的html文件,请运行该文件(大概耗时十分钟),

    注意: 运行代码前,需要在该目录下创建一个名字为 'table' 的文件夹.
"""

import parse_data
import turn_to_excels
import spider_province
import turn_to_images


if __name__ == '__main__':
    generator_spider = spider_province.begin_spider()  # 初始化爬虫,生成爬虫迭代器
    tl = turn_to_images.begin()                        # 初始化可视化模块
    for data in generator_spider:
        list_case = parse_data.parse_provinces(data[0])    # 获取爬取一天的数据
        print(list_case)
        turn_to_excels.turn_to_excels(list_case, data[1])  # 写入excel表格
        turn_to_images.turn_to_images(data[1], tl)         # 写入可视化地图
    turn_to_images.end(tl)                                 # 关闭可视化模块
    print('main_over!!')
