import torch
import torch.nn as nn
import math


# =========================
# 1. 一些基本参数
# =========================

batch_size = 2
seq_len = 4
vocab_size = 100
d_model = 8
d_k = 4


# =========================
# 2. 创建两个句子的 Token ID
# =========================

tokens = torch.tensor([
    [10, 20, 30, 40],
    [50, 60, 70, 80]
])

print("tokens:")
print(tokens)

print("tokens shape:")
print(tokens.shape)


# =========================
# 3. Token Embedding
# =========================

token_embedding = nn.Embedding(
    vocab_size,
    d_model
)

X_token = token_embedding(tokens)

print("\nX_token shape:")
print(X_token.shape)


# =========================
# 4. Position Embedding
# =========================

position_embedding = nn.Embedding(
    seq_len,
    d_model
)

positions = torch.arange(seq_len)

print("\npositions:")
print(positions)

X_position = position_embedding(positions)

print("X_position shape:")
print(X_position.shape)


# =========================
# 5. Token + Position
# =========================

X = X_token + X_position

print("\nX shape:")
print(X.shape)


# =========================
# 6. 创建 Q、K、V 的 Linear
# =========================

W_Q = nn.Linear(
    d_model,
    d_k,
    bias=False
)

W_K = nn.Linear(
    d_model,
    d_k,
    bias=False
)

W_V = nn.Linear(
    d_model,
    d_k,
    bias=False
)


# =========================
# 7. 计算 Q、K、V
# =========================

Q = W_Q(X)
K = W_K(X)
V = W_V(X)

print("\nQ shape:")
print(Q.shape)

print("K shape:")
print(K.shape)

print("V shape:")
print(V.shape)


# =========================
# 8. 计算 Attention Score
# =========================

scores = torch.matmul(
    Q,
    K.transpose(-2, -1)
)

print("\nscores shape:")
print(scores.shape)


# =========================
# 9. 除以 sqrt(d_k)
# =========================

scores = scores / math.sqrt(d_k)


# =========================
# 10. Softmax
# =========================

attention_weights = torch.softmax(
    scores,
    dim=-1
)

print("\nattention_weights shape:")
print(attention_weights.shape)

print("\n第一个句子的 Attention 权重:")
print(attention_weights[0])


# =========================
# 11. Attention Weight × V
# =========================

output = torch.matmul(
    attention_weights,
    V
)

print("\noutput shape:")
print(output.shape)

print("\n最终 output:")
print(output)