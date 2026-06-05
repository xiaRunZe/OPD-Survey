# ⚡ 十、投机解码蒸馏 + 🛠️ 十一、框架与工具包 + 🏭 十二、工业界

---

# ⚡ 十、投机解码蒸馏

> **特点**：蒸馏**草稿模型**（drafter）使其更好地模拟验证器/目标模型。
> On-policy 元素是 drafter 自己的延续。
> 目标：**推理加速**，非能力提升。

---

## 1. OSD — Online Speculative Decoding

| 项目 | 内容 |
|------|------|
| **机构** | UCB / NVIDIA |
| **时间** | 2023.10 |
| **arXiv** | [2310.07177](https://arxiv.org/abs/2310.07177) |
| **代码** | [LiuXiaoxuanPKU/OSD](https://github.com/LiuXiaoxuanPKU/OSD) |

### 🎯 动机
- 现有投机解码（SD）用固定草稿模型
- 想要"**在线/动态**"更新草稿模型

### 💡 方法思路
**核心机制**：**在线 KD on rejected tokens**

- 草稿模型 rollout
- 目标模型验证：拒绝的 token 用 KD 训练

### 📊 效果
- **首个在线/On-Policy SD 论文**

### ⚠️ 局限
- 草稿模型必须常驻

---

## 2. DistillSpec

> 🎯 **SD 蒸馏的奠基论文**

| 项目 | 内容 |
|------|------|
| **机构** | Google DeepMind |
| **时间** | 2023.10 |
| **会议** | ICLR 2024 |
| **arXiv** | [2310.08461](https://arxiv.org/abs/2310.08461) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 想要"用 KD 训练更好的草稿模型"

### 💡 方法思路
**核心机制**：**On-Policy（草稿采样） + 多散度**

- 草稿采样
- 教师（验证器）在草稿上提供 FKL/RKL/JSD/TVD 多种损失

### 📊 效果
- **SD 蒸馏的种子论文**

---

## 3. HASS — 自投机

| 项目 | 内容 |
|------|------|
| **时间** | 2024.08 |
| **arXiv** | [2408.15766](https://arxiv.org/abs/2408.15766) |
| **代码** | [HArmonizedSS/HASS](https://github.com/HArmonizedSS/HASS) |

### 🎯 动机
- 现有 SD 用独立草稿模型
- 想要"**自投机**"（同一模型作草稿和验证器）

### 💡 方法思路
**核心机制**：**多步草稿 + 对齐**

- 训练时多步草稿轨迹（on-policy）
- 多步 KD CE + 特征对齐

### ⚠️ 严格度说明
- **部分 on-policy**（多步草稿轨迹）

### 📊 效果
- 自投机 SOTA

---

## 4. Falcon — 半 AR 草稿

| 项目 | 内容 |
|------|------|
| **机构** | Bestpay |
| **时间** | 2024.12 |
| **arXiv** | [2412.12639](https://arxiv.org/abs/2412.12639) |
| **代码** | [Bestpay-inc/Falcon](https://github.com/Bestpay-inc/Falcon) |

### 🎯 动机
- 想要"半自回归（Semi-AR）草稿"
- 与自回归对齐

### 💡 方法思路
**核心机制**：**Glancing CE + KD**

- Glancing 用草稿采样
- 联合 CE + KD

### ⚠️ 严格度说明
- **部分 on-policy**（Glancing）

---

## 5. CORAL — 跨步表征对齐

| 项目 | 内容 |
|------|------|
| **时间** | 2025.02 |
| **会议** | ACL 2025 |
| **arXiv** | [2502.16880](https://arxiv.org/abs/2502.16880) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 训练/推理不一致（草稿训练用单步，推理用多步）

### 💡 方法思路
**核心机制**：**跨步对齐 + CE**

- 训练时模拟多步草稿
- 跨步表征对齐

### 📊 效果
- 解决 SD 训练/推理不一致

---

## 6. EAGLE / EAGLE-3

| 项目 | 内容 |
|------|------|
| **机构** | PKU / Microsoft |
| **时间** | 2025.03 |
| **arXiv** | [2503.01840](https://arxiv.org/abs/2503.01840) |
| **代码** | [SafeAILab/EAGLE](https://github.com/SafeAILab/EAGLE) |

### 🎯 动机
- 想要"训练时测试（Training-Time Test, TTT）"

### 💡 方法思路
**核心机制**：**EAGLE-3 — TTT 多步**

- 训练时模拟草稿 rollout
- Smooth-L1（特征）+ CE（token）

### 📊 效果
- 当时 SOTA

---

## 7. MASSV — 多模态 SD 草稿

| 项目 | 内容 |
|------|------|
| **机构** | Cerebras |
| **时间** | 2025.05 |
| **arXiv** | [2505.10526](https://arxiv.org/abs/2505.10526) |
| **类型** | 📄 paper-only |

### 💡 方法思路
- 多模态草稿
- KD CE
- 草稿采样（on-policy）

---

## 8. DVI — 草稿-验证-改进

| 项目 | 内容 |
|------|------|
| **时间** | 2025.10 |
| **arXiv** | [2510.05421](https://arxiv.org/abs/2510.05421) |
| **类型** | 📄 paper-only |

### 💡 方法思路
**核心机制**：**RL on verifier signal**

- KL → reward-masked CE + PG
- 持续在线训练

---

## 9. SpecKD / SelecTKD

| 项目 | 内容 |
|------|------|
| **作者** | Haiduo Huang 等 |
| **机构** | 西交大 |
| **时间** | 2025.10 |
| **arXiv** | [2510.24021](https://arxiv.org/abs/2510.24021) |
| **类型** | 📄 paper-only |

### 💡 方法思路
**核心机制**：**验证门控 KD**

- 反转 SD：把接受/拒绝作为 KD 损失门控
- 仅对接受 token 算 KL

### 📊 效果
- 有效利用 SD 信号

---

## 10. ReSpec — RL 草稿演化

| 项目 | 内容 |
|------|------|
| **时间** | 2025.10 |
| **arXiv** | [2510.26475](https://arxiv.org/abs/2510.26475) |
| **类型** | 📄 paper-only |

### 💡 方法思路
**核心机制**：**RL rollouts 调节 KD**

- 草稿在 RL 训练中演化
- KD 用 rollout reward 加权

---

## 11. SpecForge

| 项目 | 内容 |
|------|------|
| **机构** | SGLang |
| **时间** | 2026.03 |
| **代码** | [sgl-project/SpecForge](https://github.com/sgl-project/SpecForge) |
| **博客** | [LMSYS blog](https://www.lmsys.org/blog/2025-07-25-spec-forge/) |

### 💡 方法思路
- 开源 EAGLE-3 训练框架
- 支持 TTT

---

# 🛠️ 十一、框架与工具包

> 真正实现 OPD 训练的开源框架（学生 rollouts）。

| 框架 | 维护方 | KL 方向 | 核心特点 |
|------|-------|---------|---------|
| **TRL** | Hugging Face | FKL/RKL/GJSD | **最多样的 OPD 训练器** |
| **LLaMA-Factory** | hiyouga | (via TRL) | 最流行微调框架 |
| **ms-swift** | 阿里 ModelScope | TRL GKD | 包装 TRL GKDTrainer |
| **verl** | 字节 Seed | FKL sparse top-k | 生产级 OPD 配方 |
| **rllm** | UC Berkeley Sky | RKL advantage | `opsd/` 子目录 |
| **SkyRL** | UC Berkeley NovaSky | RKL + importance | 2025.11 新增 OPD |
| **ROLL** | 阿里巴巴 | 多种 | 一级 DistillPipeline |
| **AReaL** | 蚂蚁 / 清华 | KL 控制 | `distill_loss_weight` |
| **slime** | 清华 THUDM | RKL token | GLM-4.5/4.6 背后 |
| **NeMo-RL** | NVIDIA | FKL/RKL/混合 | 替代 NeMo-Aligner |
| **KDFlow** | BJTU | FKL/RKL/JSD/AKL/Skew | **KD-first 框架** |

### TRL `experimental/` 目录（**最多样**）

```
trl/experimental/
├── gkd/                # GKD 训练器
├── gold/               # GOLD（跨分词器）
├── minillm/            # MiniLLM
├── sdft/               # SDFT
├── self_distillation/  # 自蒸馏
├── sdpo/               # SDPO
├── nash_md/            # Nash-MD
├── xpo/                # XPO
├── online_dpo/         # Online DPO
├── papo/               # PAPO
└── prm/                # 过程奖励模型
```

> 🎯 **建议**：新项目从 TRL 起步，覆盖面最广。

### KDFlow 亮点

| 特性 | 描述 |
|------|------|
| **Decoupled Backend** | SGLang 教师 + FSDP2 学生 |
| **Zero-Copy Hidden** | 传输教师 hidden states |
| **Cross-Tokenizer** | 原生跨分词器 |
| **VLM** | Qwen3-VL 支持 |
| **Colocate Mode** | SGLang sleep/wakeup |
| **Speedup** | 1.44-6.36× over homogeneous baselines |

---

# 🏭 十二、工业界 / 量产模型

> **明确公开描述 OPD** 在后训练流水线中的旗舰模型。

| 模型 | 厂商 | 时间 | OPD 机制 | 备注 |
|------|------|------|---------|------|
| **Gemma 2** | Google | 2024.07 | KL on student samples | 首批命名 OPD 的工业模型 |
| **Qwen3** | Alibaba | 2025.05 | 两阶段（off + on policy） | **工业 OPD 标杆**，~10× 便宜于 RL |
| **GLM-4.5/4.6** | Zhipu | 2025.08 | Expert iteration + SFT | GLM-5 前身 |
| **HY-MT1.5** | Tencent | 2025.12 | RKL 强到弱 | 33 语言 MT，WMT25 冠军系 |
| **MiMo-V2-Flash** | Xiaomi | 2026.01 | MOPD（多教师） | 多教师 OPD |
| **Typhoon-S** | Typhoon AI | 2026.01 | GAD 风格 | Full logits > Top-K（泰语） |
| **Baichuan-M3** | Baichuan | 2026.02 | 三阶段 MOPD | 医疗 44.4 HealthBench-Hard |
| **GLM-5** | Zhipu | 2026.02 | 跨阶段 OPD | "OPD as stage glue" |
| **Nemotron Cascade 2** | NVIDIA | 2026.03 | MOPD | 30-160 步 vs RL 1000+ 步 |
| **Qwen3-Coder** | Alibaba | 2026.03 | SFT + on-policy | 多专家 → 80A3 学生 |
| **KAT-Coder-V2** | Kuaishou | 2026.03 | Step-level OPD | 79.6% SWE-bench |
| **HY-Embodied-0.5** | Tencent | 2026.04 | FKL embodied | MoT 2B 边缘版 |
| **DeepSeek-V4** | DeepSeek | 2026.04 | 多教师 OPD 替 RL | V4-Pro 1.6T MoE |
| **Qwen3.5-Omni** | Alibaba | 2026.04 | 跨模态 OPD | 256k 上下文 |
| **Composor2.5** | Cursor | 2026.05 | RL+OPD 反馈 | 类 RLSD |

### 重点解读

#### Qwen3 — 工业 OPD 标杆

**两阶段后训练**：
1. **Off-Policy SFT 冷启动**（用 `/think` 和 `/no_think` 教师样本）
2. **On-Policy 阶段**（学生生成 + 教师 logit-KL 监督）

**核心数据**：
- 比 RL **便宜 ~10×**
- 等价性能

**影响力**：几乎所有后续 OPD 工作都参考 Qwen3 配方。

#### DeepSeek-V4 — 首次 OPD 替 RL

**核心变化**：V3/R1 用"统一 mixed-RL 阶段"做能力整合，**V4 改用多教师 OPD**：

- 训练多个领域专家（SFT + GRPO 各领域：math、code、agent、IF）
- 统一学生**反向 KL 优化**到专家集合
- 在自己 rollouts 上训练
- **全词表 KL**（非 token 级估计）稳定梯度

#### Baichuan-M3 — 医疗 MOPD

**三阶段**：
1. **TaskRL**
2. **离线 PD**（Clip-FKL）
3. **MOPD**（RKL）

**关键点**：学生在 MOPD 中作为"决策者"协调多教师冲突建议。

#### GLM-5 — 跨阶段 OPD

**创新**：把 OPD 作为**阶段间的"反遗忘"精修**——在每个阶段后插入一轮 OPD，恢复被遗忘的能力。

#### KAT-Coder-V2 — Step-level OPD

**关键创新**：监督粒度是**步骤级**而非 token 级：
- 推理结果建模为**推理树**
- 在树节点做对齐
- 6.2× 加速（消除冗余计算）
- 79.6% SWE-bench（接近 Claude Opus 4.6 80.8%）

#### HY-Embodied-0.5 — FKL 具身

- MoT（Mixture-of-Transformers）架构
- **FKL**（与白盒 OPD 主流的 RKL 相反）
- 2B 边缘版用于真实机器人控制
- 22 个具身 benchmark

#### Composor2.5 — Cursor 的 RL+OPD

- 类似 RLSD 配方
- 工业代码 Agent

---

## 📅 2026-06 月新论文（1 篇）

#### 📄 [Draft-OPD: On-Policy Distillation for Speculative Draft Models](https://arxiv.org/abs/2605.29343) | Haodi Lei et al., 2026-05 v2
- **🎯 问题**: Speculative decoding 加速 LLM 推理 —— target model + 轻量 draft model，draft 提出 tokens 目标模型并行验证。**EAGLE3 / DFLASH** 之类 draft model 主流是 **SFT on target-generated trajectories**。但 SFT 很快 plateau —— draft 在测试数据上的 **acceptance length 不再涨**。原因：**offline-inference mismatch** —— SFT 学固定 target-generated 轨迹，但**推理时被 draft 自己提出 block 评估**。
- **💡 思路**: 既然 SFT 失败因**离线-推理 mismatch**，**OPD 训练 draft** 是自然解 —— target 在 **draft-induced states** 上监督 draft。但**直接 OPD 对 draft 难**：① draft **不能独立 roll out 完整序列**（能力不够）；② target-assisted generation 让序列 follow target 分布，**消除 on-policy 信号**（draft 不是被监督者而是"被引导者"）。问题从"如何 SFT draft"变成"**如何让 OPD 在 draft 训练上可工作**"。
- **🔧 方法**:
  1. **Draft-OPD**：
     1. **Target-assisted rollout for stable continuations** —— 用 target 帮 draft 续写，避免 draft 早早崩；
     2. **Replay drafting from verification-exposed error positions** —— 在 target verification 暴露 draft 错误的**精确位置**重新 draft，让 draft 从**自己的错误**学；
  2. 让 draft 从**target feedback on both accepted and rejected proposals**学；
  3. 训练聚焦在**限制 speculative decoding 加速比的 draft-induced errors**。
- **📊 效果**: Speculative decoding 草稿模型是 OPD 的新战场 —— 证明 OPD 比 SFT 更适合 draft model 训练。Haodi Lei 等来自复旦/上海 AI Lab，作者列表包括 Ning Ding、Yu Cheng 等。
- **⚠️ 局限**: 验证暴露错误位置的设计需工程实现；target-assisted rollout 的"协助程度"是超参；与其他 draft 训练方案（对比学习、自博弈）的对比未充分讨论；accelerator 实际收益（wall-clock speedup）需详尽实验。
- **价值**: 把"**speculative decoding 的 draft 训练**"从"**SFT plateau**"变成"**OPD 持续提升**" —— 是 draft model 训练的新范式，对所有想加速 LLM 推理的团队有直接实用价值；同时是 OPD 应用场景的**新拓展**（speculative decoding 此前不在 OPD 主流应用范围内）。


