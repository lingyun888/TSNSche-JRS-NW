import numpy as np
import pandas as pd


class NetworkAndFlowInputData:

    def __init__(self, stream_csv, topo_csv):
        self.macrotick = 100
        self.NUM_FLOW = 1000
        self.flow_data = self.processing_flow(stream_csv)
        self.topo_data = self.processing_topo(topo_csv)
        self.ES_set, self.SW_set, self.net, self.LCM = self.calculate_es_and_sw_set()

    def processing_flow(self, stream_csv):
        task = pd.read_csv(stream_csv)[:self.NUM_FLOW]
        for col in ['size', 'period', 'deadline', 'jitter']:
            task[col] = np.ceil(task[col] / self.macrotick).astype(int)
        return task

    def processing_topo(self, topo_csv):
        network = pd.read_csv(topo_csv)
        for col in ['t_proc', 't_prop']:
            network[col] = np.ceil(network[col] / self.macrotick).astype(int)
        return network

    def calculate_es_and_sw_set(self):
        nodes = list(self.topo_data['link'].apply(lambda x: eval(x)[0])) + \
                list(self.topo_data['link'].apply(lambda x: eval(x)[1]))
        NODE_SET = list(set(nodes))
        es_set = [x for x in NODE_SET if nodes.count(x) == 2]
        sw_set = list(set(NODE_SET) - set(es_set))
        LCM = np.lcm.reduce(self.flow_data['period'])
        net = np.zeros(shape=(max(NODE_SET) + 1, max(NODE_SET) + 1))
        return es_set, sw_set, net, LCM
