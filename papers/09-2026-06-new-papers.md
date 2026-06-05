# 📅 2026-06 月新论文速读（43 篇）

> 自动拉取时间：2026-06-05 13:41 GMT+8
> 数据源：arXiv（2026-05-22 ~ 2026-06-05 提交）
> 解读格式：**动机 → 方法 → 关键数字/创新点**

---

## 🔬 白盒 OPD（5 篇）

### 1. FiRe-OPD: Filter, then Reweight — Rethinking Optimization Granularity
- **arXiv**: [2606.02684](https://arxiv.org/abs/2606.02684)
- **动机**: 传统 OPD 对所有 trajectory 和所有 token 一视同仁，但 rollout 质量参差，token 重要性也不均。
- **方法**: 两阶段细粒度优化 — 先**过滤**低质量 trajectory，再对保留的 trajectory 内 token **软重加权**，突出高信息量 token。
- **关键**: 软加权 vs 硬选择（避免信息损失）+ 强对弱/单/多教师三场景验证。**AIME 2024 +6.25**，**Miner +18.81**。

### 2. SafeSteer: Localized On-Policy Distillation for Safety Alignment
- **arXiv**: [2606.02530](https://arxiv.org/abs/2606.02530)
- **动机**: 安全对齐普遍损害通用能力（"对齐税"），主流方案依赖大规模通用数据+奖励模型做平衡。
- **方法**: 提出"安全特征在输出分布中天然稀疏"，所以要**局部 OPD** 而非全局 trade-off。SafeSteer 只在稀疏安全 token 位置进行 OPD。
- **创新**: 避开 alignment tax 的关键 — 不是平衡双目标，而是**只动该动的位置**。

### 3. TS-OPSD: Internalize the Temperature as Policy Reheater
- **arXiv**: [2606.00755](https://arxiv.org/abs/2606.00755)
- **动机**: RL 训练中模型熵会崩溃（policy 越来越集中），传统补救（熵正则 / 调采样温度）都是**外部干预**，不写入参数。
- **方法**: 把高温度采样得到的"平滑分布"作为 self-teacher，**蒸馏回学生** → 温度的探索性被"内化"到参数里。
- **结果**: Qwen3-4B/8B-Base 上比标准 RL 和 rollout-level 温度修复都更强初始化。零外部教师、零特权数据、零额外推理成本。

### 4. StepOPSD: Step-Aware Online Preference Distillation for Agent RL
- **arXiv**: [2605.27140](https://arxiv.org/abs/2605.27140)
- **动机**: 多轮 Agent RL 奖励稀疏且在 trajectory 级，但成功往往取决于**几个关键的局部决策**。
- **方法**: 把 trajectory 切分为**以 step（action）为中心的段**，用 hindsight-enriched teacher 上下文重打分，转成**符号保持**的 advantage shaping + 归一化 step 信用预算。
- **结果**: ALFWorld Heat 79.1%、PickTwo 95.0%、TriviaQA 61.6%。发现"两旋钮定律"：小 α_clip 稳，大 λ_mix 视任务而定。

### 5. EchoDistill: Noisy-to-Clean Self-Distillation for Robust Audio LLMs
- **arXiv**: [2605.23954](https://arxiv.org/abs/2605.23954)
- **动机**: 音频 LLM 遇噪声就语义漂移，主流方案（波形增强 / 答案级监督 / 内部抑制）各有缺陷。
- **方法**: **对齐式 noisy-to-clean 自蒸馏** — 用干净输入的自身输出作为 teacher，去教噪声输入的输出对齐。
- **创新点**: 把"对齐"和"去噪"结合，是音频 LLM 鲁棒性的新范式。

---

## ♻️ OPSD + RL 混合（2 篇）

### 6. SDPG: Self-Distilled Policy Gradient
- **arXiv**: [2606.04036](https://arxiv.org/abs/2606.04036)
- **动机**: OPSD 是稀疏奖励 RL 的密集监督源，但怎么和现有 RL（GRPO 等）干净地结合？
- **方法**: SDPG = GRPO verifier advantages（带归一化标准差） + **全词表 OPSD reverse-KL** + reference-policy KL 正则。三个 loss 统一目标。
- **结果**: 比 RLVR 和自蒸馏基线都更稳定。

### 7. CAST: Non-Privileged Clipped Asymmetric Self-Teaching
- **arXiv**: [2606.00172](https://arxiv.org/abs/2606.00172)
- **动机**: GRPO 给的是稀疏 outcome reward，全对/全错组优势为零 → 浪费；OPSD 的 token 偏好不一定对齐 trajectory 正确性。
- **方法**: CAST 是**无答案自教学**：用 stop-gradient self-teacher 沿 trajectory 正确性塑形 token 优势。关键创新是**双向局部 advantage 翻转** — 正确 trajectory 中 teacher-negative token 拿负优势，错误 trajectory 中 teacher-positive token 拿正优势。全对/全错组也分配有界符号约束的优势。
- **结果**: 数学推理上比 RLVR 更优，保留轻量级 verifier-grounded 目标。

---

## 🖼️ 多模态 / 视觉 / 音频（5 篇）

### 8. MGSD: Modality-Gap-Aware Self-Distillation for Visual Spatial Planning
- **arXiv**: [2606.06076](https://arxiv.org/abs/2606.06076)
- **动机**: 视觉-语言模型在视觉空间规划上弱，因为有"感知-推理 modality gap" — 视觉规划要从像素推断隐状态再推理，而符号规划直接用显式对象。
- **方法**: MGSD 是个**两阶段 modality-gap-aware 自蒸馏**框架。
- **状态**: abstract 截断，方法细节待全文。

### 9. ViCuR: Visual Cues as Recoverable Privilege for Multimodal OPD
- **arXiv**: [2606.05718](https://arxiv.org/abs/2606.05718)
- **动机**: 多模态 OPD 常用"特权教师"看参考答案/解释，但造成**训练-测试失配** — 教师监督依赖学生不可见的信号，鼓励"快捷模仿"而非视觉 grounded 推理。
- **方法**: ViCuR 把"答案侧特权"换成"视觉线索"（来自同一视觉输入的查询相关证据，**可恢复**）。轻量级 cue recovery 模块用 sink-token 跨 attention 在 prefill 时聚合。
- **结果**: Qwen3-VL-2B/8B 上 7 个 benchmark，**比答案侧 OPSD +1.19/+1.24**。强教师 OPD 比基线再 +0.64/+1.08。

### 10. VGS: Decomposed OPD for Vision-Language Reasoning
- **arXiv**: [2606.00564](https://arxiv.org/abs/2606.00564)
- **动机**: 多模态 OPD 的优化动态**没研究透** — 标准 monolithic 视角掩盖了语言先验和视觉 grounding 的独立目标。
- **方法**: 数学分解损失为"语言先验"和"视觉 grounding"两部分，发现**梯度向量近乎正交** → 标准优化走的是次优妥协轨迹。VGS（Visual Gradient Steering）动态重定向更新向量**优先视觉子空间**。
- **结果**: 多个多模态 benchmark 上视觉 grounding 显著优 + 训练开销极小。

### 11. FA-OPD: Adversarial Dual On-Policy Distillation for Embodied Control
- **arXiv**: [2605.27095](https://arxiv.org/abs/2605.27095)
- **动机**: 行为克隆 + 扩散/流匹配策略仍然是**离线监督学习** — 策略只在专家状态训练，对实际访问的状态没纠正信号。标准 OPD 假设固定强教师，但 demonstration-only 控制中**没有强教师**。
- **方法**: FA-OPD 是**对抗式双 OPD** — Flow Matching 教师从演示学习，与 MLP 学生共同训练。教师提供两个信号：(1) **奖励通道**学专家相似度，驱动长程探索；(2) **动作通道**给学生访问状态提供密集局部目标。
- **结果**: 6 个机器人 navigation/manipulation/locomotion benchmark 都超基线，**对噪声/有限演示鲁棒性显著**。

### 12. CollectionLoRA: 50 Effects in 1 LoRA via Multi-Teacher OPD
- **arXiv**: [2605.25378](https://arxiv.org/abs/2605.25378)
- **动机**: 定制图像编辑要给扩散模型加多个视觉效果，每个效果存一个 LoRA → 部署成本暴涨。和加速模块级联还有参数干扰（概念串色/风格退化）。
- **方法**: CollectionLoRA 用**多教师 OPD** 把 50 个效果塞进 1 个 LoRA。
- **状态**: abstract 截断，方法细节待全文。

---

## 🤖 Agent / 机器人 / 工具（6 篇）

### 13. 分布式 DAgger: RL from Rich Feedback
- **arXiv**: [2606.05152](https://arxiv.org/abs/2606.05152)
- **动机**: RLVR 太窄 — 用一个 bit 标答案对错。但很多场景有**丰富反馈**：执行 trace、工具输出、专家纠错、自评估。
- **方法**: 经典 DAgger 的**分布变体** — learner 在当前策略访问的状态上**局部访问专家分布**。
- **洞察**: DAgger 框架被重新激活 — 不只用于模仿学习，也可作为"丰富反馈 RL"通用方法。

### 14. PGPO: Physics-Guided Policy Optimization with Self-Distillation
- **arXiv**: [2606.03620](https://arxiv.org/abs/2606.03620)
- **动机**: SDPO（自蒸馏策略优化）很敏感 — 同一更新步在不同 batch 上教师纠错可信息丰富也可误导。固定步长一刀切会让训练不稳。
- **方法**: PGPO 从**粘性流体力学**找灵感，在 SDE 层面形式化类比，引入**信息调制步长乘子**（基于学生预测和反馈条件教师之间的互信息估计）。
- **结果**: Science-QA 上 4 个域 3 个超 SDPO，**最高 +4.5**；在 SDPO 后期崩溃的场景保持稳定。

### 15. TOPD: Trajectory-aware OPD via Near-Future Guidance
- **arXiv**: [2606.00305](https://arxiv.org/abs/2606.00305)
- **动机**: OPD 学习信号是 token-level 的（高 loss token + 局部 reverse-KL 修复），但推理失败常是**短程分布漂移** — 孤立 token 级监督修不好。
- **方法**: TOPD 用**近未来 trajectory 信息**识别真正发散的状态，把指导分布到多个未来 token 上。
- **结果**: 屏蔽非发散高 loss token → 标准 OPD 47.8%→48.2%；TOPD 再 → 52.2%。**AIME24 60%→63.3%**，**AIME25 46.7%→53.3%**。

### 16. GAPD: Gold-Action Policy Distillation for KBQA
- **arXiv**: [2605.29584](https://arxiv.org/abs/2605.29584)
- **动机**: 知识库问答（KBQA）的 RL 只优化稀疏的最终答案奖励，中间 action 错误弱监督。gold logical forms 可转 action 序列，但现有 pipeline 只用于 warm-start 构造。
- **方法**: GAPD 把 gold action 序列做成**在线 policy 蒸馏的教师信号**。
- **创新点**: gold logical form 不只是数据增强，更是**在线 PD 教师**。

### 17. GDSD: Reinforcement Learning as Guided Denoiser Self-Distillation
- **arXiv**: [2605.29398](https://arxiv.org/abs/2605.29398)
- **动机**: 扩散 LLM（dLLM）的 RL 受困于**似然不可处理**。主流方案用 ELBO（随机 mask 序列估计）作似然代理 → 训练-推理失配，性能退化。
- **方法**: GDSD 直接**自蒸馏 denoiser** — 教师是 reverse-KL 正则 RL 闭式最优解导出的 advantage-guided self-teacher，**匹配 dLLM denoiser logits**，无归一化目标。
- **结果**: LLaDA-8B、Dream-7B 上**比 SOTA ELBO 方法最多 +19.6%**。揭示 ELBO-based 方法都是不同蒸馏散度的特例。

### 18. EDGE-OPD: Internalizing Privileged Context with Evidence Guidance
- **arXiv**: [2605.23493](https://arxiv.org/abs/2605.23493)
- **动机**: OPSD 中特权信息（persona/私密事实/解题过程）**会改模型行为到超出预期** — 改推理、降低通用能力、改响应长度/风格/token 偏好。学生可能学到副作用而非期望行为。
- **方法**: EDGE-OPD 两个特征：(1) **guided rollouts** 让学生在采样时就注入特权上下文行为；(2) **evidence mask** — 只在特权上下文**支持**采样 token 的位置更新学生。
- **结果**: 在 rare-token/identity 设置，OPSD/RLSD（有/无 verifier）**完全失败**学不到目标 identity；EDGE-OPD 成功。mask 区域实验显示 persona 信号**集中在正证据尾部**。

---

## 📌 其他 OPD / 自蒸馏（25 篇）

### 19. CGTR: Consolidation-Gated Teacher Refresh（OPSD 调度）
- **arXiv**: [2606.03532](https://arxiv.org/abs/2606.03532)
- **动机**: Self OPD 用学生自己参数历史当教师，但**教师更新调度**（时间耦合）作为稳定性变量从没系统研究过。
- **方法**: 在 Qwen3-8B 上 schedule 扫描 → 发现**"隔离期"**（教师完全冻结）才是稳定学习的关键，不是教师年龄。提"state-oblivious collapse"诊断（时钟驱动 refresh 把瞬时漂移的学生拷给教师）。CGTR = 保留隔离期 + **联合门控**（奖励改进 + 长度尾安全）。
- **结果**: 单参数集跨 4 任务（化学/生物/物理/工具用）**零崩溃 + 全部最佳**。

### 20. OmniOPD: Logit-Free OPD via Speculative Verification
- **arXiv**: [2606.01476](https://arxiv.org/abs/2606.01476)
- **动机**: 标准 OPD 两个耦合限制 — (1) 要教师 token-level logits（专有模型做不了教师）；(2) token 信号脆，依赖师生候选 token 重叠，会放大重复 loop。
- **方法**: OmniOPD 用 **chunk-level 监督** — Monte Carlo rollout 在多 token chunk 上用连续语义相似度近似教师偏好；**peak-entropy scheduler** 只在学生高不确定推理分支审计；Dirichlet-Multinomial 贝叶斯先验 + base-model KL anchor。
- **结果**: 数学 **+28.64%**；配 Claude-4.5-Haiku / Gemini-2.5-Flash 黑盒教师再 +9.54%。

### 21. TrOPD: Trust Region On-Policy Distillation
- **arXiv**: [2606.01249](https://arxiv.org/abs/2606.01249)
- **动机**: 师生分布差异大时 OPD 不稳定 — 教师对学生的 token 监督产生不可靠策略梯度，甚至优化失败。
- **方法**: TrOPD 三个组件：(1) **Trust-Region On-Policy Learning** — 只在教师监督可靠的区域做 OPD；(2) **Outlier Estimation** — 离群区域用梯度裁剪/mask/forward-KL；(3) **Off-Policy Guidance** — 学生从教师 prefix 续写，用 forward KL 鼓励探索向可靠区域。
- **结果**: 数学推理、代码、通用 benchmark 一致超 OPD/EOPD/REOPOLD。

### 22. OPD+: Rethinking the Advantage Design
- **arXiv**: [2606.01039](https://arxiv.org/abs/2606.01039)
- **动机**: 现有 OPD 用 stop-gradient 设计（为稳定），但**这种 advantage 估计是可疑的**。
- **方法**: 通用 f-散度优化框架，**数学证明** stop-gradient 对一般散度函数导致**有偏**奖励目标和梯度估计。OPD+ = OPD 的修正版，支持各种 f-散度。
- **结果**: 数学推理、工具调用 benchmark 上比 baseline KL 更优。

### 23. POPD / Truncated OPD: Rollout Horizon 是不是必需？
- **arXiv**: [2605.31490](https://arxiv.org/abs/2605.31490)
- **动机**: 标准 OPD 生成完整 rollout，**计算贵**且早期训练时后段教师反馈不可靠。
- **方法**: rollout horizon 是关键瓶颈。两个简单策略 — **POPD** 渐进扩展；**Truncated OPD** 永久用截断。
- **结果**: POPD 训练效率 **+3 倍**；Truncated OPD **只用 10% rollout 长度**就匹配 OPD 性能。

### 24. TRB: Trust-Region Behavior Blending
- **arXiv**: [2605.31159](https://arxiv.org/abs/2605.31159)
- **动机**: OPD 学生早期 rollout 差，教师监督落在弱/低质量 prefix 上。
- **方法**: TRB = warmup 方法 — 在 KL 信任域内用"最接近教师"的行为策略**替换**早期 rollout 策略，保留 per-prefix reverse-KL OPD loss。KL 预算退火到 0，warmup 后回到纯学生 rollout。
- **结果**: 两个数学蒸馏设置中**平均最强**。

### 25. LGR: Lookahead Group Reward
- **arXiv**: [2605.30833](https://arxiv.org/abs/2605.30833)
- **动机**: **SFD（监督保真度衰减）** — 学生前缀越长，教师 next-token 分布越不 confident/discriminative → reverse-KL 纠正信号越弱。
- **方法**: Lookahead Group Reward — 用教师在**下一步**的 confidence 评估学生 top-K 候选 token，给 group-normalized 奖励。配合熵触发的 tree-attention 保效率。
- **结果**: 6 个数学/代码 benchmark，**mean@8 比 OPD +2.57**；长生成 +4.92（AIME-26, 39k tokens）。

### 26. Canonical-Context OPD for Multi-Turn LLMs
- **arXiv**: [2605.30251](https://arxiv.org/abs/2605.30251)
- **动机**: 多轮对话中**同一完整证据**渐进揭示，模型却会答不同（"lost-in-conversation gap"）。原因 — **self-anchored drift**：部分信息下的回复引入未支撑假设，假设又扭曲最终答案。
- **方法**: Canonical-Context OPD — 用 clean FULL prompt 和 RAW-SHARDED 对话训练对齐。
- **状态**: abstract 截断，方法细节待全文。

### 27. A Predictive Law for OPSD from World Feedback
- **arXiv**: [2605.30070](https://arxiv.org/abs/2605.30070)
- **动机**: OPSD 用任意反馈作学习信号，但相对 GRPO 等成熟方法的可靠性**不清楚**。
- **方法**: 发现**惊人的线性相关** — 初始学生-自教师性能 gap vs 最终性能提升，在上下文类型和模型族上**一致**。这是个预测定律。
- **意义**: 跑 OPSD 前能**预测结果**。模型规模放大也保持 → 可能成为新**经验 scaling law**。

### 28. Draft-OPD: OPD for Speculative Draft Models
- **arXiv**: [2605.29343](https://arxiv.org/abs/2605.29343)
- **动机**: 推测解码用 SFT 训练 draft 模型（EAGLE3 / DFlash）很快 plateau — SFT 学的是 target-generated 固定轨迹，推理时被 draft 自己提出 block 评估 → offline-inference 失配。
- **方法**: Draft-OPD — 用 OPD 训练 draft 模型。
- **洞察**: 推测解码草稿模型是 OPD 的新战场。

### 29. OISD: On-Policy Internal Self-Distillation
- **arXiv**: [2605.29089](https://arxiv.org/abs/2605.29089)
- **动机**: 现有 RL 后训练主要优化最终输出策略的**稀疏 outcome reward**，几乎忽略**中间表征**中的预测信号。
- **方法**: OISD = 新范式 — 在 rollout 和 GRPO 优化中，**最终层同时作 policy 和 detached 内部教师**，向选定的**中间层**传输：(1) **logit 对齐**（怎么想）；(2) **attention 对齐**（看哪里）。两个都不需外部特权信息。
- **结果**: 4 个数学推理任务上一致超强 reasoning RL 基线。

### 30. SGSD: Skill-Conditioned Gated Self-Distillation
- **arXiv**: [2605.28791](https://arxiv.org/abs/2605.28791)
- **动机**: OPSD 用"特权信息"（参考答案/成功轨迹）作教师信号，假设 PI 信任。但 PI 能否来自**经验派生的技能库**（检索出的技能紧凑可复用但可能不相关/误导）？
- **方法**: SGSD 把基于技能的自蒸馏公式化为**教师假设验证** — 检索技能-错误对，构造多教师池，让所有技能条件教师对同一 plain-prompt 学生 rollout 评分。verifier 验证每个教师极性，鲁棒门控目标蒸馏有信息师生分歧、抑制不确定/极端信号。
- **结果**: Qwen3-1.7B 上 **AIME24/25/HMMT25 平均比 GRPO +6.2%**，**比 OPSD +1.7%**。

### 31. ADWIN: Adaptive Windows for Horizon-Aware OPD
- **arXiv**: [2605.28396](https://arxiv.org/abs/2605.28396)
- **动机**: 标准 full-rollout OPD 把每次更新绑到一次贵完成，且可能把监督过度分配到对当前学生**边际价值低**的后段。
- **方法**: 引入"有用监督 horizon"概念。ADWIN = **自适应窗口框架** — rollout 长度是**在线可接受性决策**：短教师锚定 prefix 训练，延迟 full-rollout probe 审计 prefix-full 对齐，staleness 控制下适应下一 horizon。
- **结果**: 数学/代码推理单任务/多任务/强对弱设置，**端到端训练成本最多 -4.1 倍**且精度相当或更好。

### 32. CODE: Causal On-Policy Self-Distillation Editing
- **arXiv**: [2605.28303](https://arxiv.org/abs/2605.28303)
- **动机**: 知识编辑（KE）的 Static Fact Overwriting 把 LLM 当离散数据库，强注孤立事实 → **Epistemic Dissonance**（未进化的旧先验强迫模型显式否定注入更新）。零失真代理下 95.6% self-refutation。
- **方法**: 把更新基础从孤立事实改为**显式因果叙事** → 冲突率降至 6.6%。CODE (Causal On-policy self-Distillation Editing) 内化这种进化。
- **洞察**: 知识编辑从"事实覆盖"转向"知识进化"是范式转变。

### 33. 数据高效 OPD for ASR
- **arXiv**: [2605.28139](https://arxiv.org/abs/2605.28139)
- **动机**: 强 ASR 要大规模音频监督，复现和特化贵。
- **方法**: Ark-ASR（0.6B 参数音频条件 LM，100k 小时语音训练） + 研究强 Qwen-ASR 教师能否通过 OPD 转移识别能力。
- **状态**: abstract 截断，结果待全文。

### 34. ROSD: Reflective On-Policy Self-Distillation
- **arXiv**: [2605.28014](https://arxiv.org/abs/2605.28014)
- **动机**: OPSD 域内增益有限、域外泛化差。两原因 — (1) self-teacher 条件在已验证解上鼓励**模仿训练域参考轨迹**而非错误特定纠正；(2) 在完整 response 上蒸馏**覆盖有效推理 prefix** + 强化过拟合。
- **方法**: ROSD 把参考解模仿转为**针对性推理纠正**。self-reflector 提取**纠正想法** + 定位**首个错误 span**。纠正想法引导自教师做针对性监督，错误 span 限制蒸馏到需要纠正的地方。
- **结果**: 多个域内/域外推理 benchmark — 域内推理整体更强，**域外泛化显著优于标准 OPSD**。

### 35. SC-SDPO: Pass-Rate Weighted Self-Distillation
- **arXiv**: [2605.27765](https://arxiv.org/abs/2605.27765)
- **动机**: GRPO 的 group-relative advantage 自然聚焦在**中间难度"甜点"**。SDPO 的 KL-based advantage 缺乏难度感知。
- **方法**: 透过 GRPO 优势归一化分析，扩展 learnability 框架到归一化奖励 → 归一化吸收方差 p(1-p)，**首阶 learnability 在 question 间平等**，剩 √(p(1-p)) 作为 per-question 梯度标度。处方：按 **[p̂(1-p̂)]^(1/2)** 加权每个 question 的 SDPO loss → SC-SDPO。
- **结果**: Qwen3-8B **+3.2/+4.3**（mean@16/maj@16），OLMo-3-7B **+1.8/+3.0**。权重零成本从 batch 自适应归一化 rollout 拿。

### 36. MAIGO: History-Cleaned OPSD for Multi-Turn
- **arXiv**: [2605.27186](https://arxiv.org/abs/2605.27186)
- **动机**: LLM 完整 prompt 能解，多轮展开则退化（lost-in-conversation gap）。原因 — **self-contamination**（中间助手回复进后续上下文，把早期偏差带下去）。
- **方法**: MAIGO = **on-policy 自蒸馏 + 历史清洗**。
- **状态**: abstract 截断，方法细节待全文。

### 37. CaMOPD: Counteraction-Aware Multi-Teacher OPD
- **arXiv**: [2605.27115](https://arxiv.org/abs/2605.27115)
- **动机**: 领域特化常削弱通用能力。MOPD（多教师 OPD）恢复能力，但**假设教师对齐的 prompt 覆盖**（prompt 要匹配教师训练分布）— 开源通用教师后训练数据未知时这假设难满足。
- **方法**: CaMOPD 用易得 proxy 通用 prompt。两个失败模式 — (1) recovery-preservation **counteraction**（混合冲突梯度）；(2) weak-signal flattening（均匀平均不等需求样本）。CaMOPD = **解耦交替训练** + **gap-based 样本选择**。
- **结果**: 角色扮演对话、医疗推理 QA — 通用恢复最佳且保持领域特化。

### 38. ESR: Early Stopping Rollout
- **arXiv**: [2605.27028](https://arxiv.org/abs/2605.27028)
- **动机**: 后续 token 时，学生早期轨迹作上下文（off-policy 相对教师），**教师纠错能力衰减**，可能回退到预训练阶段的 token-completion 行为。**Off-policy Teacher Decay**。
- **方法**: ESR 简单有效 — **限制 rollout 生成到 response 前几个 token**。发现 ESR 全胜过 full rollout OPD，**GPU 效率和训练稳定性更高**（特别跨模型族）。**Cascading Alignment** 和 **Sub-mode Commitment** 效应解释为何有时超教师。
- **反直觉**: KL 散度和熵信号**无法完全解释**这种位置选择。

### 39. TA-OPD: Teachability-Aware OPD
- **arXiv**: [2605.26844](https://arxiv.org/abs/2605.26844)
- **动机**: 选择性 OPD 优先高熵/高分歧 token — 但 raw KL 分歧是**学习价值的粗糙代理**，混淆"可学分歧"（教师给学生 top-K 候选分配纠错 mass）和"不兼容分歧"（教师把 mass 放在学生当前 support 外）。
- **方法**: 把局部兼容性形式化为 **token teachability**。TA-OPD = 轻量级 token 位置选择，把 OPD loss 应用到高 teachability 位置，无奖励模型/verifier。
- **结果**: Qwen2.5/Qwen3 设置上，**5% 保留 token 常超全 token OPD**。

### 40. ERPD: Extreme Region Policy Distillation
- **arXiv**: [2605.25582](https://arxiv.org/abs/2605.25582)
- **动机**: 严格 on-policy 方法单次更新后丢弃轨迹，off-policy 复用有分布失配。aggressive 多步优化 → 快速初增益 + 后期 trajectory 概率偏离 + 熵崩溃 + 性能早 plateau。紧 KL 约束只降天花板。
- **方法**: ERPD 两阶段 — (1) 弱约束 off-policy 优化在固定数据上**最大提取**训练信号；(2) 在信任域约束下**蒸馏**这些信号到基础策略。
- **关键**: 强基础模型和弱教师都受益（即使 aggressive 优化没产生更强策略，degenerate 教师也能用替代信号构造策略）。

### 41. State Distribution View: Post-Training is About States
- **arXiv**: [2605.22731](https://arxiv.org/abs/2605.22731)
- **动机**: SFT/RL/蒸馏常通过损失函数（MLE / PG / forward KL / reverse KL / 相关目标变体）分析。**互补因素** — 监督应用的**状态分布** — 少有人研究。
- **方法**: post-training = state-distribution shaping。Qwen3-0.6B-Base + GSM8K 控制实验。三现象：(1) 温和 SFT 提 GSM8K 少遗忘，stress SFT 大幅保留损失；(2) 退化 SFT 教师的 OPD 在 GSM8K/TruthfulQA/MMLU 上**反超**教师；(3) 轻量级 on-policy RL 提 GSM8K 保留。
- **结论**: 训练状态的**源和局部性**和监督信号**形式**同等重要。

### 42. SPD: Self-Policy Distillation via Capability-Selective Subspace Projection
- **arXiv**: [2605.22675](https://arxiv.org/abs/2605.22675)
- **动机**: 自蒸馏要么靠外部信号策展自生成输出（贵、前沿模型不可用），要么跳过策展全训（领域特化、难泛化）。更深弱点 — 自生成输出把**任务相关能力**和**风格/格式/模型特定错误**纠缠，稀释信号。
- **方法**: SPD = **能力选择性自蒸馏无需外部信号**。从模型自己在正确性定义 token 上的梯度**提取低秩能力子空间**，自生成时把 KV activation 投到这个子空间，用标准 next-token 预测 loss 微调 raw 输出。
- **结果**: 代码/数学/MCQ QA 上比 SOTA 自蒸馏**最多 +13%**，比预训练基线 +16%。**OOD 泛化 +15%**。

### 43. Interpretable Policy Distillation for Power Grid
- **arXiv**: [2606.00561](https://arxiv.org/abs/2606.00561)
- **动机**: 深度 RL 用于电网实时运行，但大神经网络策略评估贵、难部署、对运维人员不透明。
- **方法**: 把 PPO 教师（Grid2Op 14-bus 环境、稳定导向奖励、stress-focused 数据采集）蒸馏到**决策树和随机森林**。两者在保留 episode 上超教师奖励+生存长度。决策树和 PPO argmax 高精确动作一致，top-ranked 内近完全一致。
- **洞察**: PPO 依赖线路负载信号，蒸馏树主要由母线拓扑变量驱动。压力聚焦蒸馏把黑盒神经控制器转轻量、可审计的规则状代理。

---

## 📊 速读统计

| 类别 | 篇数 | 主要方向 |
|------|------|---------|
| 🔬 白盒 OPD | 5 | 细粒度（filter+reweight / step-aware / 温度内化）|
| ♻️ OPSD+RL | 2 | 自教学 + GRPO、密集信号结合 |
| 🖼️ 多模态 | 5 | 视觉 grounded OPD、机器人、LoRA 合并 |
| 🤖 Agent | 6 | KBQA、dLLM、embodied、电网 |
| 📌 其他 | 25 | 调度 / logit-free / trust region / OPSD 理论 / 数据高效 |

## 🔥 Top 5 最值得深读

1. **2605.30070** OPSD 预测定律 — **跑前能预测结果**，可能成新 scaling law
2. **2606.01476** OmniOPD — **chunk-level logit-free**，让专有模型做教师
3. **2605.27028** ESR 早停 rollout — 简单到反直觉，**+GPU 效率**
4. **2606.02684** FiRe-OPD — 软加权 vs 硬选择，**AIME +6.25 / Miner +18.81**
5. **2605.22675** SPD 子空间投影 — **OOD 泛化 +15%**，自蒸馏新范式
