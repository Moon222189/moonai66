# Simple reasoning engine
def infer_logic(query, knowledge_lines):
    query = query.lower()
    results = []
    for line in knowledge_lines:
        if any(word in line.lower() for word in query.split()):
            results.append(line)
    return results[:5]  # Top 5 matches
