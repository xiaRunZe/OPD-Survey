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

## 📚 2026 年 6 月论文（11 篇）

#### 📄 [OPRD: On-Policy Representation Distillation](https://arxiv.org/abs/2606.06021) | Shenzhi Yang, 2026-06-04
- **🎯 问题**: 传统 OPD 在**输出空间**（LM head 之后的 logits）做 per-token KL 监督—— 1.5× 词表 150k 的 LLM（如 Qwen）需**蒙特卡洛采样**大词表分布（要么限制 top-k，要么 full-vocab 高方差）。**采样方差 + 采样偏倚** 是 LLM 上 OPD 难超过教师的关键瓶颈。同时 LM head 的 per-token KL 计算 + 反向传播是显存与计算的双重开销（54% 显存被 logits 占用）。
- **💡 思路**: 重新思考 OPD 的“**对什么对齐**”—— 既然 LLM 中**隐藏层状态已经蕴含丰富信息**，**为什么必须对齐 LM head 输出**？如果学生-教师在**同一 rollout 上对若干层 hidden state 直接对齐 MSE**，**完全绕开 LM head**，**采样方差消失、显存下降、保留语义**。问题从“**如何高效采样大词表**”变成“**隐藏层空间能否承担监督**”。
- **🔧 方法**:
  1. **OPRD (On-Policy Representation Distillation)**：**隐藏层空间** OPD；
  2. **采样**：学生**完整生成一次**序列，学生与教师都看这个序列（**on-policy**）；
  3. **对齐**：在选定的**若干层**上，学生-教师 hidden state **MSE 回归**（L2 距离）；
  4. **完全不调 LM head**、**不计算大词表 KL**、**不需要 top-k 采样**；
  5. 选层策略：可选 **最终层**、**中间层组合**、**加权组合**（论文探索了不同选层）。
- **📊 效果**:
  - **1.44× 训练加速**、**54% 显存节省**（**不存 logits 是关键**）；
  - AIME 2024/2025、AIMO 上**闭合师生 gap**（传统 OPD 困在教师以下、**学生达不到教师**）；
  - **完全去蒙特卡洛采样**—— 实验结果可重复性提升。
- **⚠️ 局限**:
  - **需学生-教师同构**（同架构同词表），**黑盒/异构教师**不适用；
  - **选层策略**需调（最终层 vs 中间层 vs 加权）—— 可能跨任务迁移难；
  - 中间层 MSE 是否完全捕捉**推理能力**传输？**仅监督隐藏层 → 是否损失输出分布细节**？
  - 与 **黑盒 API 教师** 场景**不兼容**（不是学教师 logits）。
- **价值**: 把“**OPD 必须在输出空间**”的隐含假设**完全拆掉**—— 这是 LLM 规模下 OPD 的**重要创新方向**。完全去 MC 采样是 LLM 蒸馏几十年的未解难题，**OPRD 提供了结构层面的全新解**。代码 [ShenzhiYang2000/OPRD](https://github.com/ShenzhiYang2000/OPRD)。

---

#### 📄 [FiRe-OPD: Filter, Then Reweight — Rethinking Optimization Granularity in OPD](https://arxiv.org/abs/2606.02684) | Yuying Li, 2026-06-01 v1 / 06-04 v2
- **🎯 问题**: OPD 从 **full-trace KL 监督** 走向**选择性监督**——选**哪些轨迹**、**哪些 token**、**哪些信号**最可靠。但现有 selective OPD 主要是**硬选择**（丢弃 token / 丢弃轨迹），**信息损失** + **梯度方差大**。需要**软加权**机制保留更多信号同时提升优化稳定性。
- **💡 思路**: **Filter + Reweight 双层粒度优化**——先**过滤低质量 rollout**（避免教师被垃圾信号带偏），再在**保留轨迹上**对**有信息量的 token 软重加权**。问题从“**硬选哪些学**”变成“**软调每个学多少**”。Filter 抓**轨迹级质量**，Reweight 抓**token 级信息**—— 两层粒度互补。
- **🔧 方法**:
  1. **FiRe-OPD (Filter, then Reweight)**：**双层粒度** OPD；
  2. **Filter 阶段**：按**质量指标**（如**一致性、奖励、教师置信度**）过滤低质量 rollout；
  3. **Reweight 阶段**：在**保留轨迹**内，对**有信息量的 token 软重加权**（如高 KL、高信息增益 token）；
  4. **软加权** vs 硬选择：保留**更多信息**、**梯度方差小**、**优化稳定**；
  5. **与多种 selective OPD 子方法**正交——可叠加。
- **📊 效果**:
  - **AIME 2024**（强-弱蒸馏）：**+6.25**；
  - **Miner**（多教师）：**+18.81**；
  - **强-弱/单教师/多教师** 三种设置一致超 token-level OPD 基线；
  - **软加权机制**是核心**稳定性源**。
- **⚠️ 局限**:
  - **过滤阈值** + **软权函数** 是**两个新超参**，需调；
  - 阈值在不同任务/模型上**可能不迁移**；
  - 软权函数的选择（KL-based、奖励-based、置信度-based）需任务特定；
  - **Filter 阶段**的指标选择是关键——**质量定义**决定**保留什么**。
- **价值**: 把 “**selective OPD**” 从“**硬选 salient**” 推到“**软加权 informative**” + “**双层粒度**”—— 是 selective OPD 范式的**重要成熟化**。**+18.81 多教师**和**+6.25 强-弱**是大差距，代表**信息-损失** vs **稳定性** trade-off 的更优解。代码 [YuYingLi0/FiRe-OPD](https://github.com/YuYingLi0/FiRe-OPD)。
#### 📄 [TS-OPSD: Internalize the Temperature (Policy Reheater)](https://arxiv.org/abs/2606.00755) | Xuewei Yang, 2026-05-30
- **🎯 问题**: RLVR 训练 LLM 推理能力时，**模型熵会崩溃** —— 策略越来越集中，rollout 多样性下降、有用学习信号变弱。现有补救是**外部干预**（熵正则化、采样时调温度），都不**写入参数**。训练一停就回到熵崩溃；采样时调温度还会拖慢推理。
- **💡 思路**: 转换问题 —— **别从外部加温度，而把温度的探索性"内化"到参数里**。做法：用模型自己加高温度的"平滑分布"做 self-teacher，蒸馏回学生。学生学完后，**它在标准温度采样时自带"高温等效"的探索性**。
- **🔧 方法**:
  1. 拿一个**熵已崩溃的 RL checkpoint** 作起点；
  2. **加高温度 scale 自己 logits** → 平滑分布作 self-teacher；
  3. **蒸馏回学生**（KL loss），学生学"自己高温下的自己"；
  4. 之后可继续做 RL，**作为更强初始化**；
  5. **零外部教师、零特权数据、零额外推理成本**。
- **📊 效果**: Qwen3-4B-Base 和 Qwen3-8B-Base 上，TS-OPSD reheater **比 standard continued RL 和 rollout-level 温度修复都更强初始化**。分析发现 TS-OPSD **主要减 output sharpness**（低温概率质量被推平），**保留中间表征、top-K 候选集、推理能力**。
- **⚠️ 局限**: 是"**事后介入**"方法（要先等熵崩溃再 reheater），何时触发、是否周期性 reheater 需要调度设计；高温系数 τ 是新超参；与"持续保持高温"型方案的对比未充分讨论。
- **价值**: 把"探索性恢复"从 **RL 训练阶段的临时 trick** 变成 **模型参数里的稳定能力** —— 一次 reheater，后续所有 rollout 都受益。


#### 📄 [StepOPSD: Step-Aware Online Preference Distillation for Agent RL](https://arxiv.org/abs/2605.27140) | Yanfei Zhang, 2026-05-26
- **🎯 问题**: 多轮 Agent RL 有个根本矛盾 —— **奖励稀疏且 trajectory 级**，但成功往往由**几个关键 step** 决定。现有 online OPD 把 trajectory 当**整字符串**给 token 级监督，**关键 step 拿不到精确 credit**，非关键 step 又被过度监督。
- **💡 思路**: 转换粒度 —— **从 token 切到 step**。把 trajectory 切成 action-centered step 段，**每段独立做 hindsight 重打分和 advantage shaping**。问题从"整条 trajectory 哪里出错"变成"**哪些 step 决定成功**"。
- **🔧 方法**:
  1. 把 trajectory 分解为 **action-centered step segments**；
  2. 用 **hindsight-enriched teacher 上下文**对每段重打分（知道最终结果后回头看每个 step）；
  3. 把 **token-level log-prob gap 转成 sign-preserving advantage shaping**（保留正负号，避免梯度符号被冲淡）；
  4. 加 **归一化 per-step 信用预算**（避免一段 step 抢光 credit）；
  5. 接 **GRPO** 更新。
- **📊 效果**: Qwen3-1.7B + Qwen2.5-3B-Instruct 在 **ALFWorld Heat 79.1%**（第一）、**PickTwo 95.0%**（第一）、**TriviaQA 61.6%**（第一）、**HotpotQA 40.4%**（并列第一）。发现"**两旋钮定律**"：**α_clip**（局部信任域）越稳越好；**λ_mix**（全局混合强度）任务相关。
- **⚠️ 局限**: Step 切分要**任务特定设计**（什么算"一个 step"）；teacher 上下文构建需要历史信息 → 显存压力；α_clip/λ_mix 仍要任务级调参。
- **价值**: 把 OPD 从"**输出级**"细化为"**动作级信用分配**" —— Agent RL 中关键 step 决定成功，这篇是 token→step 的代表工作。


#### 📄 [EchoDistill: Noisy-to-Clean Self-Distillation for Robust Audio LLMs](https://arxiv.org/abs/2605.23954) | Liang Lin et al., 2026-05
- **🎯 问题**: Audio LLM 遇**真实噪声**（街道、风噪、远场）时**语义漂移 + 幻觉**。现有三类方案各有缺陷：① 波形级增强（前端去噪，可能损害语义内容）；② 答案级监督（后端修，但梯度稀疏）；③ 内部 noise 表征抑制（中间改，难定位噪声特征）。
- **💡 思路**: 重新概念化 —— **"对噪声鲁棒" = "对干净语义的对齐"**。让 frozen clean-audio teacher 提供**语义参考**，noisy student 在采样中**暴露其在测试时的真实行为**，GRPO 训练 + **token-level teacher consistency 作 reward bonus**。问题从"如何去噪"变成"**如何在噪声下保持语义**"。
- **🔧 方法**:
  1. **Frozen clean-audio teacher** 作语义参考（无需训练）；
  2. **Noisy student** 在带噪输入上**采样 candidate responses**（GRPO group）；
  3. **GRPO 优化** + **token-level teacher consistency 作 reward bonus**；
  4. **Audio-aware reward shaping** —— 区分语义对错和音频合理性。
- **📊 效果**: **复杂噪声下 Audio LLM 语义可靠性和任务性能显著提升**，**零额外推理成本**（student 单独部署）。
- **⚠️ 局限**: 仍需 **frozen clean teacher** 部署，存储/算力代价；token consistency reward 依赖预训练 teacher 质量；只在 Audio LLM 上验证。
- **价值**: 首次把"**音频鲁棒性**"形式化为"**对干净语义的对齐**" —— 比单纯去噪更本质，思路可外推到视频、点云等模态。


#### 📄 [TrOPD: Trust Region On-Policy Distillation](https://arxiv.org/abs/2606.01249) | Xingrun Xing et al., 2026-05-31 v1 / 06-03 v2
- **🎯 问题**: OPD 训练在**师生分布差异大**时不稳定 —— 教师对 student-generated token 的监督给出**不可靠策略梯度**，甚至**优化失败**。根源：reverse-KL estimator 在分布失配下**梯度噪声大、优化困难**。
- **💡 思路**: 类似 PPO 的"**信任域 + 离群处理 + 引导**"三件套搬到 OPD。问题变成"**哪些区域教师是可信的、可信区域如何利用、不可信区域如何补救**"。
- **🔧 方法** (三组件):
  1. **Trust-Region On-Policy Learning**: 只在教师提供**可靠监督**的区域做 OPD，缓解分布失配下 reverse-KL 估计器的优化难度；
  2. **Outlier Estimation**: 离群区域用 **gradient clipping / masking / forward-KL 估计**减少不可靠监督的不良影响；
  3. **Off-Policy Guidance**: student 从 **teacher prefixes 续写**，用 forward-KL imitate off-policy guidance，**鼓励 on-policy 探索向可靠区域收敛**。
- **📊 效果**: 数学推理、代码生成、通用 benchmark 上 **TrOPD 一致超 SoTA OPD baseline**（OPD/EOPD/REOPOLD），**跨任务鲁棒**。
- **⚠️ 局限**: "信任域"和"离群"的判定需要设计（阈值/启发式）；forward-KL mode-covering 在某些场景可能损害**生成多样性**；三组件的协同需要验证稳定性。
- **价值**: 把 PPO 风格的"**信任域工具箱**"完整搬到 OPD，是"OPD 训练稳定性"系列工作里**工具最齐全**的一篇。


#### 📄 [ESR: Early Stopping Rollout (Less is More)](https://arxiv.org/abs/2605.27028) | Zhou Ziheng, 2026-05-26
- **🎯 问题**: OPD 存在 "**Off-policy Teacher Decay**" 现象 —— 后段 token 时，**student 早期 trajectory 作上下文**对 teacher 是 off-policy 的，**teacher 纠错能力衰减**，可能**回退到预训练阶段的 token-completion 行为**（不是 corrective scoring）。实证显示这个问题在长 rollout 后期严重。
- **💡 思路**: 既然"长 rollout 越往后 teacher 越没用"，**就别让它做无用功** —— "**少即是多**"思路。问题变成"**如何让 teacher 在最有用的位置发力**"。
- **🔧 方法**:
  1. 实证发现 Off-policy Teacher Decay 现象（多模型/多任务）；
  2. 提出 **ESR (Early Stopping Rollout)**：**只 rollout 前 K tokens**，teacher 只在这 K 个位置提供监督；
  3. 进一步探究机制：发现 **Cascading Alignment**（前 K 个位置 teacher 监督让后续位置自动对齐）和 **Sub-mode Commitment**（student 早期被纠错后，锁定到教师期望的 sub-mode）。
- **📊 效果**: ESR **跨模型规模/家族/任务/训练 regime 全胜过 full rollout OPD**，**GPU 效率高、训练稳定性强**（尤其**跨模型族**）。惊喜：有时 **ESR 学生反超 teacher**。
- **⚠️ 局限**: **K 是新超参**，跨任务最优 K 不同；"为什么 ESR 有时反超教师"仍是 open problem（论文承认 **KL 散度和熵信号无法完全解释**）。
- **价值**: 用**最简单的方法改 OPD 最顽固的问题之一**（off-policy decay）—— 挑战"完整 rollout 更好"的默认假设，与"less is more" 哲学一致。


#### 📄 [POPD / Truncated OPD: Are Full Rollouts Necessary?](https://arxiv.org/abs/2605.31490) | Yaocheng Zhang, 2026-05-29 v1 / 06-01 v2
- **🎯 问题**: 标准 OPD **生成完整 rollout** 训练，**计算昂贵**且**早期训练时后段 teacher 反馈不可靠**。一个关键洞察：**OPD 不需要最终答案奖励**就能给学习信号（与 RLVR 不同），**完整 rollout 可能不是必需的**。
- **💡 思路**: 明确"**rollout horizon 是关键瓶颈**"。给两个简单策略：① **POPD 渐进扩展**（训练早期短 rollout，稳定后扩展）—— curriculum 思路；② **TOPD 永久截断** —— "less is more" 思路。
- **🔧 方法**:
  1. 识别 rollout horizon 是 OPD 关键瓶颈（vs 之前聚焦"教师质量"）；
  2. **POPD (Progressive OPD)**: 训练过程中**渐进式扩展** rollout 长度（先短后长，curriculum）；
  3. **TOPD (Truncated OPD)**: **永久**只用 truncated rollouts（不变长）。
- **📊 效果**: 数学推理上，**POPD 训练效率 +3 倍**（wall-clock）；**TOPD 只用 10% rollout 长度**就能**匹配 OPD 性能**。大幅 wall-clock 和显存节省。
- **⚠️ 局限**: POPD 的扩展 schedule（什么时候开始扩、扩多快）需要设计；TOPD 在**长 chain-of-thought 任务**可能截断掉关键推理步骤；只验证了数学推理。
- **价值**: 挑战"**OPD 必须完整 rollout**"的默认假设，与 ESR/POPD 共同组成"**rollout horizon 短化**"系列工作。


#### 📄 [TA-OPD: Token Teachability in On-Policy Distillation](https://arxiv.org/abs/2605.26844) | Yuanyi Wang, 2026-05-26
- **🎯 问题**: 选择性 OPD 优先**高熵/高分歧 token** —— 但 **raw KL 分歧是"学习价值"的粗糙代理**。KL 把"**可学分歧**"和"**不可比分歧**"混在一起：前者（teacher 把 mass 放在 student top-K 内）能学，后者（teacher 把 mass 放 student 现有 support 外）不能学。把后者当学习信号只会浪费梯度甚至误导。
- **💡 思路**: 重新定义"**哪些分歧值得蒸馏**" —— 不是"哪些分歧大"，而是"**哪些分歧能真的被学会**"。用 **fixed-context diagnostic**（同上下文下，teacher-student KL 减少程度）作"**teachability**"度量。
- **🔧 方法**:
  1. 在 fixed context 下，测"在该位置对 student 做蒸馏，KL 减少多少"作为**teachability** 信号；
  2. 发现：raw KL 混淆"**可学分歧**"和"**不兼容分歧**" —— 同样 KL 大小，前者能学、后者不能；
  3. 形式化 **token teachability**：综合考虑"分歧大小"和"分歧是否在 student support 内"；
  4. **TA-OPD (Teachability-Aware OPD)**：**轻量级 token 位置选择**，**只对高 teachability 位置**算 OPD loss。
- **📊 效果**: Qwen2.5/Qwen3 teacher-student 设置，**TA-OPD 只保留 5% tokens** 常超**全 token OPD**，并超 entropy- 和 divergence-based baseline。
- **⚠️ 局限**: Teachability 计算本身有开销（论文称"lightweight"，但需实验验证）；"可学/不可学"边界在不同分布上可能不明确；和"selective distillation"系列工作的本质区分需要更清晰表述。
- **价值**: 把"**selective OPD**"从"**选 salient**"变成"**选 learnable**" —— 这是关键范式转变（"salient ≠ useful"）。


#### 📄 [ERPD: Extreme Region Policy Distillation](https://arxiv.org/abs/2605.25582) | 2026-05
- **🎯 问题**: LLM RL 有个**根本 trade-off**：(1) 严格 on-policy → **一次更新就丢轨迹**，**样本效率低**；(2) off-policy 复用 → **分布失配**，已有 trust-region 方法**保守** → **浪费丰富训练信号**。实验发现：aggressive 多步优化 → **快速初增益 + 后期 trajectory 概率偏离 + 熵崩溃**，**KL 约束越紧、ceiling 越低**（解决不了根本问题）。
- **💡 思路**: 重新定义问题 —— **别再优化"KL 约束强度"，而是解耦"信号提取"和"信号转移"**。阶段 1 用**弱约束**大干一场提取信号，阶段 2 用 trust-region 蒸馏把信号**安全地**教给基础策略。
- **🔧 方法** (两阶段):
  1. **阶段 1: 弱约束 off-policy 优化** —— 在固定数据上**aggressively** 提取训练信号（不管 KL）；
  2. **阶段 2: Trust-region 蒸馏** —— 用阶段 1 得到的 policy 作 teacher，对**基础策略**蒸馏（forward/reverse KL + trust region）；
  3. 蒸馏后策略**KL 显著更小但性能相当或更好** → 阶段 1 的很多 divergence 实际是"无用 drift"而非"genuine improvement"。
- **📊 效果**: **强基础模型**（on-policy 已 plateau）有收益；**弱教师**也能用替代信号构造策略 → 实用。数学推理上验证。
- **⚠️ 局限**: 阶段 1 的"aggressive 优化"上限是另一个 open problem；两阶段耦合策略**部署复杂**；阶段 1 的过度优化可能导致无法恢复的"catastrophic"。
- **价值**: 重新定义"**distillation**"为"**信号提取 + 信号蒸馏**"两阶段，给"**trust-region 何时该严格、何时该放松**"提供新解。


#### 📄 [Data-Efficient OPD for Automatic Speech Recognition (Ark-ASR)](https://arxiv.org/abs/2605.28139) | Yiming Wang, 2026-05-27
- **🎯 问题**: 强 ASR 要**大规模音频监督**（Qwen3-Omni AuT 用 **20M 小时**），复现和特化**极其昂贵**。能不能用更小数据 + OPD 训出**可比紧凑 ASR**？
- **💡 思路**: 验证一个假设 —— "**OPD 让紧凑模型在小数据下也能追近大模型**"。具体：100k 小时训 Ark-ASR (0.6B) + 强 Qwen-ASR 教师 OPD。问题从"是否需要 20M 小时"变成"**小数据 + 强教师 OPD 能否 work**"。
- **🔧 方法**:
  1. 训 **Ark-ASR (0.6B 参数音频条件 LM)** 在 100k 小时上；
  2. 用**强 Qwen-ASR 教师**做 OPD，转移额外识别能力；
  3. Mandarin + English ASR benchmark 评估；
  4. **Support-overlap diagnostic** 验证 OPD 有效性（student-teacher 局部兼容性）。
- **📊 效果**: 5 个评估集中**4 个超** same-scale Qwen3-ASR-0.6B baseline；**只用 100k 小时**（vs 20M 小时）；1.7B 教师仍更强，但**紧凑 ASR 在小数据预算下大幅缩近 gap**。
- **⚠️ 局限**: 仍依赖**教师模型存在**（部署复杂）；100k 小时也是不小预算；模态外泛化（不同语言/口音）未验证；只验证 ASR。
- **价值**: 实证"**OPD 让紧凑模型在小数据下追近大模型**" —— 对**预算紧但想用 OPD** 的团队是直接信号。



