# 📚 arXiv 新论文（自动拉取）

> 拉取时间：2026-06-08 22:40 GMT+8


**共 19 篇**

| # | arXiv | 标题 | 类别 | 匹配关键词 |
|---|-------|------|------|-----------|
| 1 | [2606.07082](https://arxiv.org/abs/2606.07082) | On the Geometry of On-Policy Distillation | 📌 其他 | on-policy distillation |
| 2 | [2606.06712](https://arxiv.org/abs/2606.06712) | Data-Efficient Autoregressive-to-Diffusion Language Models via On-Policy Distill… | 🖼️ 多模态 | on-policy distillation |
| 3 | [2606.06076](https://arxiv.org/abs/2606.06076) | Learning Visual Spatial Planning from Symbolic State via Modality-Gap-Aware Self… | 🖼️ 多模态 | self-distillation |
| 4 | [2606.05718](https://arxiv.org/abs/2606.05718) | ViCuR: Visual Cues as Recoverable Privilege for Multimodal On-Policy Distillatio… | 🖼️ 多模态 | on-policy distillation |
| 5 | [2606.05152](https://arxiv.org/abs/2606.05152) | Reinforcement Learning from Rich Feedback with Distributional DAgger | 🤖 Agent | DAgger |
| 6 | [2606.04036](https://arxiv.org/abs/2606.04036) | Self-Distilled Policy Gradient | ♻️ OPSD+RL | self-distilled policy |
| 7 | [2606.03620](https://arxiv.org/abs/2606.03620) | Physics-Guided Policy Optimization with Self-Distillation | 🤖 Agent | self-distillation |
| 8 | [2606.03532](https://arxiv.org/abs/2606.03532) | When Should the Teacher Move? Temporal Coupling and Stability in Self On-Policy … | ♻️ OPSD | on-policy distillation |
| 9 | [2606.02684](https://arxiv.org/abs/2606.02684) | Filter, Then Reweight: Rethinking Optimization Granularity in On-Policy Distilla… | 🔬 白盒OPD | on-policy distillation |
| 10 | [2606.02530](https://arxiv.org/abs/2606.02530) | SafeSteer: Localized On-Policy Distillation for Efficient Safety Alignment | 🔬 白盒OPD | on-policy distillation |
| 11 | [2606.01476](https://arxiv.org/abs/2606.01476) | OmniOPD: Logit-Free On-Policy Distillation via Speculative Verification | 📌 其他 | on-policy distillation |
| 12 | [2606.01249](https://arxiv.org/abs/2606.01249) | Trust Region On-Policy Distillation | 📌 其他 | on-policy distillation |
| 13 | [2606.01039](https://arxiv.org/abs/2606.01039) | OPD+: Rethinking the Advantage Design for On-Policy Distillation | 📌 其他 | on-policy distillation |
| 14 | [2606.00755](https://arxiv.org/abs/2606.00755) | Internalize the Temperature: On-Policy Self-Distillation as Policy Reheater for … | 🔬 白盒OPD | on-policy self-distillation |
| 15 | [2606.00564](https://arxiv.org/abs/2606.00564) | Decomposed On-Policy Distillation for Vision-Language Reasoning: Steering Gradie… | 🖼️ 多模态 | on-policy distillation |
| 16 | [2606.00561](https://arxiv.org/abs/2606.00561) | Interpretable Policy Distillation for Power Grid Topology Control | 📌 其他 | policy distillation |
| 17 | [2606.00305](https://arxiv.org/abs/2606.00305) | Bridging Reasoning Trajectories in On-Policy Distillation via Near-Future Guidan… | 🤖 Agent | on-policy distillation |
| 18 | [2606.00172](https://arxiv.org/abs/2606.00172) | CAST: Non-Privileged Clipped Asymmetric Self-Teaching with Advantage Flipping fo… | ♻️ OPSD+RL | self-teaching |
| 19 | [2605.31490](https://arxiv.org/abs/2605.31490) | Are Full Rollouts Necessary for On-Policy Distillation? | 📌 其他 | on-policy distillation |

---

## On the Geometry of On-Policy Distillation

- **arXiv**: [2606.07082](https://arxiv.org/abs/2606.07082)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-policy distillation (OPD) is increasingly used to improve large language model reasoning, but its training dynamics remain poorly understood. We characterize the trajectory of OPD updates in parameter space and compare it with supervised fine-tuning (SFT) and reinforcement learning with verifiable rewards (RLVR). A suite of parameter-space diagnostics consistently places OPD in a relaxed off-principal regime: compared with SFT, its updates affect fewer weights and avoid principal directions more strongly, while compared with RLVR, they remain less tightly constrained. Beyond this static localization, OPD exhibits subspace locking: its cumulative updates rapidly enter a narrow low-dimensional channel. Constraining training to the update subspace formed early in training preserves OPD performance but substantially degrades SFT, indicating that the locked subspace is functionally sufficient for OPD. Control experiments further show that sparsifying the update tokens and shifting rollout generation off-policy preserve the rank dynamics, whereas mixing the OPD objective with RLVR changes them. Overall, these results suggest that OPD is not merely an intermediate point between SFT and RLVR, but induces its own update geometry in parameter space.

## Data-Efficient Autoregressive-to-Diffusion Language Models via On-Policy Distillation

- **arXiv**: [2606.06712](https://arxiv.org/abs/2606.06712)
- **类别**: 🖼️ 多模态（扩散模型 / 视觉）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
We study the transformation of autoregressive models (ARLMs) into diffusion language models (DLMs). Rather than pretraining from scratch, prior work replaces the causal attention in ARLMs with bidirectional attention and then trains the resulting model using a DLM objective. However, these approaches incur two distribution shifts. First, transitioning from a next-token prediction objective to a DLM objective can discard knowledge acquired by the ARLM during training. Second, standard DLMs suffer from a train-inference mismatch, as the training loss is defined on randomly masked sequences rather than the trajectories encountered at inference produced by confidence-based decoding. To address both challenges, we introduce an On-

## Learning Visual Spatial Planning from Symbolic State via Modality-Gap-Aware Self-Distillation

- **arXiv**: [2606.06076](https://arxiv.org/abs/2606.06076)
- **类别**: 🖼️ 多模态（多模态 OPD）
- **匹配关键词**: self-distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
While vision-language models excel at general multimodal understanding, they still struggle with visual spatial planning. We attribute this to a perception-reasoning modality gap: visual planning requires models to infer latent state structures from pixels and then reason over the recovered structure to produce valid actions, whereas symbolic planning directly leverages explicit objects and constraints. This creates dual bottlenecks in visual state recovery and multi-step planning. To address this, we propose MGSD, a two-stage modality-gap-aware self-

## ViCuR: Visual Cues as Recoverable Privilege for Multimodal On-Policy Distillation

- **arXiv**: [2606.05718](https://arxiv.org/abs/2606.05718)
- **类别**: 🖼️ 多模态（多模态 OPD）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-policy distillation (OPD) improves reasoning by training a student on trajectories sampled from its own policy under supervision from a teacher. In multimodal reasoning, a common extension is to use a privileged teacher that observes training-time-only signals such as reference answers or rationales. However, such answer-side privilege creates a train-test mismatch: the teacher&#39;s supervision may depend on signals unavailable to the student, encouraging shortcut imitation rather than visually grounded reasoning. We propose ViCuR, a visually grounded privileged-teacher distillation framework that replaces answer-side privilege with visual cues (query-related evidence in the input). Because these cues are derived from the same visual input available at inference, their evidence is recoverable by the student. To support this, ViCuR introduces a lightweight cue recovery module that uses dedicated sink-token cross-attention during prefill to aggregate task-relevant visual evidence into an internal representation, without changing the inference interface or requiring auxiliary cue-generation losses. Across seven benchmarks with Qwen3-VL-2B and 8B students, ViCuR consistently improves over answer-based on-policy self-distillation by +1.19 and +1.24 on overall average performance. It also extends naturally to stronger-teacher OPD, surpassing OPD baselines by +0.64 and +1.08, with consistent out-of-domain gains at the 8B scale. These results show that, in multimodal on-policy distillation, the design of teacher privilege is as important as teacher strength.

## Reinforcement Learning from Rich Feedback with Distributional DAgger

- **arXiv**: [2606.05152](https://arxiv.org/abs/2606.05152)
- **类别**: 🤖 Agent（Agent 应用）
- **匹配关键词**: DAgger
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Reasoning models have advanced rapidly, but the dominant reinforcement learning from verifiable rewards (RLVR) recipe remains surprisingly narrow: sample many responses and reward each with a single bit indicating whether the final answer is correct. Yet many settings provide rich feedback, including execution traces, tool outputs, expert corrections, and model self-evaluations. We study how to use such feedback through a distributional variant of the classic imitation learning algorithm DAgger, where the learner has local access to an expert distribution on states visited by the current

## Self-Distilled Policy Gradient

- **arXiv**: [2606.04036](https://arxiv.org/abs/2606.04036)
- **类别**: ♻️ OPSD+RL（OPSD + RL 混合）
- **匹配关键词**: self-distilled policy
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-policy self-distillation, where a language model conditions on privileged context to supervise its own generations, is a promising source of dense supervision for sparse-reward reinforcement learning. Actually, it can be instantiated as an auxiliary full-vocabulary student-to-teacher reverse Kullback-Leibler divergence loss. We therefore propose SDPG, a self-distilled policy-gradient framework that combines group-relative verifier advantages with normalized standard deviation, exact full-vocabulary on-policy self-distillation, as well as reference-policy KL regularization. Empirically, SDPG improves stability and performance over RLVR and self-distillation baselines. The code is available at this https URL.

## Physics-Guided Policy Optimization with Self-Distillation

- **arXiv**: [2606.03620](https://arxiv.org/abs/2606.03620)
- **类别**: 🤖 Agent（Agent 应用）
- **匹配关键词**: self-distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Self-distilled policy optimization (SDPO) has become a popular paradigm for LLM post-training, where a model learns from its own predictions conditioned on privileged information. SDPO, however, is sensitive to how much each update step should be trusted: corrections from a self-teacher can be highly informative on some batches and misleading on others, and applying them uniformly with a fixed step size can destabilize training. Drawing inspiration from viscous-fluid dynamics and formalizing the analogy at the SDE level, we propose Physics-Guided Policy Optimization (PGPO), which introduces an information-modulated step-size multiplier derived from a mutual-information estimate between the student&#39;s predictions and the feedback-conditioned teacher. We show that this modulation preserves the order-1 weak-approximation guarantees of vanilla SGD, and incurs negligible overhead per iteration. We evaluate PGPO on the Science-QA dataset, where it outperforms SDPO on 3 of the 4 domains with gains of up to +4.5 points, while remaining stable in a setting where SDPO collapses late in training.

## When Should the Teacher Move? Temporal Coupling and Stability in Self On-Policy Distillation

- **arXiv**: [2606.03532](https://arxiv.org/abs/2606.03532)
- **类别**: ♻️ OPSD（OPSD / 调度）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Self on-policy distillation trains a student policy against a teacher derived from its own parameter history, yet the teacher&#39;s update schedule -- which governs the \emph{temporal coupling} between teacher and student -- has not been systematically studied as a stability variable. Through a controlled schedule sweep on Qwen3-8B, we establish that \emph{isolation periods}, defined as complete teacher freezing between updates, are the key structural property enabling stable learning, not teacher age. To characterize these underlying training dynamics, we introduce a diagnostic framework of temporal KL structure, refresh shock, and length-tail risk. This framework further uncovers \emph{state-oblivious collapse}: optimal short-horizon fixed schedules catastrophically fail under long-horizon training because a clock-driven refresh can copy a transiently drifting student into the teacher in a single, irreversible step. This failure mode is invisible under short-horizon evaluation and mechanistically distinct from EMA&#39;s chronic contamination. To address this, we propose \emph{Consolidation-Gated Teacher Refresh} (CGTR), which preserves isolation periods while gating each refresh on joint evidence of reward improvement and length-tail safety, ensuring every teacher movement responds to genuine student consolidation rather than a clock signal. With a single shared parameter set and no per-dataset retuning, CGTR achieves \textbf{zero collapse} and the best final score on all four tasks (Chemistry, Biology, Physics, ToolUse), self-regulating its refresh frequency to each task&#39;s learning dynamics.

## Filter, Then Reweight: Rethinking Optimization Granularity in On-Policy Distillation

- **arXiv**: [2606.02684](https://arxiv.org/abs/2606.02684)
- **类别**: 🔬 白盒OPD（白盒 OPD / 细粒度）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-Policy distillation (OPD) in large language models is shifting from full-trace KL supervision toward more selective training paradigms. Recent OPD methods increasingly focus on selecting which trajectories to learn from, which tokens are most informative, and which supervision signals are most reliable. Motivated by this trend, we rethink optimization granularity of OPD and propose \fireicon\ FiRe-OPD (Filter, then Reweight), which jointly adjusts supervision signals at both trajectory and token levels. In details, FiRe-OPD first filters trajectories to remove low-quality rollout samples, and then applies soft reweighting within the retained trajectories to emphasize informative tokens. Compared with hard token selection, FiRe-OPD leverages a soft-weighting mechanism to effectively mitigate information loss and enhance optimization stability, thereby achieving finer-grained OPD optimization. We validate the effectiveness of FiRe-OPD across strong-to-weak, single-teacher, and multi-teacher settings, and demonstrate its superiority over recent token-level OPD methods ( (e.g., +6.25 on AIME 2024 in strong-to-weak, +18.81 on Miner in multi-teacher). Our code is available at this https URL.

## SafeSteer: Localized On-Policy Distillation for Efficient Safety Alignment

- **arXiv**: [2606.02530](https://arxiv.org/abs/2606.02530)
- **类别**: 🔬 白盒OPD（白盒 OPD / 安全性）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Aligning Large Language Models (LLMs) with human values often degrades their general capabilities, termed the alignment tax. Existing methods mitigate this by balancing dual objectives, which heavily rely on massive general-purpose data or auxiliary reward models. In this paper, we argue that, because safety features are inherently sparse within the output distribution, alignment requires localized modifications rather than global trade-offs. To this end, we propose SafeSteer, which performs on-

## OmniOPD: Logit-Free On-Policy Distillation via Speculative Verification

- **arXiv**: [2606.01476](https://arxiv.org/abs/2606.01476)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-Policy Distillation (OPD) trains a student model on its own generative trajectories under dense token-level feedback from a stronger teacher, mitigating both the off-policy distribution shift of Supervised Fine-Tuning (SFT) and the sparse credit assignment of Reinforcement Learning (RL). However, standard OPD faces two coupled limitations. First, it requires direct access to the teacher&#39;s token-level logits, excluding a broad class of capable proprietary models from serving as teachers. Second, the token-level logit signal itself is brittle, depending on a narrow overlap of plausible next tokens between teacher and student, and prone to amplifying degenerate patterns such as repetition loops. In this paper, we introduce OmniOPD, a novel framework that addresses both limitations through a logit-free, chunk-level supervision signal. OmniOPD replaces deterministic logit matching with Monte Carlo rollouts that approximate the teacher&#39;s local preferences through a continuous semantic similarity metric over multi-token chunks, and concentrates this supervision via a peak-entropy scheduler that audits the student only at its high-uncertainty reasoning forks. A Dirichlet-Multinomial Bayesian prior and a base-model KL anchor further bound the variance of discrete sampling and prevent policy collapse across unaudited tokens. Across competitive benchmarks, OmniOPD surpasses the standard OPD approach by up to +28.64% on math, confirming that chunk-level semantic verification extracts a more reliable learning signal than token-level logit matching, whose high information density is offset by significant noise and brittleness. Furthermore, when paired with stronger black-box teachers such as Claude-4.5-Haiku and Gemini-2.5-Flash, OmniOPD achieves an additional +9.54% relative on math over its open-weight teacher counterpart, advancing the student past the performance of self-exploratory RL.

## Trust Region On-Policy Distillation

- **arXiv**: [2606.01249](https://arxiv.org/abs/2606.01249)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-Policy Distillation (OPD) is a fundamental technique for efficient post-training of large language models (LLMs), with broad applications in agent learning, multi-task enhancement, and model compression. However, OPD training becomes unstable when the teacher and student distributions differ substantially, as teacher supervision on student-generated tokens may yield unreliable policy gradients and even cause optimization failure. This work addresses reliable on-policy token-level supervision through credit assignment strategies, and proposes Trust Region On-Policy Distillation, TrOPD. It features the following characteristics: 1) Trust-Region On-Policy Learning: TrOPD performs OPD only in regions where the teacher provides reliable supervision, mitigating the optimization difficulty of the K1 reverse-KL estimator under distribution mismatch. 2) Outlier Estimation: For outlier regions, we explore gradient clipping, masking, and forward-KL estimation to reduce the adverse effects of unreliable supervision. 3) Off-Policy Guidance: The student continues generation from teacher prefixes and uses forward KL to imitate off-policy guidance, encouraging on-policy exploration toward reliable regions. Experiments show that TrOPD consistently outperforms SoTA OPD baselines, including OPD, EOPD, and REOPOLD, across mathematical reasoning, code generation, and general-domain benchmarks.

## OPD+: Rethinking the Advantage Design for On-Policy Distillation

- **arXiv**: [2606.01039](https://arxiv.org/abs/2606.01039)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-policy distillation (OPD) is a widely used technique to transfer capabilities from capable teacher language models to the base student models, and can be formulated in a reinforcement learning style objective using student generated rollouts. Yet, despite the divergence reward being dependent on student model likelihood, existing works usually adopt a stop gradient design primarily for stability, which makes the resulting advantage estimation questionable. In this work, we provide a generic optimization framework based on f-divergence between the student and teacher, and mathematically revisit whether such design space is valid. We prove that general stop-gradient operation would lead to biased estimates of the reward objective and corresponding gradient for general divergence functions. We propose OPD+, the corrected version of OPD that demonstrates improved performance over the baseline KL approach and also supports the choice of various f-divergence. We validate our findings on mathematical reasoning and tool-use benchmarks.

## Internalize the Temperature: On-Policy Self-Distillation as Policy Reheater for Reinforcement Learning

- **arXiv**: [2606.00755](https://arxiv.org/abs/2606.00755)
- **类别**: 🔬 白盒OPD（白盒 OPD / 细粒度）
- **匹配关键词**: on-policy self-distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Reinforcement learning from verifiable rewards improves the reasoning ability of large language models, but often suffers from entropy collapse, in which increasingly concentrated policies reduce rollout diversity and useful learning signals. Existing remedies either constrain the RL objective (e.g., entropy regularization) or adjust sampling temperature during rollout collection, but these interventions remain external to the model parameters. We propose Temperature-Scaled On-Policy Self-Distillation (TS-OPSD), a lightweight policy reheating method that internalizes the exploratory effect of temperature into model parameters. Starting from an entropy-collapsed RL checkpoint, TS-OPSD constructs a self-teacher by applying high-temperature scaling to the model&#39;s own logits, then distills the resulting smoother distribution back into the student. This policy reheating requires no external teacher, privileged data, or additional inference cost. Experiments on Qwen3-4B-Base and Qwen3-8B-Base show that policy reheating yields a stronger initialization for continued RL than both standard continued RL and rollout-level temperature reheating. Further analyses show that TS-OPSD mainly reduces output sharpness while preserving intermediate representations, top candidate sets, and reasoning capability. These results suggest that entropy restoration can serve as a simple post-collapse intervention for extending reasoning-oriented RL.

## Decomposed On-Policy Distillation for Vision-Language Reasoning: Steering Gradients for Visual Grounding

- **arXiv**: [2606.00564](https://arxiv.org/abs/2606.00564)
- **类别**: 🖼️ 多模态（多模态 OPD）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
While on-policy distillation offers dense supervision for training small reasoning models, its optimization dynamics in the multimodal domain remain under-explored. In this work, we challenge the standard monolithic view of Vision-Language Model (VLM) distillation by mathematically decomposing the loss into two distinct components: the language prior and visual grounding. Our analysis uncovers that gradient vectors for these components are nearly orthogonal, indicating that the objective of aligning with the teacher&#39;s language distribution is geometrically independent from the objective of matching its visual perception. Consequently, standard optimization passively follows a suboptimal compromise trajectory that implicitly balances the two objectives. Hypothesizing that visual grounding constitutes the primary bottleneck for vision-language reasoning, we introduce Visual Gradient Steering (VGS), a method that dynamically reorients the update vector to prioritize the visual subspace. Experimental results on multiple distillation settings and complex multimodal benchmarks demonstrate that VGS significantly outperforms the standard monolithic formulation of on-policy distillation, achieving superior grounding with minimal training overhead.

## Interpretable Policy Distillation for Power Grid Topology Control

- **arXiv**: [2606.00561](https://arxiv.org/abs/2606.00561)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Deep reinforcement learning (RL) offers a promising route to real-time power grid operation, yet large neural policies are costly to evaluate, hard to deploy on constrained hardware, and opaque to operators. We ask whether a Proximal Policy Optimization (PPO) agent for grid topology control can be compressed into compact tree-based surrogates without losing operational performance. A PPO teacher is trained on Grid2Op&#39;s standard 14-bus environment with a stability-oriented reward, using stress-focused data collection on critical, high-loading states. The policy is then distilled into a decision tree and a random forest. Across held-out validation episodes, both surrogates exceed the teacher in mean reward and survival length at a fraction of the inference cost. The decision tree shows high exact-action agreement with the PPO argmax and near-complete agreement within its top-ranked actions, while remaining small enough to be inspected directly. Feature-importance analysis reveals a representational shift: the PPO policy relies mainly on line-loading signals, while the distilled tree is driven primarily by bus-topology variables. These results suggest that stress-focused distillation can convert a black-box neural controller into a lightweight, auditable rule-like surrogate suited for real-time deployment, while also surfacing risks tied to deterministic actions and topology-specific generalization.

## Bridging Reasoning Trajectories in On-Policy Distillation via Near-Future Guidance

- **arXiv**: [2606.00305](https://arxiv.org/abs/2606.00305)
- **类别**: 🤖 Agent（Agent 应用）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-Policy Distillation (OPD) improves large language model reasoning by training a student model on trajectories sampled from its own policy under teacher supervision. Although OPD operates on trajectories, its learning signal remains token-level: it identifies deviations through high-loss tokens and repairs them through local reverse-KL correction. We show that this &#34;trajectory-sampled but token-learned&#34; mechanism cannot reliably bridge student trajectories toward teacher trajectories. About 30% of high-loss tokens fall into the low-divergence regime, indicating that many are surface-form mismatches rather than real reasoning forks. Moreover, even truly divergent tokens are difficult to repair with isolated token-level supervision, since reasoning failures often unfold as short-horizon distributional drift. We propose Trajectory-aware OPD (TOPD), which uses near-future trajectory information to identify real divergent states and distribute guidance across multiple future tokens. Experiments show that suppressing non-divergent high-loss tokens improves standard OPD from 47.8% to 48.2% average accuracy, while TOPD further improves performance to 52.2%, with gains on AIME24 from 60.0% to 63.3% and AIME25 from 46.7% to 53.3%.

## CAST: Non-Privileged Clipped Asymmetric Self-Teaching with Advantage Flipping for GRPO

- **arXiv**: [2606.00172](https://arxiv.org/abs/2606.00172)
- **类别**: ♻️ OPSD+RL（OPSD + RL 混合）
- **匹配关键词**: self-teaching
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
Reinforcement learning with verifiable rewards (RLVR), especially Group Relative Policy Optimization (GRPO), has been widely used to improve reasoning in large language models. However, outcome-level rewards provide only sparse supervision, and group-relative advantages vanish when all sampled trajectories for a prompt are either correct or incorrect. On-Policy Self-Distillation (OPSD) offers dense token-level guidance, but its token preferences are not necessarily aligned with trajectory correctness; empirical diagnostics show that OPSD signals behave differently on correct and incorrect rollouts, with teacher-positive and teacher-negative gap signals exhibiting different noise profiles. These diagnostics are conducted under an OPSD-style privileged teacher context for analysis only, whereas CAST training uses answer-free self-teacher this http URL by these observations, this work proposes CAST, an answer-free self-distillation method for GRPO-style RLVR. CAST keeps the verifier-grounded GRPO objective, but uses a stop-gradient self-teacher to shape token-level advantages according to trajectory correctness. Unlike prior self-distilled RLVR methods, CAST does not require reference-solution-conditioned teacher scoring, keeps the self-teacher log-probability gap active throughout training, and applies bidirectional local advantage sign reversal: teacher-negative tokens in correct trajectories can receive negative token-level advantages, while teacher-positive tokens in incorrect trajectories can receive bounded positive local advantages. For zero-variance all-correct and all-wrong groups, CAST assigns bounded sign-constrained base advantages, so these otherwise zero-gradient groups can contribute verifier-signed token feedback. Experiments on mathematical reasoning show that CAST improves RLVR training while retaining a lightweight, verifier-grounded trajectory-level objective.

## Are Full Rollouts Necessary for On-Policy Distillation?

- **arXiv**: [2605.31490](https://arxiv.org/abs/2605.31490)
- **类别**: 📌 其他（其他 / 待人工分类）
- **匹配关键词**: on-policy distillation
- **作者**: 
- **提交日期**: 
- **主分类**: 

### Abstract
On-policy distillation (OPD) provides dense teacher feedback along student-generated rollouts rather than fixed teacher traces and has emerged as a promising post-training paradigm. However, standard OPD typically generates full rollouts during training, which is computationally expensive and may expose the student to unreliable teacher feedback at late rollout positions, especially during early training. We identify the rollout horizon as a key bottleneck in OPD that substantially impacts training efficiency. Unlike Reinforcement Learning with Verifiable Rewards (RLVR), OPD does not require a final answer reward to provide learning signals. Therefore, full rollouts may not always be necessary for OPD. Motivated by this insight, we propose two simple horizon-control strategies: Progressive OPD (POPD), which gradually expands the rollout horizon during training, and Truncated OPD (TOPD), which permanently performs distillation on reliable truncated rollouts. Experiments on mathematical reasoning show that POPD improves the training efficiency of OPD by up to 3$\times$, while TOPD matches OPD performance using only 10\% of the rollout horizon, leading to substantial wall-clock and memory reductions. These results demonstrate that controlling the rollout horizon offers a simple and practical path to more efficient OPD.
