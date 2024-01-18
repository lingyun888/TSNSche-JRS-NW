from adapter.flow_adapter import transforming_flow_feature
from adapter.topo_adapter import transforming_topo_feature
from jrs_nw_algorithm.constraints_constructor import RestrictedScheduleData
from output_results.output_results import output_schedule_results
from model.modeling_topo_and_adding_route_mapping import BuildModel
from preprocessing.topo_and_flow_extend_data import NetworkAndFlowExtendData


def plan(topo_file,
         stream_file):
    # 根据拓扑和流量需求生成拓扑文件和流量文件
    print('\n', 'phase 1: reading and converting XML files for topology and traffic...')

    # 1. 将input_xml/目录下的topo_feature.xml和flow_feature.xml转换为OpenPlanner的输入
    # 转换后的文本文件放在tmp/目录下
    stream_csv = '../tmp/stream.csv'
    topo_csv = '../tmp/topo.csv'
    transforming_topo_feature(topo_file,
                              topo_csv)

    transforming_flow_feature(stream_file,
                              stream_csv)

    # 2. 初始化预处理后输入拓扑和流量的数据
    print('\n', 'phase 2: topology and traffic data initialize and preprocess...')
    preprocessData = NetworkAndFlowExtendData(stream_csv, topo_csv)

    # 3. 建模网络拓扑和添加路由映射
    print('\n', 'phase 3: modeling network topology and adding routing mapping...')
    constructModel = BuildModel(preprocessData)

    # 4. 构建路由约束
    print('\n', 'phase 4: constructing routing constraints...')
    constraintDataSet = RestrictedScheduleData(preprocessData, constructModel)

    # 5.输出调度结果
    print('\n', 'phase 6: output scheduling results...')
    output_schedule_results(preprocessData, constructModel, constraintDataSet)

    return


if __name__ == '__main__':
    flow_file = '../input_xml/flow_feature.xml'
    network_file = '../input_xml/topo_feature.xml'
    plan(network_file, flow_file)
