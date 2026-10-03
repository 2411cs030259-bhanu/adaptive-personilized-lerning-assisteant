def make_sequences(rows,max_len=100):
    groups={}
    for r in rows: groups.setdefault(r["student_id"],[]).append(r)
    return list(groups.values())
