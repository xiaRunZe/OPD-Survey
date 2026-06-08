# 🔁 五、迭代自举 + 🤝 六、OPD-RL 混合方法

> 本章节合并两个相关方向：
> - **迭代自举**：教师=学生，但用**历史 checkpoint**
> - **OPD-RL 混合**：OPD 损失与 RL 目标融合

---

# 🔁 五、迭代自举

> **特点**：教师 = 自己的**历史 checkpoint**（冻结一轮）
>
> 区别于 OPSD（用特权上下文），这里的"教师"是**不同参数**的早期自己。

---

## 1. SPIN — Self-Play Fine-Tuning

> 🎯 **早期自举方法**，但严格意义上非 per-token logit 监督。

| 项目 | 内容 |
|------|------|
| **机构** | UCLA |
| **时间** | 2024.01 |
| **会议** | ICML 2024 |
| **arXiv** | [2401.01335](https://arxiv.org/abs/2401.01335) |
| **代码** | [uclaml/SPIN](https://github.com/uclaml/SPIN) |

### 🎯 动机
- 想要"无人类标注"的自我提升
- 现有方法（RLHF）依赖人类偏好
- 想要从"自己的输出 vs 自己的历史"中学习

### 💡 方法思路
**核心机制**：**Self-Play + DPO**

- **学生**：当前模型
- **教师**：上一轮 frozen checkpoint
- 用 DPO 偏好优化：
  - **正样本**：教师生成的回答
  - **负样本**：学生生成的回答

**关键设计**：学生 rollout → 教师生成参考 → DPO 偏好对齐

### ⚠️ 严格度说明
- C1 ✓（学生 rollout）
- C2 严格失败（非 per-token logit 监督，是序列级 DPO 偏好）
- 准确说是"**迭代 on-policy DPO**"

### 📊 效果
- 在多个任务上自我提升
- 无需外部标注

### ⚠️ 局限
- 提升幅度有限
- 训练后期会 plateau

---

## 2. rStar / rStar-Math / rStar2-Agent

| 项目 | 内容 |
|------|------|
| **机构** | Microsoft Research |
| **时间** | 2025.01+ |
| **链接** | [rStar](https://github.com/microsoft/rStar) · [rStar-Math 2501.04519](https://arxiv.org/abs/2501.04519) · [rStar2-Agent 2508.20722](https://arxiv.org/abs/2508.20722) |

### 🎯 动机
- 想要**不依赖大规模人工标注**的数学/Agent 训练
- 想要"自举"式能力增长
- 现有 RL 采样成本高

### 💡 方法思路
**核心机制**：**MCTS 过滤自举**

- 学生 rollout 多条候选解
- 用 MCTS 验证（如过程奖励模型 PRM / 判别器）**过滤高质量样本**
- 用过滤后的样本做 SFT
- 迭代多轮

### ⚠️ 严格度说明
- 严格意义非 per-token logit 监督
- 是**迭代自举**而非经典 OPD

### 📊 效果
- rStar-Math：数学推理 SOTA（小模型）
- rStar2-Agent：Agent 任务 SOTA

### ⚠️ 局限
- MCTS 计算量极大
- 验证器质量是上限

---

# 🤝 六、OPD-RL 混合方法

> **特点**：把 OPD 的 token 级 KL 监督**融入 RL 目标**（GRPO/PPO/DPO/RLVR）。
>
> 两种典型融合方式：
> - **KL as Reward**：把 KL 当 reward shaping
> - **OPD inside RL**：用 RL 算 advantage + OPD 提供密集监督

---

## 1. BOND — Best-of-N Distillation

| 项目 | 内容 |
|------|------|
| **机构** | Google DeepMind |
| **时间** | 2024.07 |
| **arXiv** | [2407.14622](https://arxiv.org/abs/2407.14622) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有 RLHF 训练**复杂、不稳定**
- 想要"用 BoN 分布做蒸馏"——把 Best-of-N 当作 target

### 💡 方法思路
**核心机制**：**BoN Target + Jeffreys 散度**

- 采样 N 个学生回答，选最好的
- 把 BoN 分布当作"教师分布"
- 蒸馏到学生

**Jeffreys 散度**：FKL + RKL，对称化

### ⚠️ 严格度说明
- 序列级，**非 per-token logit**（C2 部分失败）
- 更准确是"**on-policy 迭代对齐**"

### 📊 效果
- 训练稳定
- 简单有效

### ⚠️ 局限
- N 越大越慢
- 提升幅度有限

---

## 2. Faster WIND — 加速的 WIND

| 项目 | 内容 |
|------|------|
| **机构** | CMU / Google |
| **时间** | 2024.10 |
| **会议** | AISTATS 2025 |
| **arXiv** | [2410.20727](https://arxiv.org/abs/2410.20727) |
| **类型** | 📄 paper-only |

### 🎯 动机
- BOND 等 BoN 蒸馏**慢**（N 次采样 + 验证）
- 想要博弈论视角的加速

### 💡 方法思路
**核心机制**：**胜率优势**（Win-Rate Dominance）

- 用胜率作为学习目标（不是 KL）
- 博弈论加速

### 📊 效果
- 加速 BOND 类方法

### ⚠️ 局限
- 细节需读 paper

---

## 3. AlignDistil — RLHF 等价的 KD

| 项目 | 内容 |
|------|------|
| **作者** | Mingyang Song, 等 |
| **机构** | BJTU / 腾讯 |
| **时间** | 2025.03 |
| **会议** | ACL 2025 |
| **arXiv** | [2503.02832](https://arxiv.org/abs/2503.02832) |
| **代码** | [songmzhang/AlignDistil](https://github.com/songmzhang/AlignDistil) |

### 🎯 动机
- 想要"用 KD 复现 RLHF 效果"
- 现有方法要么不匹配（off-policy KD），要么不稳（RL）

### 💡 方法思路
**核心机制**：**DPO 风格重新框架化**

- 把 DPO 损失表示为"对 DPO 模型 + ref-model logits 的特殊组合"
- 实现"用 KD 复现 DPO"

### 📊 效果
- 在对齐任务上达到 RLHF 同等效果
- 训练更稳定

### ⚠️ 局限
- 实际部署仍需对齐数据

---

## 4. LUFFY — 混合策略 GRPO

| 项目 | 内容 |
|------|------|
| **机构** | 西湖大学 |
| **时间** | 2025.04 |
| **arXiv** | [2504.14945](https://arxiv.org/abs/2504.14945) |
| **代码** | [ElliottYan/LUFFY](https://github.com/ElliottYan/LUFFY) |

### 🎯 动机
- 现有 GRPO 训练**需要 on-policy 探索**，但 on-policy 样本可能质量低
- 想要"在 GRPO 中插入**高质量 off-policy 教师轨迹**"作为引导

### 💡 方法思路
**核心机制**：**Mixed-Policy GRPO + 策略塑形**

- 一半 on-policy 学生 rollouts
- 一半 off-policy R1 教师轨迹
- GRPO advantage 在混合数据上计算
- 政策塑形（policy shaping）让学生偏向高质量 off-policy 数据

### ⚠️ 严格度说明
- 混合策略：on-policy 部分满足 C1+C2，off-policy 部分 C1 ✗
- 整体是"**带 off-policy 注入的 OPD-flavor**"

### 📊 效果
- 推理任务上比纯 GRPO 提升明显
- 比纯 R1 SFT 更稳定

### ⚠️ 局限
- 混合比例需调
- 依赖 R1 等教师

---

## 5. KETCHUP — k 步 RL-KD

| 项目 | 内容 |
|------|------|
| **机构** | 阿尔伯塔大学 |
| **时间** | 2025.04 |
| **arXiv** | [2504.19024](https://arxiv.org/abs/2504.19024) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有 RL-KD 融合方法较简单
- 想要**k 步 Bellman return**做 RL 监督

### 💡 方法思路
**核心机制**：**k 步 REINFORCE + KD**

- 序列级 k 步 Bellman return
- 融合 KD 损失

### ⚠️ 严格度说明
- 序列级，**非 per-token logit**
- 论文自称"**RL-based KD**"，更接近 RL + KD 锚

### 📊 效果
- 在多个任务上有效

### ⚠️ 局限
- 序列级信号

---

## 6. KDRL — 联合 KD + RL

| 项目 | 内容 |
|------|------|
| **机构** | 哈工大 / 华为 |
| **时间** | 2025.06 |
| **arXiv** | [2506.02208](https://arxiv.org/abs/2506.02208) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 想要"KD + GRPO"统一目标
- 让两者同时优化

### 💡 方法思路
**核心机制**：**联合 RKL + GRPO 规则奖励**

$$
\mathcal{L} = \mathcal{L}_{\text{RKL}}(S, T) + \alpha \cdot \mathcal{L}_{\text{GRPO}}(y, \text{rule-based reward})
$$

- 教师：Skywork-OR1
- 学生：rollout + 双损失

### 📊 效果
- 推理任务提升

### ⚠️ 局限
- α 权重需调

---

## 7. SDPO — Self-Distillation Policy Optimization

> 🎯 **首次将"反馈自蒸馏"形式化为 RL 优化**

| 项目 | 内容 |
|------|------|
| **机构** | ETH / MIT |
| **时间** | 2026.01 |
| **arXiv** | [2601.20802](https://arxiv.org/abs/2601.20802) |
| **项目页** | [self-distillation.github.io/SDPO](https://self-distillation.github.io/SDPO) |
| **代码** | [lasgroup/SDPO](https://github.com/lasgroup/SDPO) |

### 🎯 动机
- RL 依赖**复杂奖励工程**
- 自蒸馏（OPSD）有潜力但形式化粗糙
- 想要"用 RL 框架统一自蒸馏"

### 💡 方法思路
**核心机制**：**反馈条件化自蒸馏策略梯度**

**训练流程**：
1. 学生 rollout
2. 用 token 化反馈（环境/规则）评估
3. 在反馈条件化下重新评估（同模型 = 教师）
4. 把"反馈条件化的 next-token 分布"作为 target
5. 用策略梯度对齐

### 📊 效果
- 在 code、tool-use、science 等任务上超过 GRPO
- 框架统一

### ⚠️ 局限
- 反馈质量敏感
- 训练流程长

---

## 8. KEPO — Knowledge-Enhanced PO

| 项目 | 内容 |
|------|------|
| **时间** | 2026.01 |
| **arXiv** | [2602.00400](https://arxiv.org/abs/2602.00400) |
| **代码** | [Corleno/KEPO](https://github.com/Corleno/KEPO) |

### 🎯 动机
- 现有偏好优化未利用外部知识
- 想要"知识库 + 偏好 RL"

### 💡 方法思路
**核心机制**：**KB 增强 PO**

- 偏好数据 + 知识库信息
- 联合训练

### ⚠️ 严格度说明
- 满足 on-policy C1，但 C2 形式（per-token KL）需读 paper

### 📊 效果
- 推理任务上有效

### ⚠️ 局限
- 知识库质量敏感

---

## 9. Open-AgentRL

| 项目 | 内容 |
|------|------|
| **机构** | Gen-Verse |
| **时间** | 2026.02 |
| **代码** | [Gen-Verse/Open-AgentRL](https://github.com/Gen-Verse/Open-AgentRL) |

### 🎯 动机
- 想要**多领域 Agent RL 训练框架**
- 包括 RLAnything / DemyAgent 等

### 💡 方法思路
**核心机制**：**多领域教师 + 过程奖励**

- 推理 / GUI / Coding 多领域
- GRPO-TCR + SandboxFusion PRM

### 📊 效果
- 多领域 Agent 训练统一框架

### ⚠️ 局限
- 实现复杂

---

## 10. DDT — On-Policy SFT 理论

| 项目 | 内容 |
|------|------|
| **机构** | MSRA / Shopee |
| **时间** | 2026.02 |
| **arXiv** | [2602.12222](https://arxiv.org/abs/2602.12222) |
| **代码** | [zhangmiaosen2000/Towards-On-Policy-SFT](https://github.com/zhangmiaosen2000/Towards-On-Policy-SFT) |

### 🎯 动机
- 想要"on-policy SFT"的理论基础
- 解释为什么 on-policy 比 off-policy SFT 更好

### 💡 方法思路
**核心机制**：**分布判别理论（Distribution Discriminant Theory）**

- 形式化 on-policy SFT 的目标函数
- 证明 on-policy 优于 off-policy 的理论依据

### ⚠️ 严格度说明
- **理论论文**，非具体算法
- 给出 on-policy SFT 的一般性框架

### 📊 价值
- 提供理论基础
- 指导后续算法设计

### ⚠️ 局限
- 理论性强，工程化需自己实现

---

## 11. 𝒳-KD — 逆 RL 风格的 KD

| 项目 | 内容 |
|------|------|
| **机构** | BUPT |
| **时间** | 2026.02 |
| **arXiv** | [2602.12674](https://arxiv.org/abs/2602.12674) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 想要"逆 RL + KD"结合
- 用 IRL 学 reward function，同时蒸馏

### 💡 方法思路
**核心机制**：**AVRIL 逆 RL + 联合 reward/policy 蒸馏**

- 联合建模 reward + policy
- 双向蒸馏

### ⚠️ 严格度说明
- 接近"IRL+OPD" 混合
- 严格的 C2 形式需读 paper

### 📊 效果
- 多个任务上有效

### ⚠️ 局限
- 复杂度高

---

## 12. RLAD — 强化感知 KD

| 项目 | 内容 |
|------|------|
| **机构** | AWS |
| **时间** | 2026.02 |
| **arXiv** | [2602.22495](https://arxiv.org/abs/2602.22495) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 想要"RL + KD"中 KL 权重自适应
- 现有方法 KL 强度固定

### 💡 方法思路
**核心机制**：**PPO/GRPO ratio 用 teacher-old-policy 混合做信任域**

- 教师：Qwen3-32B
- 学生：在 on-policy 滚出上做 PPO/GRPO
- ratio 用混合项稳定

### 📊 效果
- 推理任务稳定

### ⚠️ 局限
- 混合权重敏感

---

## 13. OpenClaw-RL

| 项目 | 内容 |
|------|------|
| **机构** | Gen-Verse |
| **时间** | 2026.03 |
| **arXiv** | [2603.10165](https://arxiv.org/abs/2603.10165) |
| **代码** | [Gen-Verse/OpenClaw-RL](https://github.com/Gen-Verse/OpenClaw-RL) |

### 🎯 动机
- 想要"统一二元 RL + OPD"训练
- 适用于 Terminal / GUI / SWE / Tool-call 等

### 💡 方法思路
**核心机制**：**GRPO + 判别器 + token-logprob gap**

- 判别器提取"事后提示"（hindsight hints）
- token-logprob gap 作为方向性 advantage
- 统一二元 RL 和 per-token OPD

### 📊 效果
- 跨域 Agent 训练

### ⚠️ 局限
- 复杂流程

---

## 14. ExGRPO — Probing-to-Refine

| 项目 | 内容 |
|------|------|
| **机构** | UNC / ASU |
| **时间** | 2026.03 |
| **arXiv** | [2603.19266](https://arxiv.org/abs/2603.19266) |
| **代码** | [Zhen-Tan-dmml/ExGRPO](https://github.com/Zhen-Tan-dmml/ExGRPO) |

### 🎯 动机
- 现有 GRPO 缺少"解释性"——学生不知"为什么"
- 想要"探针 → 解释 → GRPO"

### 💡 方法思路
**核心机制**：**解释性探针 + GRPO**

- 用探针强制学生"说出推理逻辑"
- GRPO + 对话结构奖励
- 通过解释性反转（Explanatory Inversion）做强化蒸馏

### 📊 效果
- 推理任务上解释性更好

### ⚠️ 局限
- 解释质量依赖训练

---

## 15. HDPO — 混合蒸馏 PO

| 项目 | 内容 |
|------|------|
| **机构** | NVIDIA |
| **时间** | 2026.03 |
| **arXiv** | [2603.23871](https://arxiv.org/abs/2603.23871) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有 PO 只在"困难 prompt"上需要 OPD
- 想要"按难度分流"

### 💡 方法思路
**核心机制**：**RL + OPD fallback**

- 大部分 prompt：标准 RL
- "悬崖 prompt"（学生完全失败）：生成特权 rollouts 并自蒸馏

### 📊 效果
- 兼顾 RL 效率 + OPD 质量

### ⚠️ 局限
- 悬崖判定标准

---

## 16. RLSD — Self-Distilled RLVR

| 项目 | 内容 |
|------|------|
| **机构** | 多机构 |
| **时间** | 2026.04 |
| **arXiv** | [2604.03128](https://arxiv.org/abs/2604.03128) |
| **类型** | 📄 paper-only |

### 🎯 动机
- RLVR（可验证奖励）方向单一
- 想要"自蒸馏调节 RLVR 方向"

### 💡 方法思路
**核心机制**：**RLVR direction + teacher evidence-ratio magnitude**

- RLVR 提供方向
- 教师 evidence-ratio 调节幅度
- 联合训练

### 📊 效果
- 推理任务有效

### ⚠️ 局限
- evidence-ratio 稳定性

---

## 17. NPO / AutoNPO — 向未来自己学习

> 🎯 **核心创新**：教师 = 自己**未来 checkpoint**

| 项目 | 内容 |
|------|------|
| **机构** | IIE CAS / UCAS / JD.COM |
| **时间** | 2026.04 |
| **arXiv** | [2604.20733](https://arxiv.org/abs/2604.20733) |
| **类型** | 📄 paper-only |

### 🎯 动机
- 现有 GRPO 训练**缺乏引导**——学生常陷入局部最优
- 想要"用**未来 checkpoint** 做教师"，既比自己强、又不至于太远

### 💡 方法思路
**核心机制**：**Near-Future Self + Verifier-Filtered Trajectories**

- 教师：同一训练 run 的**未来 checkpoint**（如 k 步后）
- 学生在 on-policy 滚出
- 用 verifier 过滤未来 checkpoint 的轨迹
- 序列级 trajectory 混合

**关键洞察**：Q/V ratio（信号强度 / 距离）最大化。
- 外部教师（如 R1）信号强但距离远
- 未来 self 信号弱但距离近
- **最优在中间**

### ⚠️ 严格度说明
- 与 LUFFY 类似，但教师**来自同 run 的近未来**
- 论文自称 RLVR，**严格 per-token KL 不作为损失**（监督是 verifier-filtered 序列级 mixing）

### 📊 效果
- 比 vanilla GRPO **保持更高熵**（避免早熟）
- AutoNPO 自适应调度

### ⚠️ 局限
- 需多 checkpoint 存储
- 调度策略复杂
### 🎯 动机
- 现有自蒸馏在**错误位置**也会蒸馏
- 想要"定位错误 + 局部蒸馏"

### 💡 方法思路
**核心机制**：**自反射 + 错误定位**

- 用自反射器提取**纠正思路**
- 定位**首个错误 span**
- 限制自蒸馏到对齐的错误 span

**结合 SDPO**：在错误 span 上做密集蒸馏。

### 📊 效果
- 科学、tool-use、math 任务有效
- 错误恢复能力强

### ⚠️ 局限
- 反射器需训练

---

## 📚 2026 年 6 月论文（5 篇）

#### 📄 [PGPO: Physics-Guided Policy Optimization with Self-Distillation](https://arxiv.org/abs/2606.03620) | Ke Wang, 2026-06-02
- **🎯 问题**: SDPO（Self-Distilled Policy Optimization）等 RL 范式在**长程训练中后期崩溃**——loss/gradient 震荡、最终分数下降。传统 fix 是衰减学习率或加 KL 正则，但**为什么**这样有效**没理论解释**。问题：能否从**跨学科类比**找到**结构化步长调度**，并给出**理论保证**？
- **💡 思路**: 跨学科类比——**粘性流体动力学**中"粘性"控制流体粒子的扩散行为。形式化类比：在 **SDE（随机微分方程）层面**看 SDPO 训练动力学，引入"**信息调节步长乘子**"——来自**学生预测与反馈条件教师之间的互信息估计**。问题从"调学习率"变成"**用信息论调节步长**"。
- **🔧 方法**:
  1. **PGPO (Physics-Guided Policy Optimization)**：**跨学科类比** SDE 形式化；
  2. **信息调节步长乘子**——来自学生预测 vs 反馈条件教师的**互信息估计**；
  3. **理论保证**：该调节**保留 vanilla SGD 的一阶弱近似**（理论收敛性不破坏）；
  4. **每步开销可忽略**——互信息估计轻量；
  5. 作为 SDPO 的**步长调度器**叠加使用。
- **📊 效果**:
  - **Science-QA 4 个 domain 中 3 个 +4.5 分**（相对 SDPO 基线）；
  - **SDPO 后期崩溃的场景下保持稳定**——核心解决目标达成；
  - **理论 + 实验**双验证——**收敛性**与**实践稳定性**兼得。
- **⚠️ 局限**:
  - **互信息估计需额外前向**（虽然开销可忽略但不是零）；
  - **仅在 ScienceQA 验证**——泛化到其他任务（生成/对话）**未充分验证**；
  - 跨学科类比的**直觉迁移**是否在更大模型上**严格成立**？
  - 调优**互信息估计器**本身是工程问题。
- **价值**: 把 "**粘性流体动力学**" 跨学科类比引入 SDPO 步长调度——**理论保证 + 实践稳定性**双丰收。是**理论驱动 RL 步长调度**的**有趣新方向**。

---

#### 📄 [TRB: Trust-Region Behavior Blending for On-Policy Distillation](https://arxiv.org/abs/2605.31159) | Alexey Gorbatovski, 2026-05-29
- **🎯 问题**: OPD 在学生 rollout prefix 上做教师监督 → 解决 offline 蒸馏的 prefix mismatch。但**早期训练学生 rollout 仍差**，教师监督落在**弱/低质量 prefix** 上 → 学习信号被污染。需要 warmup 机制。
- **💡 思路**: **别让学生"硬" rollout 一开始就接受教师监督**。在 warmup 阶段，**用"接近教师"的行为策略替代学生早期 rollout**（在 KL 信任域内），等学生强了再让学生接管。问题从"如何提升早期 OPD 质量"变成"**如何用 KL 门控分阶段 rollout**"。
- **🔧 方法**:
  1. **TRB (Trust-Region Behavior Blending)** —— **warmup 方法**；
  2. 在**以学生为中心的 KL 信任域**内，**用"最接近教师"的行为策略替换早期 rollout 策略**；
  3. 保留**per-prefix reverse-KL OPD loss 不变**（核心信号不变）；
  4. **KL 预算退火到 0** —— warmup 后**自然回到纯学生 rollout**（无侵入式改变）。
- **📊 效果**: 两个**数学推理蒸馏**设置中，TRB **平均最强**（对比纯 OPD、RL 起步、纯蒸馏等）。
- **⚠️ 局限**: "最近教师行为策略"的构造代价（每步需评估 KL）；KL 预算 schedule 需要设计；warmup 何时结束需调；只验证数学推理。
- **价值**: 把"**warmup 阶段如何安全做 OPD**"形式化为"**KL 信任域行为混合**" —— 是 PPO trust-region 思想在 OPD 训练初期的具体实现。


#### 📄 [LGR: Lookahead Group Reward — Combating Supervision Fidelity Decay in OPD](https://arxiv.org/abs/2605.30833) | Yanjiang Liu, 2026-05-29
- **🎯 问题**: 识别 OPD 的**关键瓶颈** —— **SFD (Supervision Fidelity Decay)**：**学生 prefix 越长，教师的 next-token 分布越不 confident/discriminative**。结果：teacher-dependent 纠错信号**在长 reasoning chain 后期被冲淡**，学生 drift 复合。reverse-KL 的"教师应该纠错"假设在长链下失效。
- **💡 思路**: 既然 SFD 是**"教师监督"会衰减**，**就用 lookahead 评估"如果教师预测下一步会多 confident"** 作信号。Group-normalized 奖励，让"教师未来 confident 的 token 拿更大优势"。问题从"如何用现有 reverse-KL"变成"**如何提前用教师 confidence**"。
- **🔧 方法**:
  1. **Lookahead Group Reward (LGR)**：用教师在**下一步**的 confidence 评估学生 top-K 候选 token；
  2. **Group-normalized 奖励**（避免尺度问题）；
  3. **熵触发的 tree-attention 机制** —— 只在需要 lookahead 时启用，保持计算效率；
  4. 核心 insight：next-step teacher confidence 反映**未来 reverse-KL 监督的判别强度**。
- **📊 效果**: 6 个数学/代码 benchmark，**7B 学生 mean@8 比 OPD +2.57**；**长生成增益最大 +4.92**（AIME-26 39k tokens）。**长链越深，优势越大**（正是 SFD 严重的地方）。
- **⚠️ 局限**: Tree-attention 实现复杂；lookahead 步数需调；group normalization 假设可能不适用所有任务；7B 学生未验证更大模型的 scalability。
- **价值**: 把"**监督保真度**"从"**被动观察**"变成"**主动 lookahead**" —— 是 SFD 系列工作的关键进展，对长 reasoning chain 训练是直接收益。


#### 📄 [ADWIN: Adaptive Windows for Horizon-Aware On-Policy Distillation](https://arxiv.org/abs/2605.28396) | Kun Liang, 2026-05-27
- **🎯 问题**: 标准 full-rollout OPD 把**每次更新绑到一次贵完成**，且可能把监督**过度分配**到对当前学生**边际价值低**的后段。隐含假设"长 rollout 总更好"未必成立 —— **学生-induced rollout 可能从某点起就漂出教师偏好**。
- **💡 思路**: 重新概念化 —— **rollout 长度不是固定值，是"在线可接受性决策"**。问题从"用多长 rollout"变成"**何时接受当前 prefix、何时启动 full rollout probe**"。
- **🔧 方法**:
  1. **ADWIN (Adaptive Windows) 自适应窗口框架**；
  2. **Useful supervision horizon** 视角：student-induced rollout 会从某点起漂出 teacher-preferred continuations；aligned prefixes 可能已保留 long-horizon OPD 更新方向；
  3. **训练在短教师锚定 prefix** 上（用 trust-region 风格约束）；
  4. **延迟 full-rollout probe 审计 prefix-full 对齐**（用 staleness control 防 stale 决策）；
  5. **在线调整下一步 horizon**。
- **📊 效果**: 数学/代码推理单任务/多任务/强对弱设置，**端到端训练成本最多 -4.1 倍**且精度相当或更好。**accuracy-compute trade-off 显著优**。
- **⚠️ 局限**: Staleness 控制的设计参数需调；"prefix-full alignment" 度量选择需适配任务；延迟 probe 本身有计算代价；可能不适用超长 reasoning（>10K tokens）任务。
- **价值**: 把"**rollout horizon 决策**"从"**离线固定**"变成"**在线可接受性**" —— 是 ESR/POPD 系列"短 rollout"思路的**自适应升级版**，代表"horizon-aware OPD" 走向成熟。


#### 📄 [CaMOPD: Counteraction-Aware Multi-Teacher OPD for General Capability Recovery with Domain Preservation](https://arxiv.org/abs/2605.27115) | Tianlei Chen, 2026-05-26
- **🎯 问题**: 领域特化（role-play、medical、...）常**削弱通用能力**。MOPD（Multi-Teacher OPD）通过多教师监督恢复能力，但**假设"教师对齐的 prompt 覆盖"** —— 开源通用教师的**后训练数据未知**，这假设难满足。直接用 proxy 通用 prompt 训练会出**两个失败模式**：① recovery-preservation **counteraction**（冲突梯度相互抵消）；② weak-signal **flattening**（信号平均稀释）。
- **💡 思路**: 不重建"教师隐藏分布"，**直面不完整覆盖的现实**，用代理 prompt + 显式处理两种失败模式。问题从"如何用完美 prompt 覆盖"变成"**如何在不完美覆盖下仍能恢复**"。
- **🔧 方法**:
  1. **CaMOPD (Counteraction-Aware MOPD)**：三个组件：
  2. **解耦交替训练** —— 通用恢复给专门更新，**周期性 review 领域 prompt 作 preservation**（避免梯度冲突同时保留领域能力）；
  3. **Gap-based 样本选择** —— 选**平均 token-level teacher-student log-prob gap 大**的样本，**集中纠错信号**；
  4. **梯度连贯性分析**（gradient coherence）支持 CaMOPD 产生**更连贯的纠错信号**。
- **📊 效果**: **角色扮演对话、医疗推理 QA** 场景，**通用恢复最佳且保持领域特化** —— 验证 CaMOPD 在不完整覆盖下能同时达成 recovery + preservation。
- **⚠️ 局限**: "解耦交替"的 schedule 需调；gap-based 选择的阈值需设；只验证了 role-play 和 medical 两个领域；不适用"通用教师数据完全不可得"的极端情况。
- **价值**: 把"**多教师 OPD 鲁棒性**"从"**假设完美 prompt 覆盖**"变成"**现实不完整覆盖**" —— 对实际部署（教师后训练数据通常不公开）是关键实用化进展。


