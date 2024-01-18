import pandas as pd


def output_schedule_results(preprocessingData, constructingModel, restrictedDataset):
    task = preprocessingData.flow_data
    task_attr = preprocessingData.task_attr
    LCM = preprocessingData.LCM
    link_to_index = preprocessingData.link_to_index
    index_to_link = preprocessingData.index_to_link
    macrotick = preprocessingData.macrotick
    link_out = constructingModel.link_out
    start = restrictedDataset.start
    end = restrictedDataset.end
    x = restrictedDataset.x
    # GCL
    GCL = []
    for i in task_attr:
        period = task.loc[i, 'period']
        for e_i in index_to_link:
            link = index_to_link[e_i]
            if x[i][e_i].x > 0:
                s = start[i][e_i].x
                e = end[i][e_i].x
                queue = 0
                for k in range(int(LCM / period)):
                    GCL.append(
                        [eval(link), 0, int(s + k * period) * macrotick, int(e + k * period) * macrotick,
                         LCM * macrotick]
                    )
    # Offset
    OFFSET = []
    for i in task_attr:
        start_link = [link for link in link_out[task_attr[i]['src']] if x[i][link_to_index[link]].x > 0][0]
        offset = start[i, link_to_index[start_link]].x
        OFFSET.append(
            [i, 0, (task.loc[i, 'period'] - offset) * macrotick]
        )
    # Route
    ROUTE = []
    for i in task_attr:
        for k, rr in enumerate(x[i]):
            if rr.x > 0:
                ROUTE.append(
                    [i, eval(index_to_link[k])]
                )
    # Queue
    QUEUE = []
    for i in task_attr:
        for k, rr in enumerate(x[i]):
            if rr.x > 0:
                e = index_to_link[k]
                QUEUE.append([i, 0, eval(e), 0])

    # 输出调度结果为csv文件
    GCL = pd.DataFrame(GCL)
    GCL.columns = ["link", "queue", "start", "end", "cycle"]
    GCL.to_csv("../output_results/3ONEDATA-%s-%d-%s-GCL.csv" % (1, 2, 3), index=False)

    OFFSET = pd.DataFrame(OFFSET)
    OFFSET.columns = ['id', 'ins_id', 'offset']
    OFFSET.to_csv("../output_results/3ONEDATA-%s-%d-%s-OFFSET.csv" % (1, 2, 3), index=False)

    ROUTE = pd.DataFrame(ROUTE)
    ROUTE.columns = ['id', 'link']
    ROUTE.to_csv("../output_results/3ONEDATA-%s-%d-%s-ROUTE.csv" % (1, 2, 3), index=False)

    QUEUE = pd.DataFrame(QUEUE)
    QUEUE.columns = ['id', 'ins_id', 'link', 'queue']
    QUEUE.to_csv("../output_results/3ONEDATA-%s-%d-%s-QUEUE.csv" % (1, 2, 3), index=False)
