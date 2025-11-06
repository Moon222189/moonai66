import torch
from torch.utils.data import DataLoader, Dataset
from torch.nn import CrossEntropyLoss
from torch.optim import Adam
from small_transformer import SmallTransformer
import numpy as np
import pickle

# 1. Load and tokenize brainknowledge.txt
with open("data/brainknowledge.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()

# Simple character-level tokenizer
chars = sorted(list(set(text)))
stoi = {c:i for i,c in enumerate(chars)}
itos = {i:c for i,c in enumerate(chars)}
vocab_size = len(chars)

data = [stoi[c] for c in text]

class CharDataset(Dataset):
    def __init__(self, data, seq_len=64):
        self.data = data
        self.seq_len = seq_len
    def __len__(self):
        return len(self.data) - self.seq_len
    def __getitem__(self, idx):
        x = self.data[idx:idx+self.seq_len]
        y = self.data[idx+1:idx+self.seq_len+1]
        return torch.tensor(x), torch.tensor(y)

dataset = CharDataset(data)
loader = DataLoader(dataset, batch_size=64, shuffle=True)

# 2. Initialize model
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SmallTransformer(vocab_size).to(device)
optimizer = Adam(model.parameters(), lr=1e-3)
criterion = CrossEntropyLoss()

# 3. Training loop
for epoch in range(10):
    for x_batch, y_batch in loader:
        x_batch, y_batch = x_batch.to(device), y_batch.to(device)
        optimizer.zero_grad()
        logits = model(x_batch)
        loss = criterion(logits.view(-1, vocab_size), y_batch.view(-1))
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# Save model and tokenizer
torch.save(model.state_dict(), "model/moonai_model.pt")
with open("model/tokenizer.pkl", "wb") as f:
    pickle.dump({"stoi": stoi, "itos": itos}, f)
