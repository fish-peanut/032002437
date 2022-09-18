import parse_data
import turn_to_excels
import spider_province
import turn_to_images


if __name__ == '__main__':
    generator_spider = spider_province.begin_spider()  # 初始化爬虫,生成爬虫迭代器
    tl = turn_to_images.begin()                        # 初始化可视化模块
    for data in generator_spider:
        list_case = parse_data.parse_provinces(data[0])    # 获取爬取一天的数据
        turn_to_excels.turn_to_excels(list_case, data[1])  # 写入excel表格
        turn_to_images.turn_to_images(data[1], tl)         # 写入可视化地图
    turn_to_images.end(tl)                                 # 关闭可视化模块
    print('main_over!!')
