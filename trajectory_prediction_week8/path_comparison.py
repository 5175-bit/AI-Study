# %%
import os

os.environ["MKL_THREADING_LAYER"] = "SEQUENTIAL"

import torch
import math
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from pathlib import Path

t = torch.arange(0, 10, 0.1)

def make_trajectory(
    kind,
    t,
    v0=1.0,
    a=0.2,
    omega=0.2
):

    if kind == "straight":

        x = v0 * t
        y = torch.zeros_like(t)

    elif kind == "accelerate":

        x = v0 * t + 0.5 * a * t ** 2
        y = torch.zeros_like(t)

    elif kind == "turn":

        if abs(omega) < 1e-8:

            x = v0 * t
            y = torch.zeros_like(t)

        else:

            R = v0 / omega

            x = R * torch.sin(omega * t)
            y = R * (1 - torch.cos(omega * t))

    else:
        raise ValueError("未知的轨迹类型")

    positions = torch.stack([x, y], dim=1)

    return positions

# %%
straight = make_trajectory("straight", t)

accelerate = make_trajectory("accelerate", t)

turn = make_trajectory("turn", t)

print(straight.shape)
print(accelerate.shape)
print(turn.shape)
# %%
def check_motion(positions, dt=0.1):

    velocity = (
        positions[1:] - positions[:-1]
    ) / dt

    speed = torch.linalg.vector_norm(
        velocity,
        dim=1
    )

    print("初始速率：", speed[0].item())
    print("末端速率：", speed[-1].item())
    print("速率最小值：", speed.min().item())
    print("速率最大值：", speed.max().item())


print("===== 匀速直线 =====")
check_motion(straight)

print("===== 匀加速直线 =====")
check_motion(accelerate)

print("===== 恒速转弯 =====")
check_motion(turn)
# %%
# %%
import math

def transform_trajectory(
    positions,
    theta,
    x0,
    y0
):

    R = torch.tensor(
        [
            [math.cos(theta), -math.sin(theta)],
            [math.sin(theta),  math.cos(theta)]
        ],
        dtype=positions.dtype,
        device=positions.device
    )

    origin = torch.tensor(
        [x0, y0],
        dtype=positions.dtype,
        device=positions.device
    )

    new_positions = positions @ R.T + origin

    return new_positions
# %%
new_turn = transform_trajectory(
    turn,
    theta=math.pi / 4,
    x0=5,
    y0=10
)

print(new_turn.shape)
print(new_turn[0])
# %%

torch.manual_seed(42)

def random_float(low, high):

    return low + (high - low) * torch.rand(1).item()

# %%
def random_trajectory(kind, t):

    # 初速度
    v0 = random_float(1.0, 2.0)

    # 加速度
    a = random_float(-0.05, 0.05)

    # 转弯角速度
    omega_abs = random_float(0.08, 0.25)

    direction = 1 if random_float(0, 1) > 0.5 else -1

    omega = direction * omega_abs

    # 初始方向
    theta = random_float(-math.pi, math.pi)

    # 初始位置
    x0 = random_float(-10, 10)
    y0 = random_float(-10, 10)

    # 先生成局部轨迹
    positions = make_trajectory(
        kind,
        t,
        v0=v0,
        a=a,
        omega=omega
    )

    # 再旋转和平移
    positions = transform_trajectory(
        positions,
        theta=theta,
        x0=x0,
        y0=y0
    )

    return positions

# %%
t = torch.arange(0, 10, 0.1)

train_trajectories = []
val_trajectories = []
test_trajectories = []

kinds = ["straight", "accelerate", "turn"]

for kind in kinds:

    trajectories = []

    for i in range(20):

        positions = random_trajectory(kind, t)

        trajectories.append(positions)

    # 随机打乱轨迹编号
    indices = torch.randperm(20).tolist()

    # 训练集：14条
    for i in indices[:14]:
        train_trajectories.append(trajectories[i])

    # 验证集：3条
    for i in indices[14:17]:
        val_trajectories.append(trajectories[i])

    # 测试集：3条
    for i in indices[17:]:
        test_trajectories.append(trajectories[i])

# %%
from torch.utils.data import Dataset

class MultiTrajectoryDataset(Dataset):

    def __init__(self, trajectories, past=10, future=30):

        self.trajectories = trajectories
        self.past = past
        self.future = future

        self.samples = []

        for traj_idx, trajectory in enumerate(trajectories):

            n = len(trajectory)

            # 计算当前轨迹能生成多少个窗口
            num_windows = max(0, n - self.past - self.future + 1)

            for start in range(num_windows):

                self.samples.append(
                    (traj_idx, start)
                )

    def __len__(self):

        return len(self.samples)

    def __getitem__(self, idx):

        traj_idx, start = self.samples[idx]

        trajectory = self.trajectories[traj_idx]

        X = trajectory[start:start + self.past]

        Y = trajectory[start + self.past:start + self.past + self.future]

        return X, Y
# %%
train_dataset = MultiTrajectoryDataset(
    train_trajectories,
    past=10,
    future=30
)

val_dataset = MultiTrajectoryDataset(
    val_trajectories,
    past=10,
    future=30
)

test_dataset = MultiTrajectoryDataset(
    test_trajectories,
    past=10,
    future=30
)

print("训练样本数：", len(train_dataset))
print("验证样本数：", len(val_dataset))
print("测试样本数：", len(test_dataset))

# %%
# %%
class RelativeMLP(nn.Module):

    def __init__(self):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(20, 64),
            nn.ReLU(),
            nn.Linear(64, 60)
        )

    def forward(self, X):

        batch_size = X.size(0)

        # 最后一个历史位置
        origin = X[:, -1:, :]

        # 转换成相对坐标
        X_rel = X - origin

        # 展平为MLP输入
        X_flat = X_rel.reshape(batch_size, 20)

        # 预测未来位移
        pred_rel = self.net(X_flat)

        # 恢复时间维度
        pred_rel = pred_rel.reshape(
            batch_size, 30, 2
        )

        # 恢复绝对位置
        pred = pred_rel + origin

        return pred

#%%
class GRUForecast(nn.Module):

    def __init__(self):
        super().__init__()

        self.gru = nn.GRU(
            input_size=2,
            hidden_size=32,
            num_layers=1,
            batch_first=True
        )

        self.head = nn.Linear(32, 60)

    def forward(self, x):

        output, h_n = self.gru(x)

        last_hidden = h_n[-1]
        pred = self.head(last_hidden)

        # 注意：保留原始batch size
        pred = pred.reshape(x.size(0),30,2)

        return pred


# %%
class RelativeGRU(nn.Module):

    def __init__(self):
        super().__init__()

        self.core = GRUForecast()

    def forward(self, X):

        origin = X[:, -1:, :]

        X_rel = X - origin

        pred_rel = self.core(X_rel)

        pred = pred_rel + origin

        return pred

# %%
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=32,
    shuffle=False
)

X_batch, Y_batch = next(iter(train_loader))

mlp = RelativeMLP()
gru = RelativeGRU()

mlp_pred = mlp(X_batch)
gru_pred = gru(X_batch)

print("X:", X_batch.shape)
print("Y:", Y_batch.shape)

print("MLP预测：", mlp_pred.shape)
print("GRU预测：", gru_pred.shape)

print(
    "MLP参数量：",
    sum(p.numel() for p in mlp.parameters())
)

print(
    "GRU参数量：",
    sum(p.numel() for p in gru.parameters())
)

# %%
def train_model(
    model,
    model_name,
    train_loader,
    val_loader,
    epochs=120,
    patience=20,
    lr=0.001
):

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=lr
    )

    criterion = nn.MSELoss()

    best_val_loss = float("inf")
    best_epoch = 0
    no_improve_count = 0

    # 创建模型保存文件夹
    save_dir = Path(
    r"E:\Miniconda\AI-Study\trajectory_prediction_week8\checkpoints"
    )

    save_dir.mkdir(parents=True, exist_ok=True)

    save_path = save_dir / f"best_{model_name}.pt"

    for epoch in range(1, epochs + 1):

        # =========================
        # 训练
        # =========================
        model.train()

        train_loss_sum = 0.0
        train_count = 0

        for X_batch, Y_batch in train_loader:

            optimizer.zero_grad()

            pred = model(X_batch)

            assert pred.shape == Y_batch.shape

            loss = criterion(pred, Y_batch)

            loss.backward()

            optimizer.step()

            batch_size = X_batch.size(0)

            train_loss_sum += loss.item() * batch_size
            train_count += batch_size

        train_loss = train_loss_sum / train_count

        # =========================
        # 验证
        # =========================
        model.eval()

        val_loss_sum = 0.0
        val_count = 0

        with torch.no_grad():

            for X_batch, Y_batch in val_loader:

                pred = model(X_batch)

                assert pred.shape == Y_batch.shape

                loss = criterion(pred, Y_batch)

                batch_size = X_batch.size(0)

                val_loss_sum += loss.item() * batch_size
                val_count += batch_size

        val_loss = val_loss_sum / val_count

        # =========================
        # 保存最佳模型
        # =========================
        if val_loss < best_val_loss:

            best_val_loss = val_loss
            best_epoch = epoch
            no_improve_count = 0

            torch.save(
                model.state_dict(),
                save_path
            )

        else:
            no_improve_count += 1

        if epoch % 10 == 0:

            print(
                f"{model_name} | "
                f"Epoch {epoch}, "
                f"Train Loss={train_loss:.6f}, "
                f"Val Loss={val_loss:.6f}"
            )

        # =========================
        # Early Stopping
        # =========================
        if no_improve_count >= patience:

            print(
                f"{model_name} 第{epoch}轮触发Early Stopping"
            )

            break

    # =========================
    # 恢复最佳模型
    # =========================
    best_weights = torch.load(
        save_path,
        map_location="cpu",
        weights_only=True
    )

    model.load_state_dict(best_weights)

    model.eval()

    print(f"{model_name} 最佳轮数：{best_epoch}")
    print(f"{model_name} 最低验证Loss：{best_val_loss:.6f}")
    print(f"已恢复第{best_epoch}轮的最佳模型")
    print(f"模型保存位置：{save_path.resolve()}")

    return best_epoch, best_val_loss
# %%
torch.manual_seed(42)

mlp = RelativeMLP()

mlp_best_epoch, mlp_best_val = train_model(
    model=mlp,
    model_name="mlp",
    train_loader=train_loader,
    val_loader=val_loader,
    epochs=120,
    patience=20,
    lr=0.001
)
# %%
torch.manual_seed(42)

gru = RelativeGRU()

gru_best_epoch, gru_best_val = train_model(
    model=gru,
    model_name="gru",
    train_loader=train_loader,
    val_loader=val_loader,
    epochs=120,
    patience=20,
    lr=0.001
)
# %%
def evaluate_ade_fde(model, loader):

    model.eval()

    ade_sum = 0.0
    fde_sum = 0.0

    total_samples = 0
    future_steps = 30

    with torch.no_grad():

        for X_batch, Y_batch in loader:

            pred = model(X_batch)

            assert pred.shape == Y_batch.shape

            errors = torch.linalg.vector_norm(
                pred - Y_batch,
                dim=-1
            )

            ade_sum += errors.sum().item()

            fde_sum += errors[:, -1].sum().item()

            total_samples += X_batch.size(0)

    ade = ade_sum / (total_samples * future_steps)
    fde = fde_sum / total_samples

    return ade, fde

# %%
def cv_predict(X, future_steps=30):

    last = X[:, -1, :]
    prev = X[:, -2, :]

    delta = last - prev

    steps = torch.arange(
        1,
        future_steps + 1,
        dtype=X.dtype,
        device=X.device
    ).reshape(1, future_steps, 1)

    pred = (
        last.unsqueeze(1)
        + steps * delta.unsqueeze(1)
    )

    return pred

# %%
class CVBaseline(nn.Module):

    def __init__(self):
        super().__init__()

    def forward(self, X):

        return cv_predict(
            X,
            future_steps=30
        )

# %%
cv = CVBaseline()

mlp_ade, mlp_fde = evaluate_ade_fde(
    mlp,
    val_loader
)

gru_ade, gru_fde = evaluate_ade_fde(
    gru,
    val_loader
)

cv_ade, cv_fde = evaluate_ade_fde(
    cv,
    val_loader
)

print("===== 验证集比较 =====")

print(f"MLP: ADE={mlp_ade:.6f}, FDE={mlp_fde:.6f}")

print(f"GRU: ADE={gru_ade:.6f}, FDE={gru_fde:.6f}")

print(f"CV : ADE={cv_ade:.6f}, FDE={cv_fde:.6f}")


# %%
class CVResidualGRU(nn.Module):

    def __init__(self):
        super().__init__()

        self.correction_net = GRUForecast()

    def forward(self, X):

        # 当前参考位置
        origin = X[:, -1:, :]

        # 相对历史轨迹
        X_rel = X - origin

        # CV基础预测
        baseline = cv_predict(
            X,
            future_steps=30
        )

        # GRU预测修正量
        correction = self.correction_net(X_rel)

        # 最终预测
        pred = baseline + correction

        return pred

# %%
torch.manual_seed(42)

residual_gru = CVResidualGRU()

residual_best_epoch, residual_best_val = train_model(
    model=residual_gru,
    model_name="cv_residual_gru_multitraj",
    train_loader=train_loader,
    val_loader=val_loader,
    epochs=120,
    patience=20,
    lr=0.001
)
# %%
residual_ade, residual_fde = evaluate_ade_fde(
    residual_gru,
    val_loader
)

print("===== 残差GRU验证结果 =====")

print(f"最佳Epoch: {residual_best_epoch}")
print(f"最低Val Loss: {residual_best_val:.6f}")

print(f"残差GRU ADE: {residual_ade:.6f}")
print(f"残差GRU FDE: {residual_fde:.6f}")
# %%
val_groups = {
    "匀速直线": val_trajectories[0:3],
    "匀变速直线": val_trajectories[3:6],
    "恒速转弯": val_trajectories[6:9]
}

models = {
    "CV": cv,
    "MLP": mlp,
    "GRU": gru,
    "CV+GRU": residual_gru
}

for scene_name, trajectories in val_groups.items():

    scene_dataset = MultiTrajectoryDataset(
        trajectories,
        past=10,
        future=30
    )

    scene_loader = DataLoader(
        scene_dataset,
        batch_size=32,
        shuffle=False
    )

    print(f"\n===== {scene_name} =====")

    for model_name, current_model in models.items():

        ade, fde = evaluate_ade_fde(
            current_model,
            scene_loader
        )

        print(
            f"{model_name}: "
            f"ADE={ade:.6f}, "
            f"FDE={fde:.6f}"
        )

# %%
criterion = nn.MSELoss()

cv_loss_sum = 0.0
val_count = 0

with torch.no_grad():

    for X_batch, Y_batch in val_loader:

        pred_cv = cv_predict(
            X_batch,
            future_steps=30
        )

        loss = criterion(pred_cv, Y_batch)

        batch_size = X_batch.size(0)

        cv_loss_sum += loss.item() * batch_size
        val_count += batch_size

cv_val_mse = cv_loss_sum / val_count

print("CV Val MSE:", cv_val_mse)

print("残差GRU最佳Val MSE:", residual_best_val)

# %%
print("===== 最终测试集结果 =====")

test_results = {}

for model_name, current_model in models.items():

    ade, fde = evaluate_ade_fde(
        current_model,
        test_loader
    )

    test_results[model_name] = (ade, fde)

    print(
        f"{model_name}: "
        f"ADE={ade:.6f}, "
        f"FDE={fde:.6f}"
    )
# %%
test_groups = {
    "匀速直线": test_trajectories[0:3],
    "匀变速直线": test_trajectories[3:6],
    "恒速转弯": test_trajectories[6:9]
}

for scene_name, trajectories in test_groups.items():

    scene_dataset = MultiTrajectoryDataset(
        trajectories,
        past=10,
        future=30
    )

    scene_loader = DataLoader(
        scene_dataset,
        batch_size=32,
        shuffle=False
    )

    print(f"\n===== 测试集：{scene_name} =====")

    for model_name, current_model in models.items():

        ade, fde = evaluate_ade_fde(
            current_model,
            scene_loader
        )

        print(
            f"{model_name}: "
            f"ADE={ade:.6f}, "
            f"FDE={fde:.6f}"
        )

# %%
import matplotlib.pyplot as plt
from pathlib import Path

# 保存图片的文件夹
fig_dir = Path(
    r"E:\Miniconda\AI-Study\trajectory_prediction_week8\figures"
)

fig_dir.mkdir(parents=True, exist_ok=True)

# 每种运动选择一条测试轨迹
selected_trajectories = {
    "straight": 0,
    "accelerate": 3,
    "turn": 6
}

for scene_name, traj_idx in selected_trajectories.items():

    trajectory = test_trajectories[traj_idx]

    # 过去10步
    X = trajectory[:10].unsqueeze(0)

    # 未来30步
    Y = trajectory[10:40]

    predictions = {}

    # 预测阶段
    with torch.no_grad():

        for model_name, current_model in models.items():

            current_model.eval()

            pred = current_model(X)

            predictions[model_name] = pred[0]

    # 创建两个子图
    fig, axes = plt.subplots(
        1, 2,
        figsize=(13, 5)
    )

    # =========================
    # 左图：二维轨迹
    # =========================
    history = X[0].cpu().numpy()
    true_future = Y.cpu().numpy()

    axes[0].plot(
        history[:, 0],
        history[:, 1],
        "ko--",
        label="History"
    )

    axes[0].plot(
        true_future[:, 0],
        true_future[:, 1],
        "g-",
        linewidth=2.5,
        label="Ground Truth"
    )

    colors = {
    "CV": "tab:blue",
    "MLP": "tab:orange",
    "GRU": "tab:purple",
    "CV+GRU": "tab:red"
}

    for model_name, pred in predictions.items():

        pred_np = pred.cpu().numpy()

        axes[0].plot(
            pred_np[:, 0],
            pred_np[:, 1],
            color=colors[model_name],
            linestyle="--",
            label=model_name
        )

    axes[0].set_title(
        f"{scene_name}: Trajectory Prediction"
    )

    axes[0].set_xlabel("x")
    axes[0].set_ylabel("y")
    axes[0].axis("equal")
    axes[0].legend()
    axes[0].grid(True)

    # =========================
    # 右图：误差随预测时间变化
    # =========================
    future_time = torch.arange(1, 31) * 0.1

    for model_name, pred in predictions.items():

        errors = torch.linalg.vector_norm(
            pred - Y,
            dim=-1
        )

        axes[1].plot(
            future_time.numpy(),
            errors.cpu().numpy(),
            color=colors[model_name],
            label=model_name
        )

    axes[1].set_title(
        f"{scene_name}: Prediction Error"
    )

    axes[1].set_xlabel("Future Time (s)")
    axes[1].set_ylabel("Position Error")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()

    save_path = fig_dir / f"{scene_name}_comparison.png"

    plt.savefig(
        save_path,
        dpi=160,
        bbox_inches="tight"
    )
    
    plt.show()
    plt.close(fig)
    print("图片保存位置：", save_path.resolve())

# %%
from pathlib import Path

save_dir = Path(
    r"E:\Miniconda\AI-Study\trajectory_prediction_week8\checkpoints"
)

print("模型保存目录：", save_dir.resolve())
print("已有模型文件：")

for file in save_dir.glob("*.pt"):
    print(file.name)