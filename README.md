<div align="center">

# OPD-Survey 📚

**中文版 On-Policy Distillation / On-Policy Self-Distillation 论文调研与解读**

[![Papers](https://img.shields.io/badge/已收录-100+-blueviolet?style=for-the-badge)](#)
[![Update](https://img.shields.io/badge/每日更新-daily-brightgreen?style=for-the-badge)](#)
[![Chinese](https://img.shields.io/badge/中文解读-100%25-red?style=for-the-badge)](#)

</div>

---

## 🎯 仓库目的

本仓库是 [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) 的**中文增强版**：

- ✅ **每个方法都配讲动机（Motivation）** —— 为什么提出这个方法？解决什么痛点？
- ✅ **每个方法都配讲方法思路（Method）** —— 核心公式、算法流程、白话解释
- ✅ **每日更新** —— 持续追踪 arXiv、小红书、知乎、微信公众号上的最新论文
- ✅ **持续完善** —— 欢迎 PR，共同完善中文社区的 OPD 文献库

---

## 📖 概念速览

### 什么是 OPD（On-Policy Distillation）？

**On-Policy Distillation（在线策略蒸馏）** 是一种 LLM 后训练方法，核心是：

```
学生模型在自己的数据分布上（On-Policy），
接收来自教师模型的密集 token 级监督信号（Distillation）。
```

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
- 学生：只看问题
- 教师：看问题 + 验证过的推理轨迹（特权信息）
- 学生自己生成答案 → 教师在每一步提供"正确答案的概率分布"作为监督

> 🎯 优势：**无需独立教师模型**，单一 LLM 通过不同上下文实现自进化。

---

## 🗂️ 目录结构

| 章节 | 论文数 | 链接 |
|------|-------|------|
| 📚 **综述、基础与立场论文** | 8 | [查看](#-一综述基础与立场论文) |
| 🔬 **白盒 OPD（外教师）** | 17 | [查看](#-二白盒-opd外部教师模型) |
| 🎭 **黑盒 OPD（API 教师）** | 4 | [查看](#-三黑盒-opdapi教师) |
| ♻️ **OPSD（特权上下文自蒸馏）** | 15 | [查看](#-四opd-自蒸馏特权上下文) |
| 🔁 **迭代自举** | 2 | [查看](#-五迭代自举) |
| 🤝 **OPD-RL 混合方法** | 17 | [查看](#-六opd-rl-混合方法) |
| 🧠 **推理 OPD（应用）** | 3 | [查看](#-七推理-opd应用) |
| 🖼️ **多模态 OPD** | 6 | [查看](#-八多模态-opd) |
| 🤖 **Agent & 具身 OPD** | 9 | [查看](#-九agent--具身-opd) |
| ⚡ **投机解码蒸馏** | 11 | [查看](#-十投机解码蒸馏) |
| 🛠️ **框架与工具包** | 11 | [查看](#-十一框架与工具包) |
| 🏭 **工业界 / 量产模型** | 13 | [查看](#-十二工业界--量产模型) |

> 📊 **总计**：约 110+ 篇论文 / 仓库 / 框架

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

---

## 📅 更新日志

| 日期 | 新增内容 | 来源 |
|------|---------|------|
| 2026-06-05 | 仓库初始化，导入 thinkwee/AwesomeOPD 全部 111 项 | AwesomeOPD + arXiv + 小红书/知乎 |
| 持续更新 | 每日新增论文 | 参见 `daily-updates/` |

---

## 🤝 贡献指南

欢迎 PR！新增论文时，请按以下格式：

```markdown
#### 📄 [论文标题](arXiv链接)
- **作者/机构**: XXX
- **时间**: YYYY-MM
- **会议/期刊**: XXX
- **arXiv**: [XXXX.XXXXX](link)
- **代码**: [链接](URL)（如有）
- **🎯 动机**: 用 2-3 句话说清楚这个方法要解决什么问题，现有方法的不足是什么
- **💡 方法思路**: 用 3-5 句话说清楚核心方法、关键公式（用 LaTeX）、算法流程
- **📊 实验效果**: 关键 benchmark 上的效果
- **⚠️ 局限**: 方法的不足之处
```

---

## 🙏 致谢

本仓库基于 [thinkwee/AwesomeOPD](https://github.com/thinkwee/AwesomeOPD) 整理，感谢原作者的卓越工作！

> ⚠️ **声明**：本仓库所有论文信息均来自公开来源（arXiv、GitHub、官方项目页等），中文解读为个人理解，如有错误欢迎指正。
