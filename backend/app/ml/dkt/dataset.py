import csv
def load_interactions(path):
    with open(path,newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
