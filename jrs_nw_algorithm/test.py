import pandas as pd
import numpy as np

macrotick = 100
sync_error = 0
time_out = 4 * 60 * 60

NUM_FLOW = 1000

task = pd.read_csv("../tmp/1_test_task.csv")[:NUM_FLOW]
network = pd.read_csv("../tmp/1_test_topo.csv")
for col in ['size', 'period', 'deadline', 'jitter']:
    task[col] = np.ceil(task[col] / macrotick).astype(int)
for col in ['t_proc', 't_prop']:
    network[col] = np.ceil(network[col] / macrotick).astype(int)

nodes = list(network['link'].apply(lambda x: eval(x)[0])) + \
        list(network['link'].apply(lambda x: eval(x)[1]))
NODE_SET = list(set(nodes))
ES_set = [x for x in NODE_SET if nodes.count(x) == 2]
SW_set = list(set(NODE_SET) - set(ES_set))
LCM = np.lcm.reduce(task['period'])
net = np.zeros(shape=(max(NODE_SET) + 1, max(NODE_SET) + 1))
