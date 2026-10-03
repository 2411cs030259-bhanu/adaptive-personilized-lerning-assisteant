import torch
from torch import nn
class DKTModel(nn.Module):
    def __init__(self,input_size=2,hidden=64,num_topics=20):
        super().__init__(); self.lstm=nn.LSTM(input_size,hidden,batch_first=True); self.fc=nn.Linear(hidden,num_topics)
    def forward(self,x): y,_=self.lstm(x); return torch.sigmoid(self.fc(y))
