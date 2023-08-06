# 代码说明
# sto_train_with_ezoo_sampl_whole_graph.py的配套代码
# 参考：https://zhuanlan.zhihu.com/p/80695364
# 代码目的是想要把 to(device)和 train 并行操作，但未达到预期效果
# 留待以后再进一步研究分析

import torch
import time

class DataPrefetcher():
    def __init__(self, loader, features, labels, device):
        self.loader = iter(loader)
        self.features = features
        self.labels = labels
        self.device = device
        self.stream = torch.cuda.Stream()
        self.preload()

    def preload(self):
        try:
            # tic_sample = time.time()
            self.input_nodes, self.seed_nodes, self.blocks = next(self.loader)
            # print(f"sample cost : {time.time() - tic_sample}s")
        except StopIteration:
            self.batch_inputs = None
            self.batch_labels = None
            self.blocks = None
            return

        # self.batch_inputs_gpu = torch.empty_like(self.features[self.input_nodes], device='cuda')
        # self.batch_labels_gpu = torch.empty_like(self.labels[self.seed_nodes], device='cuda')
        # self.stream.wait_stream(torch.cuda.current_stream())
        with torch.cuda.stream(self.stream):
            # tic_todev = time.time()
            # print(f"to(device) stream : {torch.cuda.current_stream()}")
            self.batch_inputs = self.features[self.input_nodes].to(device=self.device, non_blocking=True)
            self.batch_labels = self.labels[self.seed_nodes].to(device=self.device, non_blocking=True)
            # self.batch_inputs_gpu.copy_(self.features[self.input_nodes], non_blocking=True)
            # self.batch_labels_gpu.copy_(self.labels[self.seed_nodes], non_blocking=True)
            # self.batch_inputs = self.batch_inputs_gpu
            # self.batch_labels = self.batch_labels_gpu
            # torch.cuda.synchronize()
            # print(f"to(device) cost : {time.time() - tic_todev}s")

    def next(self):
        torch.cuda.current_stream().wait_stream(self.stream)
        seed_nodes = self.seed_nodes
        batch_inputs = self.batch_inputs
        batch_labels = self.batch_labels
        blocks = self.blocks
        if batch_inputs is not None:
            batch_inputs.record_stream(torch.cuda.current_stream())
        if batch_labels is not None:
            batch_labels.record_stream(torch.cuda.current_stream())
        self.preload()

        return seed_nodes, batch_inputs, batch_labels, blocks