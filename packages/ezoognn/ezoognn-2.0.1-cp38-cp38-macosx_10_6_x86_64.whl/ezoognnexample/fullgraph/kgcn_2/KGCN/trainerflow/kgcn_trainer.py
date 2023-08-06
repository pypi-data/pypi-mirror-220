import random
import dgl
import numpy as np
import torch as th
from torch.utils.data import DataLoader
from dgl.nn.functional import edge_softmax
from openhgnn.models import build_model
import torch.nn.functional as F
from . import BaseFlow, register_flow
from ..tasks import build_task
from sklearn.metrics import f1_score, roc_auc_score

import argparse
import numpy as np
import torch
import torch as th
from sklearn.metrics import f1_score, roc_auc_score
from ezoognn.nni.nni_params_handler import MetricsReporter
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.loader.dataset.LastFM4KGcn_ezoo_data_graph import LastFM4KGCN_0EzooGraphhDataset, LastFM4KGCN_1EzooGraphhDataset

@register_flow("kgcntrainer")
class KGCNTrainer(BaseFlow):
    """Demo flows."""

    def __init__(self, args):
        super(KGCNTrainer, self).__init__(args)
        self.in_dim = args.in_dim
        self.out_dim = args.out_dim
        self.l2_weight = args.weight_decay
        self.task = build_task(args)

        if args.dataset == 'LastFM4KGCN':
            #self.ratingsGraph = self.task.dataset.g_1.to(self.device) #data_1[0]
            
            data_0 = LastFM4KGCN_0EzooGraphhDataset(cfg_file=args.cfg_file)[EzooShapeGraphEnum.WHOLE]
            data_1 = LastFM4KGCN_1EzooGraphhDataset(cfg_file=args.cfg_file)[EzooShapeGraphEnum.WHOLE]

            self.ratingsGraph = data_1[0]
            self.neighborList = [8]
            self.trainIndex, self.evalIndex, self.testIndex = self.task.get_split() #data_1.data_1.train_idx, data_1.val_idx, data_1.test_idx
            self.hg = data_0[0]

        self.model = build_model(self.model).build_model_from_args(self.args, self.hg).to(self.device)
        self.optimizer = th.optim.Adam(self.model.parameters(), lr=self.args.lr, weight_decay=self.args.weight_decay)

    def KGCNCollate(self, index):
        item, user = self.ratingsGraph.find_edges(th.stack(index).to(self.device))
        label = self.ratingsGraph.edata['label'][th.stack(index).to(self.device)]
        inputData = th.stack([user, item, label]).t().cpu().numpy()
        deleteindex = []
        item_indices = []
        for i in range(len(inputData)):
            if inputData[i][1] in item_indices:
                deleteindex.append(i)
            else:
                item_indices.append(inputData[i][1])
        inputData = np.delete(inputData, deleteindex, axis=0)
        self.renew_weight(inputData)
        sampler = dgl.dataloading.MultiLayerNeighborSampler(self.neighborList)
        dataloader = dgl.dataloading.DataLoader(
            self.hg, th.LongTensor(inputData[:, 1]).to(device=self.hg.device), sampler,
            device=self.hg.device,
            batch_size=1024,
            shuffle=True,
            drop_last=False,
            num_workers=0)

        block = next(iter(dataloader))[2]
        return block, inputData

    def preprocess(self, dataIndex): # 准备训练数据
        self.user_emb_matrix, self.entity_emb_matrix, self.relation_emb_matrix = self.model.get_embeddings()
        self.hg.ndata['embedding'] = self.entity_emb_matrix   
        dataloader = DataLoader(dataIndex, batch_size=self.args.batch_size, shuffle=True, collate_fn=self.KGCNCollate)
        self.dataloader_it = iter(dataloader)
        return
    
    # def preprocess(args, dataIndex, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    #     dataloader = DataLoader(dataIndex, batch_size=args.batch_size, shuffle=True, collate_fn=lambda fn: KGCNCollate(fn, dataIndex, ratingsGraph, args.neighborList, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix))
    #     dataloader_it = iter(dataloader)
    #     return dataloader_it

    def _mini_train_step(self,): # 分batch更新模型参数以训练模型，并返回所有batch的平均损失。
        # random.shuffle(self.trainIndex)
        self.preprocess(self.trainIndex)
        L = 0
        import time
        t0 = time.time()
        for block, inputData in self.dataloader_it:
            t1 =time.time()
            self.labels, self.scores = self.model(block, inputData)
            t2 =time.time()
            loss = self.loss_calculation()
            t3 = time.time()
            self.optimizer.zero_grad() 
            loss.backward()
            self.optimizer.step()
            t4 = time.time()
            L = L+loss
            #print("t1_{},t2_{}, t3_{}, t4_{}".format(t1-t0, t2-t1, t3-t2, t4-t3))

        f = open('result_kgcn.txt','a') 
        res = "step: "+str(self.epoch)+'full_Loss: '+str(L)+'\n'
        f.write(res)
        print("step:", self.epoch, 'full_Loss:', L)
        
        

    def evaluate(self, dataIndex):
    # def evaluate(args, dataIndex, model, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    #     dataloader_it = preprocess(args, dataIndex, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
        self.preprocess(dataIndex)
        labelsList = []
        scoresList = []

        for block, inputData in self.dataloader_it:
            self.labels, self.scores = self.model(block, inputData)
            labelsList+=(self.labels.detach().cpu().numpy().tolist())
            scoresList+=(th.sigmoid(self.scores).detach().cpu().numpy().tolist())

        auc = roc_auc_score(y_true = np.array(labelsList), y_score = np.array(scoresList))    
        for i in range(len(scoresList)):
            if scoresList[i] >= 0.5:
                scoresList[i] = 1
            else:
                scoresList[i] = 0
    
        f1 = f1_score(y_true = np.array(labelsList), y_pred = np.array(scoresList))

        f = open('result.txt','a')
        f.write('auc:'+str(auc)+'   f1:'+str(f1)+'\n')
        print('auc:',auc,'   f1:',f1)    
        return auc ,f1
    
    def loss_calculation(self):
        labels, logits = self.labels, self.scores

        # output =  -labels * th.log(th.sigmoid(logits)) - (1-labels) * th.log(1-th.sigmoid(logits))
        output = F.binary_cross_entropy_with_logits(logits,labels.to(th.float32))
        self.base_loss = th.mean(output)

        self.l2_loss = th.norm(self.user_emb_matrix) ** 2/2 + th.norm(self.entity_emb_matrix) **2/2 + th.norm(self.relation_emb_matrix) ** 2/2
        '''
        for aggregator in self.aggregators:
            self.l2_loss = self.l2_loss + torch.norm(aggregator.weights) **2/2
        '''
 
        loss = self.base_loss + self.l2_weight * self.l2_loss
        return loss

    
    def renew_weight(self,inputData):
        # hg, user_emb_matrix, relation_emb_matrix

        user_indices = inputData[:, 0]
        self.user_embeddings = self.user_emb_matrix[user_indices]
        weight = th.mm(self.relation_emb_matrix[self.hg.edata['relation'].cpu().numpy()], self.user_embeddings.t())
        weight = weight.unsqueeze(dim=-1)
        self.hg.edata['weight'] = edge_softmax(self.hg, th.as_tensor(weight))

    
    
    def train(self):   
        
        auc_lists = []
        epoch_iter = self.args.epoch_iter
        for self.epoch in range(epoch_iter):
            self._mini_train_step()
            print('train_data:')
            self.evaluate(self.trainIndex)

            print('eval_data:')
            self.evaluate(self.evalIndex)
            
            auc, f1 = evaluate(args, val_idx, model, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
            MetricsReporter.report_intermediate_result(auc)
            auc_lists.append(auc)
        #auc = torch.mean(torch.tensor(auc_lists, dtype=float))
        MetricsReporter.report_final_result(auc)
        pass