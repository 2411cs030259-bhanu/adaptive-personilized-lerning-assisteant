def make_plan(weak,minutes=45):
    topics=[x["topic"] for x in weak[:2]] or ["Deadlock Prevention","Synchronization"]
    slots=[20,15,10]; items=[]
    for i,t in enumerate(topics): items.append({"minutes":slots[i],"topic":t})
    items.append({"minutes":10,"topic":"Practice Quiz"})
    return {"items":items,"total_minutes":sum(x["minutes"] for x in items)}
