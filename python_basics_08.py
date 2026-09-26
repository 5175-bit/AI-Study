#%%
import torch as nn
m = nn.randint(0,10,(2, 4, 5))
#%%
print(m)
print(m.transpose(0,1))
# %%
