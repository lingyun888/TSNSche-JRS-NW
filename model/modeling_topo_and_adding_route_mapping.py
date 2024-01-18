import gurobipy as gp
from gurobipy import GRB


def modeling_network(link_to_index):
    link_in = {}
    link_out = {}
    for link in link_to_index.keys():
        link = eval(link)
        link_in.setdefault(link[1], [])
        link_in[link[1]].append(str(link))
        link_out.setdefault(link[0], [])
        link_out[link[0]].append(str(link))
    return link_in, link_out


class BuildModel:
    x = None
    start = None
    end = None
    link_out = None
    link_in = None
    model = None

    def __init__(self, preprocessingData):
        self.model = gp.Model("RTNS2021")
        self.link_in, self.link_out = modeling_network(preprocessingData.link_to_index)
        self.x, self.start, self.end = self.adding_route_mapping(preprocessingData.flow_data,
                                                                 preprocessingData.link_to_index)

    def adding_route_mapping(self, task, link_to_index):
        x = self.model.addMVar(shape=(len(task), len(link_to_index)),
                                    vtype=GRB.BINARY, name="routing")
        start = self.model.addMVar(shape=(len(task), len(link_to_index)),
                                        vtype=GRB.INTEGER, name="time_start")
        end = self.model.addMVar(shape=(len(task), len(link_to_index)),
                                      vtype=GRB.INTEGER, name="time_end")
        return x, start, end
