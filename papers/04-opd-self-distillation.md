# ♻️ 四、OPSD（特权上下文自蒸馏）

> **OPSD = OPD 的特例**：教师 = 学生（同模型），但教师获得**特权上下文**（privileged context）。
>
> 特权上下文类型：验证过的推理 / 答案 / "be concise"前缀 / 更长上下文 / 文档 / 跨语言翻译 / ...

> **核心洞见**：教师和学生**参数相同**（或近似），gap 来自"**条件化的差异**"，而非权重。

---

## 1. OPSD — Self-Distilled Reasoner（OPSD 命名论文）

| 项目 | 内容 |
|------|------|
| **作者** | Siyan Zhao 等 |
| **机构** | UCLA / Meta FAIR |
| **时间** | 2026.01 |
| **arXiv** | [2601.18734](https://arxiv.org/abs/2601.18734) |
| **代码** | [siyan-zhao/OPSD](https://github.com/siyan-zhao/OPSD) |
| **博客** | [siyan-zhao.github.io/blog/2026/opsd](https://siyan-zhao.github.io/blog/2026/opsd/) |

### 🎯 动机
- 传统 OPD 需**独立教师模型**，部署复杂
- RL（GRPO）需要大量采样（如 8×16=128 个 rollout）→ 算力巨大
- 想做"**无需奖励模型**的持续对齐"：只要有带推理过程的高质量数据即可

### 💡 方法思路
**核心观察**：一个足够强的 LLM **可以合理化外部特权推理轨迹，并教给更弱的"自己"**。

**方法**：
- **单一模型**同时充当教师和学生
- **学生**：看问题（x）
- **教师**：看问题 + 验证过的推理轨迹（x, τ）
- 学生自采样（rollout）→ 教师在每步提供"正确答案的概率分布"
- 最小化 per-token **RKL**

**形式化**：
$$
\mathcal{L}_{\text{OPSD}} = \mathbb{E}_{x, y \sim \pi(\cdot|x)} \sum_t D_{\text{RKL}}\left( \pi(y_t | x, y_{<t}) \,\|\, \pi(y_t | x, y_{<t}, \tau) \right)
$$

**关键点**：
- 同一模型在**不同上下文**下扮演两个角色
- "特权信息 τ"是 gap 的来源

### 📊 效果
- 数学推理：优于 off-policy 蒸馏
- 算力开销远小于 GRPO（1×8 rollouts vs GRPO 8×16）
- 与 GRPO 在 1024 长度内对齐

### ⚠️ 局限
- 依赖**带推理过程的高质量数据**
- 模糊 SFT/RL 边界，理解有挑战

---

## 2. SDFT-Continual — 持续学习自蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | Idan Shen 等 |
| **机构** | MIT / ETH |
| **时间** | 2026.01 |
| **arXiv** | [2601.19897](https://arxiv.org/abs/2601.19897) |
| **代码** | [idanshen/Self-Distillation](https://github.com/idanshen/Self-Distillation) |

### 🎯 动机
- LLM 持续学习新知识时，**灾难性遗忘**严重
- 现有方法（EWC、replay）成本高
- 想要**自蒸馏式持续学习**

### 💡 方法思路
**核心机制**：**Demo 条件化自蒸馏**

- **学生**：面对新任务
- **教师**：同模型 + 看到 demo（特权上下文）
- 在学生 rollouts 上做 RKL 对齐

**关键洞察**：demo 提供"如何推理"的特权信号，让学生学会"在新任务上沿用相同模式"。

### 📊 效果
- 在持续学习 benchmark 上缓解灾难性遗忘
- 训练成本低

### ⚠️ 局限
- 需要 demo 数据
- 对 demo 质量敏感

---

## 3. MTP Self-Distill — 多 token 预测自蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | UMD / LLNL |
| **时间** | 2026.02 |
| **arXiv** | [2602.06019](https://arxiv.org/abs/2602.06019) |
| **代码** | [jwkirchenbauer/mtp-lm](https://github.com/jwkirchenbauer/mtp-lm) |

### 🎯 动机
- 传统 LLM 一次预测一个 token
- **多 token 预测（MTP）** 可加速推理，但训练复杂
- 想用自蒸馏做 MTP

### 💡 方法思路
**核心机制**：**同模型自蒸馏 MTP**

- **教师**：同模型 + 看到未来 token
- **学生**：同模型，只看当前 token
- 用 RKL 在学生 rollouts 上做对齐

### 📊 效果
- 实现 MTP 自蒸馏
- 推理加速

### ⚠️ 局限
- 实现复杂
- 收益取决于任务

---

## 4. OPCD — On-Policy Context Distillation

| 项目 | 内容 |
|------|------|
| **机构** | Microsoft Research |
| **时间** | 2026.02 |
| **arXiv** | [2602.12275](https://arxiv.org/abs/2602.12275) |
| **代码** | [microsoft/LMOps](https://github.com/microsoft/LMOps) |

### 🎯 动机
- 上下文学习（ICL）依赖长 prompt，但**推理时上下文未必一直可用**
- 想要"把上下文知识内化到模型参数中"
- 内部化后无需在 prompt 中重复

### 💡 方法思路
**核心机制**：**ICL 知识内化**

- **学生**：看 query（无上下文）
- **教师**：同模型 + 看 query + 上下文
- 在学生 rollouts 上做 RKL 对齐

**关键设计**：
- 上下文是"特权信息"
- 训练后学生无需上下文就能内化知识

### 📊 效果
- 在 QA 任务上内化效果显著
- 推理时无需长 prompt

### ⚠️ 局限
- 仅适合"上下文依赖型"任务
- 训练数据需要上下文标注

---

## 5. GATES — 文档条件化自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | UMD |
| **时间** | 2026.02 |
| **arXiv** | [2602.20574](https://arxiv.org/abs/2602.20574) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 文档 QA 中，学生无文档输入，回答效果差
- 想要"内化文档知识"
- 现有方法偏 off-policy

### 💡 方法思路
**核心机制**：**文档条件化教师 + 学生自采样**

- **学生**：看问题（无文档）
- **教师**：同模型 + 看问题 + 文档
- 在学生 rollouts 上做 RKL

**关键设计**：教师"看文档"是特权信号；学生学完后无需文档也能答。

### ⚠️ 严格度说明
- 论文自身消融显示：**off-policy 文档级蒸馏贡献主要增益**，on-policy student-rollout updates 贡献 "modest additional improvement"

### 📊 效果
- 在文档 QA 上有效
- 蒸馏后学生可独立回答

### ⚠️ 局限
- 主要是 off-policy 驱动
- 文档质量影响大

---

## 6. CRISP / OPSDC — 推理压缩自蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | HJSang 等 |
| **机构** | LinkedIn |
| **时间** | 2026.03 |
| **arXiv** | [2603.05433](https://arxiv.org/abs/2603.05433) |
| **代码** | [HJSang/CRISP_Reasoning_Compression](https://github.com/HJSang/CRISP_Reasoning_Compression) |

### 🎯 动机
- 长 CoT 推理（如 R1 风格）**输出太长**，部署成本高
- 直接用"长度惩罚"做 RL 训练，会**导致熵崩塌**（输出变得短而信息量低）
- 想要**压缩 CoT 同时保持质量**

### 💡 方法思路
**核心机制**：**"Be Concise" 前缀自蒸馏**

- **学生**：看问题，生成（可能冗长）
- **教师**：同模型 + 看问题 + "Be Concise" 指令前缀
- 在学生 rollouts 上做 RKL

**核心洞察**：通过指令前缀**条件化出"简洁版自己"**，而非硬性长度惩罚。

### 📊 效果
- 长 CoT 压缩效果显著
- **无熵崩塌**（对比 RL + length penalty）

### ⚠️ 局限
- 需要基模型能听懂 "Be Concise"
- 压缩幅度有限

---

## 7. OEL — Online Experiential Learning

| 项目 | 内容 |
|------|------|
| **机构** | Microsoft Research |
| **时间** | 2026.03 |
| **arXiv** | [2603.16856](https://arxiv.org/abs/2603.16856) |
| **代码** | [microsoft/LMOps](https://github.com/microsoft/LMOps) |

### 🎯 动机
- 现有 LLM 在**游戏/规划任务**上缺乏在线学习能力
- RL 方法样本效率低
- 想要"边玩边学"的自蒸馏

### 💡 方法思路
**核心机制**：**环境交互式自蒸馏**

- **学生**：在游戏环境中 rollout
- **教师**：同模型 + 看到环境反馈
- 在学生 rollouts 上做 RKL

**应用场景**：交互式游戏、规划任务

### 📊 效果
- 游戏环境下有效

### ⚠️ 局限
- 仅适合有明确环境反馈的任务
- 通用性待验证

---

## 8. Why-Does-Self-Distillation-Degrade — 失败模式诊断

> 🎯 **分析型论文**（非新算法）：揭示 OPSD 的"特权上下文过富"会**损害 OOD 能力**。

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | MSR / KAIST / SNU |
| **时间** | 2026.03 |
| **arXiv** | [2603.24472](https://arxiv.org/abs/2603.24472) |
| **代码** | [beanie00/self-distillation-analysis](https://github.com/beanie00/self-distillation-analysis) |

### 🎯 动机
- OPSD 在 in-domain 数据上提升明显，但**OOD 能力下降**
- 想要诊断"为什么"以及"什么时候"

### 💡 方法思路
**核心发现**：**特权上下文过富会抑制学生的认识性表达（epistemic verbalization）**

- 学生在特权信息引导下**变得"自信"**，但失去表达不确定性的能力
- in-domain 提升，**OOD 下降最高 40%**（Qwen3-8B / DeepSeek-Distill-Qwen-7B / Olmo3-7B-Instruct）

**诊断工具**：
- 测量学生回答中的"uncertainty tokens"（"I think"、"maybe"等）
- 训练中观察这些 token 频率变化

### ⚠️ 严格度说明
- 纯分析型论文，**未提出新算法**
- 但揭示了 OPSD 设计的**关键权衡**

### 📊 价值
- 提醒设计者：**特权上下文是双刃剑**
- 推动后续工作重新审视 OPSD 假设

### ⚠️ 局限
- 仅分析 OPSD，未给出明确修复方案

---

## 9. Apple SSD — 极简自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | Apple MLR |
| **时间** | 2026.04 |
| **arXiv** | [2604.01193](https://arxiv.org/abs/2604.01193) |
| **代码** | [apple/ml-ssd](https://github.com/apple/ml-ssd) |

### 🎯 动机
- 现有 OPSD 方法较复杂（特权上下文设计 + KL 损失）
- 想要"极简"自蒸馏

### 💡 方法思路
**核心机制**：**退化的 OPSD —— 无 KL 信号**

- 用不同 temperature/truncation 采样
- 然后 SFT 在这些自采样数据上

**"特权上下文"**：仅是解码配置（temperature）

### ⚠️ 严格度说明
- **C2 部分失败**：无真正的教师 KL 信号
- 更接近 **STaR 风格自举**，而非 OPSD

### 📊 效果
- 在代码生成任务上有效
- 实现极简

### ⚠️ 局限
- 严格意义上不算 OPSD
- 收益有限

---

## 10. Skill-SD — 多轮 Agent 技能自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | UCAS / CUHK / USTC / vivo AI Lab |
| **时间** | 2026.04 |
| **arXiv** | [2604.10674](https://arxiv.org/abs/2604.10674) |
| **项目页** | [skill-sd.github.io](https://skill-sd.github.io/) |

### 🎯 动机
- 多轮 Agent 任务（AppWorld、Sokoban）需要**技能复用**
- 想要从完成轨迹中**蒸馏出可复用技能**
- 现有 OPSD 主要是单轮文本

### 💡 方法思路
**核心机制**：**技能条件化自蒸馏**

- 学生：执行多轮任务
- 教师：同模型 + **从完成轨迹提取的技能摘要**（特权信息）
- 用 **GRPO + 加权 RKL** 训练

**关键设计**：
- 技能**仅供教师看**，学生不接触
- 动态教师同步
- 采样 token（非全 vocab）蒸馏

### 📊 效果
- AppWorld、Sokoban 等多轮任务上 SOTA
- 技能可解释

### ⚠️ 局限
- 技能摘要质量敏感
- 实现复杂

---

## 11. SD-Zero — 自修订自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | Princeton / Toronto / CMU |
| **时间** | 2026.04 |
| **arXiv** | [2604.12002](https://arxiv.org/abs/2604.12002) |
| **类型** | 📄 paper-only |

### 🎯 动机
- RL 的**二元奖励**（如答案对错）信息密度低
- 想要把二元奖励**转化为密集监督**

### 💡 方法思路
**核心机制**：**自修订器（Reviser）将二元奖励转化为密集信号**

- **Generator**：学生，生成答案
- **Reviser**：同模型 + 看到 Generator 的答案 + 二元奖励
- 蒸馏 Reviser → Generator

**特权上下文**：Generator 答案 + 二元奖励

### ⚠️ 严格度说明
- 论文与 GRPO 对比，但**本身不是 RL**（无策略梯度目标）
- 奖励作为**条件化信号**而非 return

### 📊 效果
- Qwen3-4B-Instruct / Olmo-3-7B-Instruct 上 **≥10% 超过 base**
- 优于 RFT、GRPO、SDFT

### ⚠️ 局限
- 依赖 Reviser 能力
- 需仔细调二元奖励阈值

---

## 12. π-Play — 多智能体自博弈自蒸馏

> 🎯 **首个把"自博弈 → 自蒸馏"完整化的工作**。

| 项目 | 内容 |
|------|------|
| **机构** | CASIA / UCAS / 美团 |
| **时间** | 2026.04 |
| **arXiv** | [2604.14054](https://arxiv.org/abs/2604.14054) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 搜索 / 深研究 Agent 训练需要**大量人工标注**
- 想要"无外部数据"的自博弈训练
- 稀疏奖励 → 难学

### 💡 方法思路
**核心机制**：**Examiner ↔ Student 自博弈**

- **Examiner**：同模型，生成问题（**带问题构造路径 QCP**）
- **Student/Teacher**：同模型 + EMA 跟踪（τ=0.05）
- **特权上下文**：QCP（Examiner 生成问题时用到的反向路径）
- 用 per-token **RKL** 蒸馏

**关键洞见**：QCP 是**反向求解过程**，是特权信号。

### ⚠️ 严格度说明
- 教师=学生 EMA 跟踪（参数不完全相同）
- 论文自标为 "Privileged Self-Distillation"

### 📊 效果
- **完全无外部数据**训练
- NQ、TriviaQA、HotpotQA 等 SOTA
- 比常规自博弈**样本效率高 2-3×**

### ⚠️ 局限
- EMA 跟踪需精调
- 多智能体训练不稳定

---

## 13. OPSDL — 长上下文自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | Baidu |
| **时间** | 2026.04 |
| **arXiv** | [2604.17535](https://arxiv.org/abs/2604.17535) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有 LLM 在**长上下文**任务上能力弱
- 想要长上下文自蒸馏
- 直接用长文本 OPD 显存爆炸

### 💡 方法思路
**核心机制**：**短上下文同模型做教师**

- **学生**：处理长上下文
- **教师**：同模型 + 短上下文（特权简化信息）
- 用点式 RKL 训练

### 📊 效果
- 在长上下文 benchmark 上有效

### ⚠️ 局限
- 短上下文设计影响大
- 实现细节需读 paper

---

## 14. MSD — 多语言安全自蒸馏

| 项目 | 内容 |
|------|------|
| **机构** | Tongji / 上海 AI Lab |
| **时间** | 2026.05 |
| **arXiv** | [2605.02971](https://arxiv.org/abs/2605.02971) |
| **类型** | 📄 paper-only |

### 🎯 动机
- LLM 安全对齐**主要用英语训练**，其他语言安全性差
- 想要**多语言安全自蒸馏**
- 跨语言翻译 + CoT 是特权信息

### 💡 方法思路
**核心机制**：**跨语言特权自蒸馏 + DPSW 权重**

- **学生**：面对多语言 query（任意语言）
- **教师**：同模型 + 英语翻译 + CoT 指令（特权跨语言上下文）
- 用 per-token RKL
- **DPSW 权重**（Dual-Perspective Safety Weighting）：
  $$w_t = w_t^T \cdot w_t^S$$
  - $w_t^T$：教师 top-K 熵（安全关键性）
  - $w_t^S$：学生分歧风险（$1 - p_S$）

### 📊 效果
- 越狱 + 实用性 benchmark 上提升
- 无需翻译后的多语言 response 数据

### ⚠️ 局限
- 依赖英语 CoT 质量
- 实现复杂

---

## 15. COPSD — 跨语言 OPSD

| 项目 | 内容 |
|------|------|
| **机构** | LMU Munich / MCML |
| **时间** | 2026.05 |
| **arXiv** | [2605.09548](https://arxiv.org/abs/2605.09548) |
| **代码** | [cisnlp/COPSD](https://github.com/cisnlp/COPSD) |

### 🎯 动机
- 低资源语言（17 个非洲语言）数学推理能力差
- 现有方法要么用大量翻译数据（贵），要么用英语单语训练
- 想要**模型自身高资源能力迁移到低资源语言**

### 💡 方法思路
**核心机制**：**跨语言自蒸馏**

- **学生**：在低资源语言上 rollout
- **教师**：同模型 + 英语问题翻译 + 参考解（特权跨语言上下文）
- 用全 vocab logit RKL
- 教师冻结，梯度仅通过学生

### 📊 效果
- 17 个低资源非洲语言数学推理提升
- PolyMath、AfriMGSM SOTA
- 答案格式依从性提升

### ⚠️ 局限
- 需要英语参考解
- 仅适合有英语基础的低资源语言
