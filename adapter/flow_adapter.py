import xml.etree.ElementTree as EleTree
import csv


def transforming_flow_feature(flow_xml, flow_csv):
    """
    将TSNLight的流特征的xml文件转换成OpenPlanner的拓扑文本文件
    :param flow_xml:
    :param flow_csv:
    :return:
    """

    # 解析 XML 文件

    tree = EleTree.parse(flow_xml)
    root = tree.getroot()

    # 打开 CSV 文件并创建写入器
    with open(flow_csv, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # 写入表头
        headers = ['flow_id', 'src', 'dst', 'size', 'period', 'deadline', 'jitter']
        writer.writerow(headers)

        # 遍历 XML 文件中的每个 <entry> 元素
        for entry in root.findall('entry'):
            # 获取 <entry> 元素中的各个子元素的值
            flow_id = entry.find('flow_id').text
            src = entry.find('src').text
            dst = entry.find('dst').text
            size = entry.find('size').text
            period = entry.find('period').text
            deadline = entry.find('deadline').text
            jitter = entry.find('jitter').text

            # 将各个元素的值写入 CSV 文件中
            writer.writerow([flow_id, src, dst, size, period, deadline, jitter])
    return
