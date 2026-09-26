import torch
import torch.nn as nn
import math


class CausalSelfAttention(nn.Module):

    def __init__(self, d_model, num_heads):
        super().__init__()

        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_head = d_model // num_heads

        self.W_Q = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.W_K = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.W_V = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.W_O = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

    def forward(self, X):

        B, L, D = X.shape

        Q = self.W_Q(X)
        K = self.W_K(X)
        V = self.W_V(X)

        Q = Q.reshape(
            B,
            L,
            self.num_heads,
            self.d_head
        ).transpose(1, 2)

        K = K.reshape(
            B,
            L,
            self.num_heads,
            self.d_head
        ).transpose(1, 2)

        V = V.reshape(
            B,
            L,
            self.num_heads,
            self.d_head
        ).transpose(1, 2)

        scores = torch.matmul(
            Q,
            K.transpose(-2, -1)
        )

        scores = scores / math.sqrt(
            self.d_head
        )

        mask = torch.triu(
            torch.ones(
                L,
                L,
                device=X.device
            ),
            diagonal=1
        )

        scores = scores.masked_fill(
            mask == 1,
            float("-inf")
        )

        attention_weights = torch.softmax(
            scores,
            dim=-1
        )

        output = torch.matmul(
            attention_weights,
            V
        )

        output = output.transpose(1, 2)

        output = output.reshape(
            B,
            L,
            D
        )

        output = self.W_O(output)

        return output


class FeedForward(nn.Module):

    def __init__(self, d_model, d_ff):
        super().__init__()

        self.linear1 = nn.Linear(
            d_model,
            d_ff
        )

        self.activation = nn.GELU()

        self.linear2 = nn.Linear(
            d_ff,
            d_model
        )

    def forward(self, X):

        X = self.linear1(X)

        X = self.activation(X)

        X = self.linear2(X)

        return X


class TransformerBlock(nn.Module):

    def __init__(
        self,
        d_model,
        num_heads,
        d_ff
    ):
        super().__init__()

        self.attention = CausalSelfAttention(
            d_model,
            num_heads
        )

        self.norm1 = nn.LayerNorm(
            d_model
        )

        self.ffn = FeedForward(
            d_model,
            d_ff
        )

        self.norm2 = nn.LayerNorm(
            d_model
        )

    def forward(self, X):

        attention_output = self.attention(X)

        X = self.norm1(
            X + attention_output
        )

        ffn_output = self.ffn(X)

        X = self.norm2(
            X + ffn_output
        )

        return X


# ==================================
# 测试 Transformer Block
# ==================================

B = 2
L = 4
d_model = 8
num_heads = 2
d_ff = 32

X = torch.randn(
    B,
    L,
    d_model
)

print("输入 X shape:")
print(X.shape)

block = TransformerBlock(
    d_model=d_model,
    num_heads=num_heads,
    d_ff=d_ff
)

output = block(X)

print("\n输出 shape:")
print(output.shape)