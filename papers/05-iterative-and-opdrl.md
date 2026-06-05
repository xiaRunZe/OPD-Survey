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

## 📅 2026-06 月新论文速览（增量附录）

> 完整中文解读见 [daily-updates/2026-06-05.md](../daily-updates/2026-06-05.md)。

### PGPO — Physics-Guided Policy Optimization with Self-Distillation

| 项目 | 内容 |
|------|------|
| **作者** | Ke Wang 等 |
| **时间** | 2026-06-02 |
| **arXiv** | [2606.03620](https://arxiv.org/abs/2606.03620) |
| **类别** | 🔁 SDPO 步长调度 |

**核心创新**：从粘性流体动力学获得灵感，在 SDE 层面形式化类比。引入"**信息调节步长乘子**"——来自学生预测与反馈条件教师之间的**互信息估计**。

**理论保证**：该调节保留 vanilla SGD 的一阶弱近似保证，每步开销可忽略。

**效果**：
- Science-QA 4 个 domain 中 3 个 +4.5 分
- **SDPO 后期崩溃的场景下保持稳定**

**局限**：互信息估计需额外前向；仅在 ScienceQA 验证。

---

#### 📄 [TRB: Trust-Region Behavior Blending for OPD](https://arxiv.org/abs/2605.31159)
- **arXiv**: [2605.31159](https://arxiv.org/abs/2605.31159)
- **🎯 动机**: OPD 学生早期 rollout 差，教师监督落在弱/低质量 prefix 上。
- **💡 方法**: TRB = warmup 方法 — 在 KL 信任域内用"最接近教师"的行为策略**替换**早期 rollout 策略，保留 per-prefix reverse-KL OPD loss。KL 预算退火到 0，warmup 后回到纯学生 rollout。
- **📊 数字**: 两个数学蒸馏设置中**平均最强**。


#### 📄 [LGR: Lookahead Group Reward (Combating Supervision Fidelity Decay)](https://arxiv.org/abs/2605.30833)
- **arXiv**: [2605.30833](https://arxiv.org/abs/2605.30833)
- **🎯 动机**: **SFD（监督保真度衰减）** — 学生前缀越长，教师 next-token 分布越不 confident/discriminative → reverse-KL 纠正信号越弱。
- **💡 方法**: Lookahead Group Reward — 用教师在**下一步**的 confidence 评估学生 top-K 候选 token，给 group-normalized 奖励。配合熵触发的 tree-attention 保效率。
- **📊 数字**: 6 个数学/代码 benchmark，**mean@8 比 OPD +2.57**；长生成 +4.92（**AIME-26, 39k tokens**）。


#### 📄 [ADWIN: Adaptive Windows for Horizon-Aware OPD](https://arxiv.org/abs/2605.28396)
- **arXiv**: [2605.28396](https://arxiv.org/abs/2605.28396)
- **🎯 动机**: 标准 full-rollout OPD 把每次更新绑到一次贵完成，且可能把监督过度分配到对当前学生**边际价值低**的后段。
- **💡 方法**: ADWIN = **自适应窗口框架** — rollout 长度是**在线可接受性决策**：短教师锚定 prefix 训练，延迟 full-rollout probe 审计 prefix-full 对齐。
- **📊 数字**: 数学/代码推理单任务/多任务/强对弱设置，**端到端训练成本最多 -4.1 倍**且精度相当或更好。


#### 📄 [CaMOPD: Counteraction-Aware Multi-Teacher OPD](https://arxiv.org/abs/2605.27115)
- **arXiv**: [2605.27115](https://arxiv.org/abs/2605.27115)
- **🎯 动机**: 领域特化常削弱通用能力。MOPD 恢复能力，但**假设教师对齐的 prompt 覆盖** — 开源通用教师后训练数据未知时这假设难满足。
- **💡 方法**: 用易得 proxy 通用 prompt。两个失败模式 — (1) recovery-preservation **counteraction**；(2) weak-signal flattening。CaMOPD = **解耦交替训练** + **gap-based 样本选择**。
- **📊 数字**: 角色扮演对话、医疗推理 QA — 通用恢复最佳且保持领域特化。


