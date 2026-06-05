# 🎭 三、黑盒 OPD（API 教师）

> 本章节收录**无法访问教师 logits** 的 OPD 场景（典型如 GPT-4、Claude 等闭源 API）。
> 监督信号来自：**判别器、verbal 分数、偏好对、生成对抗**。

---

## 1. ORPO-Distill

| 项目 | 内容 |
|------|------|
| **机构** | 工业界 |
| **时间** | 2025.09 |
| **arXiv** | [2509.25100](https://arxiv.org/abs/2509.25100) |
| **会议** | NeurIPS 2025 Workshop |
| **类型** | 📄 paper-only |

### 🎯 动机
- 教师是闭源 API，无法拿到 logits
- 现有 ORPO（Odds Ratio Preference Optimization）只做偏好对齐
- 想要**蒸馏 + 偏好对齐结合**

### 💡 方法思路
**核心机制**：**SGO（Student-Generated Outputs） + ORPO 对比**

- **正样本**：教师 API 的回答
- **负样本**：学生自生成的回答（不满意的）
- **损失**：ORPO 风格的对比损失

**混合策略**：学生自己生成的负样本是"动态"的 → 满足 on-policy 性质。

### 📊 效果
- 在跨架构蒸馏（学生不同 tokenizer）下效果不错

### ⚠️ 局限
- 依赖 ORPO 框架
- 偏好对构造质量影响大

---

## 2. GAD — Generative Adversarial Distillation

> 🎯 **黑盒 OPD 种子论文**：用对抗判别器作为 on-policy 奖励。

| 项目 | 内容 |
|------|------|
| **作者** | Yitian (Tian) Zhu, 等 |
| **机构** | Microsoft Research |
| **时间** | 2025.11 |
| **arXiv** | [2511.10643](https://arxiv.org/abs/2511.10643) |
| **项目页** | [ytianzhu.github.io/Generative-Adversarial-Distillation](https://ytianzhu.github.io/Generative-Adversarial-Distillation/) |
| **代码** | [microsoft/LMOps](https://github.com/microsoft/LMOps) |

### 🎯 动机
- 现有 OPD 都需要教师 logits，**闭源 API（如 GPT-5）无法用**
- 想要对 API 模型做蒸馏
- 用**判别器**代替 logits

### 💡 方法思路
**核心创新**：**对抗性判别器作为 on-policy 奖励**

**对抗游戏**：
- **判别器 D**：训练区分学生输出 vs 教师输出（如 GPT-5）
- **学生 π_S**：尽量"骗过"判别器
- **教师 API**：只提供少量 query-response 样本

**关键设计**：
- D 在学生 rollouts 上做对抗训练 → 演化为 on-policy 奖励模型
- 学生最小化 `log(1 - D)` 来模仿教师

**目标函数**：
$$
\min_{\pi_S} \max_D \mathbb{E}_{y \sim \pi_T}[\log D(y)] + \mathbb{E}_{y \sim \pi_S}[\log(1 - D(y))]
$$

### 📊 效果
- Qwen2.5-14B 学生与 GPT-5-Chat 在 LMSYS 上**可比**
- 突破闭源教师限制

### ⚠️ 局限
- 对抗训练**不稳定**
- 判别器训练成本高
- 容易出现 mode collapse

---

## 3. OVD — On-Policy Verbal Distillation

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | HKU / Huawei |
| **时间** | 2026.01 |
| **arXiv** | [2601.21968](https://arxiv.org/abs/2601.21968) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 闭源 API 只能返回文本，无法给 logits
- 现有黑盒 KD 用判别器/偏好，**信号粗粒度**
- 想用**教师自身的 verbal 评分**（0-9）作为细粒度信号

### 💡 方法思路
**核心机制**：**用 verbal 分数代替 token logit**

**训练流程**：
1. 学生 rollout 一个完整响应
2. 教师 API 给该响应打分（0-9）
3. 用分数作为 reward，**序列级 REINFORCE** 更新学生

**关键设计**：
- 用 LLM 提示工程让 API 输出 0-9 分数
- 用分数差作为 advantage

### 📊 效果
- 在多个任务上 **+25.7%** 超过 baseline
- 完全 API 友好

### ⚠️ 局限
- Verbal 分数**不稳定**（同回答多次评分可能不同）
- 0-9 粒度仍较粗
- 项目页 OVD.github.io 404，需通过 arXiv 找资源

---

## 4. SODA — Semi On-Policy Black-Box Distillation

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **时间** | 2026.04 |
| **arXiv** | [2604.03873](https://arxiv.org/pdf/2604.03873) |
| **类型** | 📄 paper-only |

### 🎯 动机
- GAD 训练慢（10× 开销）、GPU 峰值高（+27% 显存）
- 想要**Semi On-Policy**：学生只采样一次静态 snapshot（q₀ 的 zero-shot 输出），后续不动态 rollout
- 大幅降低训练成本

### 💡 方法思路
**核心创新**：**DPO 框架 + 静态半 on-policy 数据**

- **正样本**：教师 API 的回答
- **负样本**：学生基模型 q₀ 的 zero-shot 回答（**一次采样，永久复用**）

**半 on-policy 解释**：负样本来自"过去的自己"，介于纯 off-policy 和 on-policy 之间。

### 📊 效果
- **10× 训练加速**（相比 GAD）
- **27% 显存降低**
- 16 个 benchmark 中 **15 个超过 GAD**

### ⚠️ 局限
- 半 on-policy 仍非真正 on-policy
- 静态负样本可能在训练后期过时

---

## 📅 2026-06 月新论文（1 篇）

#### 📄 [OmniOPD: Logit-Free On-Policy Distillation via Speculative Verification](https://arxiv.org/abs/2606.01476)
- **arXiv**: [2606.01476](https://arxiv.org/abs/2606.01476)
- **🎯 动机**: 标准 OPD 两个耦合限制 — (1) 要教师 token-level logits（专有模型做不了教师）；(2) token 信号脆，依赖师生候选 token 重叠，会放大重复 loop。
- **💡 方法**: **chunk-level 监督** — Monte Carlo rollout 在多 token chunk 上用连续语义相似度近似教师偏好；**peak-entropy scheduler** 只在学生高不确定推理分支审计；Dirichlet-Multinomial 贝叶斯先验 + base-model KL anchor。
- **📊 数字**: 数学 **+28.64%**；配 Claude-4.5-Haiku / Gemini-2.5-Flash 黑盒教师再 +9.54%。


