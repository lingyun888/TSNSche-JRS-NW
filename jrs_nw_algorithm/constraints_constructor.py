import gurobipy as gp
from gurobipy import GRB
from tqdm import tqdm
import numpy as np


def construct_route_and_schedule_constraints(preprocessingData, constructingModel):
    task = preprocessingData.flow_data
    task_attr = preprocessingData.task_attr
    net_var = preprocessingData.net_var
    link_to_index = preprocessingData.link_to_index
    index_to_link = preprocessingData.index_to_link
    ES_set = preprocessingData.ES_set
    SW_set = preprocessingData.SW_set
    link_in = constructingModel.link_in
    link_out = constructingModel.link_out
    start = constructingModel.start
    end = constructingModel.end
    x = constructingModel.x
    m = constructingModel.model
    route_space = preprocessingData.route_space
    M = int(1e16)
    # 1. Scheduling constraint
    for s in task_attr:
        m.addConstr(
            gp.quicksum(x[s][link_to_index[link]] for link in link_in[task_attr[s]['src']]
                        if link in route_space[s]) == 0
        )

    for s in task_attr:
        m.addConstr(
            gp.quicksum(x[s][link_to_index[link]] for link in link_out[task_attr[s]['src']]
                        if link in route_space[s]) == 1
        )
        # Have to specify the source
        for v in ES_set:
            m.addConstr(
                gp.quicksum(
                    x[s][link_to_index[link]] for link in link_out[v] if v != task_attr[s]['src']
                    and link in route_space[s]
                ) == 0
            )

    for s in task_attr:
        m.addConstr(
            gp.quicksum(x[s][link_to_index[link]] for link in link_out[task_attr[s]['dst']]
                        if link in route_space[s]) == 0
        )

    for s in task_attr:
        m.addConstr(
            gp.quicksum(x[s][link_to_index[link]] for link in link_in[task_attr[s]['dst']]
                        if link in route_space[s]) == 1
        )

    for s in task_attr:
        for v in SW_set:
            m.addConstr(
                gp.quicksum(x[s][link_to_index[link]] for link in link_in[v]
                            if link in route_space[s])
                ==
                gp.quicksum(x[s][link_to_index[link]] for link in link_out[v]
                            if link in route_space[s])
            )

    for s in task_attr:
        for v in SW_set:
            m.addConstr(
                gp.quicksum(x[s][link_to_index[link]] for link in link_out[v]
                            if link in route_space[s]) <= 1
            )
    # 2. Scheduling constraint
    for s in task_attr:
        for e in index_to_link:
            if index_to_link[e] in route_space[s]:
                m.addConstr(
                    end[s][e] <= task_attr[s]['cycle_time'] * x[s][e]
                )
    for s in task_attr:
        for e in index_to_link:
            if index_to_link[e] in route_space[s]:
                m.addConstr(
                    end[s][e] == start[s][e] + x[s][e] * task_attr[s]['dtr']
                )
    for s in task_attr:
        for v in SW_set:
            m.addConstr(
                gp.quicksum(
                    end[s][link_to_index[e]] + x[s][link_to_index[e]] * net_var[eval(e)[1]]['msd']
                    for e in link_in[v] if e in route_space[s]
                ) ==
                gp.quicksum(
                    start[s][link_to_index[e]]
                    for e in link_out[v] if e in route_space[s]
                )
            )
    for s, s_p in tqdm([(s, s_p) for s in task_attr for s_p in task_attr if s < s_p]):
        s_t, s_p_t = task.loc[s].period, task.loc[s_p].period
        lcm = np.lcm(s_t, s_p_t)
        for e in index_to_link:
            if index_to_link[e] in route_space[s] and index_to_link[e] in route_space[s_p]:
                for a, b in [(a, b) for a in range(0, int(lcm / s_t)) for b in range(0, int(lcm / s_p_t))]:
                    _inte = m.addVar(vtype=GRB.BINARY, name="%d%d%s" % (s, s_p, index_to_link[e]))
                    m.addConstr(
                        end[s][e] + a * s_t <= start[s_p][e] - 1 + b * s_p_t + (2 + _inte - x[s][e] - x[s_p][e]) * M
                    )
                    m.addConstr(
                        end[s_p][e] + b * s_p_t <= start[s][e] - 1 + a * s_t + (3 - _inte - x[s][e] - x[s_p][e]) * M
                    )
    try:
        m.optimize()
    except gp.GurobiError as E:
        print("Optimize failed", E)
    return x, start, end


class RestrictedScheduleData:
    def __init__(self, preprocessingData, constructingModel):
        self.x, self.start, self.end = construct_route_and_schedule_constraints(preprocessingData,
                                                                                constructingModel)
