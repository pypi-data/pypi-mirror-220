# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 4:21 PM
# @Author  : lch
# @Email   : iltie165@163.com
# @File    : dist_train_base.py
import abc

import dgl
import torch as th
from ezoognn.distribution.dist_ezoo_replace import dist_ezoo_initialize
from ezoognn.ezoo_graph import EzooGraph
import os

class DistTrainBase:
    def __init__(self, args):
        self.args = args
        if self.args.gpu >= 0:
            self.device = th.device('cuda:%d' % self.args.gpu)
        else:
            self.device = th.device('cpu')

        self.e_graph = None
        import os
        if os.environ.get('DGL_ROLE', 'client') == 'server':
            self.e_graph = EzooGraph(url=self.args.url, dbname=self.args.dataset, cfg_file=self.args.cfg_file,
                                     restore_file=self.args.restore_file, restore_url=self.args.restore_url,
                                     gdi_ptr=self.args.gdi_ptr, cache_edge=True)
            print("###create e_graph success from python.")
            
        dist_ezoo_initialize(self.args.ip_config, self.e_graph, self.args.part_config,
                             net_type=args.net_type, submit_type=args.submit_type)  # 启动server和client, server用于读取指定的分区part数据
        self.g = None
        self.loss_fcn = None
        self.model = None
        self.optimizer = None
        self.check_filename = 'best_check.pth'

    def train(self):
        th.distributed.init_process_group(backend='gloo')
        print('before init...')
        self.g = dgl.distributed.DistGraph(self.args.dataset)
        print('init finished')

        train_nid = dgl.distributed.node_split(self.g.ndata['train_mask'])
        valid_nid = dgl.distributed.node_split(self.g.ndata['val_mask'])

        self.model, self.loss_fcn, self.optimizer = self.get_trainer_for_graph()
        self.model = th.nn.parallel.DistributedDataParallel(self.model)
        start_epoch = 0
        if self.args.checkpoint != '':
            start_epoch = self.load_checkpoint()

        import time
        print('before sample...')
        before = int(time.time())

        sampler = dgl.dataloading.MultiLayerNeighborSampler([int(fanout) for fanout in self.args.fan_out.split(',')])
        train_dataloader = dgl.dataloading.DistNodeDataLoader(
            self.g, train_nid, sampler, batch_size=self.args.batch_size,
            shuffle=True, drop_last=False)
        valid_dataloader = dgl.dataloading.DistNodeDataLoader(
            self.g, valid_nid, sampler, batch_size=self.args.batch_size,
            shuffle=False, drop_last=False)

        print('before trainning')
        import sklearn.metrics
        import numpy as np
        
        best_loss = float('inf')
        for epoch in range(start_epoch, self.args.epoch):
            # Loop over the dataloader to sample mini-batches.
            loss = self.one_step(train_dataloader)

            # validation
            predictions = []
            labels = []
            with th.no_grad(), self.model.join():
                for step, (input_nodes, seeds, blocks) in enumerate(valid_dataloader):
                    inputs = self.g.ndata['feat'][input_nodes]
                    labels.append(self.g.ndata[self.args.label_name][seeds].numpy())
                    predictions.append(self.model(blocks, inputs).argmax(1).numpy())

                predictions = np.concatenate(predictions)
                labels = np.concatenate(labels)
                accuracy = sklearn.metrics.accuracy_score(labels, predictions)
                print('Epoch {}, Validation Accuracy {}'.format(epoch, accuracy))

            if (self.args.check_interval > 0) and \
                    (epoch % self.args.check_interval == 0) and \
                        (self.args.server_id == 0) and \
                            loss < best_loss:
                self.save_checkpoint(loss, epoch)
                best_loss = loss

        after = int(time.time())
        print('cost time: {}s'.format(after - before))

    def load_checkpoint(self):
        checkpoint_pkg = '{}/{}'.format(self.args.checkpoint, self.check_filename)
        if os.path.exists(checkpoint_pkg):
            print ("try to load checkpoint {} to resume train.".format(checkpoint_pkg))
            checkpoint = th.load(checkpoint_pkg)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            return checkpoint['epoch']
        else: 
            return 0

    def save_checkpoint(self, loss, epoch):
        print("try to save checkpoint.")
        import shutil
        if os.path.exists(self.args.checkpoint):
            shutil.rmtree(self.args.checkpoint)

        os.mkdir(self.args.checkpoint)
        checkpoint = {
            'epoch': epoch,
            'loss': loss,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
        }
        th.save(checkpoint, '{}/{}'.format(self.args.checkpoint, self.check_filename))

    @abc.abstractmethod
    def get_trainer_for_graph(self):
        pass

    @abc.abstractmethod
    def one_step(self, data_loader):
        pass

    def inference(self, node=None):
        pass
