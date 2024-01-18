from preprocessing.topo_and_flow_input_data import NetworkAndFlowInputData
import numpy as np


def find_all_paths(graph, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return [path]
    paths = []
    for node in set(np.reshape(np.argwhere(graph[start] > 0), -1)):
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


class NetworkAndFlowExtendData(NetworkAndFlowInputData):

    def __init__(self, stream_csv, topo_csv):
        super(NetworkAndFlowExtendData, self).__init__(stream_csv, topo_csv)

        self.task_attr = self.generate_task_matrix()
        self.net_var = self.generate_net_matrix()
        self.link_to_index, self.index_to_link = self.generate_link_to_index()
        self.route_space = self.generate_route_space()

    def generate_task_matrix(self):
        task_attr = {}
        for k, row in self.flow_data.iterrows():
            task_attr.setdefault(k, {})

            task_attr[k]['src'] = int(row['src'])
            task_attr[k]['dst'] = int(eval(row['dst'])[0])
            task_attr[k]['cycle_time'] = int(row['period'])
            task_attr[k]['size'] = int(row['size'])
            task_attr[k]['l'] = int(row['deadline'])
            task_attr[k]['dtr'] = int(row['size']) * 8
        return task_attr

    def generate_net_matrix(self):
        net_var = {}
        for _, row in self.topo_data.iterrows():
            net_var.setdefault(eval(row['link'])[0], {})
            net_var[eval(row['link'])[0]]['msd'] = row['t_proc']
            self.net[eval(row['link'])[0], eval(row['link'])[1]] = 1
        return net_var

    def generate_link_to_index(self):
        link_to_index = {}
        index_to_link = {}

        counter = 0
        for _, row in self.topo_data.iterrows():
            link = row['link']
            link_to_index[link] = counter
            index_to_link[counter] = link
            counter += 1
        return link_to_index, index_to_link

    def generate_route_space(self):
        paths = {}
        for i in self.task_attr:
            paths[i] = find_all_paths(self.net, self.task_attr[i]['src'], self.task_attr[i]['dst'])
            for k in range(len(paths[i])):
                paths[i][k] = list(
                    {x: int(eval(str(paths[i][k]))[h + 1]) for h, x in enumerate(eval(str(paths[i][k]))[:-1])}.items())
        route_space = {}
        for i in paths:
            route_space[i] = set([str(x) for y in paths[i] for x in y if
                                  len(y) * (self.task_attr[i]['size'] + max(self.topo_data['t_proc'])) <=
                                  self.task_attr[i]['l']])
            # route_space[i] = set(link_to_index.keys())
        return route_space