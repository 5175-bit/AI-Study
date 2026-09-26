import torch
import torch.nn as nn
import math


# =========================================
# 1. 设置基本参数
# =========================================

batch_size = 2
seq_len = 4
vocab_size = 100
d_model = 8
d_k = 4


# =========================================
# 2. Token ID
# =========================================

tokens = torch.tensor([
    [10, 20, 30, 40],
    [50, 60, 70, 80]
])

print("tokens:")
print(tokens)

print("\ntokens shape:")
print(tokens.shape)


# =========================================
# 3. Token Embedding
# =========================================

token_embedding = nn.Embedding(
    vocab_size,
    d_model
)

X_token = token_embedding(tokens)

print("\nX_token shape:")
print(X_token.shape)


# =========================================
# 4. Position Embedding
# =========================================

position_embedding = nn.Embedding(
    seq_len,
    d_model
)

positions = torch.arange(seq_len)

X_position = position_embedding(positions)

print("\npositions:")
print(positions)

print("\nX_position shape:")
print(X_position.shape)


# =========================================
# 5. Token Embedding + Position Embedding
# =========================================

X = X_token + X_position

print("\nX shape:")
print(X.shape)


# =========================================
# 6. 创建 Q、K、V 线性变换
# =========================================

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


# =========================================
# 7. 计算 Q、K、V
# =========================================

Q = W_Q(X)
K = W_K(X)
V = W_V(X)

print("\nQ shape:")
print(Q.shape)

print("\nK shape:")
print(K.shape)

print("\nV shape:")
print(V.shape)


# =========================================
# 8. 计算 Attention Scores
# =========================================

scores = torch.matmul(
    Q,
    K.transpose(-2, -1)
)

scores = scores / math.sqrt(d_k)

print("\n原始 scaled scores shape:")
print(scores.shape)

print("\n第一句话 Mask 前的 scores:")
print(scores[0])


# =========================================
# 9. 创建 Causal Mask
# =========================================

mask = torch.triu(
    torch.ones(seq_len, seq_len),
    diagonal=1
)

print("\nCausal Mask:")
print(mask)


# =========================================
# 10. 把未来位置设置成 -inf
# =========================================

scores = scores.masked_fill(
    mask == 1,
    float("-inf")
)

print("\n第一句话 Mask 后的 scores:")
print(scores[0])


# =========================================
# 11. Softmax
# =========================================

attention_weights = torch.softmax(
    scores,
    dim=-1
)

print("\n第一句话的 Attention Weights:")
print(attention_weights[0])


# =========================================
# 12. Attention Weight × V
# =========================================

output = torch.matmul(
    attention_weights,
    V
)

print("\noutput shape:")
print(output.shape)

print("\n最终 output:")
print(output)