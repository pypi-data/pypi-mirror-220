import dgl
import argparse
import numpy as np
import torch
import torch as th
from KGCN import KGCN
import torch.nn.functional as F
from torch.utils.data import DataLoader
from dgl.nn.functional import edge_softmax
from sklearn.metrics import f1_score, roc_auc_score
from ezoognn.nni.nni_params_handler import MetricsReporter
from ezoognn.loader.dataset.ezoo_data_graph import EzooShapeGraphEnum
from ezoognn.loader.dataset.LastFM4KGcn_ezoo_data_graph import LastFM4KGCN_0EzooGraphhDataset, LastFM4KGCN_1EzooGraphhDataset


def evaluate(args, dataIndex, model, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    dataloader_it = preprocess(args, dataIndex, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
    labelsList = []
    scoresList = []

    for block, inputData in dataloader_it:
        labels, scores = model(block, inputData)
        labelsList += (labels.detach().cpu().numpy().tolist())
        scoresList += (th.sigmoid(scores).detach().cpu().numpy().tolist())

    auc = roc_auc_score(y_true=np.array(labelsList), y_score=np.array(scoresList))
    for i in range(len(scoresList)):
        if scoresList[i] >= 0.5:
            scoresList[i] = 1
        else:
            scoresList[i] = 0

    f1 = f1_score(y_true=np.array(labelsList), y_pred=np.array(scoresList))

    f = open('result.txt', 'a')
    f.write('auc:' + str(auc) + '   f1:' + str(f1) + '\n')
    print('auc:', auc, '   f1:', f1)
    return auc, f1


def loss_calculation(labels, scores, l2_weight, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    labels, logits = labels, scores

    # output =  -labels * th.log(th.sigmoid(logits)) - (1-labels) * th.log(1-th.sigmoid(logits))
    output = F.binary_cross_entropy_with_logits(logits, labels.to(th.float32))
    base_loss = th.mean(output)

    l2_loss = th.norm(user_emb_matrix) ** 2 / 2 + th.norm(entity_emb_matrix) ** 2 / 2 + th.norm(
        relation_emb_matrix) ** 2 / 2
    '''
    for aggregator in self.aggregators:
        self.l2_loss = self.l2_loss + torch.norm(aggregator.weights) **2/2
    '''

    loss = base_loss + l2_weight * l2_loss
    return loss


def renew_weight(inputData, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    user_indices = inputData[:, 0]
    user_embeddings = user_emb_matrix[user_indices]
    weight = th.mm(relation_emb_matrix[hg.edata['relation'].cpu().numpy()], user_embeddings.t())
    weight = weight.unsqueeze(dim=-1)
    hg.edata['weight'] = edge_softmax(hg, th.as_tensor(weight))


def KGCNCollate(index, device, ratingsGraph, neighborList, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    item, user = ratingsGraph.find_edges(th.stack(index).to(device))
    label = ratingsGraph.edata['label'][th.stack(index).to(device)]
    inputData = th.stack([user, item, label]).t().cpu().numpy()
    deleteindex = []
    item_indices = []
    for i in range(len(inputData)):
        if inputData[i][1] in item_indices:
            deleteindex.append(i)
        else:
            item_indices.append(inputData[i][1])
    inputData = np.delete(inputData, deleteindex, axis=0)
    renew_weight(inputData, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
    sampler = dgl.dataloading.MultiLayerNeighborSampler(neighborList)
    dataloader = dgl.dataloading.DataLoader(
        hg, th.LongTensor(inputData[:, 1]).to(device=hg.device), sampler,
        device=hg.device,
        batch_size=1024,
        shuffle=True,
        drop_last=False,
        num_workers=0)

    block = next(iter(dataloader))[2]
    return block, inputData


def preprocess(args, dataIndex, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    dataloader = DataLoader(dataIndex, batch_size=args.batch_size, shuffle=True, collate_fn=lambda fn: KGCNCollate(fn, dataIndex, ratingsGraph, args.neighborList, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix))
    dataloader_it = iter(dataloader)
    return dataloader_it


def _mini_train_step(args, trainIndex, model, hg, ratingsGraph, user_emb_matrix, entity_emb_matrix, relation_emb_matrix):
    optimizer = th.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    # random.shuffle(self.trainIndex)
    dataloader_it = preprocess(args, trainIndex, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)

    L = 0
    import time
    t0 = time.time()
    for block, inputData in dataloader_it:
        t1 = time.time()
        labels, scores = model(block, inputData)
        t2 = time.time()
        loss = loss_calculation(labels, scores, args.weight_decay, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
        t3 = time.time()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        t4 = time.time()
        L = L + loss
        # print("t1_{},t2_{}, t3_{}, t4_{}".format(t1-t0, t2-t1, t3-t2, t4-t3))

    f = open('result.txt', 'a')
    res = "step: " + str(args.epoch) + 'full_Loss: ' + str(L) + '\n'
    f.write(res)
    print("step:", args.epoch, 'full_Loss:', L)


def main(args):
    # data loader
    data_0 = LastFM4KGCN_0EzooGraphhDataset(cfg_file=args.cfg_file)[EzooShapeGraphEnum.WHOLE]
    data_1 = LastFM4KGCN_1EzooGraphhDataset(cfg_file=args.cfg_file)[EzooShapeGraphEnum.WHOLE]

    # 训练集、验证集、测试集/ self.trainIndex, self.evalIndex, self.testIndex
    train_idx, val_idx, test_idx = data_1.train_idx, data_1.val_idx, data_1.test_idx
    hg = data_0[0]
    ratingsGraph = data_1[0] #self.task.dataset.g_1.to(self.device)

    model = KGCN(hg, args)
    user_emb_matrix, entity_emb_matrix, relation_emb_matrix = model.get_embeddings()
    hg.ndata['embedding'] = entity_emb_matrix

    auc_lists = []
    epoch_iter = args.epoch_iter
    for epoch in range(epoch_iter):
        _mini_train_step(args, train_idx, model, hg, ratingsGraph, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
        print('train_data:')
        evaluate(args, train_idx, model, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)

        print('val_data:')
        auc, f1 = evaluate(args, val_idx, model, ratingsGraph, hg, user_emb_matrix, entity_emb_matrix, relation_emb_matrix)
        MetricsReporter.report_intermediate_result(auc)
        auc_lists.append(auc)
    auc = torch.mean(torch.tensor(auc_lists, dtype=float))
    MetricsReporter.report_final_result(auc)
    pass


if __name__ == "__main__":
    """
        KGCN
        """
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description="KGCN")

    parser.add_argument(
        "--aggregate", type=str, default="SUM", help="aggregate type."
    )
    parser.add_argument(
        "--batch-size", type=int, default=128, help="batch_size."
    )
    # data source params
    parser.add_argument(
        "--dataset", type=str, default="LastFM4KGCN", help="Name of dataset."
    )
    parser.add_argument(
        "--dataset-name", type=str, default="LastFM4KGCN", help="Name of dataset."
    )
    parser.add_argument(
        "--device", type=str, default="cpu", help="cpu or gpu."
    )
    parser.add_argument(
        "--epoch", type=int, default=1, help="cpu or gpu."
    )
    parser.add_argument(
        "--epoch-iter", type=int, default=100, help="cpu or gpu."
    )
    # cuda params
    parser.add_argument(
        "--gpu", type=int, default=-1, help="GPU index. Default: -1, using CPU."
    )
    parser.add_argument("--hpo-search-space", type=int, default=None, help="searchspace.")
    parser.add_argument("--hpo-trials", type=int, default=100, help="hpo trials.")
    parser.add_argument("--in-dim", type=int, default=16, help="in_dim.")
    parser.add_argument("--load-from-pretrained", type=bool, default=False, help="load_from_pretrained.")
    parser.add_argument("--lr", type=float, default=0.002, help="lr.")
    parser.add_argument("--max-epoch", type=int, default=1, help="max_epoch.")
    parser.add_argument("--model", type=str, default='KGCN', help="model.")
    parser.add_argument("--model-name", type=str, default='KGCN', help="modelname.")

    parser.add_argument("--n-item", type=int, default=60, help="n_item.")
    parser.add_argument("--n-neighbor", type=int, default=8, help="n_neighbor.")
    parser.add_argument("--neighborList", type=object, default=[8], help="n_neighbor.")
    parser.add_argument("--n-relation", type=int, default=60, help="n_relation.")
    parser.add_argument("--n-user", type=int, default=3139, help="n_user.")
    parser.add_argument("--optimizer", type=str, default='Adam', help="optimizer.")
    parser.add_argument("--out-dim", type=int, default=16, help="out_dim.")
    parser.add_argument("--output-dir", type=str, default='./openhgnn/output/KGCN', help="output_dir.")
    parser.add_argument("--patience", type=int, default=1, help="patience.")
    parser.add_argument("--seed", type=str, default=0, help="seed.")
    parser.add_argument("--task", type=str, default='recommendation', help="task.")
    parser.add_argument("--use-best-config", type=bool, default=False, help="use_best_config.")
    parser.add_argument("--weight-decay", type=float, default=0.0001, help="weight_decay.")
    parser.add_argument("-cfg", "--cfg-file", type=str, default="/home/zz/project/ezoodb/.tmp/.config/conf.conf",#os.path.join(current_dir, '../../../../../resources/conf/ezoodb.conf'),
                        help="ezoo cfg config")
    args = parser.parse_args()
    # 使用nni
    MetricsReporter.update_report_params(args)
    print(args)

    main(args)

