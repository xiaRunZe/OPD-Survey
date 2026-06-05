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

## 📅 2026-06 月新论文速览（增量附录）

> 完整中文解读见 [daily-updates/2026-06-05.md](../daily-updates/2026-06-05.md)。

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


#### 📄 [FA-OPD: Adversarial Dual OPD for Embodied Control](https://arxiv.org/abs/2605.27095)
- **arXiv**: [2605.27095](https://arxiv.org/abs/2605.27095)
- **🎯 动机**: 行为克隆 + 扩散/流匹配策略仍然是**离线监督学习** — 策略只在专家状态训练，对实际访问的状态没纠正信号。
- **💡 方法**: FA-OPD 是**对抗式双 OPD** — Flow Matching 教师从演示学习，与 MLP 学生共同训练。教师提供两个信号：(1) **奖励通道**学专家相似度；(2) **动作通道**给学生访问状态提供密集局部目标。
- **📊 数字**: 6 个机器人 navigation/manipulation/locomotion benchmark 都超基线，**对噪声/有限演示鲁棒性显著**。


#### 📄 [CollectionLoRA: 50 Effects in 1 LoRA via Multi-Teacher OPD](https://arxiv.org/abs/2605.25378)
- **arXiv**: [2605.25378](https://arxiv.org/abs/2605.25378)
- **🎯 动机**: 定制图像编辑要给扩散模型加多个视觉效果，每个效果存一个 LoRA → 部署成本暴涨。和加速模块级联还有参数干扰。
- **💡 方法**: CollectionLoRA 用**多教师 OPD** 把 50 个效果塞进 1 个 LoRA。
- **📊 数字**: abstract 截断，详细结果待全文。
#### 📄 [TOPD: Trajectory-aware OPD via Near-Future Guidance](https://arxiv.org/abs/2606.00305)
- **arXiv**: [2606.00305](https://arxiv.org/abs/2606.00305)
- **🎯 动机**: OPD 学习信号是 token-level 的，但推理失败常是**短程分布漂移** — 孤立 token 级监督修不好。
- **💡 方法**: TOPD 用**近未来 trajectory 信息**识别真正发散的状态，把指导分布到多个未来 token 上。
- **📊 数字**: 屏蔽非发散高 loss token → 标准 OPD **47.8%→48.2%**；TOPD 再 → **52.2%**。**AIME24 60%→63.3%**，**AIME25 46.7%→53.3%**。


#### 📄 [GAPD: Gold-Action Policy Distillation for KBQA](https://arxiv.org/abs/2605.29584)
- **arXiv**: [2605.29584](https://arxiv.org/abs/2605.29584)
- **🎯 动机**: 知识库问答（KBQA）的 RL 只优化稀疏的最终答案奖励，中间 action 错误弱监督。
- **💡 方法**: GAPD 把 gold action 序列做成**在线 policy 蒸馏的教师信号**。
- **📊 数字**: gold logical form 不只是数据增强，更是**在线 PD 教师**。


#### 📄 [GDSD: Guided Denoiser Self-Distillation for Diffusion LLMs](https://arxiv.org/abs/2605.29398)
- **arXiv**: [2605.29398](https://arxiv.org/abs/2605.29398)
- **🎯 动机**: 扩散 LLM（dLLM）的 RL 受困于**似然不可处理**。主流方案用 ELBO 作似然代理 → 训练-推理失配。
- **💡 方法**: GDSD 直接**自蒸馏 denoiser** — 教师是 reverse-KL 正则 RL 闭式最优解导出的 advantage-guided self-teacher，**匹配 dLLM denoiser logits**。
- **📊 数字**: LLaDA-8B、Dream-7B **比 SOTA ELBO 方法最多 +19.6%**。


#### 📄 [Canonical-Context OPD for Multi-Turn Language Models](https://arxiv.org/abs/2605.30251)
- **arXiv**: [2605.30251](https://arxiv.org/abs/2605.30251)
- **🎯 动机**: 多轮对话中**同一完整证据**渐进揭示，模型却会答不同（"lost-in-conversation gap"）。原因 — **self-anchored drift**。
- **💡 方法**: Canonical-Context OPD — 用 clean FULL prompt 和 RAW-SHARDED 对话训练对齐。
- **📊 数字**: abstract 截断，详细结果待全文。


#### 📄 [Interpretable Policy Distillation for Power Grid Topology Control](https://arxiv.org/abs/2606.00561)
- **arXiv**: [2606.00561](https://arxiv.org/abs/2606.00561)
- **🎯 动机**: 深度 RL 用于电网实时运行，但大神经网络策略评估贵、难部署、对运维人员不透明。
- **💡 方法**: 把 PPO 教师（Grid2Op 14-bus、稳定导向奖励、stress-focused 数据采集）蒸馏到**决策树和随机森林**。
- **📊 数字**: 决策树和 PPO argmax 高精确动作一致。PPO 依赖线路负载信号，蒸馏树主要由母线拓扑变量驱动。


