<div align="center">

# OPD-Survey 📚

**中文版 On-Policy Distillation / On-Policy Self-Distillation 论文调研与解读**

[![Papers](https://img.shields.io/badge/已收录-150+-blueviolet?style=for-the-badge)](papers/)
[![Chinese](https://img.shields.io/badge/中文解读-100%25-red?style=for-the-badge)](papers/)
[![Source](https://img.shields.io/badge/参考-thinkwee%2FAwesomeOPD-orange?style=for-the-badge)](https://github.com/thinkwee/AwesomeOPD)

</div>

---

## 🎯 仓库目的

本仓库是 [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) 的**中文增强版**：

- ✅ **每个方法都配讲动机（Motivation）** —— 为什么提出这个方法？解决什么痛点？
- ✅ **每个方法都配讲方法思路（Method）** —— 核心公式、算法流程、白话解释

---

## 📖 概念速览

### 什么是 OPD（On-Policy Distillation）？

**On-Policy Distillation（在线策略蒸馏）** 是一种 LLM 后训练方法，核心是：

> 学生模型在自己的数据分布上（On-Policy），
> 接收来自教师模型的密集 token 级监督信号（Distillation）。

> 🎯 一句话：**学生一边自己开车（生成），教练一边对每一步动作打分**（KL 散度对齐）。

### 三大范式对比

| 范式 | 类型 | 类比 | 核心问题 |
|------|------|------|----------|
| **SFT** | Off-Policy | 学员看教练开车的录像并模仿 | 分布不匹配 → 复合误差 |
| **RL（如 GRPO）** | On-Policy | 学员自己开车，到终点才被告知对错 | 奖励稀疏 → 学习低效 |
| **OPD** | On-Policy | 学员自己开车，教练对每一步实时打分 | ✅ 结合两者优点 |

### 什么是 OPSD（On-Policy Self-Distillation）？

**OPSD 是 OPD 的特例**：教师 = 学生（同模型），但教师在**特权上下文**（privileged context）下工作。

例如：
- **学生**：只看问题
- **教师**：看问题 + 验证过的推理轨迹（特权信息）
- 学生自己生成答案 → 教师在每一步提供"正确答案的概率分布"作为监督

> 🎯 优势：**无需独立教师模型**，单一 LLM 通过不同上下文实现自进化。

---

## 🗂️ 目录结构（按论文类别）

| 章节 | 论文数 | 文件 |
|------|------:|------|
| 📚 [一、综述、基础与立场论文](papers/01-surveys-foundations.md) | 11 | `papers/01-surveys-foundations.md` |
| 🔬 [二、白盒 OPD（外部教师）](papers/02-white-box-opd.md) | 28 | `papers/02-white-box-opd.md` |
| 🎭 [三、黑盒 OPD（API 教师）](papers/03-black-box-opd.md) | 5 | `papers/03-black-box-opd.md` |
| ♻️ [四、OPSD（特权上下文自蒸馏）](papers/04-opd-self-distillation.md) | 29 | `papers/04-opd-self-distillation.md` |
| 🔁🤝 [五、迭代自举 + OPD-RL 混合方法](papers/05-iterative-and-opdrl.md) | 24 | `papers/05-iterative-and-opdrl.md` |
| 🧠🖼️🤖 [六、推理 / 多模态 / Agent OPD（应用）](papers/06-applications.md) | 32 | `papers/06-applications.md` |
| ⚡🛠️🏭 [七、投机解码 / 框架 / 工业界](papers/07-speculative-frameworks-industrial.md) | 38 | `papers/07-speculative-frameworks-industrial.md` |

> 📊 **总计**：约 150+ 篇论文 / 仓库 / 框架。每章末尾的 **「📚 2026 年 6 月论文」** 区块按主题归位到对应章。

---

## 📂 仓库根目录

```
OPD-Survey/
├── README.md                                ← 本文件
└── papers/                                  ← 论文中文解读
    ├── 01-surveys-foundations.md            ← 一、综述、基础与立场论文
    ├── 02-white-box-opd.md                  ← 二、白盒 OPD
    ├── 03-black-box-opd.md                  ← 三、黑盒 OPD
    ├── 04-opd-self-distillation.md          ← 四、OPSD 自蒸馏
    ├── 05-iterative-and-opdrl.md            ← 五、迭代自举 + OPD-RL 混合
    ├── 06-applications.md                   ← 六、推理 / 多模态 / Agent OPD
    └── 07-speculative-frameworks-industrial.md  ← 七、投机 / 框架 / 工业
```

---

## 🧭 缩写速查

| 缩写 | 全称 | 含义 |
|------|------|------|
| **FKL** | Forward KL | 前向 KL 散度，mode-covering 行为 |
| **RKL** | Reverse KL | 逆向 KL 散度，mode-seeking 行为 |
| **JSD** | Jensen-Shannon Divergence | 对称化 KL 散度 |
| **Skew-KL** | Skewed KL | FKL/RKL 加权混合 |
| **CMDP** | Constrained MDP | 带 KL 约束的马尔可夫决策过程 |
| **BoN** | Best-of-N | N 选优 |
| **VLA** | Vision-Language-Action | 视觉-语言-动作模型 |
| **PPO** | Proximal Policy Optimization | 经典 RL 算法 |
| **GRPO** | Group Relative Policy Optimization | DeepSeek 提出的无 Critic RL 算法 |
| **DPO** | Direct Preference Optimization | 偏好对齐 |
| **RLHF** | RL from Human Feedback | 人类反馈强化学习 |
| **RLVR** | RL with Verifiable Rewards | 可验证奖励强化学习 |
| **MCTS** | Monte Carlo Tree Search | 蒙特卡洛树搜索 |
| **MLLM** | Multimodal LLM | 多模态 LLM |
| **OPSD** | On-Policy Self-Distillation | 在线策略自蒸馏 |
| **OPD** | On-Policy Distillation | 在线策略蒸馏 |
| **EMA** | Exponential Moving Average | 指数移动平均 |

---

## 🏷️ 严格度标签

为方便读者快速识别"真 OPD"和"边缘方法"，本仓库使用以下标签：

| 标签 | 含义 |
|------|------|
| ✅ **严格 OPD** | 满足 C1（学生 rollout）+ C2（教师 per-token 监督） |
| ⚠️ **序列级 OPD** | C1 满足，C2 是序列级（如 DPO/BOND）非 per-token |
| ⚠️ **Offline OPD** | 不严格满足 C1（如 Lightning OPD 用历史数据） |
| ⚠️ **混合 OPD** | on-policy 与 off-policy 混合（如 LUFFY） |
| ⚠️ **退化为自举** | 无真实 KL 信号（如 Apple SSD） |
| ℹ️ **理论分析** | 论文自身不提出新算法（如 DDT、Why-SD-Degrade） |

---

## 🙏 致谢

本仓库基于 [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) 整理，感谢原作者的卓越工作！

> ⚠️ **声明**：本仓库所有论文信息均来自公开来源（arXiv、GitHub、官方项目页等），中文解读为个人理解，如有错误欢迎指正。
