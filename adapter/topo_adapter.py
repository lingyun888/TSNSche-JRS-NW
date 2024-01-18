import xml.etree.ElementTree as EleTree
import csv


def transforming_topo_feature(topo_xml, topo_csv):
    """
    将TSNLight的流特征的xml文件转换成jrs-nw的拓扑csv文件
    :param topo_xml:
    :param topo_csv:
    :return:
    """
    # 解析 XML 文件

    tree = EleTree.parse(topo_xml)
    root = tree.getroot()

    # 打开 CSV 文件并创建写入器
    with open(topo_csv, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 写入表头
        headers = ['link', 'q_num', 'rate', 't_proc', 't_prop']
        writer.writerow(headers)

        # 遍历 XML 文件中的每个 <entry> 元素
        for entry in root.findall('entry'):
            # 获取 <entry> 元素中的各个子元素的值
            link = entry.find('link').text
            q_num = entry.find('q_num').text
            rate = entry.find('rate').text
            t_proc = entry.find('t_proc').text
            t_prop = entry.find('t_prop').text

            # 将各个元素的值写入 CSV 文件中
            writer.writerow([link, q_num, rate, t_proc, t_prop])
    return
