import torch
import torchvision
import torchvision.transforms as transforms
import os
import torch.optim as optim
import numpy as np
import random

import copy
import torch.optim as optim


import copy
import math
import random
import time
from collections import OrderedDict, defaultdict
from typing import Union, List

import numpy as np
import torch
from matplotlib import pyplot as plt
from torch import nn
from torch.optim import *
from torch.optim.lr_scheduler import *
from torch.utils.data import DataLoader
from torchprofile import profile_macs
from torchvision.datasets import *
from torchvision.transforms import *
from tqdm.auto import tqdm

from torchprofile import profile_macs

assert torch.cuda.is_available(), \
"The current runtime does not have CUDA support." \
"Please go to menu bar (Runtime - Change runtime type) and select GPU"





random.seed(321)
np.random.seed(432)
torch.manual_seed(223)


Byte = 8
KiB = 1024 * Byte
MiB = 1024 * KiB
GiB = 1024 * MiB


class sconce:
    
    def __init__(self, model: nn.Module, dataloader: DataLoader, criterion: nn.Module, optimizer: Optimizer,
              scheduler: LambdaLR, config, callbacks = None ):
        
        self.model = model
        self.dataloader = dataloader
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.config = config
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.callbacks = callbacks
        
    def train(self) -> None:
        
        torch.cuda.empty_cache()
        
        self.model.to(self.device)
        
        val_acc = 0
        running_loss = 0.0
        for epoch in range(config.epochs):
            self.model.train()
            
            validation_acc = 0
            for data in tqdm(self.dataloader['train'], desc='train', leave=False):
                # Move the data from CPU to GPU
                if(config.goal != 'autoencoder'):
                    inputs, targets = data
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                elif(config.goal == 'autoencoder'):
                    inputs, targets = data.to(self.device), data.to(self.device)

                # Reset the gradients (from the last iteration)
                self.optimizer.zero_grad()

                # Forward inference
                outputs = self.model(inputs)
                loss = self.criterion(outputs, targets)

                # Backward propagation
                loss.backward()

                # Update optimizer and LR scheduler
                self.optimizer.step()
                if(self.scheduler is not None):
                    self.scheduler.step()

                if (self.callbacks is not None):
                    for callback in self.callbacks:
                        callback()
                running_loss += loss.item()
                
            print(f'Epoch:{epoch + 1} Train Loss: {running_loss / 2000:.3f}')
            running_loss = 0.0
            
            validation_acc = self.validate()
            if(validation_acc> val_acc):
                torch.save(self.model.state_dict(), config.expt_name+'.pth')

    
    @torch.inference_mode()
    def validate(self):
        self.model.eval()
        with torch.no_grad():
            correct = 0
            total = 0
            for images, labels in self.dataloader['test']:
                images, labels = images.to("cuda"), labels.to("cuda")
                outputs = self.model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
            acc = 100 * correct / total

            print('Test Accuracy: {} %'.format(acc))
            return acc
        
        
    ### Model Profiling ###
    

    def get_model_macs(self, inputs) -> int:
            return profile_macs(self.model, inputs)


    def get_sparsity(self, tensor: torch.Tensor) -> float:

        """
        calculate the sparsity of the given tensor
            sparsity = #zeros / #elements = 1 - #nonzeros / #elements
        """
        return 1 - float(tensor.count_nonzero()) / tensor.numel()


    def get_model_sparsity(self) -> float:
        """
        calculate the sparsity of the given model
            sparsity = #zeros / #elements = 1 - #nonzeros / #elements
        """
        num_nonzeros, num_elements = 0, 0
        for param in self.model.parameters():
            num_nonzeros += param.count_nonzero()
            num_elements += param.numel()
        return 1 - float(num_nonzeros) / num_elements

    def get_num_parameters(self, count_nonzero_only=False) -> int:
        """
        calculate the total number of parameters of model
        :param count_nonzero_only: only count nonzero weights
        """
        num_counted_elements = 0
        for param in self.model.parameters():
            if count_nonzero_only:
                num_counted_elements += param.count_nonzero()
            else:
                num_counted_elements += param.numel()
        return num_counted_elements


    def get_model_size(self, data_width=32, count_nonzero_only=False) -> int:
        """
        calculate the model size in bits
        :param data_width: #bits per element
        :param count_nonzero_only: only count nonzero weights
        """
        return self.get_num_parameters(count_nonzero_only) * data_width
    
    @torch.no_grad()
    def measure_latency(self, dummy_input, n_warmup=20, n_test=100):
        self.model.eval()
        # warmup
        for _ in range(n_warmup):
            _ = self.model(dummy_input)
        # real test
        t1 = time.time()
        for _ in range(n_test):
            _ = self.model(dummy_input)
        t2 = time.time()
        return round((t2 - t1) / n_test* 1000, 1)  # average latency in ms

