## Page 1

AI Hiring with LLMs: A Context-Aware and Explainable Multi-Agent
Framework for Resume Screening
Frank P.-W. Lo1
Jianing Qiu2
Zeyu Wang1
Haibao Yu3
Yeming Chen4
Gao Zhang5
Benny Lo1
1Imperial College London
2The Chinese University of Hong Kong
3The University of Hong Kong
4Wedon Education Technologies
5Brest Business School
{po.lo15, zeyu.wang20, benny.lo}@imperial.ac.uk, jianingqiu@cuhk.edu.hk,
yuhaibao94@gmail.com, chenym@wedon.com, gao.zhang@brest-bs.com
Abstract
Resume screening is a critical yet time-intensive process in
talent acquisition, requiring recruiters to analyze vast vol-
ume of job applications while remaining objective, accu-
rate, and fair. With the advancements in Large Language
Models (LLMs), their reasoning capabilities and extensive
knowledge bases demonstrate new opportunities to stream-
line and automate recruitment workﬂows. In this work, we
propose a multi-agent framework for resume screening us-
ing LLMs to systematically process and evaluate resumes.
The framework consists of four core agents, including a re-
sume extractor, an evaluator, a summarizer, and a score for-
matter. To enhance the contextual relevance of candidate
assessments, we integrate Retrieval-Augmented Generation
(RAG) within the resume evaluator, allowing incorporation
of external knowledge sources, such as industry-speciﬁc ex-
pertise, professional certiﬁcations, university rankings, and
company-speciﬁc hiring criteria. This dynamic adaptation
enables personalized recruitment, bridging the gap between
AI automation and talent acquisition. We assess the effec-
tiveness of our approach by comparing AI-generated scores
with ratings provided by HR professionals on a dataset of
anonymized online resumes. The ﬁndings highlight the po-
tential of multi-agent RAG-LLM systems in automating re-
sume screening, enabling more efﬁcient and scalable hiring
workﬂows.
1. Introduction
Automated resume screening is a critical component of the
hiring process. Companies often receive a high volume of
job applications, making it difﬁcult to manually review ev-
ery resume or CV efﬁciently. Traditional resume screening
methods primarily rely on rule-based approaches, and key-
Figure 1. Illustration diagram of ﬁne-tuned LLM and RAG-
LLM for resume screening.
(a) Traditional ﬁne-tuning ap-
proaches (e.g., LoRA) require updating model parameters to adapt
to new tasks (i.e., new companies’ hiring requirements). (b) Our
model uses RAG, eliminating the need for ﬁne-tuning by dynami-
cally retrieving relevant information from external sources.
word matching, which often fail to include job-speciﬁc re-
quirements and lack adaptability. In addition, such methods
provide limited transparency and feedback, making it difﬁ-
cult for recruiters to interpret and validate AI-driven deci-
sions. Traditional methods also face several technical chal-
lenges, including difﬁculties in comprehending the nuanced
choice of words in a resume and accurately interpreting the
syntax of unstructured written language [1]. Most impor-
tantly, resume screening systems are expected to keep up
with the constantly changing job market and business needs.
Therefore, models need to be updated frequently as new job
opportunities emerge. For instance, a recommendation that
was relevant last month might become obsolete if the job
market shifts, such as due to a sudden surge in demand for
speciﬁc skills. Hence, the integration of real-time data and
This CVPR Workshop paper is the Open Access version, provided by the Computer Vision Foundation.
Except for this watermark, it is identical to the accepted version;
the final published version of the proceedings is available on IEEE Xplore.
4193


---

## Page 2

continuous learning is still a key focus of ongoing research.
Recent advancements in LLMs have demonstrated re-
markable reasoning capabilities [7], enabling new possibil-
ities for intelligent resume screening. However, most ex-
isting LLM-driven screening systems operate as monolithic
models [8], where resume parsing, evaluation, and feedback
generation are handled in a single-step process (i.e., single
LLM). The major drawback of single LLM approaches is
their lack of modularity. Since resume extraction, evalua-
tion, and feedback generation are coupled in a single model
call, modifying the scoring logic requires retraining or ﬁne-
tuning the entire model (e.g., using Low-Rank Adaptation
(LoRA)) as shown in Figure 1(a). This makes it difﬁcult
to adapt screening criteria across different industries and
job roles, reducing overall scalability1. Additionally, when
multiple reasoning steps (e.g., extracting information from
resume, applying scoring criteria, and justifying decisions)
are handled simultaneously, it becomes difﬁcult to interpret
the decision-making process. This lack of transparency lim-
its recruiters’ ability to validate AI-driven evaluations and
adjust the system without extensive reconﬁguration.
To address these challenges, we propose a multi-agent
framework for resume screening, leveraging Retrieval-
Augmented Generation enhanced LLMs (RAG-LLMs) [9]
within an agentic architecture [10]. Unlike single-step mod-
els, our framework consists of four core agents, each re-
sponsible for a distinct function: resume extraction (hiring
assistant agent), evaluation (hiring manager agent), sum-
marization (hiring coordinator agent), and score format-
ting (data curator agent). This modular structure provides
greater ﬂexibility, and in our design, the evaluation agent
can dynamically retrieve company-speciﬁc hiring criteria
via RAG. Instead of requiring ﬁne-tuning, the system can
adjust its evaluation standards in real-time by allowing HR
professionals to upload job requirement documents to the
backend, making it highly adaptable across different indus-
tries and job roles as shown in Figure 1(b). Moreover, by
dividing the screening process into multiple independent
agents, the framework enhances transparency and explain-
ability. Each stage of the process remains clearly deﬁned,
allowing recruiters to trace how a candidate was assessed
and why a particular score was assigned (i.e., instead of out-
putting a score alone, the evaluation criteria can be inferred
from the extracted resume content and the generated feed-
back, resulting in more meaningful and explainable out-
comes). This also ensures that changes in scoring criteria
does not interfere with data extraction and feedback genera-
tion. By leveraging multi-agent modularity and RAG-based
dynamic retrieval, our framework provides a scalable, trans-
1In typical recruitment workﬂows, candidates are evaluated by HR
across multiple dimensions, such as experience, skills, and education,
based on job-speciﬁc scoring criteria, which can vary signiﬁcantly across
companies and roles.
parent, and adaptable solution for AI-driven resume screen-
ing. Figure 2 illustrates how AI-driven hiring technologies
have evolved to address other challenges as well. The con-
tributions of this paper are summarized as follows:
• We propose a multi-agent architecture that introduces a
modular structure, enhancing explainability and trans-
parency in resume screening.
• Our framework is designed to adapt to diverse hiring
criteria across different roles (e.g., leadership skills for
department directors, HR expertise for human resource
associates), enabling a more context-aware and role-
adaptive screening process.
• By integrating RAG, our system allows recruiters to dy-
namically adjust screening parameters (e.g., prioritiz-
ing speciﬁc university rankings, certiﬁcations, or domain
expertise) without requiring LLM retraining/ﬁne-tuning,
thereby enhancing adaptability and customization.
• We discuss the future of AI in hiring, addressing ethi-
cal considerations, bias mitigation, and regulatory chal-
lenges, while also examining how LLMs can enhance
fairness and efﬁciency in recruitment.
2. Related Work
2.1. AI-driven hiring
The adoption of AI in hiring has signiﬁcantly trans-
formed recruitment processes, enabling automation in re-
sume screening [11], resume classiﬁcation [12–19], resume
ranking [20, 21], interview evaluation [22–25], salary pre-
diction [26, 27], and also bias mitigation [28–31]. With the
emergence of ML, DL, and LLMs, AI-driven hiring sys-
tems have evolved from simple keyword-based matching to
context-aware decision-making.
2.2. Resume screening systems
Early AI-driven resume screening systems primarily relied
on traditional machine learning methods, such as Bag-of-
Words (BoW), Support Vector Machines (SVM), and Ran-
dom Forests (RF) [12].
These methods treated resumes
as structured data, applying rule-based decision-making to
assess candidate qualiﬁcations.
However, these models
lacked semantic understanding and relied solely on key-
word matching (e.g., failing to recognize that software de-
veloper is equivalent to software engineer), leading to high
error rates in candidate selection. The transition from tra-
ditional machine learning to deep learning marked a sig-
niﬁcant shift in resume screening, enabling models to pro-
cess sequential and semantic text information. Convolu-
tional Neural Networks (CNNs), Recurrent Neural Net-
works (RNNs) and Long Short-Term Memory (LSTMs)
[15] were among the ﬁrst deep learning models applied to
resume screening, improving accuracy by capturing sequen-
tial dependencies in text data. Further advancements in-
4194


---

## Page 3

Figure 2. The evolution of AI-driven hiring technologies. This ﬁgure presents the transition of AI-driven hiring methods across three
major eras: traditional machine learning (2010-2016), deep learning (2016-2022), and large language models (2022-present). It highlights
key advancements in AI hiring technologies and notable case studies demonstrating their real-world applications [2–6].
troduced word embeddings (e.g., Word2Vec [32]), which
replaced keyword matching with semantic similarity, al-
lowing AI to recognize that terms like software engineer
and software developer are contextually related. However,
these embeddings are context-independent. More recently,
transformer-based models (e.g., BERT [33]) introduced
context-aware text understanding, enabling AI to assess re-
sume relevance in full-sentence representations rather than
isolated keywords. While deep learning improved resume
parsing, job matching, and ranking, these models required
large-scale labeled data for training, limiting their adapt-
ability across diverse hiring contexts. The advancements
of LLMs have transformed AI-driven resume screening, en-
abling zero-shot and few-shot learning to assess candidates
without extensive labeled training data. Unlike traditional
machine learning and early deep learning models, LLMs
could leverage large-scale pre-training to extract key re-
sume attributes, analyze job relevance, and infer contextual
qualiﬁcations dynamically.
Prior advancements, such as
Word2Vec and BERT, already improved semantic resume-
job matching, reducing reliance on exact keyword matches.
However, LLMs further enhance contextual reasoning, al-
lowing for deeper candidate evaluation, such as identifying
transferable skills (i.e., recognizing transferable skills such
as proﬁciency in C++ from experience with embedded sys-
tems or Python from data analysis projects, even if not ex-
plicitly stated in the resume) and inferring implicit qualiﬁ-
cations. Nevertheless, there are limited studies on applying
LLMs to resume screening [11, 34, 35], and key challenges
remain. For instances, LLMs rely on static pretraining data,
restricting their ability to adapt to dynamic hiring criteria
and evolving job requirements as mentioned.
2.3. LLMs with RAG
RAG has been widely explored in ﬁelds like customer
support [36], legal research [37], medicine [38, 39], ﬁ-
nance [40], and education [41, 42], enhancing LLMs by
integrating real-time, domain-speciﬁc information retrieval.
It improves accuracy, reduces hallucinations, and enables
context-aware decision-making [43]. However, its appli-
cation in resume screening remains limited, with most AI
resume screening systems relying on static embeddings
or rule-based models.
Exploring RAG-enhanced resume
screening could improve hiring procedure by integrating
real-time labor market data and hiring trends, offering a
more adaptive and intelligent screening process.
3. Problem Deﬁnition
Our framework enables dynamic, context-aware resume
screening by adapting evaluation scores based on the ap-
plied job role. Unlike traditional models with ﬁxed evalua-
tion scores, our framework assesses candidates using role-
speciﬁc standards. Given a resume R, the model generates
a score vector:
SJ = {SJ
S, SJ
K, SJ
W , SJ
B, SJ
E}
(1)
4195


---

## Page 4

Figure 3. Illustration of the proposed multi-agent framework for resume screening. The framework consists of four core agents:
Resume extractor, responsible for parsing and structuring resume content; Resume evaluator, which assigns scores based on predeﬁned
criteria while integrating external knowledge via RAG; Resume summarizer, which consists of three sub-agents that generate feedback
through collective decision-making, ensuring a comprehensive evaluation of the candidate’s strengths and weaknesses; Score formatter,
which organizes evaluation results into a structured format for future analysis. This modular approach enhances explainability and adapt-
ability, as recruiters can review each step of the evaluation process without requiring to examine the raw resume directly.
where SJ
S refers to the score of self-evaluation, SJ
K
refers to the score of skills & specialties, SJ
W
refers
to the score of work experience,
SJ
B
refers to the
score of basic information, SJ
E refers to the score of
education background and J refers to the applied job po-
sition. Each evaluation criterion is assigned a ﬁxed weight
across all job roles:
W = {wS, wK, wW , wB, wE},

wi = 1
(2)
where wi remains constant regardless of the applied job po-
sition. Besides, one of the most challenging aspects of this
work is role-speciﬁc scoring. A candidate applying for a HR
intern versus a HR director should receive different scores,
even with the same resume:
SIntern
W
> SDirector
W
(for low-experience candidates)
(3)
Different aspects of evaluation should be interpreted con-
textually based on job requirements. In our work, the LLM
generates job-speciﬁc evaluation scores via job applied J:
SJ = LLM(R, J).
(4)
The ﬁnal score for a candidate is computed as:
SJ
ﬁnal =

wiSJ
i ,
(5)
4. Detailed Information and Methodology
The proposed framework streamlines resume screening us-
ing a multi-agent approach, where different components
work together to analyze and evaluate job applications efﬁ-
ciently. The framework consists of four core agents: the re-
sume extractor, resume evaluator, resume summarizer, and
score formatter, each handling a speciﬁc task in the process
as shown in Figure 3. First, the resume extractor identiﬁes
key details from a candidate’s resume. Since resumes come
in different formats, this step ensures that all information is
structured in a clear and standardized way. Next, the resume
evaluator reviews the extracted details and assigns scores
based on how well the candidate’s qualiﬁcations match the
job requirements. The resume summarizer then generates
a concise, easy-to-understand report, highlighting the can-
didate’s strengths and areas for improvement. This helps
recruiters quickly assess candidates without going through
lengthy resumes. Finally, the score formatter standardizes
the evaluation output into a structured numerical format.
This ensures consistency in how candidate scores are pre-
sented, making it easier to compare applicants and integrate
results into decision-making systems.
4196


---

## Page 5

4.1. Resume extractor agent
The extractor agent, acting as the hiring assistant, leverages
reasoning capabilities of LLM to extract structured informa-
tion from unstructured text accurately, ensuring the precise
identiﬁcation of key details such as the 1) position applied
for (i.e., position name and its level: junior, mid-level, se-
nior, or leadership) 2) self-evaluation 3) skills & specialties
4) work experience (i.e., company name, duration, and re-
sponsibilities) 5) basic information, and 6) education back-
ground. Unlike traditional keyword-based extraction meth-
ods, the LLM processes unstructured text with contextual
understanding, allowing it to infer missing details, and rec-
ognize implicit skills.
4.2. Resume evaluator agent
The evaluator agent, functioning as a hiring manager, as-
signs scores based on ﬁve evaluation categories:
self-
evaluation (score: 0-1), skills & specialties (score: 0-2),
work experience (score: 0-4), basic information (score: 0-
1), and educational background (score: 0-2). Instead of re-
lying solely on predeﬁned rules, the evaluator agent lever-
ages RAG to dynamically retrieve company-speciﬁc hir-
ing criteria, job descriptions, and other relevant information
from an external source. The details of the RAG pipeline
can be structured as follows:
4.2.1. Vector embedding
All document (i.e., external source) chunks are encoded into
dense vector representations using an embedding function
fembed. Let the original job query (e.g., a job requirement)
and document chunks be denoted as qtext and di,text.
q = fembed(qtext),
di = fembed(di,text)
(6)
where q, di ∈RD, and D is the embedding dimension (i.e.,
we use OpenAIEmbeddings to generate dense vector repre-
sentations and ChromaDB as the vector database).
4.2.2. Cosine similarity computation
The relevance of document chunks to the query is quanti-
ﬁed using cosine similarity. For the query q and the i-th
document chunk di:
sim(q, di) =
q · di
∥q∥∥di∥
(7)
where sim(q, di) is the similarity between the vectors, with
higher values indicating greater relevance.
A relevance
threshold τ = 0.3 is used to ﬁlter out low-relevance doc-
ument chunks:
sim(q, di) ≥τ ⇐⇒Retrieve di
(8)
where q refers to the query and di refers to the document
chunks.
Figure 4. Query formulation for resume evaluation agent. The
query instructs the system to score extracted resume details by as-
sessing skills, work experience, and education in relation to the
applied job (J). It incorporates retrieved knowledge chunks (C) to
ensure job-speciﬁc scoring criteria are considered.
4.2.3. Contextual prompt construction
Retrieved chunks are formatted into a structured input
prompt P as follows:
P = concat(Q, J, C)
(9)
C = d(retrieved)
1
∪d(retrieved)
2
∪· · · ∪d(retrieved)
i
(10)
where C is the concatenation of the retrieved document
chunks, Q represents the query text, and J denotes the ap-
plied job position. The formatted prompt P serves as the
input to the evaluator agent, which processes the structured
information to assess the candidate’s background against
predeﬁned job-speciﬁc criteria and assigns a resume score
accordingly as shown in Figure 4.
4.2.4. Speciﬁc requirements from external sources
In addition to structured attributes such as university rank-
ings and professional certiﬁcations, we further analyze
historical resumes of outstanding candidates and incorpo-
rate up-to-date skill demands to reﬁne job-speciﬁc require-
ments. By leveraging LLM-driven summarization, we ex-
tract key qualiﬁcations, skills, and experience patterns from
past hires, establishing a dynamic baseline for evaluating
different job positions. This approach ensures that screen-
ing criteria remain relevant and adaptive to evolving indus-
try needs.
4.3. Resume summarizer agent
The summarizer agent functions as an hiring coordinator,
generating personalized resume feedback by analyzing a
candidate’s proﬁle against job requirements. It consists of
three sub-agents including the CEO agent, CTO agent, and
HR agent, which engage in an internal discussion to reﬁne
the feedback based on the scores provided by the evalua-
tor agent. The CEO agent assesses leadership potential, the
CTO agent evaluates technical expertise, and the HR agent
focuses on soft skills and cultural ﬁt. Through collabora-
tive reasoning, these sub-agents exchange insights, debate
strengths and weaknesses, and produce structured feedback.
This multi-agent approach ensures context-aware, balanced,
and actionable recommendations, enhancing the adaptabil-
ity and explainability of AI-driven resume evaluations.
4197


---

## Page 6

Table 1. Comparison of single LLMs and the multi-agent RAG-LLMs with different LLM backbones
Model
PC20↑*
SC20↑
PC15↑
SC15↑
PC10↑
SC10↑
MAE↓
Single LLM
GPT-4o
0.67
0.59
0.69
0.62
0.74
0.65
1.26
DeepSeek-V3
0.67
0.60
0.67
0.62
0.70
0.71
1.08
RAG-LLM (ours)
GPT-4o
0.69
0.66
0.72
0.70
0.80
0.74
1.05
DeepSeek-V3
0.70
0.66
0.75
0.69
0.84
0.74
0.90
*↑indicates that higher values are better, while ↓indicates that lower values are better. PC refers to Pearson Correlation, and SC refers to Spearman
Correlation. MAE refers to Mean Absolute Error. The number following PC/SC represents the percentage of scores used in the evaluation. For example,
PC10 evaluates model performance only on the subset of candidates whose ground truth scores lie in the top and bottom 10% percentiles.
Table 2. Ablation study of multi-agent RAG-LLMs with and with-
out resume extraction agent
Model
PC20
SC20
PC15
SC15
PC10
SC10
RAG-LLM
w/o extract.
GPT-4o
0.63
0.66
0.70
0.71
0.81
0.74
DS-V3
0.65
0.63
0.69
0.68
0.80
0.79
RAG-LLM
w/ extract.
GPT-4o
0.69
0.66
0.72
0.70
0.80
0.74
DS-V3
0.70
0.66
0.75
0.69
0.84
0.74
*DS-V3 refers to DeepSeek-V3
4.4. Score formatter agent
The score formatter agent (i.e., acting as the data curator)
standardizes the output of candidate evaluations into a struc-
tured format (e.g., [1.0, 1.5, 3.5, 0.8, 1.5]), ensuring consis-
tency across different assessment components. It takes raw
scores generated by various evaluation agents (e.g., expe-
rience, skills, education) and converts them into a uniform
numerical array for downstream processing. This structured
output enables easy integration with ranking models and
decision-making pipelines.
5. Experimental Results
Our LLM-driven resume screening system is implemented
using CrewAI, which coordinates multiple AI agents to
enable structured and automated resume evaluation. The
framework runs on a PC equipped with an NVIDIA A6000
GPU, ensuring efﬁcient processing of large-scale resume
data.
It integrates LLMs via the OpenRouter API, uti-
lizing models such as DeepSeek-V3, and GPT-4o, with
LangChain facilitating seamless interaction between com-
ponents.
For RAG, the system employs ChromaDB as
a vector database for efﬁcient semantic search, enabling
retrieval of relevant hiring criteria and context-aware job
matching. Additionally, OpenAI embeddings are used to
generate dense vector representations, enhancing the accu-
racy of similarity-based retrieval. Note that for users requir-
ing local implementation due to privacy concerns, Ollama
can be integrated to facilitate the local execution of LLMs.
5.1. Dataset
We evaluated our model on a dataset consisting of 105 fully
anonymized online resumes. The dataset was labeled by
HR professionals, who assigned scores based on ﬁve key
aspects: self-evaluation, skills & specialties, work experi-
ence, basic information, and education. To ensure privacy,
all personally identiﬁable information, including names and
company names, was removed. The resumes in the dataset
correspond to various job positions, primarily in the ﬁeld
of human resources. The job levels can be categorized into
four groups: junior, mid-level, senior, and leadership. The
junior-level positions include HR intern and HR assistant,
while the mid-level roles consist of HR associate and HR
specialist. Senior-level positions include HR manager and
senior HR, whereas leadership roles encompass HR director
and strategic HR partner.
5.2. Evaluation metrics
To evaluate our proposed resume screening system, we
employ the following evaluation metrics: a) Pearson cor-
relation measures the linear relationship between the AI-
estimated scores and the human reviewer scores. This met-
ric helps evaluate if the AI system assigns scores in a man-
ner similar to human evaluators b) Spearman correlation as-
sesses the rank-based monotonic relationship between AI
and human reviewer scores. Unlike Pearson correlation, it
captures non-linear relationships by ranking the scores be-
fore computing the correlation c) MAE measures the abso-
lute difference between AI predictions and HR scores, cap-
turing the average magnitude of errors. This metric is par-
ticularly useful in understanding the extent of AI’s deviation
from human judgment.
5.3. Performance of multi-agent RAG-LLMs
5.3.1. Comparison with single model approaches
To evaluate the effectiveness of the proposed multi-agent
RAG-LLMs, we ﬁrst compare their performance against
single LLMs across multiple evaluation metrics. Table 1
presents results using different LLM backbones, includ-
ing GPT-4o and DeepSeek-V3.
The results demonstrate
that our proposed RAG-LLM framework achieves satis-
factory performance and consistently outperforms single
LLMs, conﬁrming its robustness and reliability in AI-driven
resume screening. Our evaluation focuses on candidates
whose ground truth scores fall within the top and bot-
tom 10%, 15%, and 20% percentiles, enabling a more nu-
anced analysis of ranking performance under varying se-
4198


---

## Page 7

Figure 5. Comparison of candidate scores assigned by human
evaluators (HR) and a RAG-LLM (DeepSeek-V3). (a) The scat-
ter plot showing the distribution of scores (b) Histogram showing
the number of candidates in each score range based on HR and
LLM evaluations.
Figure 6. Comparison of candidate scores estimated by human
evaluators (HR) and RAG-LLM (DeepSeek-V3) across differ-
ent resume attributes. The scatter plot visualizes the distribution
of scores across ﬁve main categories.
lection thresholds. As shown in Table 1, our RAG-LLM
with DeepSeek-V3 achieves the highest Pearson correlation
(PC10 = 0.84, p-value < 0.001), Spearman correlation
(SC10 = 0.74, p-value < 0.001), and lowest MAE (0.90),
outperforming single LLM baselines. Similar trends per-
sist across the 15% and 20% thresholds, highlighting RAG-
LLM’s consistent ability to accurately differentiate top-tier
candidates from lower-performing ones, ensuring stable and
reliable assessments. For borderline candidates, discrepan-
cies between human evaluations and LLM predictions may
arise due to subjective judgment, but such variations are ex-
pected and fall within a reasonable margin.
5.3.2. Evaluating the impact of extraction agent
We further conducted an ablation study to assess the im-
pact of the resume extraction agent, as presented in Table
2. The results show that incorporating structured extraction
consistently improves Pearson correlation (PC) and Spear-
man correlation (SC) across all evaluation thresholds, with
DeepSeek-V3 achieving the highest performance when us-
ing the extraction module. These ﬁndings highlight the im-
portance of high-quality structured resume parsing in en-
hancing LLM-based candidate evaluations.
5.3.3. Comparison of AI and human resume screening
To assess the alignment between human evaluators (HR)
and the RAG-LLM model, we analyze the score distribu-
tions of both systems. Figure 5(a) presents a scatter plot
comparing candidate scores assigned by HR and RAG-
LLM (DeepSeek-V3), where the mean scores remain close
(i.e., 7.68 for HR vs.
7.76 for LLM), indicating high
agreement. Figure 5(b) further illustrates this distribution
through a histogram, showing that the number of candidates
in each score range follows a similar pattern between HR
and LLM. These results suggest that RAG-LLM not only
achieves strong correlation with human evaluations but also
maintains score distribution consistency, reinforcing its reli-
ability for AI-driven hiring applications. Besides, we evalu-
ate the alignment between HR and RAG-LLM assessments
across different resume attributes, as shown in Figure 6,
which compares the score distributions for self-evaluation,
skills & specialties, work experience, basic information,
and education background.
5.4. Qualitative analysis of feedback system
As shown in Figure 7 , the summarizer agent consolidates
insights from multiple sub-agents, allowing for traceable
evaluations.
This process reduces recruiter workload by
highlighting key strengths and pinpointing missing compe-
tencies, eliminating the need for manual resume reviews.
Additionally, the system dynamically adapts feedback to
different job roles, ensuring that recommendations align
with position-speciﬁc requirements.
To further improve
usability, these insights can even be presented in bullet
points that summarize strengths and weaknesses, allowing
recruiters to efﬁciently compare multiple candidates.
6. Discussion
With the advancement of LLMs and multi-agent systems,
AI-driven resume screening has become more effective and
reliable than ever.
Our study demonstrates that a multi-
agent approach offers several advantages over traditional
4199


---

## Page 8

Figure 7. Qualitative analysis of resume screening feedback. Targeted recommendations generated by the summarizer agent after
internal discussion among multiple sub-agents (i.e., CEO, CTO, HR agent).
single deep learning models or single LLM-driven screen-
ing, particularly in terms of explainability, decision efﬁ-
ciency, and evaluation reliability. One of the most notable
ﬁndings is that the modular architecture of our system po-
tentially enhances transparency and explainability in AI-
driven resume screening. Unlike single model approaches,
where recruiters receive only a ﬁnal score without insight
into the reasoning process, our system decomposes resume
evaluation into multiple specialized agents. This modularity
allows for step-by-step tracking of how each extracted infor-
mation contributes to the ﬁnal assessment, improving over-
all decision accountability. Furthermore, our study high-
lights an important technical consideration. The extraction
agent has a measurable impact on the assessment quality.
Speciﬁcally, we found that extraction can enhance evalua-
tion by structuring the input data more effectively. How-
ever, its effectiveness depends on the model’s reasoning
ability, particularly in determining what information should
be extracted. Models with stronger reasoning capabilities
and a larger number of parameters tend to perform better in
this step. This suggests that model selection is crucial, es-
pecially in systems where the quality of extraction directly
inﬂuences the reliability of post-extraction evaluation.
7. Future Work
In future work, the integration of multimodal data in LLM-
driven hiring has great potential. Current LLM-driven hir-
ing systems mainly focus on text-based resume evaluation,
limiting the assessment of soft skills and communication
abilities. Incorporating LLM-driven video interview anal-
ysis alongside textual evaluation could further provide a
more comprehensive assessment of candidate suitability.
The system may also generate suitable aptitude and atti-
tude tests to validate a candidate’s actual capabilities (i.e.,
to verify whether the individual can truly perform the skills
or tasks they claim to possess). Apart from this, bias in
AI-driven hiring remains a critical concern due to imbal-
anced training data (e.g., certain demographic groups are
underrepresented in the dataset). RAG presents a poten-
tial solution by enabling the dynamic retrieval of diverse
and up-to-date hiring criteria, reducing reliance on static,
historically biased datasets.
Future work should explore
bias-aware retrieval mechanisms and ranking strategies to
enhance the equity and transparency of automated evalua-
tions. Last, privacy considerations in AI-driven hiring re-
main a critical area for future research, especially as LLMs
inference APIs become integral to downstream applica-
tions. While external APIs enhance model effectiveness,
they also introduce risks of exposing sensitive data to third-
party providers. Companies with sufﬁcient computational
resources may opt for local LLM deployment to reduce
these risks. The future of AI-driven hiring will likely focus
on privacy-preserving architectures that enable API-based
inference while ensuring compliance with data protection
regulations (e.g., GDPR, CCPA). End-to-end encrypted in-
ference techniques, enabling LLMs to compute without di-
rectly accessing sensitive data, along with Model Context
Protocol (MCP) for structured data ﬂow and context man-
agement, are emerging as key research directions. Their
integration is expected to play a crucial role in developing
secure, scalable, and legally compliant AI-driven hiring sys-
tems in the future.
8. Conclusion
In this work, we proposed a multi-agent framework for re-
sume screening using RAG-LLMs. The framework is de-
signed with four core agents that work together to extract
key resume information, evaluate candidates based on pre-
deﬁned scoring criteria, generate a concise evaluation sum-
mary, and format the output in a structured manner. By
leveraging RAG, the system can assess resumes against
company-speciﬁc scoring criteria in a context-aware and
tailored manner without requiring model retraining or ﬁne-
tuning. To evaluate the effectiveness of our approach, we
tested the model using online resume datasets and compared
its performance against HR evaluations. The results demon-
strated that our proposed framework achieved comparable
performance to human evaluators, highlighting the poten-
tial of LLMs as an alternative solution for automated and
scalable AI hiring.
4200


---

## Page 9

References
[1] Arvind Kumar Sinha, Md Amir Khusru Akhtar, and Ashwani
Kumar. Resume screening using natural language process-
ing and machine learning: A systematic review. Machine
Learning and Information Processing: Proceedings of ICM-
LIP 2020, pages 207–214, 2021. 1
[2] LinkedIn Corporate Communications. Linkedin to acquire
bright, 2014. URL https://news.linkedin.com/
2014/02/linkedin-to-acquire-bright.
Ac-
cessed: 2023-03-14. 3
[3] Forbes.
Checkr — company overview & news, 2024.
URL https : / / www . forbes . com / companies /
checkr/. Accessed: 2025-03-14.
[4] Forbes.
Recruiters and job candidates love talking with
this ai assistant, 2019. URL https://www.forbes.
com/sites/sap/2019/08/06/recruiters-and-
job-candidates-love-talking-with-this-
ai-assistant/. Accessed: 2025-03-14.
[5] Google Cloud.
Google introduces hire, a new recruiting
app that integrates with g suite, 2017.
URL https://
cloud.google.com/blog/products/g-suite/
google- introduces- hire- new- recruiting-
app-integrates-g-suite. Accessed: 2025-03-14.
[6] Ms Swati Samadhiya and Archana Awasthi. Importance of
artiﬁcial intelligence in hiring and recruitment process. of the
Book: A Flourishing Digital Era: Innovations in Industry,
Education, 1(1):524, 2022. 3
[7] Jiankai Sun, Chuanyang Zheng, Enze Xie, Zhengying
Liu, Ruihang Chu, Jianing Qiu, Jiaqi Xu, Mingyu Ding,
Hongyang Li, Mengzhe Geng, et al. A survey of reasoning
with foundation models. arXiv preprint arXiv:2312.11562,
2023. 2
[8] Daniel-Costel Bouleanu, Marco Alfredo Loaiza Carrillo,
Costin B˘adic˘a, Raffaele Gravina, and Giancarlo Fortino.
Beneﬁts of agent-oriented transitioning from monolithic to
service-based architectures. In 2024 International Confer-
ence on INnovations in Intelligent SysTems and Applications
(INISTA), pages 1–6. IEEE, 2024. 2
[9] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio
Petroni, Vladimir Karpukhin, Naman Goyal,
Heinrich
K¨uttler, Mike Lewis, Wen-tau Yih, Tim Rockt¨aschel, et al.
Retrieval-augmented generation for knowledge-intensive nlp
tasks. Advances in neural information processing systems,
33:9459–9474, 2020. 2
[10] Jianing Qiu, Kyle Lam, Guohao Li, Amish Acharya,
Tien Yin Wong, Ara Darzi, Wu Yuan, and Eric J Topol. Llm-
based agentic systems in medicine and healthcare. Nature
Machine Intelligence, 6(12):1418–1420, 2024. 2
[11] Chengguang Gan, Qinghao Zhang, and Tatsunori Mori. Ap-
plication of llm agents in recruitment: A novel framework for
resume screening. arXiv preprint arXiv:2401.08315, 2024.
2, 3
[12] Riya Pal, Shahrukh Shaikh, Swaraj Satpute, and Sumedha
Bhagwat.
Resume classiﬁcation using various machine
learning algorithms. In ITM web of conferences, volume 44,
page 03011. EDP Sciences, 2022. 2
[13] Irfan Ali, Nimra Mughal, Zahid Hussain Khand, Javed
Ahmed, and Ghulam Mujtaba. Resume classiﬁcation sys-
tem using natural language processing and machine learning
techniques. Mehran University Research Journal Of Engi-
neering & Technology, 41(1):65–79, 2022.
[14] Kameni Florentin Flambeau Jiechieu and Norbert Tsopze.
Skills prediction based on multi-label resume classiﬁcation
using cnn with model predictions explanation. Neural Com-
puting and Applications, 33(10):5069–5087, 2021.
[15] Amirreza Jalili, Hamed Tabrizchi, Jafar Razmara, and Amir
Mosavi. Bilstm for resume classiﬁcation. In 2024 IEEE 22nd
World Symposium on Applied Machine Intelligence and In-
formatics (SAMI), pages 000519–000524. IEEE, 2024. 2
[16] Shabna Nasser, C Sreejith, and M Irshad. Convolutional neu-
ral network with word embedding based approach for resume
classiﬁcation. In 2018 International Conference on Emerg-
ing Trends and Innovations In Engineering And Technologi-
cal Research (ICETIETR), pages 1–6. IEEE, 2018.
[17] S Ramraj, V Sivakumar, et al. Real-time resume classiﬁ-
cation system using linkedin proﬁle descriptions. In 2020
International Conference on Computational Intelligence for
Smart Power System and Sustainable Energy (CISPSSE),
pages 1–4. IEEE, 2020.
[18] Panagiotis Skondras, Panagiotis Zervas, and Giannis Tzimas.
Generating synthetic resume data with large language mod-
els for enhanced job description classiﬁcation. Future Inter-
net, 15(11):363, 2023.
[19] S Bharadwaj, Rudra Varun, Potukuchi Sreeram Aditya,
Macherla Nikhil, and G Charles Babu. Resume screening
using nlp and lstm. In 2022 international conference on in-
ventive computation technologies (ICICT), pages 238–241.
IEEE, 2022. 2
[20] K
Satheesh,
A
Jahnavi,
L
Iswarya,
K
Ayesha,
G Bhanusekhar, and K Hanisha.
Resume ranking based
on job description using spacy ner model.
International
Research Journal of Engineering and Technology, 7(05):
74–77, 2020. 2
[21] K Tejaswini, V Umadevi, Shashank M Kadiwal, and San-
jay Revanna. Design and development of machine learning
based resume ranking system. Global Transitions Proceed-
ings, 3(2):371–375, 2022. 2
[22] Agata Mirowska and Laura Mesnet.
Preferring the devil
you know: Potential applicant reactions to artiﬁcial intelli-
gence evaluation of interviews. Human Resource Manage-
ment Journal, 32(2):364–383, 2022. 2
[23] Padma
Jyothi
Uppalapati,
Madhavi
Dabbiru,
and
Venkata Rao Kasukurthi.
Ai-driven mock interview
assessment:
leveraging generative language models for
automated evaluation.
International Journal of Machine
Learning and Cybernetics, pages 1–23, 2025.
[24] Changwoo Kim, Jinho Choi, Jongyeon Yoon, Daehun Yoo,
and Woojin Lee.
Fairness-aware multimodal learning in
automatic video interview assessment.
IEEE Access, 11:
122677–122693, 2023.
[25] Sri Roshan RK, GS Vidharsana, et al. Ai-enhanced eye track-
ing for candidate assessment in job interviews. In 2025 6th
International Conference on Mobile Computing and Sustain-
able Informatics (ICMCSI), pages 810–815. IEEE, 2025. 2
4201


---

## Page 10

[26] Sayan Das, Rupashri Barik, and Ayush Mukherjee. Salary
prediction using regression techniques. Proceedings of In-
dustry Interactive Innovations in Science, Engineering &
Technology (I3SET2K19), 2020. 2
[27] Sananda Dutta, Airiddha Halder, and Kousik Dasgupta. De-
sign of a novel prediction engine for predicting suitable
salary for a job. In 2018 Fourth International Conference on
Research in Computational Intelligence and Communication
Networks (ICRCICN), pages 275–279. IEEE, 2018. 2
[28] Ketki V Deshpande, Shimei Pan, and James R Foulds. Miti-
gating demographic bias in ai-based resume ﬁltering. In Ad-
junct publication of the 28th ACM conference on user mod-
eling, adaptation and personalization, pages 268–275, 2020.
2
[29] Kyra Wilson and Aylin Caliskan. Gender, race, and intersec-
tional bias in resume screening via language model retrieval.
In Proceedings of the AAAI/ACM Conference on AI, Ethics,
and Society, volume 7, pages 1578–1590, 2024.
[30] Le Chen, Ruijun Ma, Anik´o Hann´ak, and Christo Wilson.
Investigating the impact of gender on rank in resume search
engines. In Proceedings of the 2018 chi conference on human
factors in computing systems, pages 1–14, 2018.
[31] Dena F Mujtaba and Nihar R Mahapatra. Ethical consider-
ations in ai-based recruitment. In 2019 IEEE International
Symposium on Technology and Society (ISTAS), pages 1–7.
IEEE, 2019. 2
[32] Kenneth Ward Church. Word2vec. Natural Language Engi-
neering, 23(1):155–162, 2017. 3
[33] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina
Toutanova. Bert: Pre-training of deep bidirectional trans-
formers for language understanding. In Proceedings of the
2019 conference of the North American chapter of the asso-
ciation for computational linguistics: human language tech-
nologies, volume 1 (long and short papers), pages 4171–
4186, 2019. 3
[34] Esmail Salakar, Jivitesh Rai, Aayush Salian, Yasha Shah,
and Jyoti Wadmare. Resume screening using large language
models. In 2023 6th International Conference on Advances
in Science and Technology (ICAST), pages 494–499. IEEE,
2023. 3
[35] Srushti Haryan, Rupin Malik, Prathamesh Redij, and Sujata
Kulkarni. Fairhire: A fair and automated candidate screen-
ing system. In International Conference on Machine Intel-
ligence, Tools, and Applications, pages 372–382. Springer,
2024. 3
[36] Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie
Wang, Manasi Deshpande, Xiaofeng Wang, and Zheng Li.
Retrieval-augmented generation with knowledge graphs for
customer service question answering. In Proceedings of the
47th International ACM SIGIR Conference on Research and
Development in Information Retrieval, pages 2905–2909,
2024. 3
[37] Nirmalie Wiratunga, Ramitha Abeyratne, Lasal Jayawar-
dena, Kyle Martin, Stewart Massie, Ikechukwu Nkisi-Orji,
Ruvan Weerasinghe, Anne Liret, and Bruno Fleisch. Cbr-
rag: case-based reasoning for retrieval augmented generation
in llms for legal question answering. In International Con-
ference on Case-Based Reasoning, pages 445–460. Springer,
2024. 3
[38] Cyril Zakka, Rohan Shad, Akash Chaurasia, Alex R
Dalal,
Jennifer L Kim,
Michael Moor,
Robyn Fong,
Curran Phillips, Kevin Alexander, Euan Ashley, et al.
Almanac—retrieval-augmented language models for clinical
medicine. Nejm ai, 1(2):AIoa2300068, 2024. 3
[39] Guangzhi Xiong, Qiao Jin, Zhiyong Lu, and Aidong Zhang.
Benchmarking retrieval-augmented generation for medicine.
In Findings of the Association for Computational Linguistics
ACL 2024, pages 6233–6251, 2024. 3
[40] Antonio Jimeno Yepes, Yao You, Jan Milczek, Sebastian
Laverde, and Renyu Li.
Financial report chunking for
effective retrieval augmented generation.
arXiv preprint
arXiv:2402.05131, 2024. 3
[41] Zachary Levonian, Chenglu Li, Wangda Zhu, Anoushka
Gade, Owen Henkel, Millie-Ellen Postle, and Wanli Xing.
Retrieval-augmented generation to improve math question-
answering: Trade-offs between groundedness and human
preference. arXiv preprint arXiv:2310.03184, 2023. 3
[42] Hao Wei, Jianing Qiu, Haibao Yu, and Wu Yuan. Medco:
Medical education copilots based on a multi-agent frame-
work. European Conference on Computer Vision Workshop,
2024. 3
[43] Huayang Li, Yixuan Su, Deng Cai, Yan Wang, and Lemao
Liu. A survey on retrieval-augmented text generation. arXiv
preprint arXiv:2202.01110, 2022. 3
4202
