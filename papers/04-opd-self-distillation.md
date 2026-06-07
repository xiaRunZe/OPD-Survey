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

---

## 📅 2026-06 月新论文（9 篇）

> 本月新拉取的 9 篇 OPSD 论文，按主题归位到本章。每篇采用 5 段结构（问题-思路-方法-效果-局限）。

### CGTR — When Should the Teacher Move?（Self-OPD 时序耦合）

| 项目 | 内容 |
|------|------|
| **作者** | Haowei Guo 等 |
| **时间** | 2026-06-02 |
| **arXiv** | [2606.03532](https://arxiv.org/abs/2606.03532) |
| **类别** | ♻️ OPSD / 教师调度 |

**核心创新**：发现 Self-OPD 失败模式 **state-oblivious collapse**——短时最优的固定刷新在长程训练中**灾难性失败**。提出 **Consolidation-Gated Teacher Refresh (CGTR)**，仅在"奖励改善 + length-tail 安全"双重证据下更新教师。

**关键发现**：
- "隔离期"（教师两次更新间完全冻结）才是关键，非教师年龄
- 诊断框架：temporal KL structure / refresh shock / length-tail risk
- 4 任务（Chem/Bio/Phys/ToolUse）**零崩溃 + 最高最终分**
- **自调节**刷新频率，无需 per-dataset 调参

**局限**：需可靠 reward；调度策略对超参敏感。

---

### COPSD — Constitutional On-Policy Safe Distillation

| 项目 | 内容 |
|------|------|
| **作者** | Ming Wen 等 |
| **时间** | 2026-06-02 |
| **arXiv** | [2606.03089](https://arxiv.org/abs/2606.03089) |
| **类别** | ♻️ OPSD / 安全对齐 |

**核心创新**：把 OPSD 失败形式化为"**非正交语义空间的几何泄漏**"——安全压力泄漏到表达性维度。提出 COPSD = Cross-SFT cold-start 校准教师 + 宪法条件化 OPSD。
- 12 个 benchmark 上更强 safety-helpfulness 权衡
- 对通用推理的 **safety tax 显著降低**

**局限**：Cross-SFT 需额外数据；几何泄漏理论待形式化。

---

### DistIL — Distributional DAgger（理论）

| 项目 | 内容 |
|------|------|
| **作者** | Rishabh Agrawal, Jacob Fein-Ashley, Paria Rashidinejad |
| **时间** | 2026-06-03 |
| **arXiv** | [2606.05152](https://arxiv.org/abs/2606.05152) |
| **类别** | ♻️ OPSD / 理论 + 实践 |

**核心创新 / 理论贡献**：
- **理论证明**：基于 RKL 或 JSD 的自蒸馏目标**不能保证**单调策略改进（即使专家奖励更高，更新仍可能增加差动作概率）
- **FKL（前向交叉熵）能保证**单调改进 + regret bound
- 序列级梯度做 dense credit assignment

**实践**：DistIL 在科学推理、编程、难数学题上**稳定超越** RLVR 和 RL+自蒸馏基线，Pass@N 提升。

**局限**：FKL 是 mode-covering，可能过度泛化。

**意义**：从理论上解释了为何 RKL/JSD 自蒸馏常不稳定。

---

### SDPG — Self-Distilled Policy Gradient

| 项目 | 内容 |
|------|------|
| **作者** | Yifeng Liu 等 |
| **时间** | 2026-06-02 |
| **arXiv** | [2606.04036](https://arxiv.org/abs/2606.04036) |
| **代码** | [lauyikfung/SDPG](https://github.com/lauyikfung/SDPG) |
| **类别** | ♻️ OPSD + RL 混合 |

**核心机制**：
- GRPO group-relative verifier advantage + 标准化 std
- **全词表 on-policy 自蒸馏 KL** 辅助损失
- 参考策略 KL 正则

**效果**：比 RLVR 和自蒸馏基线**更稳定、更高分**。

**局限**：全词表蒸馏显存贵；组合损失权重敏感。

---

### Sleep — LMs Need Sleep（持续学习 OPSD）

| 项目 | 内容 |
|------|------|
| **作者** | Ali Behrouz 等 |
| **时间** | 2026-06-02 |
| **arXiv** | [2606.03979](https://arxiv.org/abs/2606.03979) |
| **类别** | ♻️ OPSD / 持续学习循环 |

**核心范式**（仿人脑"睡眠"）：
1. **Memory Consolidation**（向上蒸馏）：小模型记忆 → 大模型容量扩张，**on-policy distillation + RL 模仿学习**（Generalized Distillation）
2. **Dreaming**（自我改进）：用 RL 生成合成数据 curriculum

**效果**：long-horizon、持续学习、知识并入、few-shot 泛化均显著。

**局限**：训练流程复杂；RL 阶段计算量大。

---

#### 📄 [CAST: Non-Privileged Clipped Asymmetric Self-Teaching](https://arxiv.org/abs/2606.00172)
- **arXiv**: [2606.00172](https://arxiv.org/abs/2606.00172) | 2026-06
- **🎯 问题**: GRPO 的 outcome-level reward **稀疏**；group-relative advantage 在**全对/全错**组里**为零梯度**（浪费）。OPSD 给出 dense token 信号，但**token 偏好未必对齐 trajectory 正确性** —— 经验诊断显示 OPSD 信号在正确/错误 trajectory 上**噪声分布不同**。
- **💡 思路**: **别要参考解，也能让 token 监督和 trajectory 正确性对齐**。用 stop-gradient self-teacher 沿**trajectory 正确性**塑形 token advantage —— 把"答案信息"换成"对错信号"，更通用。
- **🔧 方法**:
  1. **CAST = answer-free self-distillation for GRPO-style RLVR**（不需要参考答案/特权信息）；
  2. Stop-gradient self-teacher 沿 trajectory 正确性塑形 token-level advantages；
  3. **双向局部 advantage 符号翻转**：
     - 正确 trajectory 中 **teacher-negative tokens** 拿**负 advantage**（抑制错误 sub-mode）；
     - 错误 trajectory 中 **teacher-positive tokens** 拿**有界正 advantage**（鼓励正确 sub-mode）；
  4. **零方差组**（all-correct/all-wrong）分配**有界符号约束**基础 advantage → 这些本应零梯度的组也能贡献 verifier-signed token feedback。
- **📊 效果**: 数学推理上 CAST 改进 RLVR 训练同时保留轻量级 verifier-grounded trajectory-level 目标；**零方差组有效利用**是 GRPO-style RLVR 的关键优化。
- **⚠️ 局限**: 仍需 verifier 信号（不是完全 unsupervised）；teacher-positive/negative 阈值需设计；对 verifier 质量敏感；与标准 OPSD 的算力开销对比未详细讨论。
- **价值**: 把 GRPO 和 OPSD **正交结合**（保留 verifier-grounded 目标 + token 监督），且**不需要参考解** —— 适用范围比标准 OPSD 更广，零方差组利用是 RLVR 实操上的关键收益。


#### 📄 [SGSD: Skill-Conditioned Gated Self-Distillation for LLM Reasoning](https://arxiv.org/abs/2605.28791) | Jiazhen Huang, 2026-05-27
- **🎯 问题**: 现有 OPSD 用"**可信 PI**"（参考解/成功轨迹）作教师信号。但 PI 能否来自**经验派生的技能库**（从历史训练数据归纳的"知识-错误"对，紧凑可复用但**可能不相关/误导**）？换言之 —— **"特权信息"必须可信**这个默认假设是否必要？
- **💡 思路**: 形式化重定义 —— **不假设教师可信，每个教师假设都要 verifier 验证极性**。"技能库"作为多教师池的来源，**每条技能都可能是错的**，但 verifier 知道哪条有用。
- **🔧 方法**:
  1. **检索 skill-mistake pairs**（从经验数据）；
  2. 构造**多教师池**（每个教师条件在一条技能上）；
  3. 所有技能条件教师**对同一 plain-prompt student rollout 评分**；
  4. **Verifier 验证每个教师极性**：
     - 支持成功 / 抑制失败 → **正监督**；
     - 反向 → **翻转**（正变负 / 负变正）；
  5. **鲁棒 gated 目标** 蒸馏**有信息师生分歧**，抑制**不确定/极端**信号。
- **📊 效果**: 数学推理 benchmark 一致超 GRPO；Qwen3-1.7B 上 **AIME24/25/HMMT25 平均超 GRPO +6.2%、超 OPSD +1.7%**。代码 [walawalagoose/SGSD](https://github.com/walawalagoose/SGSD)。
- **⚠️ 局限**: 技能库质量影响大；多教师池构造代价；verifier 验证成本；技能检索准确性。是否适用非数学/工具调用任务未验证。
- **价值**: 把"**特权信息**"从"**必须可信**"变成"**可以怀疑**" —— 让 OPSD 适用范围从"有标准答案的任务"扩展到"任何能验证结果的任务"。


#### 📄 [ROSD: Reflective On-Policy Self-Distillation for LLM Reasoning across Domains](https://arxiv.org/abs/2605.28014) | Ziqi Zhao, 2026-05-27
- **🎯 问题**: 现有 OPSD **域内增益有限、域外泛化差**。两个根因：① self-teacher 条件在**已验证解**上 → 鼓励**模仿训练域参考轨迹**（不是学推理，是学参考解）；② 在**完整 response** 上蒸馏 → **覆盖有效推理 prefix** + 强化对参考解的过拟合。
- **💡 思路**: 转换范式 —— **别"模仿"，"纠错"**。让模型**先反思自己哪里错**，**只在错的地方学**。问题从"如何模仿得更像"变成"**如何纠错更准**"。
- **🔧 方法**:
  1. **Self-reflector** 提取**纠正想法**（该 rollout 应该怎么改） + **定位首个错误 span**（该改的精确位置）；
  2. 纠正想法引导 self-teacher → **针对性监督**（不是"模仿参考解"，是"修正自己"）；
  3. 错误 span 限制蒸馏到**需要纠正的位置** → 保留 valid prefixes（不覆盖已经做对的部分）；
  4. 代码 [ZiqiZhao1/ROSD](https://github.com/ZiqiZhao1/ROSD)。
- **📊 效果**: 多个 in/out-of-domain reasoning benchmark — 域内推理整体更强，**域外泛化显著优于标准 OPSD**。验证"模仿 → 纠错"范式转变确实改善泛化。
- **⚠️ 局限**: Self-reflector 需要训练（额外成本）；错误 span 定位准确性影响效果；可能仍需参考解作反射起点；反射器在长 chain-of-thought 上效果未充分验证。
- **价值**: 与 SGSD 思路互补（**SGSD 改"教师来源"，ROSD 改"蒸馏位置"**）—— OPSD 从"模仿"转"纠错"对 OOD 泛化是关键范式转变。


#### 📄 [SC-SDPO: Restoring the Sweet Spot — Pass-Rate Weighted Self-Distillation](https://arxiv.org/abs/2605.27765) | Zehao Liu, 2026-05-26
- **🎯 问题**: GRPO 的 group-relative advantage **自然聚焦在中间难度"甜点"**（容易组和全对组 advantage 都被压缩为零）。SDPO 的 KL-based advantage **缺乏难度感知** —— 它不区分"该学的题"和"已会/不会的题"，学习信号平均散到所有题。
- **💡 思路**: 借鉴 GRPO 的 "learnability" 框架，**显式按难度加权**。问题不是"如何改进 SDPO 损失"而是"**如何让 SDPO 自然有 difficulty awareness**"。
- **🔧 方法**:
  1. 通过 learnability 框架分析 GRPO advantage normalization（为什么 GRPO 自然聚焦甜点）；
  2. 推广到归一化奖励 → normalization 吸收 variance 项 p(1-p) → 留 **√p(1-p)** 作 per-question gradient 唯一残差 scaling factor；
  3. 处方：**按 [p̂(1-p̂)]^(1/2) 加权每个 question 的 SDPO loss** → **SC-SDPO**（Scale-Consistent SDPO）；
  4. **权重零成本**：p̂ 从 batch 自适应归一化 rollout 拿 → **隐式 curriculum 跟踪模型能力演化**。
- **📊 效果**: 科学推理和工具调用 benchmark 一致超 SDPO；**Qwen3-8B +3.2/+4.3**（mean@16/maj@16）；**OLMo-3-7B +1.8/+3.0**。稳定训练动态。
- **⚠️ 局限**: p̂ 估计依赖 batch（batch 太小时不稳定）；权重函数 [p̂(1-p̂)]^(1/2) 是否最优仍是 open；只验证了科学推理和工具调用。
- **价值**: 把"**难度感知**"从"**GRPO 经验直觉**"变成"**理论推出的 SC-SDPO 权重**"，且**零额外成本**接入 SDPO —— 复用了 GRPO 的隐式 curriculum 优势。


#### 📄 [MAIGO: Mitigating Lost-in-Conversation with History-Cleaned OPSD](https://arxiv.org/abs/2605.27186) | Haoyu Zheng, 2026-05-26
- **🎯 问题**: LLM **完整 prompt 能解，多轮展开退化**（"lost-in-conversation" / LiC gap）。论文追溯到 **self-contamination**：**中间助手回复进入后续上下文，把早期偏差带下去**。结果是模型越往后越偏。
- **💡 思路**: 对症下药 —— **既然是"中间回复污染"，就在训练时"清洗历史"**。问题从"如何提升多轮鲁棒性"变成"**如何让模型不学'污染'模式**"。
- **🔧 方法**:
  1. MAIGO = **on-policy self-distillation + 历史清洗**（不需要 verifier / state labels / inference-time scaffolding）；
  2. **中间轮** (middle turns)：**移除 prior 助手回复**（保留 user-visible sharded prefix）→ "干净"参考；
  3. **答案轮** (answer turns)：配对 **full-view references**（看完整 user-side dialogue）作"完整"参考；
  4. **可靠性权重**降低与 clean reference 不一致的中间轮样本；
  5. 在 **LiC paired-view protocol**（deterministic verifiers）下验证。
- **📊 效果**: Qwen2.5-7B-Instruct **SHARDED 准确率 52.8 → 66.1**（**+13.3**）；**SHARDED/FULL 比率 66.5% → 84.1%**（**+17.6%**）；FULL 准确率损失 **< 2.3 点**。
- **⚠️ 局限**: 要 paired-view 数据（同一对话的 full 和 sharded 视图）；reliability weight 阈值需设定；多轮多步推理场景未验证；推理时仍用完整多轮（清洗只在训练）。
- **价值**: 首次把 LiC gap 归因到 **self-contamination**（**可训练成分**），给出**对症**修复（history cleaning），是 OPSD 走向多轮对话的关键一步。


#### 📄 [SPD: Self-Policy Distillation via Capability-Selective Subspace Projection](https://arxiv.org/abs/2605.22675) | Guangya Hao, 2026-05-21
- **🎯 问题**: 现有自蒸馏两类方案都有根本缺陷：① 靠**外部信号策展**自生成输出（正确性过滤、执行反馈、奖励搜索）→ **贵**，**最强前沿模型不可用**；② **跳过策展全训** → 任务特定、难泛化。**更深弱点**：自生成输出把**任务相关能力**和**风格/格式/模型特定错误**纠缠 —— 想学 A 能力，style/format B 错误也一起学。
- **💡 思路**: 转换维度 —— **别在"要不要外部信号"上选，去找"信号在模型内部哪里"**。**从模型自己在正确性定义 token 上的梯度里提取低秩能力子空间**，自生成时把 KV activation 投到子空间 → 学生生成内容**自动聚焦在能力维度**而非风格/格式维度。
- **🔧 方法**:
  1. 提取**低秩 capability subspace**（从正确性定义 token 的梯度，主成分分析出"能力方向"）；
  2. 自生成时**把 KV activation 投到子空间**（隐式策展：不学风格/格式，只学能力）；
  3. 标准 next-token prediction loss 训练（**无外部信号**）；
  4. 整个流程是**self-contained**（不依赖外部奖励/过滤）。
- **📊 效果**: 代码/数学/MCQ QA **比 SOTA 自蒸馏最多 +13%**，**比预训练基线 +16%**。**OOD 泛化 +15%**（关键能力选择让学到的能力是 generalizable 的，不是 task-specific）。
- **⚠️ 局限**: 低秩子空间**维度是新超参**；正确性定义 token 选择需要任务知识（不能完全自包含）；预训练梯度计算代价；是否适用开放生成任务未验证。
- **价值**: 把"**自蒸馏策展**"从"**需要外部信号**"变成"**内嵌于模型梯度**" —— 实用性大幅提升，且"能力选择"机制让 OOD 泛化自然涌现。


#### 📄 [CODE: From Fact Overwriting to Knowledge Evolution — Causal On-Policy Self-Distillation Editing](https://arxiv.org/abs/2605.28303) | Shuaike Li, 2026-05-27
- **🎯 问题**: 知识编辑 (KE) 主流 "**Static Fact Overwriting**" 把 LLM 当**离散数据库**，**强插孤立事实** → 触发 **Epistemic Dissonance**：未演化的旧先验强迫模型**显式否定**新事实。零失真代理下，**95.6% self-refutation**（即模型自己否定新插入的事实）。
- **💡 思路**: 范式转变 —— **别"覆盖事实"，"进化知识"**。基于**显式因果叙事**作更新 → conflict rate 6.6%（vs 95.6%）。再通过 on-policy distillation 把"进化"内化到参数。
- **🔧 方法**:
  1. **Causal Bootstrapping** 用显式因果叙事（vs 孤立事实）作更新基础；
  2. **Asymmetric On-Policy Distillation** 把**因果转换逻辑**"刻进"参数（asymmetric：保留旧相关事实 + 学新因果链）；
  3. 在 LLaMA-3.1 / Qwen-2.5 上验证。
- **📊 效果**: **Self-refutation 1.8%**（从 95.6% 暴跌）；**多跳准确率最高 83.5%**；离散事实注入 → 连贯知识进化。
- **⚠️ 局限**: 因果叙事需要**人为提供**（不是 unsupervised）；多步编辑场景未充分验证；non-QA 任务（生成）上未验证；长期稳定性（多次编辑后）需要进一步实验。
- **价值**: 把 KE 范式从"**Static Fact Overwriting**"转到"**Knowledge Evolution**" —— 是 KE 领域的范式转变，与"知识作为可演化系统"的认识论一致。代码 [CrashBugger/CODE](https://github.com/CrashBugger/CODE)。


#### 📄 [EDGE-OPD: Internalizing Privileged Context with Evidence Guided On-Policy Distillation](https://arxiv.org/abs/2605.23493) | 2026-05
- **🎯 问题**: OPSD 中**特权信息**（persona/私密事实/解题过程）**会改模型行为到超出预期** —— 改推理、降低通用能力、改响应长度/风格/局部 token 偏好。**OPSD 可能把学生训在副作用上**，而非预期的 transferable 行为。
- **💡 思路**: 在 **rare-token/identity 设置**下，把问题具体化为"学不到罕见目标" → 找原因（特权信息被稀释 / 被混淆） → 给"引导 rollout + 证据 mask"修复。
- **🔧 方法**:
  1. **Guided rollouts** —— 让特权上下文行为**在采样时就注入**，使罕见目标行为**真的出现在 on-policy 数据中**（vs 让学生自采样而特权信息被忽略）；
  2. **Evidence mask** —— student **只在特权上下文支持采样 token 的位置更新**（不是每个 token 都学），让 persona signal 集中在**正证据尾部**；
  3. Ablation：mask-region 显示 persona signal 局部化，证实证据驱动机制。
- **📊 效果**: **OPSD/RLSD（有/无 verifier）完全 fail 学不到 target identity**；EDGE-OPD + guided rollouts 成功。**OPSD/RLSD 在 rare 行为上的失败是**这篇工作的关键负面发现**，比"有效方法"更值得社区关注。
- **⚠️ 局限**: Rare-token/identity 设置是 narrow 场景；guided rollouts 实际实现复杂（要把特权信息在 rollout 阶段"提示"学生）；evidence mask 阈值需设定；通用行为（非 rare）是否也受益未验证。
- **价值**: 揭示 OPSD **副作用问题**（在 rare 行为上） + 给出**精准修复**（evidence mask），是 OPSD 走向实用的关键一步。负面发现（OPSD/RLSD 完全失败）比论文给出的"成功方法"更有指导意义。


#### 📄 [OISD: On-Policy Internal Self-Distillation of Language Models](https://arxiv.org/abs/2605.29089) | Pan He, 2026-05-27
- **🎯 问题**: 现有 RL post-training 主要优化**最终输出策略**的**稀疏 outcome reward**，**几乎忽略中间表征中的预测信号**。结果：RL 只动最后一层（logit head + 最后一两个 block），**前面所有层是"死"的**。
- **💡 思路**: 转换优化目标 —— **别只优化"最后一层的输出分布"，让最终层作"内部教师"教前面所有层**。"教师"不在模型外，**在模型内**。问题从"如何用 RL 优化最后一层"变成"**如何让整个网络在 RL 中一起学**"。
- **🔧 方法**:
  1. **OISD 范式**：final layer **同时**作 policy + detached 内部 teacher；
  2. 两种对齐机制：
     - **Logit alignment** —— 转移 high-level reasoning behavior（"how to think"，从最后一层 logits 教中间层 logits）；
     - **Attention alignment** —— 强制一致的 attention pattern（"where to look"，从最后一层 attention 教中间层 attention）；
  3. **Signed advantage-weighted JSD alignment**（带 signed advantage 加权 → 与 GRPO 兼容）；
  4. **统一 acting policy 保持策略一致性**（避免训练/推理分布漂移）。
- **📊 效果**: 4 个数学推理任务上**一致超 reasoning RL baselines**。表征收备在推理 RL 中是新增的优化维度。
- **⚠️ 局限**: 选定**哪些中间层**是新设计选择（全部？每隔一层？哪些维度？）；JSD 对齐强度需调；attention alignment 计算代价（每层 attention map 对齐）；不依赖外部 PI 的代价是内部信号可能不如外部教师强。
- **价值**: 把 RL 后训练从"**只动最后一层**"变成"**整个网络一起学**" —— 表征级优化是 post-training 的新维度，**不依赖外部 PI** 让其成为 OPSD 家族里独特的"内化"路线。代码 [THE-MALT-LAB/OISD](https://github.com/THE-MALT-LAB/OISD)。


