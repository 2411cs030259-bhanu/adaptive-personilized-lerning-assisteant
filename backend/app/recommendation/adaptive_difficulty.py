def choose_difficulty(mastery,recent_score):
    if mastery>=.8 and recent_score>=.75:return "hard"
    if mastery<.5 or recent_score<.55:return "easy"
    return "medium"
