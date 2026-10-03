import argparse
from .dataset import load_interactions
def main():
    p=argparse.ArgumentParser();p.add_argument("--data",required=True);p.add_argument("--model",required=True);a=p.parse_args()
    rows=load_interactions(a.data);print({"rows":len(rows),"note":"Use held-out sequences and report AUC/accuracy after full topic-vocabulary training."})
if __name__=="__main__":main()
