# Beyond Output Confidence (ACL Findings 2026)

Extracted characters: 41346


## 3
Method

3
Method


## 4
Experiments

4
Experiments


## 4.1
Experimental Setup

4.1
Experimental Setup
Datasets
We conduct closed-book evaluation on
three standard open-domain QA benchmarks; mod-
els must answer solely from parametric memory.
For each corpus, we fix the first 1,000 examples of
the official test set to ensure deterministic and re-
producible uncertainty estimation (Niu et al., 2025).
TriviaQA (Joshi et al., 2017) — trivia-style ques-
tions requiring encyclopedic knowledge. Natu-
ral Questions (NQ) (Kwiatkowski et al., 2019)
— real user queries with Wikipedia gold spans;
we retain single-short answers. HaluEval-QA (Li
et al., 2023; Zhu et al., 2024) — adversarially con-
structed QA pairs where 50% of fluent answers are
factually incorrect, enabling direct assessment of
low-entropy hallucinations.
Models and Hyper-parameters
We cover both
scale and architectural diversity: Llama-3.1-8B-
Instruct (Dubey et al., 2024), Qwen-2.5-7B-
Instruct, and Qwen-2.5-14B-Instruct (Qwen et al.,
2025). All parameters remain frozen; only de-
coding hyper-parameters are adjusted. Following
consistency-based baselines (Chen et al., 2024), a
hybrid greedy–stochastic strategy is adopted: one
greedy sequence for answer generation and nine
stochastic samples (T=0.5, top-k=5, top-p=0.99,
repetition penalty 1.2) for covariance estimation.*
Evaluation Metrics
Hallucination detection is
cast as a binary classification task. We report AU-
ROC, which measures the probability that a ran-
domly drawn positive example is assigned a higher
uncertainty score than a negative example; higher
AUROC indicates better ranking quality (Azaria
and Mitchell, 2023). To mitigate surface-form bias,
two complementary correctness labels are gener-
ated for every answer:
1. Lexical (AUROCr): ROUGE-L F-measure
≥0.5 against any reference, following Lin
(2004). ROUGE-L quantifies the longest com-
mon subsequence between the generated text
and the ground-truth span; we use the F1 score
to balance precision and recall.
2. Semantic (AUROCs): cosine similarity ≥
0.9 between the generated sentence and the
ground-truth answer, using 768-dimensional
*White-box hidden states are extracted from the middle
layer of the model (layer L
2 ).
13800

Table 3: Main results across three public open-domain QA benchmarks (NQ, TriviaQA, HaluEval-QA) and three
model scales (8B, 7B, 14B). Each cell reports AUROCr / AUROCs (%, higher is better) under lexical and semantic
correctness criteria, respectively. Best score in bold; second-best underlined. Suffix “-AIC” denotes coupling
the corresponding one-dimensional uncertainty with our proposed Answer-level Intrinsic Cognition to form a
two-dimensional hallucination detector. All improvements are absolute percentage points over the baseline method
in the same row. The consistent gains validate that AIC calibration suppresses low-entropy hallucinations across
domains, model sizes, and uncertainty backbones.
Model
Method
NQ
TriviaQA
HaluEval-QA
AUROCr
AUROCs
AUROCr
AUROCs
AUROCr
AUROCs
Llama-3.1-8B
EigenScore
76.8
76.2
80.0
78.8
74.3


## 4.2
Main Results

4.2
Main Results
Effectiveness
Table 3 shows that coupling AIC
with one-dimensional indicators to form two-
dimensional features yields consistent and sig-
nificant AUROC gains across all baselines, sup-
porting the generality of the proposed calibra-
tion.
For Llama-3.1-8B on NQ, PPL-AIC im-
proves AUROCr from 73.0 to 76.7 (∆↑+3.7) and
AUROCs from 76.9 to 79.4 (∆↑+2.5); Energy-
AIC delivers an absolute AUROCr gain of 10.7.
Similar trends hold on TriviaQA and HaluEval-QA
and remain stable across model scales, indicating
that the gains are not domain-specific.
Scale effect on hallucination rate
As parame-
ter count increases, the raw hallucination rate de-
creases monotonically: on HaluEval-QA, Qwen2.5-
14B achieves 86.4/86.7 with PPL, outperforming
the 7B counterpart by 4.1 points. This observa-
tion aligns with the theoretical expectation that
ˆP(I(x) = 1) approaches 1 for larger models,
thereby reducing the room for calibration.
Diminishing calibration gains
Although two-
dimensional calibration remains beneficial, its
marginal improvement shrinks as model scale
grows. On HaluEval-QA (AUROCr), PPL-AIC
yields an absolute gain of 0.4 percentage points
for Qwen2.5-7B and 0.5 points for 14B; Energy-
AIC drops from 3.1 points (7B) to 2.8 points (14B).
The same decay pattern holds for AUROCs and for
NQ/TriviaQA, where the absolute gains likewise
decrease with model scale, consistent with Eq. (10):
as ˆπ1 →1, S(x, y) →U(y | x), leaving less room
for correction.


## 4.3
Ablation Studies

4.3
Ablation Studies
Impact of automatic correctness criteria
De-
signing QA correctness metrics that align with hu-
man judgment is non-trivial; the chosen threshold
therefore constitutes a major source of variance
in hallucination detection. On Llama-3.1-8B +
NQ, we sweep ROUGE-L and Sentence-Similarity
Table 4: Correctness measures vs. threshold (ROUGE-L
/ Sentence Similarity).
Method
ROUGE-L
Sentence Similarity
0.3
0.5
0.7
0.7
0.8


## 5
Conclusion

5
Conclusion
We introduced a training-free, two-dimensional un-
certainty framework that couples output uncertainty
13803

17.5
20.0
22.5
25.0
27.5


## 6
Limitations

6
Limitations
The framework relies on answer-level consistency
across stochastic decodings as an indirect proxy
for the model’s cognitive boundary. This design
choice incurs extra forward passes, yields a single
global estimate for the entire answer, and becomes
less informative under low-temperature sampling,
thereby propagating latency, granularity, and sensi-
tivity issues into downstream deployment. Future
work that obtains the boundary through more di-
rect and efficient signals could lift these constraints
without altering the core two-dimensional calibra-
tion principle.
AI Usage Statement
Large language models were used exclusively for
grammar checking, wording refinement, and La-
TeX formatting. All scientific content, claims, and
final decisions were made by the human authors.
References
Robert B Ash and Catherine A Doléans-Dade. 2000.
Probability and measure theory. Academic press.
Amos Azaria and Tom Mitchell. 2023. The internal
state of an llm knows when it’s lying. arXiv preprint
arXiv:2304.13734.
Bernd Bohnet, Vinh Q Tran, Pat Verga, Roee Aha-
roni, Daniel Andor, Livio Baldini Soares, Massimil-
iano Ciaramita, Jacob Eisenstein, Kuzman Ganchev,
Jonathan Herzig, and 1 others. 2022.
Attributed
question answering: Evaluation and modeling for
attributed large language models.
arXiv preprint
arXiv:2212.08037.
Chao Chen, Kai Liu, Ze Chen, Yi Gu, Yue Wu,
Mingyuan Tao, Zhihang Fu, and Jieping Ye. 2024.
Inside: Llms’ internal states retain the power of hal-
lucination detection. Preprint, arXiv:2402.03744.
Yung-Sung Chuang, Linlu Qiu, Cheng-Yu Hsieh, Ran-
jay Krishna, Yoon Kim, and James Glass. 2024.
Lookback lens: Detecting and mitigating contextual
hallucinations in large language models using only
attention maps. arXiv preprint arXiv:2407.07071.
Roi Cohen, May Hamri, Mor Geva, and Amir Glober-
son. 2023. Lm vs lm: Detecting factual errors via
cross examination. arXiv preprint arXiv:2305.13281.
Jinhao Duan, Hao Cheng, Shiqi Wang, Alex Zavalny,
Chenan Wang, Renjing Xu, Bhavya Kailkhura, and


# Targeted passages

## Search term: limitation[s]?

wo distinct cognitive states: A. Within-boundary uncertainty: the query lies inside the cognitive boundary, but ambiguity or noise yields high entropy; B. Outside-boundary confidence: the query lies beyond the boundary, yet the model remains confident and incorrect. One- dimensional indicators cannot disentangle these states, producing false negatives in state B and false positives in state A (Lin et al., 2023; Ren et al., 2022). To address this limitation, we propose a two- dimensional, training-free hallucination detec- tor that augments output uncertainty with Answer- level Intrinsic Cognition (AIC). AIC quantifies the stability of the cognitive boundary by aggre- gating answer-level consistency across multiple stochastic decodings of the same question, with- out supervision or gradients (Chen et al., 2024; Lin et al., 2023; Kossen et al., 2024). By decom- posing the joint distribution through the law of total probability (Lyu et al., 2019; Gal and Ghahra- mani, 2016), we prove that the nuisance term in- duced by boundary miscalibration is asymptotically bounded, thereby restricting hallucination signals to the subspace where the model believes it knows yet answers incorrectly. The resulting score approx- imates the true uncertainty conditioned on knowl- edgeability. The entire framework is training-free and re- quires no external knowledge, enabling seamless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms 

## Search term: limitation[s]?

al to the region where “the model believes it knows yet answers incorrectly.” Beyond empirical gains, the work shifts hallucination detection from single scalar statistics to joint cognition–uncertainty mod- eling, offering a plug-in module for safety-critical deployments under black-box constraints. Future directions include reducing sampling cost and ex- tending the principle to long-form generation and retrieval-augmented dual verification. 6 Limitations The framework relies on answer-level consistency across stochastic decodings as an indirect proxy for the model’s cognitive boundary. This design choice incurs extra forward passes, yields a single global estimate for the entire answer, and becomes less informative under low-temperature sampling, thereby propagating latency, granularity, and sensi- tivity issues into downstream deployment. Future work that obtains the boundary through more di- rect and efficient signals could lift these constraints without altering the core two-dimensional calibra- tion principle. AI Usage Statement Large language models were used exclusively for grammar checking, wording refinement, and La- TeX formatting. All scientific content, claims, and final decisions were made by the human authors. References Robert B Ash and Catherine A Doléans-Dade. 2000. Probability and measure theory. Academic press. Amos Azaria and Tom Mitchell. 2023. The internal state of an llm knows when it’s lying. arXiv preprint arXiv:2304.13734. Bernd Bohnet, Vinh Q Tran, Pat Verga, Roee Aha- roni, Daniel Andor, Livio Baldini Soar

## Search term: we propose

ns are pro- duced with high statistical certainty. Exist- ing approaches commonly use output proba- bility as a proxy for truthfulness; however, this signal is confounded by epistemic uncertainty and cannot reliably distinguish genuine uncer- tainty from fabricated content. We argue that effective hallucination detection requires inte- grating surface-level confidence with signals that reflect the model’s underlying epistemic state. To this end, we propose Answer-level Intrinsic Cognition (AIC), a model-agnostic metric that captures epistemic boundary de- viations by measuring answer-level stability across multiple stochastic forward passes. By coupling AIC with conventional output uncer- tainty, we derive a composite metric that dis- entangles within-boundary uncertainty from outside-boundary confidence. Across three public question-answering benchmarks and di- verse model scales, the two-dimensional score consistently outperforms strong uncertainty- only baselines, with larger gains on adver- sarially constructed hallucination sets. The code is available at: https://github.com/ HXYfighter/AIC-ACL2026. 1 Introduction Large language models (LLMs) achieve human- level fluency on open-domain question answer- ing, dialogue generation, and code completion (Ouyang et al., 2022; Huang et al., 2025; Li et al., 2025; Dubey et al., 2024). This fluency, however, coexists with a systematic tendency to hallucinate: LLMs often produce statements that contradict ver- ifiable facts while maintaining high predictive con- fidence (Ji et al., 2023; Liu

## Search term: we propose

cognitive states: A. Within-boundary uncertainty: the query lies inside the cognitive boundary, but ambiguity or noise yields high entropy; B. Outside-boundary confidence: the query lies beyond the boundary, yet the model remains confident and incorrect. One- dimensional indicators cannot disentangle these states, producing false negatives in state B and false positives in state A (Lin et al., 2023; Ren et al., 2022). To address this limitation, we propose a two- dimensional, training-free hallucination detec- tor that augments output uncertainty with Answer- level Intrinsic Cognition (AIC). AIC quantifies the stability of the cognitive boundary by aggre- gating answer-level consistency across multiple stochastic decodings of the same question, with- out supervision or gradients (Chen et al., 2024; Lin et al., 2023; Kossen et al., 2024). By decom- posing the joint distribution through the law of total probability (Lyu et al., 2019; Gal and Ghahra- mani, 2016), we prove that the nuisance term in- duced by boundary miscalibration is asymptotically bounded, thereby restricting hallucination signals to the subspace where the model believes it knows yet answers incorrectly. The resulting score approx- imates the true uncertainty conditioned on knowl- edgeability. The entire framework is training-free and re- quires no external knowledge, enabling seamless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms one-dimensio

## Search term: we introduce

incipled approach to uncertainty cal- ibration via uncertainty post-processing, which is training-free, black-box friendly, and explicitly boundary-aware. 3 Method 3.1 Problem Formulation and Analysis Let θ denote a frozen LLM. For an input question x, the LLM autoregressively generates an answer y = (y1, . . . , yt). Our goal is to produce a cali- brated hallucination score for the pair (x, y) with- out updating θ and without any labelled data. We introduce two random variables: 1. Epistemic uncertainty I(x) ∈{0, 1}. I(x) = 1 signifies that x lies inside the LLM’s cog- nitive boundary; I(x) = 0 signifies that the LLM lacks the knowledge required for x. 2. Output uncertainty U(y | x) ∈R. This statis- tic is directly computable from the LLM out- put, e.g., perplexity or energy. Hallucination risk is defined as the conditional uncertainty given that the LLM believes it knows: η(x, y) ≜E  U(y | x) | I(x) = 1  . (1) Applying the law of total probability (Ash and Doléans-Dade, 2000) to E(U(y | x)) gives E  U(y | x)  = E1π1 + E0π0, (2) where E∗= E  U(y | x) | I(x) = ∗  and π∗= P  I(x) = ∗  . Solving (2) for η(x, y) yields η(x, y) = E  U(y | x)  −E0π0 π1 . (3) The term E0π0 captures the contribution to un- certainty arising from the model’s lack of knowl- edge regarding the query condition. When the model is entirely unaware of the relevant context, uncertainty is not merely unquantifiable; the con- cept itself ceases to apply. Hence E0π0 is not a bias to be bounded but a nuisance term inherent to standard uncertainty formulations, and it

## Search term: we introduce

uence- level model confidence, whereas AIC measures answer-level consistency across multiple genera- tions. The low correlation indicates limited redun- dancy between the two dimensions, making them suitable candidates for feature concatenation. Con- sequently, coupling AIC with any one-dimensional uncertainty measure yields complementary two- dimensional features without requiring additional training or architectural modifications. 5 Conclusion We introduced a training-free, two-dimensional un- certainty framework that couples output uncertainty 13803 17.5 20.0 22.5 25.0 27.5 30.0 Energy 0.4 0.6 0.8 1.0 AIC r = 0.334 (a) Energy vs. AIC (r = 0.334) 0.0 0.5 1.0 1.5 PPL 0.4 0.6 0.8 1.0 AIC r = -0.324 (b) PPL vs. AIC (r = −0.324) Figure 3: Pearson correlation analysis between AIC and one-dimensional uncertainty measures. Weak correlations (|r| < 0.35) indicate that AIC captures complementary information to scalar baselines, validating its use for feature calibration. with Answer-level Intrinsic Cognition. By explic- itly modeling the model’s own cognitive-boundary stability, the approach recalibrates any off-the- shelf uncertainty score without gradients, labels, or external knowledge. Consistent improvements across multiple benchmarks and model scales indi- cate that the paradigm effectively suppresses low- entropy hallucinations that remain invisible to one- dimensional detectors. Theoretically, the decompo- sition bounds the bias induced by out-of-boundary queries and confines the hallucination signal to the region where “the model bel

## Search term: training-free

ndary uncertainty: the query lies inside the cognitive boundary, but ambiguity or noise yields high entropy; B. Outside-boundary confidence: the query lies beyond the boundary, yet the model remains confident and incorrect. One- dimensional indicators cannot disentangle these states, producing false negatives in state B and false positives in state A (Lin et al., 2023; Ren et al., 2022). To address this limitation, we propose a two- dimensional, training-free hallucination detec- tor that augments output uncertainty with Answer- level Intrinsic Cognition (AIC). AIC quantifies the stability of the cognitive boundary by aggre- gating answer-level consistency across multiple stochastic decodings of the same question, with- out supervision or gradients (Chen et al., 2024; Lin et al., 2023; Kossen et al., 2024). By decom- posing the joint distribution through the law of total probability (Lyu et al., 2019; Gal and Ghahra- mani, 2016), we prove that the nuisance term in- duced by boundary miscalibration is asymptotically bounded, thereby restricting hallucination signals to the subspace where the model believes it knows yet answers incorrectly. The resulting score approx- imates the true uncertainty conditioned on knowl- edgeability. The entire framework is training-free and re- quires no external knowledge, enabling seamless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms one-dimensional un- certainty baselines across

## Search term: training-free

decom- posing the joint distribution through the law of total probability (Lyu et al., 2019; Gal and Ghahra- mani, 2016), we prove that the nuisance term in- duced by boundary miscalibration is asymptotically bounded, thereby restricting hallucination signals to the subspace where the model believes it knows yet answers incorrectly. The resulting score approx- imates the true uncertainty conditioned on knowl- edgeability. The entire framework is training-free and re- quires no external knowledge, enabling seamless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms one-dimensional un- certainty baselines across models of varying scales, with larger improvements observed on more chal- lenging, adversarially constructed hallucination datasets. We summarize our contributions as follows: 1. Answer-level Intrinsic Cognition (AIC) — a training-free metric that quantifies cognitive- boundary stability by aggregating answer- consistency across multiple stochastic decod- ings of the same question. 2. Two-dimensional uncertainty decomposition — a principled derivation that bounds the nui- sance term induced by boundary miscalibration, yielding a hallucination score conditioned on knowledgeability. 3. Extensive empirical validation — consistent gains over one-dimensional uncertainty base- lines on three public QA benchmarks across model scales, with larger improvements on ad- versarially constructed low-entropy hallucina- tion 

## Search term: training-free

mless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms one-dimensional un- certainty baselines across models of varying scales, with larger improvements observed on more chal- lenging, adversarially constructed hallucination datasets. We summarize our contributions as follows: 1. Answer-level Intrinsic Cognition (AIC) — a training-free metric that quantifies cognitive- boundary stability by aggregating answer- consistency across multiple stochastic decod- ings of the same question. 2. Two-dimensional uncertainty decomposition — a principled derivation that bounds the nui- sance term induced by boundary miscalibration, yielding a hallucination score conditioned on knowledgeability. 3. Extensive empirical validation — consistent gains over one-dimensional uncertainty base- lines on three public QA benchmarks across model scales, with larger improvements on ad- versarially constructed low-entropy hallucina- tion sets. 2 Related Work Hallucination detection has converged to three mainstream paradigms, each implicitly assuming that “the model knows what it does not know” and consequently exhibiting limited robustness under distribution shift (Sriramanan et al., 2024; Ren et al., 2022; Liu et al., 2020; Kadavath et al., 2022). One-dimensional uncertainty estimation relies exclusively on the target model θ and can be subdi- vided into two strands. (1) Token-level probability indicators such as perplexity or energy scores

## Search term: training-free

ust external evidence.” A typical pipeline (a) atom- izes claims, (b) retrieves passages from encyclope- dias or the web, and (c) labels truthfulness with an NLI or similarity model (Hu et al., 2024; Cohen et al., 2023; Kry´sci´nski et al., 2020; Bohnet et al., 2022). Although interpretable and updateable as knowledge bases evolve, the approach introduces 13797 Table 1: Comparison of hallucination-detection ap- proaches along three key axes. 1: Training-free (no gra- dient updates or labelled data at test time); 2: Black-box friendly (compatible with gradient-frozen, parameter- locked APIs); 3: Boundary-aware (explicitly models the model’s cognitive boundary). ✓/✗indicate satis- fied/unsatisfied criteria. Approach 1 2 3 One-dimensional uncertainty ✓✓✗ External knowledge verification ✓✓✗ Hidden-state probing ✗✗✗ Two-dimensional uncertainty ✓✓✓ non-trivial latency (retrieve–align–judge) and re- turns “unknown” when evidence is itself missing. Our two-dimensional framework is orthogonal: re- trieval confidence can be treated as an additional observation and fused with AIC in a two-factor uncertainty model, thereby converting the ternary decision {True, False, Unknown} into a continuous risk score. Hidden-state probing trains lightweight clas- sifiers on internal activations or attention pat- terns to discriminate faithful from hallucinated out- puts (Azaria and Mitchell, 2023; Chuang et al., 2024; Kossen et al., 2024). While often achieving the highest absolute accuracy, these probes require white-box access, labelled hallucination example

## Search term: training-free

irectly equate “low probability,” “incon- sistency,” or “external conflict” with hallucination signals, thereby neglecting the cognitive boundary that separates “knowing” from “not knowing.” By explicitly modelling this boundary through answer- level Intrinsic Cognition and jointly reasoning with output uncertainty, our two-dimensional framework provides a principled approach to uncertainty cal- ibration via uncertainty post-processing, which is training-free, black-box friendly, and explicitly boundary-aware. 3 Method 3.1 Problem Formulation and Analysis Let θ denote a frozen LLM. For an input question x, the LLM autoregressively generates an answer y = (y1, . . . , yt). Our goal is to produce a cali- brated hallucination score for the pair (x, y) with- out updating θ and without any labelled data. We introduce two random variables: 1. Epistemic uncertainty I(x) ∈{0, 1}. I(x) = 1 signifies that x lies inside the LLM’s cog- nitive boundary; I(x) = 0 signifies that the LLM lacks the knowledge required for x. 2. Output uncertainty U(y | x) ∈R. This statis- tic is directly computable from the LLM out- put, e.g., perplexity or energy. Hallucination risk is defined as the conditional uncertainty given that the LLM believes it knows: η(x, y) ≜E  U(y | x) | I(x) = 1  . (1) Applying the law of total probability (Ash and Doléans-Dade, 2000) to E(U(y | x)) gives E  U(y | x)  = E1π1 + E0π0, (2) where E∗= E  U(y | x) | I(x) = ∗  and π∗= P  I(x) = ∗  . Solving (2) for η(x, y) yields η(x, y) = E  U(y | x)  −E0π0 π1 . (3) The term E0π0 captures th

## Search term: calibration

Cognition (AIC). AIC quantifies the stability of the cognitive boundary by aggre- gating answer-level consistency across multiple stochastic decodings of the same question, with- out supervision or gradients (Chen et al., 2024; Lin et al., 2023; Kossen et al., 2024). By decom- posing the joint distribution through the law of total probability (Lyu et al., 2019; Gal and Ghahra- mani, 2016), we prove that the nuisance term in- duced by boundary miscalibration is asymptotically bounded, thereby restricting hallucination signals to the subspace where the model believes it knows yet answers incorrectly. The resulting score approx- imates the true uncertainty conditioned on knowl- edgeability. The entire framework is training-free and re- quires no external knowledge, enabling seamless deployment under white-box or black-box settings. Experiments on three public question-answering benchmarks show that the two-dimensional indica- tor consistently outperforms one-dimensional un- certainty baselines across models of varying scales, with larger improvements observed on more chal- lenging, adversarially constructed hallucination datasets. We summarize our contributions as follows: 1. Answer-level Intrinsic Cognition (AIC) — a training-free metric that quantifies cognitive- boundary stability by aggregating answer- consistency across multiple stochastic decod- ings of the same question. 2. Two-dimensional uncertainty decomposition — a principled derivation that bounds the nui- sance term induced by boundary miscalibration, yielding a hallucination

## Search term: calibration

n more chal- lenging, adversarially constructed hallucination datasets. We summarize our contributions as follows: 1. Answer-level Intrinsic Cognition (AIC) — a training-free metric that quantifies cognitive- boundary stability by aggregating answer- consistency across multiple stochastic decod- ings of the same question. 2. Two-dimensional uncertainty decomposition — a principled derivation that bounds the nui- sance term induced by boundary miscalibration, yielding a hallucination score conditioned on knowledgeability. 3. Extensive empirical validation — consistent gains over one-dimensional uncertainty base- lines on three public QA benchmarks across model scales, with larger improvements on ad- versarially constructed low-entropy hallucina- tion sets. 2 Related Work Hallucination detection has converged to three mainstream paradigms, each implicitly assuming that “the model knows what it does not know” and consequently exhibiting limited robustness under distribution shift (Sriramanan et al., 2024; Ren et al., 2022; Liu et al., 2020; Kadavath et al., 2022). One-dimensional uncertainty estimation relies exclusively on the target model θ and can be subdi- vided into two strands. (1) Token-level probability indicators such as perplexity or energy scores measure the sharp- ness of local probabilities pθ(yt | y<t, x) along a generated sequence, operating under the premise that higher uncertainty implies higher hallucina- tion probability (Sriramanan et al., 2024; Ren et al., 2022). Low-entropy hallucinations provide a counter-example: f

## Search term: calibration

., 2023; Chen et al., 2024). In contrast, AIC regards agreement as nec- essary but not sufficient for falling inside the cogni- tive boundary: outside-boundary queries may also collapse to a misleadingly consistent but incorrect answer. By using the leading explained-variance ra- tio ˜λ1 as an explicit estimate of knowability π1 and dividing the original uncertainty by this estimate, we convert consistency from a binary verdict into a continuous calibration factor; Table 2 summarizes the conceptual difference. Table 2: Comparison of uncertainty-based detectors. “Cal. low-H” = calibrates high-confidence hallucinations outside cognitive boundary. Method Train-free Cal. low-H One-dimensional ✓ ✗ Consistency ✓ ✗ Two-dimensional (ours) ✓ ✓ 4 Experiments 4.1 Experimental Setup Datasets We conduct closed-book evaluation on three standard open-domain QA benchmarks; mod- els must answer solely from parametric memory. For each corpus, we fix the first 1,000 examples of the official test set to ensure deterministic and re- producible uncertainty estimation (Niu et al., 2025). TriviaQA (Joshi et al., 2017) — trivia-style ques- tions requiring encyclopedic knowledge. Natu- ral Questions (NQ) (Kwiatkowski et al., 2019) — real user queries with Wikipedia gold spans; we retain single-short answers. HaluEval-QA (Li et al., 2023; Zhu et al., 2024) — adversarially con- structed QA pairs where 50% of fluent answers are factually incorrect, enabling direct assessment of low-entropy hallucinations. Models and Hyper-parameters We cover both scale and archite

## Search term: calibration

ROCr / AUROCs (%, higher is better) under lexical and semantic correctness criteria, respectively. Best score in bold; second-best underlined. Suffix “-AIC” denotes coupling the corresponding one-dimensional uncertainty with our proposed Answer-level Intrinsic Cognition to form a two-dimensional hallucination detector. All improvements are absolute percentage points over the baseline method in the same row. The consistent gains validate that AIC calibration suppresses low-entropy hallucinations across domains, model sizes, and uncertainty backbones. Model Method NQ TriviaQA HaluEval-QA AUROCr AUROCs AUROCr AUROCs AUROCr AUROCs Llama-3.1-8B EigenScore 76.8 76.2 80.0 78.8 74.3 73.8 LNE 70.9 73.2 80.6 78.8 77.7 77.2 SAR 75.9 75.7 80.4 79.3 79.4 79.3 SE 76.7 76.3 79.3 78.1 76.3 76.6 AIC 73.0 71.6 75.2 74.3 72.4 72.1 PPL 73.0 76.9 80.5 80.5 76.7 77.3 PPL-AIC 76.7 79.4 82.8 82.7 78.8 79.2 Energy 63.0 65.5 74.5 74.1 73.5 74.8 Energy-AIC 73.7 73.0 79.0 78.2 75.8 75.9 CCP 79.3 81.6 82.9 82.8 80.5 82.3 CCP-AIC 80.9 82.4 83.5 82.9 81.8 83.2 Qwen2.5-7B EigenScore 74.7 75.2 77.8 76.8 74.4 73.5 LNE 74.1 73.5 81.5 80.7 79.4 78.1 SAR 63.0 63.7 70.5 71.9 70.4 71.2 SE 64.7 65.9 70.5 71.9 70.4 71.2 AIC 75.9 77.2 77.4 77.0 77.0 76.2 PPL 75.6 75.0 84.9 84.4 82.3 81.7 PPL-AIC 76.7 76.4 85.5 84.9 82.7 82.1 Energy 66.0 66.9 79.4 80.3 75.2 75.9 Energy-AIC 72.0 73.6 82.8 83.1 78.3 78.4 CCP 68.4 67.8 70.5 71.9 70.4 71.2 CCP-AIC 71.2 70.7 74.7 74.7 72.7 73.2 Qwen2.5-14B EigenScore 75.2 73.8 77.0 76.6 74.1 74.6 LNE 76.0 74.3 80.8 79.6 81.9 82.1 SAR 57.9 55.2 65.2 

## Search term: calibration

main stable across model scales, indicating that the gains are not domain-specific. Scale effect on hallucination rate As parame- ter count increases, the raw hallucination rate de- creases monotonically: on HaluEval-QA, Qwen2.5- 14B achieves 86.4/86.7 with PPL, outperforming the 7B counterpart by 4.1 points. This observa- tion aligns with the theoretical expectation that ˆP(I(x) = 1) approaches 1 for larger models, thereby reducing the room for calibration. Diminishing calibration gains Although two- dimensional calibration remains beneficial, its marginal improvement shrinks as model scale grows. On HaluEval-QA (AUROCr), PPL-AIC yields an absolute gain of 0.4 percentage points for Qwen2.5-7B and 0.5 points for 14B; Energy- AIC drops from 3.1 points (7B) to 2.8 points (14B). The same decay pattern holds for AUROCs and for NQ/TriviaQA, where the absolute gains likewise decrease with model scale, consistent with Eq. (10): as ˆπ1 →1, S(x, y) →U(y | x), leaving less room for correction. 4.3 Ablation Studies Impact of automatic correctness criteria De- signing QA correctness metrics that align with hu- man judgment is non-trivial; the chosen threshold therefore constitutes a major source of variance in hallucination detection. On Llama-3.1-8B + NQ, we sweep ROUGE-L and Sentence-Similarity Table 4: Correctness measures vs. threshold (ROUGE-L / Sentence Similarity). Method ROUGE-L Sentence Similarity 0.3 0.5 0.7 0.7 0.8 0.9 EigenScore 75.8 76.8 76.1 71.7 74.1 76.2 AIC 72.4 73.0 72.1 66.8 69.7 71.6 PPL 72.4 73.0 75.7 65.4 71.1 76.9 PPL-AIC 75
