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

---

## 📅 2026-06 月新论文（9 篇）

> 本月新拉取的 9 篇推理/多模态/Agent OPD 论文。每篇采用 5 段结构（问题-思路-方法-效果-局限）。

### ViCuR — Visual Cues as Recoverable Privilege for Multimodal OPD

| 项目 | 内容 |
|------|------|
| **作者** | Kanghui Tian 等 |
| **时间** | 2026-06-04 |
| **arXiv** | [2606.05718](https://arxiv.org/abs/2606.05718) |
| **类别** | 🖼️ 多模态 OPD / 视觉线索特权 |

**核心创新**：用**视觉线索（query-related evidence）替代答案特权**——这些线索来自同一视觉输入，学生**推理时可恢复**。实现上加轻量 cue recovery module（sink-token cross-attention prefill），不改推理接口。

**效果**：
- 7 个 benchmark，Qwen3-VL-2B/8B
- 相对"答案特权自蒸馏"+1.19/+1.24 平均分
- 相对"更强教师 OPD"+0.64/+1.08

**局限**：需设计有效视觉线索；cue recovery 模块加少量预填充开销。

**意义**：证明"教师特权的设计"和"教师强度"同样重要。

---

### MGSD — Modality-Gap-aware Self-Distillation（视觉规划）

| 项目 | 内容 |
|------|------|
| **作者** | Jiahui Liu 等 |
| **时间** | 2026-06-04 |
| **arXiv** | [2606.06076](https://arxiv.org/abs/2606.06076) |
| **代码** | [Oranger-l/MGSD](https://github.com/Oranger-l/MGSD) |
| **类别** | 🖼️ 多模态 OPSD / 视觉空间规划 |

**核心创新**：把视觉规划差归因于"感知-推理模态差距"。两阶段：
1. cold-start 视觉学生有可靠 state 表征
2. **特权教师**用**显式符号状态**监督学生**自己的视觉 rollout 前缀**

推理时纯视觉，符号数据仅训练用。

**效果**：4B/8B backbone macro avg 提升 19.3% / 18.4%。

**局限**：需符号化训练数据；泛化到非规划任务待验证。

---

### DuDi — Dual-Signal Distillation（多语言）

| 项目 | 内容 |
|------|------|
| **作者** | Patomporn Payoungkhamdee 等 |
| **时间** | 2026-06-03 |
| **arXiv** | [2606.04694](https://arxiv.org/abs/2606.04694) |
| **类别** | 🖼️ 多模态 / 多语言 |

**核心创新**：**双信号** = 序列级（在线 LM 损失）+ token 级（off-policy + on-policy KL）。**跨语言 verbalizer** 提升师生传递性。

**效果**：SEA-HELM 上**全面超越**蒸馏基线；三种信号**互补**。

**局限**：跨语言 verbalizer 构造较复杂。

---

### SafeSteer — Localized OPD for Safety Alignment

| 项目 | 内容 |
|------|------|
| **作者** | Hao Li, Jingkun An 等 11 人 |
| **时间** | 2026-06-01 |
| **会议** | EMNLP 2026 投稿 |
| **arXiv** | [2606.02530](https://arxiv.org/abs/2606.02530) |
| **项目页** | [anjingkun.github.io/SafeSteer](https://anjingkun.github.io/SafeSteer) |
| **类别** | 🖼️ 安全应用 / 白盒 OPD 细粒度 |

**核心创新**：安全特性在输出分布中本就稀疏——应该**局部修改**而非全局权衡。三件套：
1. **激活引导构造 safety teacher**
2. **safety token 选择算法**
3. 仅对这些 token 计算 RKL

**效果**：
- 7 个 safety + 5 个通用 benchmark，**最强 trade-off**
- 仅用 **100 个 harmful 样本**（不到基线 1%）

**局限**：依赖 token 分类器质量；RKL 仍可能 mode-seeking。

---

#### 📄 [VGS: Decomposed OPD for Vision-Language Reasoning (Steering Gradients)](https://arxiv.org/abs/2606.00564)
- **arXiv**: [2606.00564](https://arxiv.org/abs/2606.00564)
- **🎯 动机**: 多模态 OPD 的优化动态**没研究透** — 标准 monolithic 视角掩盖了语言先验和视觉 grounding 的独立目标。
- **💡 方法**: 数学分解损失为"语言先验"和"视觉 grounding"两部分，发现**梯度向量近乎正交** → 标准优化走的是次优妥协轨迹。VGS 动态重定向更新向量**优先视觉子空间**。
- **📊 数字**: 多个多模态 benchmark 上视觉 grounding 显著优 + 训练开销极小。


#### 📄 [VGS: Decomposed OPD for Vision-Language Reasoning — Steering Gradients for Visual Grounding](https://arxiv.org/abs/2606.00564) | Hee Suk Yoon, ICML 2026 Spotlight
- **🎯 问题**: 多模态 OPD 的**优化动态没研究透** —— 标准 monolithic 视角把"语言先验"和"视觉 grounding"当作一锅炖，**掩盖了两个独立目标**。结果：标准 OPD 走的是次优妥协轨迹。
- **💡 思路**: **数学分解损失**为两个独立成分，分析梯度结构。**问题从"如何做 multimodal OPD"变成"语言/视觉梯度的几何关系是什么"**。
- **🔧 方法**:
  1. 数学分解 VLM OPD 损失为**语言先验**和**视觉 grounding**两部分；
  2. **梯度分析**：发现**两个梯度向量近乎正交** → 两个目标在几何上**独立**；
  3. 假设"**视觉 grounding 是 VLM reasoning 的主要瓶颈**"；
  4. **VGS (Visual Gradient Steering)**：**动态重定向更新向量优先视觉子空间**（不平均两个目标，**专攻瓶颈**）；
  5. 训练开销极小（steering 是几何变换，不引入新参数）。
- **📊 效果**: 多个 VLM 蒸馏设置 + 复杂多模态 benchmark 上，**显著超标准 monolithic OPD**，**superior grounding + 极小训练开销**。ICML 2026 Spotlight。
- **⚠️ 局限**: "视觉是瓶颈"假设需任务验证（对 language-heavy 任务可能不成立）；正交性是否对所有 VLM 普遍；steering 强度是新的隐式超参。
- **价值**: 把"**多模态 OPD 优化**"从"**一锅炖**"变成"**梯度空间几何分析 + 针对性 steering**" —— 几何视角是 VLM 优化的新方法论，对其他多目标多模态训练场景有外推价值。


#### 📄 [FA-OPD: Adversarial Dual On-Policy Distillation from Expressive Teacher](https://arxiv.org/abs/2605.27095) | Zhenglin Wan, 2026-05-26 v1 / 06-01 v2
- **🎯 问题**: Embodied control 的"**演示学习**"（BC + 扩散/流匹配策略）仍是**离线监督学习** —— 策略只在专家状态训练，对**实际访问的状态没纠正信号**。标准 OPD 假设**强固定教师** —— 但 embodied 场景通常**只有演示**，没教师。问题：能不能用演示训出"教师"再做 OPD？
- **💡 思路**: **不要"训完教师再做 OPD"的两阶段**，**"教师-学生"共训，对抗式双 OPD**。**教师从演示学** + **学生学教师**，**教师还提供"学生访问状态"的密集局部目标**。问题从"如何获取教师"变成"**如何让师生相互促进**"。
- **🔧 方法**:
  1. **FA-OPD (Adversarial Dual OPD)**：**Flow Matching 教师**从演示学习 + **轻量 MLP 学生**共训；
  2. 教师提供**两个互补信号**：
     - **奖励通道** —— 学 state-action 对的 expert-likeness 目标，驱动**长 horizon 在线探索**；
     - **动作通道** —— 给**学生访问状态**提供**密集局部目标**，稳定 exploit；
  3. **Reward distillation** 让泛化超出 point-wise demonstrations，**action distillation** 保持 explore 锚定 expert-like behavior。
- **📊 效果**: 6 个机器人 navigation / manipulation / locomotion benchmark **超强基线**；**对噪声/有限演示鲁棒性显著**。代码 [vanzll/FA-OPD](https://github.com/vanzll/FA-OPD)。
- **⚠️ 局限**: 教师 + 学生共训的不稳定性；FM 教师代价大；reward/action 两通道的平衡需调；演示质量仍是上限。
- **价值**: 把"**embodied control 的 OPD**"从"**先 BC 再 OPD**"变成"**师生对抗共训**" —— 是 RL/IL 与 OPD 融合的代表性工作，对演示质量敏感场景有直接价值。


#### 📄 [CollectionLoRA: Collecting 50 Effects in 1 LoRA via Multi-Teacher OPD](https://arxiv.org/abs/2605.25378) | Fangtai Wu, 2026-05
- **🎯 问题**: 定制图像编辑需要给扩散模型加多个视觉效果（艺术风格、相机、...），每个效果存一个 LoRA → **部署成本暴涨**。和加速模块级联还触发**严重参数干扰**（concept bleeding + style degradation）。问题：**怎么把 50 个效果塞进 1 个 LoRA**？
- **💡 思路**: 不用"加更多 LoRA"，**用一个 LoRA 蒸馏所有效果**。多教师 OPD 形式化"**多源知识到单 LoRA**"的蒸馏。问题从"如何避免 LoRA 干扰"变成"**如何让单 LoRA 表达多效果**"。
- **🔧 方法**:
  1. **CollectionLoRA = multi-teacher on-policy distillation 框架**；
  2. 蒸馏 **50 个 effect LoRAs + 少步生成能力**到**单 LoRA**；
  3. 三个组件：
     - **Probabilistic Dual-Stream Routing** —— 训练时随机切换数据源，增强 unseen 场景泛化；
     - **Asymmetric Orthogonal Prompting** —— prompt 空间的概念隔离；
     - **Coarse-to-Fine Distillation Objective** —— 缓解师生分布 gap；
  4. 一次性解决**特征干扰**问题 + **减少部署成本**。
- **📊 效果**: 50 个效果 + 少步生成都进 1 个 LoRA，**concept fidelity 与单 LoRA 相当或更好**，**部署开销大幅降低**。代码 [Qwen-Applications/CollectionLoRA](https://github.com/Qwen-Applications/CollectionLoRA)。
- **⚠️ 局限**: 50 个效果是否可继续扩展到 100/500；prompt 空间概念隔离是否完全消除 bleeding；少步生成质量损失程度；训练多教师代价高（虽然推理快）。
- **价值**: 把"**多 LoRA 部署成本**"从"**线性增长**"变成"**单 LoRA**"，对**AIGC 产品的存储/计算成本**有直接商业价值；和"多教师 OPD"系列工作一脉相承。


#### 📄 [TOPD: Bridging Reasoning Trajectories in On-Policy Distillation via Near-Future Guidance](https://arxiv.org/abs/2606.00305) | Yuxuan Jiang, 2026-05-29
- **🎯 问题**: OPD 学习信号是 **token-level** 的，但**推理失败常是短程分布漂移** —— 孤立 token 级监督**修不好**。实证：~30% high-loss tokens 处于 low-divergence regime，**很多是 surface-form mismatches 而非真实推理分叉**。
- **💡 思路**: 重新设计 OPD 的"loss 来源" —— **别用"孤立高 loss token"作信号，用"近未来 trajectory 是否发散"作信号**。问题从"token-level 监督怎么改进"变成"**如何用 trajectory-level 信息定位真正发散**"。
- **🔧 方法**:
  1. **TOPD (Trajectory-aware OPD)**：用**近未来 trajectory 信息**识别真正发散的状态；
  2. 把指导**分布到多个未来 token**（不是单点 token 监督）；
  3. **屏蔽非发散 high-loss tokens**（避免 surface-form 误导）；
  4. 把监督聚焦在"**真正发散且可修复**"的 trajectory 段。
- **📊 效果**: **屏蔽非发散高 loss token → 标准 OPD 47.8%→48.2%**（**+0.4**）；**TOPD 再 → 52.2%**（**+3.6**）；**AIME24 60.0%→63.3%**（**+3.3**）；**AIME25 46.7%→53.3%**（**+6.6**）。**TOPD 增益最大的正是 reasoning 难任务**。
- **⚠️ 局限**: "近未来 trajectory"长度是超参；如何识别"真正发散"需任务特定设计；对超长 reasoning chain 算力代价。
- **价值**: 把"**OPD 监督粒度**"从"**单 token loss**"提升到"**trajectory-aware 分布监督**" —— 是"短程分布漂移"问题的精准修复，对 reasoning 任务直接收益。


#### 📄 [GAPD: Gold-Action Policy Distillation for Agentic RL in KBQA](https://arxiv.org/abs/2605.29584) | Xin Sun, 2026-05-28 v1 / 06-03 v2
- **🎯 问题**: 知识库问答 (KBQA) 的 RL 是 agentic 任务 —— 模型需发 executable actions、观察 KB feedback、给最终答案。**当前 RL-based KBQA 只优化稀疏的最终答案奖励**，**中间 action 错误弱监督**。Gold logical forms 可转 executable action sequences，但**现有 pipeline 只用作 warm-start 数据增强**，**不用于 on-policy RL 更新**。
- **💡 思路**: 重新定位 gold logical forms —— **不只是"数据增强"**，**是"on-line PD 教师"**。**对齐 gold actions 和 on-policy student rollouts** 后，把 current policy (conditioned on aligned gold action) 作 stop-gradient teacher。问题从"如何用 gold 数据"变成"**如何用 gold 数据作 on-policy 监督**"。
- **🔧 方法**:
  1. **GAPD (Gold-Action PD)**：训练时给 outcome-based RL 加 **dense token-level guidance**；
  2. **MID-ANCHOR MATCHING**：把 student exploration 到达的中间 entities 和 gold execution 到达的 entities 作 **state anchors**，通过这些 entities 匹配 student state 到 gold state；
  3. Current policy (conditioned on aligned gold action) 作 **stop-gradient teacher**；
  4. Teacher 的 token 分布**蒸馏回 ordinary student policy** over generated action-token spans。
- **📊 效果**: **WebQSP / GrailQA / GraphQ** 一致超 SOTA，**KBQA 任务的有效 on-policy gold-action 利用**。
- **⚠️ 局限**: 依赖 gold logical form 标注（KBQA 任务的强假设）；mid-anchor matching 在 entity 集不重叠时可能 fail；on-policy gold action 的对齐代价。
- **价值**: 把"**gold logical forms 在 KBQA RL 中的角色**"从"**warm-start 数据**"提升到"**on-policy 教师信号**"，是 gold-action 利用的范式升级，对所有"有 gold 结构化标注"的 agentic RL 任务可推广。


#### 📄 [GDSD: Reinforcement Learning as Guided Denoiser Self-Distillation for Diffusion LLMs](https://arxiv.org/abs/2605.29398) | Xiaohang Tang, 2026-05-28
- **🎯 问题**: 扩散 LLM (dLLM) 的 RL 受困于 **policy likelihood 不可处理**。主流方案用 **ELBO 作 likelihood 代理**（从随机 mask 序列估计）→ **训练-推理 mismatch**（用 ELBO 作 surrogate），性能退化。
- **💡 思路**: 重新概念化 —— **别管"likelihood 不可处理"问题，直接 self-distill denoiser**。教师是 reverse-KL regularized RL 的 **closed-form optimum** 导出的 advantage-guided self-teacher。**问题从"如何估计 likelihood"变成"如何直接蒸馏 denoiser"**。
- **🔧 方法**:
  1. **GDSD (Guided Denoiser Self-Distillation)**：直接蒸馏 dLLM denoiser；
  2. Teacher 是 **advantage-guided self-teacher**（从 reverse-KL regularized RL closed-form optimum 导出）；
  3. **Normalization-free objective**：把 dLLM denoiser logits 对齐到 teacher logits；
  4. **RL 简化为 likelihood-free self-distillation** —— **bypass ELBO bias**；
  5. 分析：近期 ELBO-based 方法是不同 distillation divergence 的实例，**GDSD 避免其可诊断的病态**。
- **📊 效果**: LLaDA-8B、Dream-7B 在 planning/math/coding 上**比 SOTA ELBO 方法最多 +19.6%**；**训练 reward dynamics 更稳定**。代码 [GaryBall/GDSD](https://github.com/GaryBall/GDSD)。
- **⚠️ 局限**: Advantage-guided self-teacher 的 closed-form 推导是否在所有 RL setting 都成立；normalization-free objective 与其他 KL/JSD 选择未充分对比；只验证了 8B/7B。
- **价值**: 把"**dLLM 的 RL**"从"**用 ELBO 凑合**"变成"**直接 denoiser 自蒸馏**" —— 是 dLLM 后训练的范式转变，+19.6% 是大差距，对 dLLM 社区意义重大。


#### 📄 [CCOPD: Same Evidence, Different Answers — Canonical-Context On-Policy Distillation for Multi-Turn LLMs](https://arxiv.org/abs/2605.30251) | Zizhuo Lin, 2026-05-28
- **🎯 问题**: LLM **完整 prompt 能解，但同一信息**渐进揭示在多轮里**答不同**（lost-in-conversation gap）。同一完整证据在 clean FULL prompt 和 RAW-SHARDED 对话中应得相同答案。归因：**self-anchored drift** —— 部分信息下的回复**引入未支持假设**，**假设扭曲最终答案**。
- **💡 思路**: **用 clean FULL prompt 作 canonical reference**。同一基座模型**双角色**：frozen teacher (clean FULL) + trainable student (incremental multi-turn)。**对齐 student 在自己 trajectory 上的行为和 teacher's canonical full-context 行为**。问题从"如何让多轮鲁棒"变成"**如何让 multi-turn student 对齐 full-context teacher**"。
- **🔧 方法**:
  1. **CCOPD (Canonical-Context OPD)**：训练时**同基座模型双角色**；
  2. **Frozen teacher** 看 **clean FULL prompt**（canonical context）；
  3. **Trainable student** 通过 **multi-turn conversation** 接收**同一证据渐进**；
  4. **对齐 student 在自己 trajectory 上的行为**与 teacher's **canonical full-context 行为**；
  5. 仅在数学问题对话训练，评估**数学 + 5 个 zero-shot OOD 任务**。
- **📊 效果**: **RAW-SHARDED 性能 32% 平均相对提升**（数学 + 5 OOD 任务），**full-context 性能大致保留**。分析显示 CCOPD **强化 user evidence grounding + 减少早期 assistant turn 的污染敏感性**。
- **⚠️ 局限**: 仅在数学问题训练（其他领域迁移性未验证）；需要 same-evidence 的 full/sharded 配对数据；推理时仍用 multi-turn（canonical teacher 仅在训练时）。
- **价值**: 与 MAIGO 思路互补（**MAIGO 改 student 的 reference 来源，CCOPD 改 student 的 teacher 形态**）—— 都是对"lost-in-conversation"的 on-policy 修复，代表 multi-turn LLM 鲁棒性训练的新方向。


#### 📄 [Interpretable Policy Distillation for Power Grid Topology Control](https://arxiv.org/abs/2606.00561) | Karlis Freivalds, 2026-05-30
- **🎯 问题**: 深度 RL 用于电网实时运行有"**实用三难**"：① 大神经网络策略**评估贵**；② **难部署**在受限硬件；③ **对运维人员不透明**。问：能否把 PPO agent 压缩到**可审计的 tree-based 代理**而不丢性能？
- **💡 思路**: **PPO 教师 + 决策树/随机森林学生**，**stress-focused data collection**（聚焦 critical 高负载状态）作为蒸馏集。问题从"如何压缩"变成"**如何在 stress 状态下还能压缩**"。
- **🔧 方法**:
  1. PPO 教师：Grid2Op 14-bus 环境，**stability-oriented reward**；
  2. **Stress-focused data collection** —— 聚焦 critical, high-loading states；
  3. 蒸馏到 **decision tree** 和 **random forest**；
  4. **Feature importance 分析**揭示 representational shift（PPO 依赖线路负载信号，蒸馏树主要由母线拓扑变量驱动）。
- **📊 效果**: held-out 验证集上**两个代理超教师**（mean reward + survival length），**推理代价是 PPO 一小部分**；**决策树和 PPO argmax 高度一致**（top-ranked 动作 near-complete 一致）；决策树**小到可直接检查**。
- **⚠️ 局限**: 仅 14-bus 环境（更复杂电网需验证）；stress-focused data 偏态可能限制泛化；deterministic action 风险（论文明确指出）；**representational shift** 提示**蒸馏可能改变行为模式**（不只是压缩）。
- **价值**: 把"**电网 DRL 黑盒**"变成"**可审计 tree-based surrogate**"，是**critical infrastructure RL 部署**的实用化方向 —— "representational shift" 的发现对所有 RL-to-tree 蒸馏场景都值得警惕。


