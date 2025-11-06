import torch
import torch.nn as nn
import torch.optim as optim
from model.transformer import SmallTransformer

import os

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train_model(knowledge_file, epochs=3, lr=0.001):
    # Read knowledge
    with open(knowledge_file, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    
    # Build vocab (simple tokenizer)
    vocab = {}
    for line in lines:
        for word in line.split():
            if word not in vocab:
                vocab[word] = len(vocab)
    inv_vocab = {v: k for k, v in vocab.items()}
    
    # Convert text to indices
    data = []
    for line in lines:
        indices = [vocab[word] for word in line.split() if word in vocab]
        if indices:
            data.append(indices)
    
    # Prepare sequences
    max_len = max(len(seq) for seq in data)
    padded = [seq + [0]*(max_len - len(seq)) for seq in data]
    inputs = torch.tensor(padded, dtype=torch.long, device=DEVICE)
    
    # Model
    model = SmallTransformer(vocab_size=len(vocab)+1, max_len=max_len).to(DEVICE)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Training
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs.view(-1, outputs.size(-1)), inputs.view(-1))
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")
    
    # Save model
    os.makedirs("model/saved", exist_ok=True)
    torch.save({
        "model_state": model.state_dict(),
        "vocab": vocab,
        "inv_vocab": inv_vocab
    }, "model/saved/moonai_model.pt")
    print("Model trained and saved!")
