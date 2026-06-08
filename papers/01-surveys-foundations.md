# 📚 一、综述、基础与立场论文

> 本章节收录 OPD/OPSD 领域的**元文献**：奠基性论文、综述博客、立场论文。

---

## 1. GKD — On-Policy Distillation of Language Models

> 🎯 **奠基性论文**，首次正式命名并形式化 "On-Policy Distillation" 概念，ICLR 2024。

| 项目 | 内容 |
|------|------|
| **作者** | Rishabh Agarwal, Nino Vieillard, Yongchao Zhou, Piotr Stanczyk, Sabela Ramos Garea, Matthieu Geist, Olivier Bachem |
| **机构** | Google DeepMind |
| **时间** | 2023.06 |
| **会议** | ICLR 2024 |
| **arXiv** | [2306.13649](https://arxiv.org/abs/2306.13649) |
| **代码** | [TRL `GKDTrainer`](https://github.com/huggingface/trl/blob/main/trl/experimental/gkd/gkd_trainer.py) |

### 🎯 动机
传统的知识蒸馏（KD）使用**固定数据集**（教师预先生成）训练学生，这会引发两个问题：
1. **分布不匹配（Distribution Mismatch）**：学生训练时看到的是教师的数据分布，但推理时会按自己参数生成
2. **复合误差（Compounding Error）**：学生一旦犯错，会进入教师从未访问过的状态，导致错误累积

而强化学习（RL）虽然解决了分布不匹配问题，但**奖励信号稀疏**（如数学题只有最终答案对错），无法指导每一步决策。

### 💡 方法思路
**GKD 核心思想**：让学生在自己生成的样本上接受教师的监督，损失采用**可配置的 f-散度**：

$$
\mathcal{L}_{\text{GKD}} = \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_{\text{student}}(\cdot|x)} \left[ D_f\left(\pi_{\text{student}}(\cdot|x,y) \,\|\, \pi_{\text{teacher}}(\cdot|x,y)\right) \right]
$$

**两个关键技术**：
1. **数据混合**（λ-interpolation）：在 SFT 静态数据和学生自采样数据之间按比例混合
2. **Generalized JSD**：Jensen-Shannon 散度的广义形式，配置参数 β 即可在 FKL 和 RKL 之间切换

**三种配置**：
- `β=0`：前向 KL（FKL，mode-covering）
- `β=1`：逆向 KL（RKL，mode-seeking）
- `0<β<1`：JSD 插值

### 📊 效果
- 在多个任务上优于 SFT 和离线 KD
- 证明了**学生自生成数据 + 教师 token 级监督**的有效性

### ⚠️ 局限
- 仅适用于**白盒教师**（能拿到 logits）
- 计算成本仍较高（需要边采样边计算教师前向）

---

## 2. Thinking Machines Lab — On-Policy Distillation 博客

> 🎯 **工业界最佳实践指南**，2025 年下半年最火的 OPD 入门材料。

| 项目 | 内容 |
|------|------|
| **作者** | Kevin Lu 等 |
| **机构** | Thinking Machines Lab |
| **时间** | 2025.10 |
| **链接** | [thinkingmachines.ai/blog/on-policy-distillation](https://thinkingmachines.ai/blog/on-policy-distillation/) |
| **代码** | [tinker-cookbook](https://github.com/thinking-machines-lab/tinker-cookbook) |

### 🎯 动机
- 学术界已经有 GKD 等 OPD 论文，但**工业界落地经验**少
- 很多团队想用 RL（如 GRPO）训练推理模型，但 RL **采样成本高**（需 8×16 = 128 个 rollout）
- 需要一份**工程友好的"OPD 替代 RL" 实战指南**

### 💡 方法思路
**核心理念**：把"用 RL 训练学生"改成"用教师 logits 监督学生"：

```python
# 伪代码：将 RL 的 reward 换成 KL 散度
loss = -reward * log_prob              # RL 风格
loss = -log_prob_teacher * log_prob    # OPD 风格（KL 散度）
```

**三大实践要点**：
1. **教师 logit 缓存**：避免每步重新计算教师前向，节省显存
2. **逆向 KL（Mode-Seeking）**：用 RKL 让学生精确匹配教师的某个高质量模式，而非覆盖所有模式
3. **替换 RL 中的 ref model**：原来 RL 训练需要 ref model（冻结的初始模型）做 KL 约束，现在直接用更强的教师代替

**关键结论**：
> 用 7.7 万个 prompts 训练，达到 SFT 200 万 prompts 的效果 → **效率提升 25 倍**。

### 📊 效果
- 复现了 Qwen3 的 OPD 训练结果
- 算力仅需 RL 的 1/10

### ⚠️ 局限
- 需要部署"教师模型推理服务"
- 教师和学生 tokenizer 不一致时需要特殊处理（见 GOLD）

---

## 3. Revisiting OPD — 失败模式与简单修复

| 项目 | 内容 |
|------|------|
| **作者** | Xiaoyu Fu, 等 |
| **机构** | 中科院自动化所（CASIA） |
| **时间** | 2026.03 |
| **arXiv** | [2603.25562](https://arxiv.org/abs/2603.25562) |
| **代码** | [hhh675597/revisiting_opd](https://github.com/hhh675597/revisiting_opd) |

### 🎯 动机
GKD 等 OPD 方法理论上很自然，但**实际训练时常常不稳定**——同样的超参、同样的代码，在不同训练步数下表现差异巨大。作者通过分析训练日志、曲线，发现了**三类典型失败模式**。

### 💡 方法思路
**三类失败模式**：
1. **不均衡的单 token 信号（Imbalanced One-Token Signal）**：教师在学生采样的某个 token 上只给一个确定性答案，监督信号过强导致其他 token 学不到
2. **不可靠的前缀指导（Unreliable Prefix Guidance）**：长序列生成时，教师对早期 token 的指导会随序列变长而失真
3. **分词器不匹配（Tokenizer Mismatch）**：教师和学生的 tokenizer 不同，token 序列无法直接对齐

**修复方案**：
- **截断式逆向 KL**（Truncated Reverse KL）：用 top-p 采样，过滤低概率 token
- **特殊 token 掩码**（Special Token Masking）：忽略 padding、bos、eos 等无意义 token
- **规范化策略**：重新对齐不同 tokenizer 的概率分布

### 📊 效果
- 在多个 OPD 训练场景下显著提升稳定性
- 提供了一套**易复现的修复 recipe**

### ⚠️ 局限
- 修复方案在 1.5B–7B 模型上验证，超大规模（如 70B+）未充分测试

---

## 4. 腾讯 OPD 综述

| 项目 | 内容 |
|------|------|
| **作者** | Mingyang Song, Mao Zheng |
| **机构** | Tencent |
| **时间** | 2026.04 |
| **arXiv** | [2604.00626](https://arxiv.org/abs/2604.00626) |
| **类型** | 综述 |

### 🎯 动机
- 2024–2026 年 OPD 方向论文爆发式增长（50+ 篇），**缺少统一索引**
- 各类方法分散在 SFT、RL、KD、RLHF 领域，难以系统比较

### 💡 方法思路
**综述的分类法**：
- 按教师来源：外教师（白盒/黑盒）/ 自教师（同模型/历史 checkpoint）
- 按监督粒度：token 级 / 序列级 / 偏好级
- 按数据来源：固定数据集 / 学生自采样 / 混合

**核心贡献**：
- 整理了 50+ 种 OPD 变体
- 提供对比表格和实现细节
- 提出未来研究方向

### 📊 价值
- 作为**参考索引**使用，不必从头读
- 适合快速了解某个子方向

### ⚠️ 局限
- 综述方法，而非新方法
- 部分新方法（2026.04+）未涵盖

---

## 5. THUNLP Rethinking OPD — 现象、机制与配方

| 项目 | 内容 |
|------|------|
| **作者** | Yaxuan Li, Yuxin Zuo, Bingxiang He, Jinqian Zhang, Chaojun Xiao, Cheng Qian, Tianyu Yu, Huan-ang Gao, Wenkai Yang, Zhiyuan Liu, Ning Ding |
| **机构** | 清华大学 THUNLP |
| **时间** | 2026.04 |
| **arXiv** | [2604.13016](https://arxiv.org/abs/2604.13016) |
| **代码** | [thunlp/OPD](https://github.com/thunlp/OPD) |

### 🎯 动机
- OPD 已成为 LLM 后训练核心方法，但**训练动力学机制不清楚**
- 实践中 OPD 经常失败：相同代码、同超参，配置稍变结果就崩
- 需要系统研究："OPD 到底什么时候工作？什么时候失败？为什么？"

### 💡 方法思路
**两大核心发现**：

#### 发现 1：OPD 成功取决于两个条件
1. **思维模式兼容**（Compatible Thinking Patterns）：学生和教师必须有相似的思考方式
2. **真实新能力**（Genuinely New Capability）：即使思维模式一致，教师必须提供**学生在训练中从未见过**的真实新能力

**验证实验**："弱到强逆向蒸馏"——同家族 1.5B 蒸馏到 7B、7B 蒸馏到 14B，从学生视角看，教师分布与自身几乎无法区分 → 蒸馏失败。这反证了"新能力"的必要性。

#### 发现 2：Token 级机制
成功 OPD 的特征是**在学生访问的状态上，高概率 token 逐步对齐**：
- 97%-99% 的概率质量集中在**小共享 token 集**
- 训练过程中，这部分 token 的对齐程度持续提升

**修复方案**：
- **Off-policy 冷启动**：先用 SFT 数据做一轮预热
- **教师对齐的 prompt 选择**：挑选教师能给出"新能力"的 prompt 做 OPD

### 📊 效果
- 在 Qwen3-1.7B/4B 教师-学生对上的实验验证
- 提供**详细诊断工具**（token 对齐率曲线）

### ⚠️ 局限
- 实验规模为 1.7B–4B，超大规模未验证
- "教师必须更大"是经验性结论，缺乏理论证明

---

## 6. Lightning OPD — 离线 OPD 提升训练效率

| 项目 | 内容 |
|------|------|
| **作者** | Wu, Han, Cai |
| **机构** | 学术 |
| **时间** | 2026.04 |
| **arXiv** | [2604.13010](https://arxiv.org/abs/2604.13010) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 传统 OPD 需要**实时运行教师模型**，显存/算力开销大
- 教师模型必须与学生同步部署，**系统复杂度高**
- 想做"事后 OPD"：学生 SFT 完，再统一蒸馏

### 💡 方法思路
**核心创新**：**离线 OPD** —— 一次性缓存教师的 log-prob，后续学生训练时直接复用。

**关键技术**：
1. **教师一致性**（Teacher Consistency）：SFT 阶段和 OPD 阶段必须使用**同一教师的 log-prob**，否则会有梯度偏差
2. **缓存策略**：将教师对 SFT 数据的 log-prob 预先计算并存储

### ⚠️ 严格度说明
- 严格意义上不满足 "C1: 学生主动采样"（用历史 SFT 数据），作者称之为 **offline OPD**

### 📊 效果
- **消除了实时教师推理服务**
- 训练速度提升（无教师前向开销）

### ⚠️ 局限
- 牺牲了"on-policy"的灵活性，无法动态更新教师
- 缓存占用额外存储

---

## 7. OPSD Survey — On-Policy Self-Distillation 综述

| 项目 | 内容 |
|------|------|
| **时间** | 2026.05 |
| **arXiv** | [2605.18141](https://arxiv.org/abs/2605.18141) |
| **类型** | 综述 |

### 🎯 动机
- OPSD 作为 OPD 的子方向，独立成为研究热点
- 各类 OPSD 方法的"特权上下文"设计差异很大，缺少统一分类

### 💡 方法思路
**八大设计维度**：
1. 特权上下文类型（验证推理、CoT、文档等）
2. 教师/学生是否共享参数
3. 损失函数选择
4. 数据采样方式
5. 训练阶段
6. 应用领域
7. 评估方式
8. 失败模式分析

**核心价值**：作为该方向的"参考索引"使用。

---

## 8. OPSD — Self-Distilled Reasoner（OPSD 命名论文）

> 🎯 **OPSD 概念的奠基性论文**，首次提出"同一模型在特权上下文下同时做教师和学生"。

| 项目 | 内容 |
|------|------|
| **作者** | Siyan Zhao 等 |
| **机构** | UCLA / Meta FAIR |
| **时间** | 2026.01 |
| **arXiv** | [2601.18734](https://arxiv.org/abs/2601.18734) |
| **代码** | [siyan-zhao/OPSD](https://github.com/siyan-zhao/OPSD) |
| **博客** | [siyan-zhao.github.io/blog/2026/opsd](https://siyan-zhao.github.io/blog/2026/opsd/) |

### 🎯 动机
- RL（GRPO）需要**大量采样**（如 8×16=128 个 rollout）才能计算 advantage，**算力开销巨大**
- 传统 OPD 需要**独立教师模型**，部署复杂
- 想做"**无需奖励模型**的持续对齐"——只要有带推理过程的高质量数据就行

### 💡 方法思路
**核心观察**：一个足够强的 LLM **可以合理化外部的特权推理轨迹，并教给更弱的"自己"**。

**方法**：
1. **单一模型同时充当教师和学生**（不同上下文）
2. **学生**：只看问题（Problem）
3. **教师**：看问题 + 验证过的推理轨迹（Privileged Trace）
4. 学生自采样（rollout）→ 教师在每一步提供"正确答案的概率分布" → 最小化 RKL

**形式化**：
$$
\mathcal{L}_{\text{OPSD}} = \mathbb{E}_{x, y \sim \pi_{\text{student}}(\cdot|x)} \sum_t D_{\text{RKL}}\left( \pi_{\text{student}}(y_t | x, y_{<t}) \,\|\, \pi_{\text{teacher}}(y_t | x, y_{<t}, \text{trace}) \right)
$$

### 📊 效果
- 数学推理 benchmark：优于 off-policy 蒸馏
- Token 效率优于 GRPO
- 算力开销**远小于** GRPO

### ⚠️ 局限
- 需要**高质量推理过程数据**（如带 step-by-step solution 的数学题）
- 模糊了 SFT 和 RL 的边界，理解上有挑战
- 依赖模型本身有"合理化"能力（小模型可能学不会）

---

## 📌 小结

| 资源 | 关键定位 |
|------|---------|
| **GKD** | 奠基性概念提出者 |
| **Thinking Machines Blog** | 工业界最佳实践 |
| **Revisiting OPD** | 失败模式诊断 |
| **腾讯综述** | 50+ 方法索引 |
| **THUNLP Rethinking** | 理论机制分析 |
| **Lightning OPD** | 离线优化变体 |
| **OPSD Survey** | OPSD 子方向综述 |
| **Self-Distilled Reasoner** | OPSD 奠基论文 |

---

## 📚 2026 年 6 月论文（3 篇）

#### 📄 [OPD+: Rethinking the Advantage Design for On-Policy Distillation](https://arxiv.org/abs/2606.01039) | Hanyang Zhao, 2026-05-31
- **🎯 问题**: OPD 几乎所有实现都在**教师 logit 上加 stop-gradient**（避免教师随学生一起被更新导致不稳定）。这个操作是**经验工程技巧**，没人从数学上验证它对**各种 f-散度**（不只 KL）是否成立。一旦改成 JSD、χ²、reverse-KL，stop-gradient 是否还给出**正确的 advantage 估计**？不确定。
- **💡 思路**: 把 OPD 写成**通用 f-散度最小化**的统一目标，反过来**严格推导**在 stop-gradient 下梯度的偏差表达式 —— 用数学证明代替经验假设。问题变成"stop-gradient 对哪些散度类有偏、如何修正"。
- **🔧 方法**: 
  1. 在统一 f-散度框架下重新表述 OPD 的 advantage 估计；
  2. 数学证明：**对一般散度函数**，stop-gradient 会导致 advantage 估计**有偏**，且这个偏差会通过梯度累积污染最终目标；
  3. 提出 **OPD+**：去掉 stop-gradient 但加**正确的策略梯度修正项**（数学上让梯度无偏）；
  4. 框架支持任意 f-散度（KL、JSD、χ²、TV 等），用户按需选。
- **📊 效果**: 数学推理和工具调用 benchmark 上，OPD+ **比 stop-gradient 的 baseline KL 一致提升**，并且不同 f-散度选型带来额外的可调自由度。
- **⚠️ 局限**: 论文给出**理论修正项**，但实际实现代价（多算一份教师梯度、或维护一个 detached 副本）未详细讨论；对超大教师/学生模型的**显存与吞吐**影响需要工程验证。
- **价值**: 把"OPD 实现细节"从"经验技巧"变成"可证伪的数学对象"，是后续 OPD 理论工作（如 RKLOPD、F-divergence survey）的基础。


#### 📄 [A Predictive Law for On-Policy Self-Distillation From World Feedback](https://arxiv.org/abs/2605.30070) | Tommy He, 2026-05-28
- **🎯 问题**: 业界正从"标量奖励"走向"**丰富世界反馈**"（自然语言、verifier、模拟器）。OPSD 是这条路最自然的载体 —— 用任意反馈作 token 级学习信号。但问题是：**和 GRPO 等成熟方法相比，OPSD 到底什么时候有效、能不能预测它的结果？** 没人知道。你不知道该不该上 OPSD，也不知道该用哪种反馈、训练多久。
- **💡 思路**: 转换问题 —— **不要"事后解释 OPSD 结果"，而要"事前预测 OPSD 结果"**。从经验数据中找 OPSD 训练前后性能的**可量化关系**。如果发现一个简单物理量（初始 gap）就能预测最终提升，那 OPSD 就有"设计参数"可调。
- **🔧 方法**: 
  1. 收集大量 OPSD 实验数据，涵盖**多种上下文类型**（代码、数学、对话）和**多种模型族**（不同规模 + 不同基座）；
  2. 测量两个数：训练前**学生 vs 自教师**的性能 gap，训练后学生 vs ground-truth 的提升；
  3. 散点图 → 发现**惊人的线性关系**：gap 越大、最终提升越大（且 R² 极高）；
  4. 验证：换 context、换模型族、换模型规模，**线性关系稳定**；
  5. 推论：模型越大，关系越紧 → **OPSD 可能有自己的经验 scaling law**。
- **📊 效果**: 给出一条**直尺**：拿一个 OPSD 配置，先跑几百步小实验估 gap，就能预测完整训练的最终效果，**避免跑废**。也意味着 OPSD 反馈信号的选择可以用 gap 大小作为**统一度量**。
- **⚠️ 局限**: 线性关系是**经验发现**而非理论证明；gap 本身的定义依赖"自教师"在 OPSD 中的特化形式，换非 OPSD 设置是否还有类似关系**未知**；是否能外推到 GPT-4 级模型需要更贵实验验证。
- **价值**: 让 OPSD 从"试一下"变成"**可预测的设计参数**"，对实际工程选型（投入多大教师、选哪个反馈信号）有直接指导价值。


#### 📄 [Post-Training is About States, Not Tokens: A State Distribution View of SFT, RL, and OPD](https://arxiv.org/abs/2605.22731) | 2026-05
- **🎯 问题**: SFT/RL/OPD 总是从**损失函数**视角分析（MLE、PG、forward KL、reverse KL...）。但有个常被忽略的问题：**这些监督到底作用在哪些状态上？** 一个 state = prompt + 已生成 prefix。SFT 作用在"数据集状态"，RL/OPD 作用在"学生自己 roll 出来的状态"。**这俩分布差得远**。如果不看状态分布只看 loss 函数，会漏掉 post-training 大量现象。
- **💡 思路**: 把 post-training 重新定义为 **state-distribution shaping**（塑形训练状态分布）。提问："温和的 SFT 为什么不灾难性遗忘？degraded 教师 OPD 怎么能反超教师？轻量级 RL 怎么能保留能力？"如果都从 state 分布的角度看，答案可能很统一。
- **🔧 方法**: **控制变量小规模实验** —— Qwen3-0.6B-Base 在 GSM8K 训练，TruthfulQA/MMLU 作 retention 评估。三组对比：
  1. **温和 SFT vs stress SFT**：温和几乎不遗忘，stress 灾难性遗忘 → 状态分布**偏移**和遗忘强相关；
  2. **degraded SFT 教师 → OPD 学生**：教师自己答得烂，但**OPD 学生反超教师**（GSM8K/TruthfulQA/MMLU 三个全涨）→ 学生用 on-policy 状态"**逃出**"教师状态分布的死角；
  3. **轻量级 on-policy RL**：GSM8K 涨 + 几乎不遗忘 → on-policy 状态分布天然和原任务契合。
- **📊 效果**: 三个现象强支持"**state-distribution shaping**"视角：状态分布的来源（dataset vs student rollout）和它的偏移幅度，比 loss 函数形式更决定 post-training 的取舍（精度 vs 保留）。
- **⚠️ 局限**: 小规模实验（0.6B + GSM8K），三个数字"现象性"而非"机制性" —— 论文没回答 "**为什么**温和 SFT 状态偏移小"；推广到大规模 + 复杂任务需要进一步实验。
- **价值**: 改变 post-training 社区的**提问方式** —— 从"用什么 loss"到"在什么 state 上训练"。和"训练数据分布"在传统 ML 里的地位类似，这篇是 LLM post-training 领域呼唤"state 视角"的代表。


