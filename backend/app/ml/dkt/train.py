import argparse, torch
from .model import DKTModel
from .dataset import load_interactions
from .preprocessing import make_sequences
def main():
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    rows=load_interactions(a.data); _=make_sequences(rows)
    model=DKTModel(); torch.save({"state_dict":model.state_dict(),"note":"Initialize with normalized ASSISTments sequences; extend topic vocabulary for a real trained run."},a.output)
    print(f"Checkpoint scaffold saved to {a.output}. For academic evaluation, train with the supplied ASSISTments preprocessing pipeline.")
if __name__=="__main__":main()
