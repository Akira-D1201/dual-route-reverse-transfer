# -*- coding: utf-8 -*-
"""
双路由逆向迁移计算模型：
模型A：字形激活（基于 BIA+ 模型），模拟汉日同形词加工。
模型B：概念激活（基于非选择性激活），模拟图片命名/概念驱动加工。
对比两种认知路径下，L3 日语学习对 L1 汉语词汇激活的影响。
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================
# 1. 共享参数设置
# =============================================
L1_base = 0.8  # 汉语词汇基线
L2_base = 0.5  # 英语词汇基线
L3_base_start = 0.1  # 日语词汇初始基线

learning_rate = 0.008  # 每日学习提升
days = 180  # 模拟6个月
measurement_days = [0, 30, 90, 180]  # 对应0,1,3,6月
inhibition = 0.7  # 抑制强度
decay = 0.1  # 自然衰减
input_strength = 0.1  # 外部输入强度
steps = 100  # 每个试次的时间步数


# =============================================
# 2. 模型A：字形激活（BIA+框架）
# =============================================
def simulate_orthographic(L1_base, L3_base, L2_base=0.5):
    L1_act = np.zeros(steps)
    L2_act = np.zeros(steps)
    L3_act = np.zeros(steps)

    L1_act[0] = 0.0
    L2_act[0] = 0.0
    L3_act[0] = 0.0

    for t in range(1, steps):
        inp_L1 = input_strength * L1_base
        inp_L2 = input_strength * 0.01  # L2几乎不被激活
        inp_L3 = input_strength * L3_base

        decay_L1 = decay * L1_act[t - 1]
        decay_L2 = decay * L2_act[t - 1]
        decay_L3 = decay * L3_act[t - 1]

        inhib_L1 = inhibition * (L2_act[t - 1] + L3_act[t - 1])
        inhib_L2 = inhibition * (L1_act[t - 1] + L3_act[t - 1])
        inhib_L3 = inhibition * (L1_act[t - 1] + L2_act[t - 1])

        L1_act[t] = L1_act[t - 1] + inp_L1 - decay_L1 - inhib_L1
        L2_act[t] = L2_act[t - 1] + inp_L2 - decay_L2 - inhib_L2
        L3_act[t] = L3_act[t - 1] + inp_L3 - decay_L3 - inhib_L3

        L1_act[t] = max(0, L1_act[t])
        L2_act[t] = max(0, L2_act[t])
        L3_act[t] = max(0, L3_act[t])

    return np.max(L1_act)


# =============================================
# 3. 模型B：概念激活（非选择性词汇激活）
# =============================================
def simulate_concept(L1_base, L2_base, L3_base):
    """
    返回 (L1_peak, L2_peak)，以便绘制L2的变化。
    """
    L1_act = np.zeros(steps)
    L2_act = np.zeros(steps)
    L3_act = np.zeros(steps)

    L1_act[0] = 0.0
    L2_act[0] = 0.0
    L3_act[0] = 0.0

    for t in range(1, steps):
        inp_L1 = input_strength * L1_base
        inp_L2 = input_strength * L2_base
        inp_L3 = input_strength * L3_base

        decay_L1 = decay * L1_act[t - 1]
        decay_L2 = decay * L2_act[t - 1]
        decay_L3 = decay * L3_act[t - 1]

        inhib_L1 = inhibition * (L2_act[t - 1] + L3_act[t - 1])
        inhib_L2 = inhibition * (L1_act[t - 1] + L3_act[t - 1])
        inhib_L3 = inhibition * (L1_act[t - 1] + L2_act[t - 1])

        L1_act[t] = L1_act[t - 1] + inp_L1 - decay_L1 - inhib_L1
        L2_act[t] = L2_act[t - 1] + inp_L2 - decay_L2 - inhib_L2
        L3_act[t] = L3_act[t - 1] + inp_L3 - decay_L3 - inhib_L3

        L1_act[t] = max(0, L1_act[t])
        L2_act[t] = max(0, L2_act[t])
        L3_act[t] = max(0, L3_act[t])

    return np.max(L1_act), np.max(L2_act)


# =============================================
# 4. 纵向模拟循环
# =============================================
results_A = {}
results_B_L1 = {}
results_B_L2 = {}
daily_A = []
daily_B_L1 = []
daily_B_L2 = []

L3_current = L3_base_start
for day in range(days + 1):
    peak_A = simulate_orthographic(L1_base, L3_current)
    peak_B_L1, peak_B_L2 = simulate_concept(L1_base, L2_base, L3_current)
    daily_A.append(peak_A)
    daily_B_L1.append(peak_B_L1)
    daily_B_L2.append(peak_B_L2)

    if day in measurement_days:
        month = {0: 0, 30: 1, 90: 3, 180: 6}[day]
        results_A[month] = peak_A
        results_B_L1[month] = peak_B_L1
        results_B_L2[month] = peak_B_L2
        print(
            f"Day {day} (Month {month}): A L1={peak_A:.4f}, B L1={peak_B_L1:.4f}, B L2={peak_B_L2:.4f}, L3 base={L3_current:.4f}")

    L3_current += learning_rate

# =============================================
# 5. 可视化对比（包含L2曲线）
# =============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：每日L1/L2峰值变化对比
ax = axes[0]
ax.plot(daily_A, label='Model A: L1 (Orthographic)', color='blue', alpha=0.8)
ax.plot(daily_B_L1, label='Model B: L1 (Conceptual)', color='red', alpha=0.8)
ax.plot(daily_B_L2, label='Model B: L2 (Conceptual)', color='green', linestyle='--', alpha=0.8)
ax.set_title('Activation Over 6 Months')
ax.set_xlabel('Day')
ax.set_ylabel('Peak Activation')
ax.legend()
ax.axhline(y=0.8, color='gray', linestyle='--', alpha=0.5)

# 右图：四个测量时间点柱状图（只对比L1）
ax = axes[1]
months = [0, 1, 3, 6]
x = np.arange(len(months))
width = 0.35
bars_A = ax.bar(x - width / 2, [results_A[m] for m in months], width, label='Model A L1', color='blue', alpha=0.7)
bars_B = ax.bar(x + width / 2, [results_B_L1[m] for m in months], width, label='Model B L1', color='red', alpha=0.7)
ax.set_title('L1 Peak at Measurement Points')
ax.set_ylabel('L1 Peak Activation')
ax.set_xticks(x)
ax.set_xticklabels([f'Month {m}' for m in months])
ax.legend()
ax.set_ylim(0, 1.0)

plt.tight_layout()
plt.savefig('dual_route_comparison.png', dpi=150)
plt.show()

print("\n===== Simulation Complete =====")
print("Chart saved as 'dual_route_comparison.png'")