def weak_topics(states,threshold=.6): return [s for s in states if s["mastery"]<threshold]
