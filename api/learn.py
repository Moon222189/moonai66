def append_new_knowledge(new_text, existing_lines, existing_embeddings, log_enabled=False):
    logs = []
    new_emb = create_embeddings([new_text])[0]
    for emb in existing_embeddings:
        if cosine_similarity(new_emb, emb) > 0.8:
            return existing_lines, existing_embeddings, logs
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as f:
        f.write(new_text + "\n\n")
    existing_lines.append(new_text)
    existing_embeddings.append(new_emb)
    msg = "Added knowledge: " + new_text[:60] + "..."
    if log_enabled:
        logs.append(msg)
    return existing_lines, existing_embeddings, logs
