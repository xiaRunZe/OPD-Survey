# 🔬 二、白盒 OPD（外部教师模型）

> 本章节收录**使用外部教师 logits 监督学生**的 OPD 方法。每个方法都已验证：
> - (a) 在学生自生成 rollouts 上训练
> - (b) token 级监督

---

## 1. MiniLLM

> 🎯 **最早的"OPD 配方"**，与 GKD 同期的另一奠基性工作。

| 项目 | 内容 |
|------|------|
| **作者** | Yuxian Gu, Li Dong, Furu Wei, Minlie Huang |
| **机构** | 清华大学 / Microsoft |
| **时间** | 2023.06 |
| **会议** | ICLR 2024 |
| **arXiv** | [2306.08543](https://arxiv.org/abs/2306.08543) |
| **代码** | [microsoft/LMOps/minillm](https://github.com/microsoft/LMOps/tree/main/minillm) |

### 🎯 动机
- 传统白盒 KD 用**前向 KL**（FKL）作为损失，但 FKL 是 **mode-covering**（试图覆盖教师所有模式），容易导致学生输出**平庸化**
- 想要 mode-seeking 行为（精确匹配教师的高质量模式），但朴素 RKL 难以通过 policy gradient 优化
- 想要避开 SFT 的复合误差问题

### 💡 方法思路
**核心创新**：把 RKL 蒸馏改写为**策略梯度**形式：

$$
\nabla_{\theta} \mathcal{L}_{\text{RKL}} = \mathbb{E}_{y \sim \pi_\theta} \left[ (\log \pi_{\text{teacher}}(y|x) - \log \pi_\theta(y|x)) \nabla_\theta \log \pi_\theta(y|x) \right]
$$

这本质上是把 RKL 当作"reward"做 REINFORCE。

**关键技术**：
- **单步留数（Single-Sample Estimate）**：学生自采样一个完整序列
- **Teacher-Forcing 初始化**：先 SFT 一轮做冷启动
- **Length-Normalized Loss**：避免长序列偏差

### 📊 效果
- 在多个 NLP 任务上超过 SFT 和传统 KD
- 7B 学生接近 13B 教师的部分能力

### ⚠️ 局限
- 高方差（policy gradient 通病）
- 需要 SFT 冷启动，不能从零训练

---

## 2. DistiLLM

| 项目 | 内容 |
|------|------|
| **作者** | Jongwoo Ko 等 |
| **机构** | KAIST / Microsoft |
| **时间** | 2024.02 |
| **会议** | ICML 2024 |
| **arXiv** | [2402.03898](https://arxiv.org/abs/2402.03898) |
| **代码** | [jongwooko/distillm](https://github.com/jongwooko/distillm) |

### 🎯 动机
- 传统 KD 全用 off-policy 数据（教师采样），学生分布与教师分布偏差大
- 朴素 OPD（全用 on-policy）则训练信号稀疏、样本效率低
- 想**自适应混合 on/off-policy**

### 💡 方法思路
**核心创新**：**Skewed-KL 散度**——FKL 和 RKL 的加权混合：

$$
D_{\text{skew}}^\alpha(P\|Q) = \alpha \cdot D_{\text{FKL}}(P\|Q) + (1-\alpha) \cdot D_{\text{RKL}}(P\|Q)
$$

**α 的角色**：
- α=0：纯 RKL（mode-seeking）
- α=1：纯 FKL（mode-covering）
- 0<α<1：混合，平衡两种行为

**数据混合策略**：
- **自适应 off→on 切换**：训练初期偏 off-policy（数据丰富），后期偏 on-policy（分布一致）
- **重要性重采样**：用 student/teacher 概率比对样本加权

### 📊 效果
- 在 7B/13B 蒸馏场景下效果优于 MiniLLM 和 GKD
- 收敛更快

### ⚠️ 局限
- α 是超参，需要调
- 重要性重采样引入额外计算

---

## 3. Speculative KD — 推测式蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | Peng Xu 等 |
| **机构** | UCSB / Google |
| **时间** | 2024.10 |
| **会议** | ICLR 2025 |
| **arXiv** | [2410.11325](https://arxiv.org/abs/2410.11325) |
| **代码** | [google-research/speculative_kd](https://github.com/google-research/google-research/tree/master/speculative_kd) |

### 🎯 动机
- 教师和学生能力差距大时，学生可能完全学不到教师的高质量模式
- 一次性让学生模仿教师**困难太大**
- 想**循序渐进**：先让学生"提议"，教师来"纠正"

### 💡 方法思路
**核心机制**：**交错提议-纠正**（Interleaved Propose-and-Correct）

**算法流程**（单步）：
1. 学生采样一个 token
2. 教师评估：如果学生 token 概率高，接受；否则教师**提出替代**
3. 用门控 KL 损失（Gated KL）训练

**关键设计**：
- **门控（Gate）**：仅当教师认为学生"错了"时计算 KL 损失
- **提议机制（Propose）**：教师给出"如果是我会生成什么"的分布

### 📊 效果
- 在大模型蒸馏小模型场景下显著优于传统 KD
- 推理时学生可以独立生成（无教师依赖）

### ⚠️ 局限
- 训练流程复杂，需要交错采样
- 教师仍需在训练循环中

---

## 4. DistiLLM-2

| 项目 | 内容 |
|------|------|
| **作者** | Jongwoo Ko 等 |
| **机构** | KAIST / Microsoft |
| **时间** | 2025.03 |
| **会议** | ICML 2025 Oral |
| **arXiv** | [2503.07067](https://arxiv.org/abs/2503.07067) |
| **代码** | [jongwooko/distillm-2](https://github.com/jongwooko/distillm-2) |

### 🎯 动机
- DistiLLM 用单一 Skew-KL 处理所有数据，未区分"教师数据"和"学生数据"
- 这两类数据**分布性质不同**（教师数据是 off-policy，学生数据是 on-policy），应用同一损失不合理

### 💡 方法思路
**核心创新**：**非对称损失**——在两类数据上用不同的散度：

$$
\mathcal{L} = \underbrace{\mathbb{E}_{x \sim \mathcal{D}_{\text{teacher}}}\left[ D_{\text{Skew-FKL}}(\pi_S \| \pi_T) \right]}_{\text{off-policy 部分}} + \underbrace{\mathbb{E}_{x \sim \mathcal{D}_{\text{student}}}\left[ D_{\text{Skew-RKL}}(\pi_S \| \pi_T) \right]}_{\text{on-policy 部分}}
$$

- **教师数据**（off-policy）：用 Skew-FKL 鼓励覆盖教师分布
- **学生数据**（on-policy）：用 Skew-RKL 鼓励精确匹配

### 📊 效果
- ICML 2025 Oral（高质量）
- 比 DistiLLM 进一步提升

### ⚠️ 局限
- 实现更复杂，需维护两个数据源
- 损失组合权重需调

---

## 5. DSKDv2 — 跨分词器蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | Mingyang Song, 等 |
| **机构** | 北京交通大学（BJTU） |
| **时间** | 2025.04 |
| **arXiv** | [2504.11426](https://arxiv.org/abs/2504.11426) |
| **代码** | [songmzhang/DSKDv2](https://github.com/songmzhang/DSKDv2) |

### 🎯 动机
- 教师和学生使用**不同 tokenizer** 时（如 Qwen2 训 Llama），token 序列无法直接对齐
- 现有方法要么强制共享 vocab（损失表达能力），要么丢弃 OPD（用离线蒸馏）
- 想做**真正的跨分词器 OPD**

### 💡 方法思路
**核心创新**：**双对齐空间** —— 在对齐的字符级特征空间中计算 KL：

1. **字符级对齐**：把学生和教师的 token 序列先按字符串对齐
2. **双空间映射**：分别在学生和教师的 hidden space 中提取分布
3. **KL in aligned space**：在统一空间计算散度

**支持模式**：
- on-policy：学生自采样 → 教师打分
- off-policy：教师数据 → 学生模仿

### 📊 效果
- 跨分词器蒸馏 Qwen2→Llama-3 等组合
- 与同分词器蒸馏效果接近

### ⚠️ 局限
- 对齐算法对低资源语言不友好
- 计算量略高

---

## 6. Constrained OPD — CMDP 视角

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | Huawei Noah's Ark |
| **时间** | 2025.09 |
| **arXiv** | [2509.22921](https://arxiv.org/abs/2509.22921) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 传统 OPD 用**软 KL 惩罚**作为正则项，KL 强度难以精确控制
- 训练过程中 KL 可能无界增长，导致学生过度保守或崩塌
- 想做**硬约束**而非软惩罚

### 💡 方法思路
**核心创新**：把 OPD 形式化为**带 KL 约束的 MDP（CMDP）**：

$$
\max_\pi \mathbb{E}_{x,y \sim \pi}[\text{reward}] \quad \text{s.t.} \quad D_{\text{KL}}(\pi \| \pi_{\text{teacher}}) \leq \epsilon
$$

**关键技术**：
- 用 Lagrangian 乘子法把约束融入目标
- 训练过程中**严格控制 KL** 不超过阈值

### ⚠️ 严格度说明
- 属于"OPD-RL 边界"方法，介于纯 OPD 和 RL 之间

### 📊 效果
- KL 曲线更稳定
- 避免训练崩塌

### ⚠️ 局限
- 边界方法，需约束优化求解
- 实际收益取决于具体场景

---

## 7. AdaSwitch — 自适应 on/off-policy 切换

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | 人民大学 / 百度 |
| **时间** | 2025.10 |
| **arXiv** | [2510.07842](https://arxiv.org/abs/2510.07842) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 训练不同阶段最优的 on/off-policy 比例不同
- 固定比例的混合策略在训练后期会**次优**
- 想要**动态切换**

### 💡 方法思路
**核心创新**：**基于分歧度自适应切换**：

- 当学生与教师分歧小时：偏 on-policy（继续提升）
- 当学生与教师分歧大时：偏 off-policy（重新对齐）

**切换指标**：用 student-teacher KL 估计分歧度，超过阈值则切换。

### 📊 效果
- 训练曲线更平滑
- 避免学生"走偏"

### ⚠️ 局限
- 阈值需调
- 切换频率影响最终效果

---

## 8. Veto — 稳定 OPD

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | 首尔大学（SNU） |
| **时间** | 2026.01 |
| **会议** | ACL 2026 Findings |
| **arXiv** | [2601.07155](https://arxiv.org/abs/2601.07155) |
| **类型** | 📄 paper-only |

### 🎯 动机
- OPD 训练常出现"logit 爆炸"——教师在某些 token 上 logit 极大，KL 主导训练
- 学生在这些 token 上**过度拟合**，其他 token 学不到
- 想要**自适应梯度否决**

### 💡 方法思路
**核心创新**：**Logit 空间的几何桥 + 自适应梯度否决**

- **几何桥**：把教师和学生的 logit 投影到统一空间
- **Veto 机制**：当某 token 的梯度方向不一致时**暂时跳过**

### 📊 效果
- 训练更稳定
- 优于原始 GKD 基线

### ⚠️ 局限
- 实现复杂

---

## 9. G-OPD — OPD 作为 KL 约束的 RL

> 🎯 **理论统一**：把 OPD 形式化为 KL-constrained RL，允许学生"超越"教师。

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | 人民大学 / 腾讯 |
| **时间** | 2026.02 |
| **arXiv** | [2602.12125](https://arxiv.org/abs/2602.12125) |
| **代码** | [RUCBM/G-OPD](https://github.com/RUCBM/G-OPD) |

### 🎯 动机
- 传统 OPD 中学生受 KL 约束，**无法超过教师**（教师是上界）
- 但学生有可能在某些任务上**找到更好的解**
- 想要**奖励外推**（Reward Extrapolation）

### 💡 方法思路
**核心思想**：把 OPD 形式化为：

$$
\max_\pi \mathbb{E}_{x,y \sim \pi}[R(y) - \beta \cdot D_{\text{KL}}(\pi \| \pi_{\text{teacher}})]
$$

其中 **R(y) 可以是大于 1 的外推奖励**。

**ExOPD 变体**：通过 `reward_scale > 1` 的外推，让学生有机会"超越"教师。

### 📊 效果
- 在推理任务上超过教师模型的 baseline
- 理论优美

### ⚠️ 局限
- 外推系数需精调
- 实际"超越"幅度有限

---

## 10. Fast OPD — 推理前缀截断

| 项目 | 内容 |
|------|------|
| **作者** | 工业界 |
| **时间** | 2026.02 |
| **arXiv** | [2602.15260](https://arxiv.org/abs/2602.15260) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 长 CoT 推理（如 DeepSeek R1 风格）序列长达 16K
- 完整序列做 OPD **计算量巨大**
- 观察到：推理的"前缀"对最终答案影响最大，"中间探索"价值较低

### 💡 方法思路
**核心创新**：**前缀截断**（Prefix Truncation）

- 截取前 N 个 token 做密集 OPD 训练
- 后续 token 用普通 SFT 损失
- 推理阶段让学生自然展开

### 📊 效果
- **2×~47× 训练加速**
- 推理性能几乎无损失

### ⚠️ 局限
- N 截断点的选择依赖任务
- 不适合长 CoT 探索性任务

---

## 11. Entropy-Aware OPD — 熵感知切换

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | KAIST / IBM |
| **时间** | 2026.03 |
| **arXiv** | [2603.07079](https://arxiv.org/abs/2603.07079) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 不同位置的 token 信息量不同：低熵 token 学生容易模仿，高熵 token 难模仿
- 统一用 RKL 会让**低熵位置过拟合，高熵位置欠拟合**
- 想做**位置自适应散度**

### 💡 方法思路
**核心创新**：**基于教师熵自适应切换 FKL/RKL**

- 教师熵高 → 用 FKL（mode-covering，鼓励多样性）
- 教师熵低 → 用 RKL（mode-seeking，精确匹配）

### 📊 效果
- 在推理任务上更稳定
- 提升学生多样性

### ⚠️ 局限
- 切换阈值敏感
- 实现略复杂

---

## 12. REOPOLD — 宽松 OPD

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | KAIST / Microsoft |
| **时间** | 2026.03 |
| **arXiv** | [2603.11137](https://arxiv.org/abs/2603.11137) |
| **类型** | 📄 paper-only（code soon） |

### 🎯 动机
- 传统 OPD 视为"用 KL 替换 reward 的 RL"
- 实际上 OPD 的损失设计**更复杂**（涉及 clipping、采样策略等）
- 想做**统一的视角**

### 💡 方法思路
**核心创新**：把 OPD 视为**带 log-ratio 奖励的策略优化**

- **KL 奖励**：reward = log(π_teacher) - log(π_student)
- **混合奖励裁剪**：mixture-based reward clipping
- **基于熵的动态采样**：entropy-based dynamic sampling

### 📊 效果
- 在推理任务上效果优于 GKD
- 理论统一性好

### ⚠️ 局限
- 需读全 paper 才能理解细节
- 实战调参难度大

---

## 13. PACED — 前沿课程自蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | HJSang 等 |
| **机构** | LinkedIn |
| **时间** | 2026.03 |
| **arXiv** | [2603.11178](https://arxiv.org/abs/2603.11178) |
| **代码** | [HJSang/OPSD_OnPolicyDistillation](https://github.com/HJSang/OPSD_OnPolicyDistillation) |

### 🎯 动机
- 学生自蒸馏时，"用什么数据训练"非常关键
- 太简单的 prompt 学生已经会，没新信息
- 太难的 prompt 学生学不会
- 想要**课程学习**（curriculum）

### 💡 方法思路
**核心创新**：**Frontier Curriculum at Student Competence Boundary**

- **前沿选择**：选学生"刚好不会"的数据
- **难度权重**：`w(p) = p(1-p)`（p 是学生正确率，最大化在 0.5 处）

### ⚠️ 严格度说明
- 属于"自蒸馏"风格（privileged-context 或 earlier-checkpoint）

### 📊 效果
- 训练效率高
- 学生进步明显

### ⚠️ 局限
- 课程调度难
- 对教师能力假设较强

---

## 14. TSD-KD — Token 选择性双蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | 高丽大学 |
| **时间** | 2026.03 |
| **会议** | ICLR 2026 |
| **arXiv** | [2603.13260](https://arxiv.org/abs/2603.13260) |
| **代码** | [kmswin1/TSD-KD](https://github.com/kmswin1/TSD-KD) |

### 🎯 动机
- 现有 OPD 多数用单一损失（FKL/RKL/JSD），忽略了"哪些 token 值得蒸馏"
- 有些 token 蒸馏价值低（如停用词、标点），浪费算力
- 想要**token 选择性 + 间接/直接双蒸馏**

### 💡 方法思路
**两个机制**：
1. **间接蒸馏（Indirect）**：学生 propose → 教师 re-rank
2. **直接蒸馏（Direct）**：选择性 logit KD

**混合策略**：部分 token 走间接（用对比学习），部分 token 走直接（用 logit KL）。

### 📊 效果
- 在多个任务上超过 GKD 基线
- 计算量降低

### ⚠️ 局限
- 间接/直接比例难调

---

## 15. SCOPE — 信号校准双路径

| 项目 | 内容 |
|------|------|
| **作者** | 学术 |
| **机构** | USTC / 美团 / 复旦 |
| **时间** | 2026.04 |
| **arXiv** | [2604.10688](https://arxiv.org/abs/2604.10688) |
| **代码** | [machine981/SCOPE](https://github.com/machine981/SCOPE) |

### 🎯 动机
- 学生 rollout 中既有"正确"也有"错误"轨迹
- 现有 OPD 对两类轨迹用同一损失，**信号未校准**
- 想要**针对正确/错误轨迹用不同损失**

### 💡 方法思路
**核心创新**：**双路径自适应加权**

- **错误轨迹**：用 **Teacher-PPL 加权 KL**（高 PPL = 教师不自信，权重低）
- **正确轨迹**：用 **Student-PPL 加权 MLE**（学生 PPL 越低越自信，权重高）

**Verifier-Routing**：用验证器判断轨迹对错，分发到不同路径。

### 📊 效果
- 信号利用率高
- 在推理任务上 SOTA

### ⚠️ 局限
- 需要 verifier
- 实现复杂

---

## 16. TIP — Token Importance 自蒸馏

| 项目 | 内容 |
|------|------|
| **作者** | HJSang 等 |
| **机构** | Meta / LinkedIn |
| **时间** | 2026.04 |
| **arXiv** | [2604.14084](https://arxiv.org/abs/2604.14084) |
| **代码** | [HJSang/OPSD_OnPolicyDistillation](https://github.com/HJSang/OPSD_OnPolicyDistillation) |

### 🎯 动机
- 不是所有 token 都值得做 KL 蒸馏
- 高熵 token（学生不确定的位置）才是信息密集的
- 低熵 token（学生确定的位置）蒸馏无新信息

### 💡 方法思路
**核心创新**：**Top-50% 高熵 token 携带 OPD 信号**

- 训练时**只对熵 top 50% 的 token 计算 KL 损失**
- 其他 token 用普通 SFT/CE

### 📊 效果
- **47% 显存节省**
- 性能不降反升
- 与 PACED 共享仓库

### ⚠️ 局限
- 50% 是经验值
- 不适合所有任务

---

## 17. HPD — Hybrid Policy Distillation

| 项目 | 内容 |
|------|------|
| **作者** | zwhong714 |
| **时间** | 2026.04 |
| **arXiv** | [2604.20244](https://arxiv.org/abs/2604.20244) |
| **代码** | [zwhong714/Hybrid-Policy-Distillation](https://github.com/zwhong714/Hybrid-Policy-Distillation) |

### 🎯 动机
- 现有 KD 多数用 FKL 或 RKL 二选一
- 但 FKL 鼓励多样性（mode-covering），RKL 鼓励精确（mode-seeking），**两种行为在不同阶段都有价值**
- 想要**统一框架**

### 💡 方法思路
**核心创新**：**Token 级重加权对数似然**

$$
\mathcal{L} = -\sum_t w_t \cdot \log \pi_{\text{student}}(y_t | x, y_{<t})
$$

权重 w_t 综合 FKL 和 RKL 特性：
- **轻量 on-policy 采样**：每 N 步做一次
- **统一 KD**：FKL + RKL 重加权

### 📊 效果
- 训练效率高
- 在 LlamaFactory + verl 后端集成好

### ⚠️ 局限
- 权重设计需调
- 实际收益因任务而异

---

## 📅 2026-06 月新论文速览（增量附录）

> 完整中文解读见 [daily-updates/2026-06-05.md](../daily-updates/2026-06-05.md)。

### OPRD — On-Policy Representation Distillation

| 项目 | 内容 |
|------|------|
| **作者** | Shenzhi Yang 等 |
| **时间** | 2026-06-04 |
| **arXiv** | [2606.06021](https://arxiv.org/abs/2606.06021) |
| **代码** | [ShenzhiYang2000/OPRD](https://github.com/ShenzhiYang2000/OPRD) |
| **类别** | 🔬 白盒 OPD / 隐藏层空间 |

**核心创新**：把 OPD 从"输出空间"提到"隐藏层空间"——学生-教师在同一 rollout 上对若干层 hidden state 直接对齐 MSE，**完全绕开 LM head**。
- 消除大词表（Qwen ~150k）的 MC-KL 采样方差
- 1.44× 训练加速、54% 显存节省
- AIME 2024/2025、AIMO 上**闭合师生 gap**（传统 OPD 困在教师以下）

**局限**：需学生-教师同构；选层策略待研究。

---

### FiRe-OPD — Filter, Then Reweight

| 项目 | 内容 |
|------|------|
| **作者** | Yuying Li 等 |
| **时间** | 2026-06-01 v1 / 06-04 v2 |
| **arXiv** | [2606.02684](https://arxiv.org/abs/2606.02684) |
| **代码** | [YuYingLi0/FiRe-OPD](https://github.com/YuYingLi0/FiRe-OPD) |
| **类别** | 🔬 白盒 OPD / 轨迹 + token 粒度 |

**核心创新**：**Filter + Reweight** 双层粒度优化——先过滤低质量 rollout，再在保留轨迹上对 token 软重加权。软加权保留更多信号。
- AIME 2024（强-弱）：+6.25
- Miner（多教师）：+18.81

**局限**：过滤阈值/软权函数为新超参。
#### 📄 [TS-OPSD: Internalize the Temperature (Policy Reheater)](https://arxiv.org/abs/2606.00755)
- **arXiv**: [2606.00755](https://arxiv.org/abs/2606.00755)
- **🎯 动机**: RL 训练中模型熵会崩溃，传统补救（熵正则 / 调采样温度）都是**外部干预**，不写入参数。
- **💡 方法**: 把高温度采样得到的"平滑分布"作为 self-teacher，**蒸馏回学生** → 温度的探索性被"内化"到参数里。**零外部教师、零特权数据、零额外推理成本**。
- **📊 数字**: Qwen3-4B/8B-Base 上比标准 RL 和 rollout-level 温度修复都更强初始化。


#### 📄 [StepOPSD: Step-Aware Online Preference Distillation for Agent RL](https://arxiv.org/abs/2605.27140)
- **arXiv**: [2605.27140](https://arxiv.org/abs/2605.27140)
- **🎯 动机**: 多轮 Agent RL 奖励稀疏且在 trajectory 级，但成功往往取决于**几个关键的局部决策**。
- **💡 方法**: 把 trajectory 切分为**以 step 为中心的段**，用 hindsight-enriched teacher 上下文重打分，转成**符号保持**的 advantage shaping + 归一化 step 信用预算。
- **📊 数字**: **ALFWorld Heat 79.1%**，**PickTwo 95.0%**，**TriviaQA 61.6%**。发现"两旋钮定律"。


#### 📄 [EchoDistill: Noisy-to-Clean Self-Distillation for Robust Audio LLMs](https://arxiv.org/abs/2605.23954)
- **arXiv**: [2605.23954](https://arxiv.org/abs/2605.23954)
- **🎯 动机**: 音频 LLM 遇噪声就语义漂移，主流方案（波形增强 / 答案级监督 / 内部抑制）各有缺陷。
- **💡 方法**: **对齐式 noisy-to-clean 自蒸馏** — 用干净输入的自身输出作为 teacher，去教噪声输入的输出对齐。
- **📊 数字**: 把"对齐"和"去噪"结合，是音频 LLM 鲁棒性的新范式。


#### 📄 [TrOPD: Trust Region On-Policy Distillation](https://arxiv.org/abs/2606.01249)
- **arXiv**: [2606.01249](https://arxiv.org/abs/2606.01249)
- **🎯 动机**: 师生分布差异大时 OPD 不稳定 — 教师对学生的 token 监督产生不可靠策略梯度，甚至优化失败。
- **💡 方法**: 三组件：(1) **Trust-Region On-Policy Learning** 只在可靠区域做 OPD；(2) **Outlier Estimation** 离群区域梯度裁剪/mask/forward-KL；(3) **Off-Policy Guidance** 学生从教师 prefix 续写。
- **📊 数字**: 数学推理、代码、通用 benchmark 一致超 OPD/EOPD/REOPOLD。


#### 📄 [ESR: Early Stopping Rollout (Less is More)](https://arxiv.org/abs/2605.27028)
- **arXiv**: [2605.27028](https://arxiv.org/abs/2605.27028)
- **🎯 动机**: 后续 token 时，学生早期轨迹作上下文（off-policy 相对教师），**教师纠错能力衰减**（Off-policy Teacher Decay）。
- **💡 方法**: ESR 简单有效 — **限制 rollout 生成到 response 前几个 token**。发现 **Cascading Alignment** 和 **Sub-mode Commitment** 效应。
- **📊 数字**: ESR **全胜过 full rollout OPD**，**GPU 效率和训练稳定性更高**（特别跨模型族）。KL 散度和熵信号**无法完全解释**。


#### 📄 [POPD / Truncated OPD: Are Full Rollouts Necessary?](https://arxiv.org/abs/2605.31490)
- **arXiv**: [2605.31490](https://arxiv.org/abs/2605.31490)
- **🎯 动机**: 标准 OPD 生成完整 rollout，**计算贵**且早期训练时后段教师反馈不可靠。
- **💡 方法**: rollout horizon 是关键瓶颈。两个简单策略 — **POPD** 渐进扩展；**Truncated OPD** 永久用截断。
- **📊 数字**: POPD 训练效率 **+3 倍**；Truncated OPD **只用 10% rollout 长度**就匹配 OPD 性能。


#### 📄 [TA-OPD: Token Teachability in On-Policy Distillation](https://arxiv.org/abs/2605.26844)
- **arXiv**: [2605.26844](https://arxiv.org/abs/2605.26844)
- **🎯 动机**: 选择性 OPD 优先高熵/高分歧 token — 但 raw KL 分歧是**学习价值的粗糙代理**。
- **💡 方法**: 把局部兼容性形式化为 **token teachability**。TA-OPD = 轻量级 token 位置选择，把 OPD loss 应用到高 teachability 位置。
- **📊 数字**: Qwen2.5/Qwen3 设置上，**5% 保留 token 常超全 token OPD**。


#### 📄 [ERPD: Extreme Region Policy Distillation](https://arxiv.org/abs/2605.25582)
- **arXiv**: [2605.25582](https://arxiv.org/abs/2605.25582)
- **🎯 动机**: 严格 on-policy 单次更新后丢弃轨迹，off-policy 复用有分布失配。aggressive 多步优化 → 快速初增益 + 后期 trajectory 概率偏离 + 熵崩溃。
- **💡 方法**: ERPD 两阶段 — (1) **弱约束 off-policy 优化**最大提取训练信号；(2) 在信任域约束下**蒸馏**这些信号到基础策略。
- **📊 数字**: 强基础模型和弱教师都受益 — 即使 aggressive 优化没产生更强策略，degenerate 教师也能用替代信号构造策略。


#### 📄 [Data-Efficient OPD for Automatic Speech Recognition](https://arxiv.org/abs/2605.28139)
- **arXiv**: [2605.28139](https://arxiv.org/abs/2605.28139)
- **🎯 动机**: 强 ASR 要大规模音频监督，复现和特化贵。
- **💡 方法**: Ark-ASR（0.6B 参数音频条件 LM，100k 小时语音训练） + 研究强 Qwen-ASR 教师能否通过 OPD 转移识别能力。
- **📊 数字**: abstract 截断，详细结果待全文。


