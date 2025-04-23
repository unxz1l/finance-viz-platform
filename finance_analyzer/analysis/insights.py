def generate_insights(current, previous):
    insights = []
    if current["ROE"] > previous["ROE"]:
        insights.append("ROE 上升，代表資金運用效率改善。")
    if current["R&D Expense"] > previous["R&D Expense"]:
        insights.append("研發投入增加，有助於未來競爭力。")
    return insights