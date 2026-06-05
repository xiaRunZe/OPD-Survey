# 🧠 七、推理 OPD + 🖼️ 八、多模态 OPD + 🤖 九、Agent & 具身 OPD

> 本章节合并**应用方向**的方法。这些论文的核心是 OPD/OPSD，但按"应用"分类。

---

# 🧠 七、推理 OPD（应用）

> **特点**：专注于数学 / 代码 / 长 CoT 推理任务。
>
> 真正的推理 OPD 已分散在前面 OPSD / Iterative / OPD-RL / White-Box 章节中，本节仅列出未涵盖的。

---

## 1. G-OPD（跨列）
- 见第二章 §9：人民大学/腾讯，把 OPD 形式化为 KL 约束 RL
- 在推理任务上效果显著

## 2. OPD-AVMP — 自动驾驶运动规划

| 项目 | 内容 |
|------|------|
| **时间** | 2026.04 |
| **arXiv** | [2604.07944](https://arxiv.org/abs/2604.07944) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有自动驾驶运动规划 LLM 大、慢
- 想要**蒸馏小模型**到 1/5 体积

### 💡 方法思路
**核心机制**：**GPT-Driver 框架 + GKD**

- 学生：自动 rollout 驾驶轨迹
- 教师：LLM 教师，token 级监督

### 📊 效果
- 模型大小减小 5×
- 性能接近原 LLM

### ⚠️ 局限
- 限定自动驾驶场景

## 3. Rethinking OPD（跨列）
- 见第一章 §5：THUNLP 出品
- 在 Qwen3-1.7B/4B 推理任务上验证

---

# 🖼️ 八、多模态 OPD

> **特点**：在 VLM、Video、Audio、Image 上做 OPD。

---

## 1. π-Flow — 图像/流 OPD

| 项目 | 内容 |
|------|------|
| **机构** | 多机构 |
| **时间** | 2025.10 |
| **会议** | ICLR 2026 |
| **arXiv** | [2510.14974](https://arxiv.org/abs/2510.14974) |
| **代码** | [Lakonik/piFlow](https://github.com/Lakonik/piFlow) |

### 🎯 动机
- 现有扩散模型 step 多、推理慢
- 想要**少步蒸馏**
- 传统知识蒸馏在流模型上不 work

### 💡 方法思路
**核心机制**：**流模型上的严格 OPD**

- 学生流模型自 rollout（沿自身轨迹预测）
- 教师：teacher velocity field
- 损失：L2 imitation distillation

**关键洞察**：流模型每步预测"速度场"，恰好对应"策略"。

### 📊 效果
- 严格的"扩散模型 OPD"
- 少步生成质量保留

### ⚠️ 局限
- 实现复杂

---

## 2. VOLD — LLM→VLM 蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | INRIA / Goethe Univ. |
| **时间** | 2025.10 |
| **会议** | ICLR 2026 |
| **arXiv** | [2510.23497](https://arxiv.org/abs/2510.23497) |
| **项目页** | [walidbousselham.com/VOLD](https://walidbousselham.com/VOLD/) |

### 🎯 动机
- 现有 VLM 训练从零开始，**冷启动困难**
- 想要把纯文本 LLM 的能力迁移到 VLM

### 💡 方法思路
**核心机制**：**GRPO + On-Policy KL 蒸馏**

- 冷启动 SFT
- 统一 RL+KD 阶段

### 📊 效果
- 旗舰 VLM OPD 配方

### ⚠️ 局限
- repo 占位符
- 细节需读 paper

---

## 3. Step-Audio-R1 — 音频推理

| 项目 | 内容 |
|------|------|
| **机构** | StepFun |
| **时间** | 2025.11 |
| **arXiv** | [2511.15848](https://arxiv.org/abs/2511.15848) |
| **代码** | [stepfun-ai/Step-Audio-R1](https://github.com/stepfun-ai/Step-Audio-R1) |

### 🎯 动机
- 音频模态缺乏推理能力
- 想要"**音频模态的 R1 风格推理**"

### 💡 方法思路
**核心机制**：**模态接地的自蒸馏 + SFT + PPO/RLVR**

- 迭代 on-policy 循环
- 仅使用**音频相关问题**做自蒸馏

### 📊 效果
- 音频推理 SOTA

### ⚠️ 局限
- 限定音频模态

---

## 4. CORD — 文本→音频对齐

| 项目 | 内容 |
|------|------|
| **机构** | 百度 Ernie |
| **时间** | 2026.01 |
| **arXiv** | [2601.16547](https://arxiv.org/abs/2601.16547) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 音频模型缺乏文本推理能力
- 想要"跨模态推理能力对齐"

### 💡 方法思路
**核心机制**：**自模型 + 文本 + 多损失**

- 自模型有文本时为教师
- Token 级 RKL + 序列级 KL + GRPO

### 📊 效果
- 跨模态推理能力提升

### ⚠️ 局限
- 限定音频

---

## 5. Video-OPD

| 项目 | 内容 |
|------|------|
| **机构** | 工业界 |
| **时间** | 2026.02 |
| **arXiv** | [2602.02994](https://arxiv.org/abs/2602.02994) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 视频理解需要**时间定位**
- 想要用 OPD 训练

### 💡 方法思路
**核心机制**：**MLLM + LLM 教师**

- 学生 MLLM rollout 视频理解轨迹
- 教师 LLM 提供 token 级 KL 监督

### 📊 效果
- 时间视频定位有效

### ⚠️ 局限
- 视频处理成本高

---

## 6. X-OPD — 语音 LLM

| 项目 | 内容 |
|------|------|
| **机构** | 腾讯混元 / 浙大 |
| **时间** | 2026.03 |
| **arXiv** | [2603.24596](https://arxiv.org/abs/2603.24596) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 语音 LLM 能力弱于文本 LLM
- 想要"文本 LLM → 语音 LLM 能力对齐"

### 💡 方法思路
**核心机制**：**跨模态 token 级 KL**

- 文本 LLM 教师
- 语音 LLM 学生
- 跨模态对齐

### 📊 效果
- 语音 LLM 能力提升

### ⚠️ 局限
- 跨模态对齐难

---

## 7. Uni-OPD — 统一 OPD

> 🎯 **首个"LLM + MLLM 统一 OPD"框架**

| 项目 | 内容 |
|------|------|
| **时间** | 2026.05 |
| **arXiv** | [2605.03677](https://arxiv.org/abs/2605.03677) |
| **代码** | [WenjinHou/Uni-OPD](https://github.com/WenjinHou/Uni-OPD) |

### 🎯 动机
- 现有 OPD 框架分散在 LLM / MLLM
- 想要"**统一**"框架
- 探索强到弱、跨模态 OPD

### 💡 方法思路
**核心机制**：**双视角配方**

- **视角 1（数据平衡）**：解决"信息性学生状态探索不足"
- **视角 2（边缘校准）**：解决"教师监督不可靠"
  - 用 outcome-guided margin calibration 恢复正确/错误轨迹的 order-consistency

**支持**：单教师/多教师，强到弱、跨模态，5 域 16 benchmark

### 📊 效果
- 统一框架效果好
- 多模态 OPD 统一

### ⚠️ 局限
- 框架复杂
- 多教师协调难

---

# 🤖 九、Agent & 具身 OPD

> **特点**：学生是 Agent（rollout 动作），教师监督这些轨迹。

---

## 1. LLM4Teach — 早期小 Agent + LLM 教师

| 项目 | 内容 |
|------|------|
| **机构** | 之江实验室 AMMI |
| **时间** | 2023.11（更新 2025） |
| **arXiv** | [2311.13373](https://arxiv.org/abs/2311.13373) |
| **代码** | [ZJLAB-AMMI/LLM4Teach](https://github.com/ZJLAB-AMMI/LLM4Teach) |

### 🎯 动机
- 早期工作（2023）：**小 RL Agent 性能差**
- 想要"用 LLM 教师指导"
- 严格 OPD for embodied

### 💡 方法思路
**核心机制**：**动作级 LLM 教师 + RL**

- 小 Agent rollout
- LLM 教师在动作级别给指导
- 蒸馏 + RL 退火

### 📊 效果
- 早期具身 OPD
- 性能提升

### ⚠️ 局限
- 早期工作，规模小

---

## 2. RPD — Refined Policy Distillation

| 项目 | 内容 |
|------|------|
| **机构** | TUM / 弗赖堡 |
| **时间** | 2025.03 |
| **会议** | IROS 2026 |
| **arXiv** | [2503.05833](https://arxiv.org/abs/2503.05833) |
| **项目页** | [refined-policy-distillation.github.io](https://refined-policy-distillation.github.io/) |
| **代码** | [Refined-Policy-Distillation/RPD](https://github.com/Refined-Policy-Distillation/RPD) |

### 🎯 动机
- VLA（Vision-Language-Action）模型训练难
- 想要"PPO + BC on rollouts"

### 💡 方法思路
**核心机制**：**PPO + 行为克隆 on student rollouts**

- 教师 VLA 给出动作
- 学生 VLA rollout 后做 BC
- PPO 优化

### 📊 效果
- 干净 VLA-OPD 配方

### ⚠️ 局限
- 限定机器人操作

---

## 3. SCoRe — 自我纠正

| 项目 | 内容 |
|------|------|
| **机构** | 阿里巴巴 ModelScope |
| **时间** | 2025.09 |
| **arXiv** | [2509.14257](https://arxiv.org/abs/2509.14257) |
| **代码** | [modelscope/easydistill/projects/SCoRe](https://github.com/modelscope/easydistill) |

### 🎯 动机
- 12 个 Agent benchmark 上学生能力弱
- 想要"教师纠正最早错误"实现小模型追平大模型

### 💡 方法思路
**核心机制**：**最早错误纠正 + SFT + 短程 RL**

- 72B 教师在学生 rollout 中找到**最早错误**
- 在错误位置做纠正
- SFT on corrections + 短程 RL

### 📊 效果
- 7B 学生匹配 72B 教师

### ⚠️ 局限
- 依赖教师能力

---

## 4. OpenClaw-RL（跨列）
- 见第六章 §13
- 跨域 Agent 训练

---

## 5. VLA-OPD

| 项目 | 内容 |
|------|------|
| **机构** | HKUST（广州）IRPN Lab |
| **时间** | 2026.03 |
| **arXiv** | [2603.26666](https://arxiv.org/abs/2603.26666) |
| **项目页** | [irpn-lab.github.io/VLA-OPD](https://irpn-lab.github.io/VLA-OPD/) |

### 🎯 动机
- 现有 VLA 训练有 online RL（高方差）和 offline SFT（无探索）
- 想要"**桥接**"两者

### 💡 方法思路
**核心机制**：**专家 VLA + Dense Token 监督**

- 学生 VLA rollout 轨迹
- 专家 VLA 教师给**密集 token 级监督**
- 用 **RKL**（避免 FKL 熵爆炸 + Hard-CE 坍缩）

### 📊 效果
- 替换稀疏 RL 奖励
- 保留通用先验，缓解灾难性遗忘
- LIBERO、RoboTwin2.0 benchmark SOTA

### ⚠️ 局限
- code 即将发布

---

## 6. Skill-SD（跨列）
- 见第四章 §10
- 多轮 Agent 技能自蒸馏

---

## 7. TCOD — 时间课程 OPD

| 项目 | 内容 |
|------|------|
| **机构** | 通义实验室 / CUHK |
| **时间** | 2026.04 |
| **arXiv** | [2604.24005](https://arxiv.org/abs/2604.24005) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 多轮 Agent 任务中，**完整轨迹 OPD 不稳定**
- 想要"**按暴露深度课程化**"

### 💡 方法思路
**核心机制**：**F2B / B2F 时间课程**

- **F2B（Front-to-Back）**：先暴露浅层（前几轮），逐步加深
- **B2F（Back-to-Front）**：先让教师演示开头，学生学结尾
- 线性 pacing schedule

### 📊 效果
- 解决多轮 OPD 轨迹级 KL 不稳定

### ⚠️ 局限
- 课程调度敏感

---

## 8. Healthcare AI GYM

| 项目 | 内容 |
|------|------|
| **机构** | Upstage AI / 高丽大学 |
| **时间** | 2026.05 |
| **arXiv** | [2605.02943](https://arxiv.org/abs/2605.02943) |
| **代码** | [minstar/Healthcare_GYM](https://github.com/minstar/Healthcare_GYM) |

### 🎯 动机
- 医疗 Agent 训练需要真实临床环境
- 想要"医疗 Agent RL + OPD"

### 💡 方法思路
**核心机制**：**临床 Agent 训练场 + TT-OPD**

- 提供医疗 Agent RL 环境
- 用 **EMA 教师 + 结果特权信息**提供**回合级 KL 正则**
- 损失：GRPO + TT-OPD（Turn-level Truncated OPD）

### 📊 效果
- 临床 Agent 训练有效
- 训练场可复现

### ⚠️ 局限
- 限定医疗领域

---

## 9. HyperEyes — 多模态搜索 Agent

> 🎯 **小红书 + 剑桥出品**！

| 项目 | 内容 |
|------|------|
| **机构** | 小红书 / Cambridge |
| **时间** | 2026.05 |
| **arXiv** | [2605.07177](https://arxiv.org/abs/2605.07177) |
| **代码** | [DeepExperience/HyperEyes](https://github.com/DeepExperience/HyperEyes) |

### 🎯 动机
- 现有搜索 Agent 训练效率低
- 想要"**双粒度效率感知**"训练

### 💡 方法思路
**核心机制**：**宏观（轨迹）+ 微观（token）双粒度**

- **TRACE**（trajectory-level adaptive cost efficiency）：轨迹级
- **OPD**（token-level）：token 级
- **GRPO**

### 📊 效果
- 并行多模态搜索 Agent
- 双粒度联合训练

### ⚠️ 局限
- 实现复杂
