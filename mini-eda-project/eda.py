
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# %% 1. 路径和环境设置

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "ai4i2020.csv"
FIGURE_DIR = BASE_DIR / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# 中文字体
plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei", "SimHei", "DejaVu Sans"
]
plt.rcParams["axes.unicode_minus"] = False

# %% 2. 读取数据与质量检查

df = pd.read_csv(DATA_PATH)

print("========== 数据基本信息 ==========")
print(df.head())
print("数据维度：", df.shape)

df.info()

print("\n各列缺失值数量：")
print(df.isna().sum())

print("\n重复记录数量：", df.duplicated().sum())

print("\n描述性统计：")
print(df.describe())

# %% 3. 总体故障率分析

normal_count = (df["Machine failure"] == 0).sum()
failure_count = (df["Machine failure"] == 1).sum()

failure_rate = failure_count / len(df)

print("\n========== 总体故障情况 ==========")
print("正常记录数量：", normal_count)
print("故障记录数量：", failure_count)
print(f"总体故障率：{failure_rate:.2%}")

# %% 4. 按设备类型分组统计

type_summary = df.groupby("Type").agg(
    sample_count=("Machine failure", "size"),
    failure_count=("Machine failure", "sum"),
    failure_rate=("Machine failure", "mean")
).reset_index()

type_summary = type_summary.sort_values(
    "sample_count", ascending=False
)

print("\n========== 不同设备类型统计 ==========")
print(type_summary)

# 统计不同类型设备的运行参数
operation_columns = [
    "Rotational speed [rpm]",
    "Torque [Nm]",
    "Tool wear [min]"
]

operation_summary = df.groupby("Type")[
    operation_columns
].agg(["mean", "min", "max"])

print("\n========== 不同类型运行参数 ==========")
print(operation_summary)

# %% 5. 图1：设备类型样本数量

plt.figure(figsize=(8, 5))

plt.bar(
    type_summary["Type"],
    type_summary["sample_count"]
)

plt.xlabel("Type")
plt.ylabel("Sample Count")
plt.title("Sample Count by Type")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "type_sample_count.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 6. 图2：不同类型的故障率

max_index = type_summary["failure_rate"].idxmax()
max_type = type_summary.loc[max_index, "Type"]
max_failure_rate = type_summary.loc[
    max_index, "failure_rate"
]

print("\n故障率最高的设备类型：", max_type)
print(f"对应故障率：{max_failure_rate:.2%}")

plt.figure(figsize=(8, 5))

plt.bar(
    type_summary["Type"],
    type_summary["failure_rate"]
)

plt.gca().yaxis.set_major_formatter(
    PercentFormatter(1.0)
)

plt.xlabel("Type")
plt.ylabel("Failure Rate")
plt.title("Failure Rate by Type")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "type_failure_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 7. 图3：设备转速分布

speed = df["Rotational speed [rpm]"]

speed_mean = speed.mean()
speed_median = speed.median()
high_speed_count = (speed > 2750).sum()

print("\n========== 转速统计 ==========")
print(f"平均转速：{speed_mean:.2f} rpm")
print(f"转速中位数：{speed_median:.2f} rpm")
print("超过2750 rpm的记录数量：", high_speed_count)

plt.figure(figsize=(8, 5))

plt.hist(
    speed,
    bins=30,
    edgecolor="black"
)

plt.axvline(
    speed_mean,
    linestyle="--",
    label="Mean"
)

plt.axvline(
    speed_median,
    linestyle=":",
    label="Median"
)

plt.xlabel("Rotational Speed [rpm]")
plt.ylabel("Frequency")
plt.title("Distribution of Rotational Speed")
plt.legend()

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "rotational_speed_hist.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 8. 图4：转速与扭矩的关系

speed_col = "Rotational speed [rpm]"
torque_col = "Torque [Nm]"

correlation = df[speed_col].corr(df[torque_col])

print("\n========== 转速与扭矩相关性 ==========")
print(f"Pearson相关系数：{correlation:.4f}")

plt.figure(figsize=(8, 5))

plt.scatter(
    df[speed_col],
    df[torque_col],
    alpha=0.3,
    s=8
)

plt.xlabel("Rotational Speed [rpm]")
plt.ylabel("Torque [Nm]")
plt.title(
    f"Rotational Speed vs Torque (r={correlation:.2f})"
)

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "speed_torque_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 9. 图5：正常与故障记录的工具磨损

normal_wear = df.loc[
    df["Machine failure"] == 0,
    "Tool wear [min]"
]

failure_wear = df.loc[
    df["Machine failure"] == 1,
    "Tool wear [min]"
]

normal_mean = normal_wear.mean()
failure_mean = failure_wear.mean()

normal_median = normal_wear.median()
failure_median = failure_wear.median()

print("\n========== 工具磨损统计 ==========")

print(
    f"正常记录：均值={normal_mean:.2f}，"
    f"中位数={normal_median:.2f}"
)

print(
    f"故障记录：均值={failure_mean:.2f}，"
    f"中位数={failure_median:.2f}"
)

plt.figure(figsize=(8, 5))

plt.boxplot([normal_wear, failure_wear])

plt.xticks(
    [1, 2],
    ["Normal", "Failure"]
)

plt.xlabel("Machine Status")
plt.ylabel("Tool Wear [min]")
plt.title("Tool Wear by Machine Status")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "tool_wear_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 10. 工具磨损等级划分

df["wear_level"] = pd.cut(
    df["Tool wear [min]"],
    bins=[
        -float("inf"),
        50,
        100,
        150,
        float("inf")
    ],
    labels=[
        "低磨损",
        "中低磨损",
        "中高磨损",
        "高磨损"
    ]
)

wear_summary = df.groupby(
    "wear_level",
    observed=True
).agg(
    sample_count=("Machine failure", "size"),
    failure_count=("Machine failure", "sum"),
    failure_rate=("Machine failure", "mean")
).reset_index()

print("\n========== 不同磨损等级故障率 ==========")
print(wear_summary)

# %% 11. 图6：磨损等级与故障率

plt.figure(figsize=(8, 5))

plt.bar(
    wear_summary["wear_level"].astype(str),
    wear_summary["failure_rate"]
)

plt.gca().yaxis.set_major_formatter(
    PercentFormatter(1.0)
)

plt.xlabel("Tool Wear Level")
plt.ylabel("Failure Rate")
plt.title("Failure Rate by Tool Wear Level")

plt.tight_layout()

plt.savefig(
    FIGURE_DIR / "wear_failure_rate.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# %% 12. 程序结束

print("\n========== EDA分析完成 ==========")
print("图片保存目录：", FIGURE_DIR)
print("共生成6张分析图表。")
