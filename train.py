import torch 
import pickle

with open('data/board_states.pkl', 'rb') as f:
    x = pickle.load(f)
with open('data/results.pkl', 'rb') as f:
    y = pickle.load(f)

print(len(x))
print(len(y))
