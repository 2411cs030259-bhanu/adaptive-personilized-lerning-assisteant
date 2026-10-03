def next_topic(states):
    return min(states,key=lambda x:x["mastery"])["topic"] if states else "Deadlock Prevention"
