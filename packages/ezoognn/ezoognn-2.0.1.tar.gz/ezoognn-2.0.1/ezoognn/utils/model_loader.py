import os
import torch

from .. import get_ezoo_home

class ModelLoader():
    """
    The ModelLoader class is the utility of loading and saving GNN model.
    """
    def __init__(self, args):
        self.args = args
        self.ezoo_home = get_ezoo_home(args.cfg_file)
        self.model_saved_path = f'{self.ezoo_home}/{self.args.dataset}-{self.args.gnn_type}.pth'

    def load_model(self, model):
        if not os.path.exists(self.model_saved_path):
            return False
        print(f'Load model from {self.model_saved_path}')
        model.load_state_dict(torch.load(self.model_saved_path))
        return True

    def save_model(self, model):
        if not os.path.exists(self.ezoo_home):
            os.makedirs(self.ezoo_home)
        print(f'Save model to {self.model_saved_path}')
        torch.save(model.state_dict(), self.model_saved_path)