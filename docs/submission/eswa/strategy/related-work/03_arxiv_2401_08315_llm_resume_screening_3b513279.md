## Page 1

Application of LLM Agents in Recruitment: A Novel Framework for
Resume Screening
Chengguang Gan1
Qinghao Zhang2
Tatsunori Mori1
1Yokohama National University, Japan
gan-chengguan-pw@ynu.jp, tmori@ynu.ac.jp
2Department of Information Convergence Engineering,
Pusan National University, South Korea
zhangqinghao@pusan.ac.kr
Abstract
The automation of resume screening is a crucial
aspect of the recruitment process in organiza-
tions. Automated resume screening systems
often encompass a range of natural language
processing (NLP) tasks. This paper introduces
a novel Large Language Models (LLMs) based
agent framework for resume screening, aimed
at enhancing efficiency and time management
in recruitment processes. Our framework is
distinct in its ability to efficiently summarize
and grade each resume from a large dataset.
Moreover, it utilizes LLM agents for decision-
making. To evaluate our framework, we con-
structed a dataset from actual resumes and
simulated a resume screening process. Subse-
quently, the outcomes of the simulation experi-
ment were compared and subjected to detailed
analysis. The results demonstrate that our auto-
mated resume screening framework is 11 times
faster than traditional manual methods. Further-
more, by fine-tuning the LLMs, we observed a
significant improvement in the F1 score, reach-
ing 87.73%, during the resume sentence clas-
sification phase. In the resume summarization
and grading phase, our fine-tuned model sur-
passed the baseline performance of the GPT-3.5
model (Ouyang et al., 2022). Analysis of the
decision-making efficacy of the LLM agents in
the final offer stage further underscores the po-
tential of LLM agents in transforming resume
screening processes.
1
Introduction
Resume screening is a crucial aspect of recruitment
for all companies, particularly larger ones, where
it becomes a labor-intensive and time-consuming
endeavor. In contrast to smaller firms, a large corpo-
ration might receive thousands of resumes during
a hiring phase, making efficient screening of these
numerous applications a significant challenge. To
reduce labor costs associated with resume screen-
ing, developing an automated framework is essen-
tial. Utilizing natural language processing (NLP)
Resume
Text Classification
Unstructured Text
Grade/Evaluation & Summarization
Resume
Structured Text
HR
Manual Screening
Automated Screening
Resume
Figure 1: The Process of automated resume screening.
technology for this purpose is increasingly becom-
ing the preferred approach.
The automated resume screening (Singh et al.,
2010a) process encompasses two primary compo-
nents: information extraction (Singhal et al., 2001)
and evaluation. As illustrated in Figure 1, resumes
typically exist as unstructured or semi-structured
text, varying in format. The initial step of the au-
tomated framework is to convert this unstructured
text into a structured format. This process involves
a key NLP task: text classification (Bayer et al.,
2022), specifically sentence classification (Minaee
et al., 2021). It entails extracting and classifying
sentences related to personal information, educa-
tion, and work experience, transforming them into
structured data that is easily stored and manipu-
lated.
Upon structuring the resume text, it must then
arXiv:2401.08315v2  [cs.CL]  13 Aug 2024


---

## Page 2

be summarized and evaluated. The lower part of
Figure 1 depicts this process, which includes both
automatic and manual screening. Manual screen-
ing involves grading and summarizing extensive
sections of the resume text, after which the graded
and summarized resumes are presented to HR for
review, leading to the selection of qualified can-
didates. This approach significantly reduces the
time HR personnel spend perusing resumes and de-
liberating decisions by shortening the resume text
and implementing a grading system for ranking.
The aim is to enhance the efficiency of the screen-
ing process. NLP technology can also automate
this process, culminating in the output of qualified
resumes.
Corpus
Langugae Model
Unsupervised
Learning
Pre-trained
Langugae Model
Task-specific PLM
Fine-tune
Donwstream
Task Dataset
Figure 2: The illustration reprehsents the process of
pre-training a language model and applying the pre-
trained language model to a downstream task through
fine-tuning method.
In the preceding discussion, we elucidated two
NLP tasks pertinent to the automated extraction of
information from resumes. Addressing these tasks
necessitates the employment of Language Models
(LMs) . Presently, the most prevalent infrastructure
for LMs is the transformer architecture (Vaswani
et al., 2017), distinguished by its attention mech-
anism. These LMs are predominantly trained on
extensive corpora, endowing them with a broad
spectrum of knowledge. The seq2seq (sequence-
to-sequence) (Sutskever et al., 2014) structure is
instrumental in this context, enabling the conver-
sion of an input sequence into a predicted output
sequence. This mechanism facilitates the adaptabil-
ity of LMs to a diverse range of NLP tasks.
As illustrated in Figure 2, the process of LMs
spans from their training to their application in
various downstream NLP tasks. The initial phase
involves assembling a substantial corpus for unsu-
pervised learning, encompassing a broad array of
general knowledge. This corpus is typically derived
from sources such as Wikipedia 1 and extensive
web content. Subsequently, these voluminous, un-
labeled corpora serve as the foundation for training
LMs. Through this process, LMs acquire founda-
tional linguistic competencies and general knowl-
edge autonomously. Following the pre-training
phase, Pre-trained Language Models (PLMs) (Min
et al., 2023) undergo fine-tuning (Ding et al., 2023)
with different datasets tailored to specific down-
stream tasks. The culmination of this process is
the development of task-specific PLMs, capable of
effectively predicting or processing relevant NLP
tasks.
The initial PLMs, such as BERT (Devlin et al.,
2018), T5 (Raffel et al., 2020), and GPT-2 (Rad-
ford et al., 2019), were characterized by their rel-
atively modest size, containing only several hun-
dred million parameters. However, the advent of
GPT-3 (Brown et al., 2020) marked a significant
leap in this field, boasting an impressive 135 bil-
lion parameters. This escalation was not merely
quantitative but also qualitative, as evidenced by
the subsequent development of ChatGPT (Ouyang
et al., 2022). ChatGPT underscored how expanding
the pre-trained corpus and increasing the parameter
count of PLMs could substantially enhance their
capabilities, thereby heralding a new era in the
development of Large Language Models (LLMs)
(Zhao et al., 2023).
Despite these advancements, concerns have
arisen regarding the closed-source models devel-
oped by major corporations, particularly in terms
of user security. The primary issue lies in the po-
tential for private information leakage. Utilizing
these LLMs typically requires users to upload their
data, creating a risk of data compromise. This
is especially pertinent in applications like resume
screening, where sensitive personal information is
involved. In contrast to closed-source models like
GPT-3.5 and GPT-4 (OpenAI et al., 2023), there are
open-source LLMs available, such as LLaMA1/2
(Touvron et al., 2023a,b). While these open-source
1https://www.wikipedia.org/


---

## Page 3

models may not yet match the capabilities of their
closed-source counterparts, they offer a significant
advantage: the ability to run locally on a user’s
machine. This local execution ensures greater secu-
rity for private data, making these models a more
secure option for handling sensitive information.
The preceding overview delineates the particu-
lar NLP tasks essential for the automated resume
screening framework.
Additionally, it is high-
lighted that the tasks, as marked by the blue blocks
in Figure 1, are manageable through PLMs and
LLMs. A succinct explanation of the fundamen-
tal principles of LMs is also provided.
Subse-
quent paragraphs will offer a comprehensive ex-
position on the implementation of an automated
resume screening system utilizing agents derived
from LLMs.
LLM Agent
Character
Memory
Planning
Action
Figure 3: The illustration depict LLM as the backbone
of the agent system.
Figure 3 presents a schematic representation of
a fundamental agent system. This diagram illus-
trates the segmentation of Language Model (LLM)
agents into four core components: Character, Mem-
ory, Planning, and Action. Initially, the LLM agent
is assigned a distinct character, essentially defin-
ing its role or function. For instance, in this study,
the LLM agent is designated as an adept Human
Resources (HR) professional. This role encapsu-
lates the responsibilities and duties expected of
the LLM agent. Subsequently, ’Memory’ pertains
to the requisite knowledge base necessary for the
agent to execute its role effectively. In the con-
text of an HR professional, this encompasses a
comprehensive understanding of employee skill re-
quirements, salary management, and relevant laws
and regulations. This aspect is analogous to an
LLM’s capability to access and utilize its inter-
nal knowledge database. The next phase involves
’Planning,’ where the LLM agent strategizes the
execution of tasks. This process entails decom-
posing a complex task into smaller, manageable
subtasks, thereby enhancing the efficiency in ad-
dressing intricate assignments. This stage is indica-
tive of an LLM’s reasoning and problem-solving
abilities. Finally, the ’Action’ component repre-
sents the implementation stage. In the context of
an automated resume screening system, this would
involve the LLM agent filtering and selecting re-
sumes that align with specific job requirements.
This final stage exemplifies the practical applica-
tion of the LLM agent’s planning and reasoning in
a real-world scenario.
In this study, we integrate a LLM agent into the
process of automated resume screening. We pro-
pose an innovative framework that leverages the
LLM agent for automated extraction and analysis
of resumes. This framework streamlines the entire
process, from initial resume screening to the final
selection of qualified candidates, significantly en-
hancing the efficiency of this task. For our analysis,
we utilized a publicly available IT industry-specific
resume dataset2, optimized for sentence classifica-
tion. Through fine-tuning of the LLM, we achieved
an F1 score of 87.73 in sentence classification. This
improvement is particularly notable in the model’s
ability to identify and exclude personal informa-
tion from resumes, thereby mitigating the risk of
privacy breaches when employing models like GPT-
3.5/4. Additionally, we developed an HR Agent,
designed to both grade and summarize resumes.
We created a specialized Grade & Summarization
Resume (GSR) dataset, derived from the initial
dataset, using the GPT-4 model. This GSR dataset
was instrumental in evaluating other LLMs. In
these evaluations, the LLaMA2-13B model, once
fine-tuned, achieved a ROUGE-1 score of 37.30 in
summarization and a Grade accuracy of 81.35, sig-
nificantly surpassing the baseline GPT-3.5-Turbo
model. Finally, we deployed the HR Agent to select
suitable candidates, further analyzing the decision-
making outcomes.
In addition, we conducted experiments using
GPT-4-Turbo and GPT-3.5-Turbo-16k to demon-
strate that LLMs are capable of processing long-
context resume information effectively. To further
validate the effectiveness of our proposed LLM-
based resume screening framework, we randomly
selected 50 resumes for manual summarization
2https://huggingface.co/datasets/
ganchengguang/resume_seven_class


---

## Page 4

and evaluation. The performance of the LLMs
was benchmarked against this manually labeled
dataset. Our analysis of the experiments and spe-
cific samples indicated that LLMs’ evaluations and
decisions closely resemble those of human review-
ers. Additionally, to assess the framework’s abil-
ity to meet complex recruitment requirements, we
incorporated additional criteria beyond the basic
requirements into the framework. The decision-
making outcomes were then analyzed to determine
the adaptability of the LLMs to these enhanced
requirements.
Our comprehensive experiments and analysis
demonstrate the LLM agent’s robust capability in
resume screening. As an HR agent, it effectively
facilitates the candidate selection process.
2
Related Work
2.1
Resume Information Extraction
Resume screening is a classic application of infor-
mation extraction, evolving from rule-based meth-
ods (Mooney, 1999) to the use of toolkits for au-
tomating these rules (Ciravegna and Lavelli, 2004).
Over time, techniques such as Hidden Markov
Models (HMM) and Support Vector Machines
(SVM) developed into Cascaded Hybrid Models
for segment classification in resumes (Yu et al.,
2005). The adoption of deep learning, utilizing
Convolutional Neural Networks (CNNs) and Long
Short-Term Memory networks (LSTMs), further
enhanced extraction methods (Harsha et al., 2022;
Sinha et al., 2021; Kinge et al., 2022; Ali et al.,
2022; Bharadwaj et al., 2022; Zu and Wang, 2019;
Barducci et al., 2022), with Conditional Random
Fields (CRFs) improving LSTM models by refining
sequence labeling (Ayishathahira et al., 2018).
Recent advances incorporate pre-trained lan-
guage models like BERT, integrated with LSTMs
and CRFs, significantly enhancing contextual un-
derstanding for resume information extraction (Tal-
lapragada et al., 2023). This has been applied in
developing algorithms for automating recruitment,
with applications in ranking candidates for specific
jobs (Erdem, 2023).
Additionally, new tools such as PROSPECT
have been developed to support resume screening
by extracting and ranking candidate skills and expe-
riences using CRFs (Singh et al., 2010b). Another
approach involves using NLP and similarity mea-
sures to improve the efficiency of job candidate
selection through automated systems that match re-
sumes with job descriptions (Daryani et al., 2020).
2.2
Large Language Model in Recruit
Application
After the advent of LLM, there were other jobs that
used LLM in the recruitment process. The work
(Du et al., 2024) introduces an LLM-based GANs
Interactive Recommendation (LGIR) method that
enhances job recommendation systems by using
Generative Adversarial Networks to refine resume
representations, improving the accuracy of job
matching by overcoming issues of fabricated con-
tent and insufficient data. JobRecoGPT (Ghosh and
Sadaphal, 2023) explores four job recommendation
methods using LLMs to analyze unstructured job
and candidate data, highlighting advantages, limi-
tations, and efficiency in IT domain job matching.
2.3
Decision Making with LLM Agent
In addition, the LLM agent is employed in decision-
making processes across various applications. This
paper (Huang et al., 2024) evaluates the decision-
making capabilities of LLMs in complex multi-
agent environments using a novel framework. This
paper (Ma et al., 2024) introduces a novel frame-
work, Human-AI Deliberation, designed to en-
hance AI-assisted decision-making by fostering
a deliberative dialogue between humans and AI.
(Chen et al., 2023) introduces "Introspective Tips,"
a novel approach for enhancing the decision-
making capabilities of LLMs without the need for
fine-tuning. (Wei et al., 2022) highlights that en-
hanced decision-making abilities can be achieved
by incorporating a series of intermediate reasoning
steps. (Yao et al., 2022) presents ReAct, a novel
method that integrates reasoning with action gen-
eration, enhancing the synergy between language
comprehension and decision-making in interactive
tasks.
2.4
Compare LLM-based Resume Screening
and Traditional Methods
The application of LLMs to resume screening
frameworks offers significant advantages over tra-
ditional methods. Firstly, unlike PLMs which are
constrained to processing a maximum of 512 to-
kens, LLMs can manage considerably longer texts.
This capability allows LLMs to effectively handle
resumes of virtually any length, enhancing the com-
prehensiveness of the screening process. Secondly,
LLMs possess a broader knowledge base, enabling


---

## Page 5

Resume
Segment to
Sentence
Sentence 1
Sentence 2
Sentence 3
... ... 
Open Source
LLMs
Segmented
Resume Sentence
Label       Sentence
Expreinece
Exprience in IT ...
Personal
Information
Name: Mike ...
Education
MIT University ...
...
...  ...
Remove
Personal
Information
Grade & Summarization
HR Agent
Grade & Summarization
Resume 1
90/100
Summary Text 1
Resume 2
85/100
Summary Text 2
Resume 3
75/100
Summary Text 3
...
...
... ...
Decision Making
HR Agent
Human HR
Qualified
Resumes
Classification
Rule base
Rule base
Figure 4: The illustration depict the workflow of LLM agent base Automated Resume Screening Framework.
their deployment across various industries for re-
sume data processing without the need for specific
fine-tuning. Furthermore, LLMs demonstrate en-
hanced performance compared to traditional PLMs,
providing evaluations and judgments that are more
aligned with human reasoning. This makes LLMs
particularly valuable in contexts where nuanced
understanding and decision-making are crucial.
3
Resume Screening Framework Based
on LLM Agents
This section provides a comprehensive overview
of the workflow within an novel automated resume
screening framework that utilizes a LLM agent. It
focuses on the application of the LLM agent in effi-
ciently identifying and selecting qualified resumes
from a substantial pool of candidates. To main-
tain clarity, this overview condenses some aspects,
retaining only the essential steps. Detailed discus-
sions of these steps are presented in the subsequent
three subsections.
Figure 4 illustrates the architecture of our inno-
vative automated resume screening system, which
is underpinned by a LLM agent. The process be-
gins with the transformation of a multitude of re-
sumes, each in disparate formats like PDF, DOCX,
and TXT, into a uniform JSON format. This is
achieved through a rule-based algorithm designed
to standardize the diverse formatting and file types
into coherent, individual sentences.
Such pre-
processing is crucial for enabling consistent analy-
sis in later stages. The next step involves segment-
ing these uniformly formatted resumes into distinct
sentences, based on criteria like line breaks. This
segmentation is vital for the effective functioning
of the open-source LLM, which operates locally to
classify each sentence. Critical to this process is
the categorization of various sentence types, rang-
ing from personal information, which is earmarked
for removal to protect privacy, to other categories
like work experience, education, and skills. This
categorization is particularly significant because it
allows for a tailored analysis based on the specific
requirements of a job position. For instance, certain
roles may prioritize a candidate’s skills over their
educational background. By extracting and focus-
ing on the segments of a resume that detail relevant
skills, the system can more effectively screen can-
didates for such positions. While our framework
currently focuses primarily on the basic function-


---

## Page 6

ality of removing personal information, it lays the
groundwork for more nuanced and customized re-
sume screening processes in the future.
Upon removed personal information from re-
sumes, the next step involves utilizing the GPT-3.5
model for grading and summarizing these docu-
ments. This task primarily falls under the purview
of the HR agent. The grading system serves as
a mechanism to rank candidates, streamlining the
process of identifying top applicants. Summariza-
tion, on the other hand, is aimed at conserving time
for the decision-making agent, who must evaluate
these summaries. The brevity of summarized con-
tent not only expedites the process but also benefits
human HR professionals by reducing the time re-
quired for initial resume screening. Once resumes
are assigned grades and summaries, the decision
regarding the candidates’ progression can be made
either by an HR agent or a human HR professional.
Utilizing grades as a comprehensive metric allows
for an efficient ranking of candidates. Depending
on the specific requirements, a selection of the top
10 or 100 candidates can be made for the next stage
of the screening process. This step, whether per-
formed by an HR agent or a human, significantly
reduces the time and effort involved in decision-
making. The final stage involves choosing candi-
dates for interviews or extending job offers directly,
based on the refined pool of qualified resumes. This
method optimizes the recruitment process, ensuring
efficiency and effectiveness in candidate selection.
The preceding section outlined the comprehen-
sive procedure for automated resume screening uti-
lizing open source LLM and LLM agents. Subse-
quent subsections will elaborate on the implemen-
tation of the three pivotal steps: sentence classifica-
tion, grade & summarization, and decision-making.
3.1
Sentence Classification
In our methodology, the LLaMA2 model serves
as the foundational base for sentence classifica-
tion. We enhanced this base model through fine-
tuning, specifically targeting the classification of
resume sentences. Unlike previous Pretrained Lan-
guage Models (PLMs), the LLaMA2 model does
not straightforwardly accept a sentence as input
and produce a corresponding predicted label. This
limitation stems from the model’s architecture, as
depicted in Figure 5. The LLaMA2-chat variant,
developed from the original LLaMA2 model, un-
dergoes a specialized instruction tuning process
using an instruction dataset, followed by further
LLaMA2 Chat
Pretrained
LLaMA2
Instruction
Dataset
Instruction
Tuning
Human
Preference
Data
RLHF
Figure 5: The illustration depict the process of instruc-
tion tuning and RLHF for the LLaMA2 model.
Question: Classify the above text into
the following seven labels: <personal
information>, <experience>,
<summary>, <education>,
<qualification certification>, <skill>,
<object>.\nAnswer:
Text: Resume Sentence.
Input
<personal information>
Output
Figure 6: The illustration depict the components of the
converted resume sentence instruction dataset.
refinement through Reinforcement Learning from
Human Feedback (RLHF). This approach presents
a challenge: simply inputting a sentence into the
model does not guarantee the generation of the
appropriate prediction label, a phenomenon also
evidenced in our subsequent experimental results.
The underlying reason for this is the model’s
design to respond according to the instruction
dataset’s guidelines. To elaborate, the input not
only contains the query sentence but also incor-
porates specific textual instructions guiding the


---

## Page 7

model’s response. As illustrated in Figure 6, to
address this, we append a question to the resume
sentence requiring classification. This question
instructs the model to categorize the preceding sen-
tence into one of seven predefined labels. Along-
side this, we introduce the "Answer:" prompt as
part of the input text sequence. Consequently, we
utilize the LLaMA2 model, fine-tuned with a spe-
cially curated resume sentence instruction dataset,
for the effective classification of resume sentences.
This fine-tuned LLaMA2 model demonstrates en-
hanced performance in the task at hand.
3.2
Grade & Summarization
Upon extracting the resume text with personal de-
tails redacted, our objective is to assess and encap-
sulate each resume. This process involves a shared
component: both evaluation and summarization
require a comprehensive understanding of the re-
sume’s content. Consequently, we amalgamated
these two processes into a singular question and
answer task. Figure 7 illustrates this integration,
where the red block denotes the assigned role to
the LLM agent, exemplified as an HR professional
in an IT firm with over a decade of HR experi-
ence. This role-play empowers the HR agent to
conduct an analysis with the insight of a seasoned
HR expert.
Then, briefly summarize the resume in one
paragraph (not exceeding 100 words).
Answer:
Resume: Sentence1 Sentence2 ...
Input
Question: You are currently an HR in an IT
company. You have more than ten years of
HR experience.
First, you need to grade this resume
(Example: Grade: XX/100), grade as
accurately and diversely as possible.
Resume
Assignment
Roles
Task1
Task2
Answer
Grade: 85/100
Summarization Text
Task1
Task2
Figure 7: The illustration depict assignment of roles and
tasks to the LLM agent.
The initial task involves the HR agent appraising
the resume, striving for precision and variety in
assessment. For guidance, a scoring example (e.g.,
Grade: XX/100) is provided, deliberately without
a predetermined score to avoid biasing the agent’s
evaluation. Following this, the agent is tasked with
summarizing the resume in a concise paragraph,
limited to 100 words. The culmination of this pro-
cess is the agent presenting both the grade and a
succinct summary of the resume.
3.3
Decision Making
The concluding phase of the resume screening sys-
tem involves evaluating candidates based on their
assigned grades and summaries. In this study, we
have bifurcated this stage into two distinct pro-
cesses: automatic and manual. This bifurcation al-
lows for flexibility to cater to various requirements.
Even when the ultimate selection is executed man-
ually by human HR personnel, the highly-rated
resumes can be efficiently sifted through utilizing
grade rankings. Additionally, the provided sum-
maries facilitate a rapid comprehension of the key
elements in each resume by the HR staff, thereby
significantly reducing the time required for resume
Input
You are now a CEO of an IT company.The
above are the best candidates selected from
hundreds of resumes. You now need to decide
on one candidate and give him a formal offer.
Please make a judgment based on grade and
summary of the resume.
Assignment Roles
Grade & Summarization
ID 3
90/100
Summary Text 1
ID 2
85/100
Summary Text 2
ID 3
75/100
Summary Text 3
...
...
... ...
Answer
Qualified Resume ID
Reasoning and Explanation
Figure 8: The illustration depict the HR agent making a
final Decision to select a qualified candidate.


---

## Page 8

screening.
On the other hand, the process of automated
decision-making can be further pursued through
the use of a LLM agent. As depicted in Figure
8, each resume is initially provided with a format-
ted identifier, grade, and summary. This procedure
simulates the selection of final candidates. Conse-
quently, the role assignments in the red block are
altered, transitioning from an experienced HR pro-
fessional to a CEO. The task involves selecting one
candidate out of ten, based on the provided grades
and summaries. Following this, the agent will iden-
tify the chosen resume by its ID and articulate the
rationale behind this particular selection.
Consequently, a multitude of resumes undergo a
series of evaluative processes to identify the most
suitable candidates. The automated resume screen-
ing framework employed in this process is versatile,
allowing customization to meet various require-
ments and real-world scenarios. For instance, this
research replicates the resume evaluation criteria
of IT companies, which prioritize candidates’ tech-
nical skills. Accordingly, the screening process em-
phasizes skill-related information in the resumes.
This approach is adaptable to other sectors such as
Marketing, Education, Finance, etc., by modifying
the keywords and criteria. Furthermore, the system
can be designed to mitigate educational bias by pri-
oritizing skills and work experience, thus focusing
on the candidates’ competencies. Additionally, the
framework’s screening parameters are flexible; for
example, it can be set to select the top 10% of can-
didates based on specific criteria. In summary, this
adaptability enhances the overall effectiveness and
applicability of the screening framework.
4
Experiment Setup
In this section, we will introduce how to simulate
a resume screening process to verify the effective-
ness of the automated resume screening framework
based on LLM agent. This includes the prepara-
tion of the resume dataset and some settings for
simulating the resume screening 4.1. The selec-
tion of LLM for the backbone of the LLM agent,
and the parameter settings for model inference and
fine-tuning 4.2. And description of the evaluation
method 4.3.
4.1
Resume Dataset and Screening Simulation
In the initial phase of our study, we opted for a
classification dataset comprising sentences from
resumes (Gan and Mori, 2022). This dataset en-
compasses seven categories: personal information,
experience, summary, education, qualification cer-
tification, skill, and objectives. It includes a total of
1,000 resumes, amounting to 78,668 sentences, pre-
dominantly from the IT sector. Thus, the simulation
of resume screening in this research is contextual-
ized within an IT company recruitment framework.
And we set that the person who is used to grade
each resume is an experienced HR stuff. Then, we
set that the top 10 resumes of grade go to the fi-
nal round of decision making. Finally, the CEO
is set to screen the resume grades and summaries
of these 10 candidates in order to select a final
qualified candidate.
Conversely, given the lack of grade and summa-
rization annotations in the original resume dataset,
the GPT-4 model, which currently exhibits superior
performance, was employed for annotating these re-
sumes. The annotations generated by GPT-4 served
as a benchmark for evaluating the performance of
other models, essentially treating GPT-4’s output as
a gold standard (100% performance) against which
to measure other LLMs. This approach facilitated
the creation of a comprehensive dataset for simu-
lating resume screening processes. Moreover, due
to the token limit of 4096 in the LLaMA2 model,
resumes exceeding this token count were excluded.
Consequently, a refined dataset of 838 resumes re-
mained, which was then utilized for the second
phase of testing.
To enhance the validation of our proposed re-
sume screening framework, we randomly selected
50 resumes, which were then summarized and eval-
uated manually. This process mirrored the previous
method of labeling using GPT-4, where each re-
sume was concisely summarized in approximately
100 words and assessed on a 100-point scale.
We enlisted three graduate students to annotate
the resumes manually. Before beginning the anno-
tation process, these evaluators received compre-
hensive training and were provided with several
exemplars to standardize their markings. Specif-
ically, the summaries required detailed inclusion
of the candidate’s work experience, years in the
field, educational achievements (including under-
graduate and graduate degrees), skills, experience
at major companies, and any other notable experi-
ences, while adhering strictly to 100 word limit.
During the grading phase, we establish specific
criteria for evaluation. For instance, we consider
skills that may not be directly relevant to the needs


---

## Page 9

of an IT company, such as marketing management.
Candidates with limited work experience typically
receive grades between 50 and 65. Conversely,
candidates who possess several years of IT expe-
rience along with undergraduate and graduate de-
grees in computer science are usually scored within
the range of 80 to 95. Due to the inherent impre-
cision of the scoring process, we adopt a scoring
interval of 5 points. Ultimately, the grades are aver-
aged across three evaluators. We then review three
different summaries of each resume and select the
one that most accurately reflects the original docu-
ment as the final labeled result.
4.2
Prepare Backbone LLMs and Parameter
Sets
In the initial phase of the sentence classification
task, the LLaMA2-7B model was chosen for fine-
tuning. The dataset, comprising 78,668 sentences,
was partitioned into training, validation, and testing
sets in a 7:1.5:1.5 ratio. A random seed of 42 was
set to ensure reproducibility. This configuration
aligns with the experimental setup described in
the original paper pertaining to the resume dataset,
enabling direct comparisons with other PLMs. For
the training process, each GPU was assigned a
batch size of 32, and the model underwent training
for 2 epochs using 32-bit floating-point precision.
In the subsequent phase, specifically the second
stage of grading and summarization, we selected
LLaMA2-7B/13/70B and GPT-3.5-turbo-0614 as
the backbone LLMs for the HR agent. Initially,
we employed a zero-shot methodology to grade
and summarize 838 resumes using four different
LLMs, aiming to assess and compare their efficacy.
During this process, we meticulously configured
the parameters for model generation. The maxi-
mum number of new tokens was set at 200. This
parameter choice was informed by the requirement
that each resume should be graded and summa-
rized in over 100 words. Additionally, we incorpo-
rated the ’do sample’ and ’early stopping’ features
to optimize the summarization process. Except
for these specific adjustments, all other parameters
were maintained at their default settings.
In additional, we involved enhancing LLaMA2-
7B/13B’s capabilities by fine-tuning it with a spe-
cialized dataset focused on resume grading and
summarization. Initially, this dataset was parti-
tioned into two distinct subsets: a training set with
500 resumes and a test set comprising 383 resumes.
Subsequently, the model underwent a training pro-
cess where each GPU was allocated a batch size of
eight. This training was conducted over 2 epochs,
utilizing BF16 precision to optimize performance
and computational efficiency.
In conclusion, our experimental setup involved
conducting the inference tests for LLaMA2-
7B/13B using a dual RTX 3090 24G GPU configu-
ration with float16 precision. In contrast, both the
fine-tuning procedures for LLaMA2-7B/13B and
the inference tests for LLaMA2-70B were executed
on an RTX A800 80G * 8 GPU server.
4.3
Evaluation
In the initial phase of resume sentence classifica-
tion, we utilize the F1 score as the primary evalu-
ation metric. This score comprehensively reflects
the model’s performance by harmonizing precision
and recall into a balanced mean. This approach of-
fers a more accurate representation of the model’s
effectiveness.
For the resume summarization segment, our eval-
uation employs two predominant metrics: ROUGE-
1/2/L (Lin and Och, 2004) and BLEU. These
metrics are extensively recognized in the auto-
matic evaluation of summarization tasks.
Al-
though BLEU is traditionally associated with trans-
lation evaluations, its application in summarization
tasks provides valuable insights. By incorporating
BLEU, we aim to achieve a more holistic assess-
ment of the summarization quality.
Regarding the evaluation of grade scores, our
methodology focuses on accuracy. This is particu-
larly crucial given the significant variance in grade
distribution across different models. We adopt a
tolerance range approach in calculating accuracy:
a generated grade is deemed accurate if it falls
within a margin of ±5 from the actual grade. The
calculation adheres to the following principle: if
the absolute difference between the predicted and
the actual grade is 5 or less, the prediction is con-
sidered correct (recorded as 1, with 0 indicating
an error). To derive the final grade accuracy, we
divide the total count of correct predictions by the
total number of actual grades (PG is denote Predict
Grade, TG is denote True Grade).
Accuracy =
PN
i=1 1 (|PGi −TGi| ≤5)
N


---

## Page 10

Table 1: Results of resume sentence classification dataset.
Model
F1 Score
BERT Large
86.67
ALBERT Large
86.40
RoBERTa Large
87.00
T5 Large
87.35
LLaMA2-7B-chat
78.16
LLaMA2-7B-chat (Instruction Format)
87.73
Table 2: Results of resume grade and summarization dataset (ROUGE-1/2/L).
Model
ROUGE-1
ROUGE-2
ROUGE-L
LLaMA2-7B
26.35
6.22
24.00
LLaMA2-13B
25.31
5.83
22.99
LLaMA2-70B
28.12
7.70
25.68
GPT-3.5-Turbo
34.75
12.34
31.92
Table 3: Results of resume grade and summarization
dataset (BLEU and Grade Accuracy).
Model
BLEU
Grade Accuracy
LLaMA2-7B
2.66
47.49
LLaMA2-13B
2.56
59.31
LLaMA2-70B
3.73
23.27
GPT-3.5-Turbo
7.31
47.61
5
Results
In the results of sentence classification for resumes,
we conducted comparative experiments on the per-
formances of several large-scale models: BERT
Large, ALBERT Large, RoBERTa Large, and T5
Large. The results, detailed in Table 1, reveal a no-
table enhancement in the F1 score of the LLaMA2-
7B-chat model, which reaches 87.73, attributed
to the implementation of the instruction format
for both input and output. Interestingly, a direct
fine-tuning of the LLaMA2-7B-chat model, using
the conventional approach of inputting sentences
and outputting labels as done with previous PLMs,
resulted in a significant drop in the F1 score to
78.16. This outcome undergrades the efficacy of
the instruction format we proposed. Furthermore,
it highlights a critical consideration for fine-tuning
LLMs in sentence classification tasks: adhering to
the instruction format used during the instruction
learning phase is crucial for optimizing the models’
sentence classification capabilities.
In the evaluation of the grading and summariza-
tion component of the automated resume screening
framework, we conducted tests using three different
model sizes of LLaMA2 and GPT-3.5-Turbo. The
results, as presented in Table 2, indicate that GPT-
3.5-Turbo outperformed the others across all three
ROUGE metrics: ROUGE-1 (34.75), ROUGE-2
(12.34), and ROUGE-L (31.92), significantly sur-
passing the LLaMA2-70B model. Furthermore,
under the BLEU evaluation metric (Table 3), GPT-
3.5-Turbo achieved a score of 7.31, nearly tripling
the performance of its counterparts. This suggests
that, if not using the fine-tuning method (0-shot
inference). Utilizing closed-source models like
GPT-3.5-Turbo and GPT-4 as the backbone for
HR agents is crucial for enhanced performance.
Interestingly, in the aspect of grading accuracy,
LLaMA2-13B outshined the other models with a
score of 59.31, notably exceeding the LLaMA2-
70B model by 23.27. This anomaly and its implica-
tions will be further analyzed and discussed in the
following subsection.
Finally, the LLaMA2-7B/13B model was sub-
jected to fine-tuning, yielding notable improve-
ments as documented in Table 4. Specifically, the
refined LLaMA2-13B model demonstrated remark-
able grades of 37.30, 13.90, and 33.93 in ROUGE-
1/2/L metrics, respectively. This performance no-
tably surpassed that of the 0-shot GPT-3.5 Turbo
model in the test set evaluations. Furthermore, Ta-
ble 5 presents the enhancements in BLEU grades,
where the LLaMA2-7B and LLaMA2-13B models
recorded increments to 8.45 and 8.62, respectively.
Correspondingly, there was a significant improve-
ment in grade accuracy, reaching 76.19 and 81.35


---

## Page 11

Table 4: Results of fine-tuned LLaMA2-7B/13B in resume grade and summarization dataset (ROUGE-1/2/L).
Model
ROUGE-1
ROUGE-2
ROUGE-L
GPT-3.5-Turbo
34.61
12.18
31.83
LLaMA2-7B
36.50
13.32
33.48
LLaMA2-13B
37.30
13.90
33.93
Table 5: Results of fine-tuned LLaMA2-7B/13B in
resume grade and summarization dataset (BLEU and
Grade Accuracy).
Model
BLEU
Grade Accuracy
GPT-3.5-Turbo
7.40
45.24
LLaMA2-7B
8.45
76.19
LLaMA2-13B
8.62
81.35
for each model. These results clearly indicate that,
with adequate resume datasets for fine-tuning, opt-
ing for open-source LLaMA2-7B/13B models as
the foundation for HR agent systems is a more
effective strategy.
5.1
Normal Distribution of Grade
Figure 9 & 10 presents the normal distribution plots
for the evaluations assigned by five different LLMs.
Notably, the GPT-4 model generally aligns with the
normal distribution across all grades, with a marked
preference for assigning grades within the 85-90
range. This skew towards higher grades may stem
from GPT-4’s inclination to award more favorable
ratings during fine-tuning processes, such as RLHF.
Despite this, the impact on final resume screening
remains minimal, as the system consistently prior-
itizes the top 10 resumes based on grades. While
there may be some uncertainty regarding the extent
to which these LLM-based HR agents accurately
reflect the actual quality of each resume, the simu-
lation experiment suggests that the grading patterns
of all five LLMs largely adhere to a normal distribu-
tion. This indicates that the application of LLMs in
resume evaluation is a successful experiment, with
outcomes mirroring those expected in real-world
scenarios.
The data presented in Figure 9 & 10 and Table 6
reveals that the three LLaMA2 models exhibit in-
stances of zero grading. This phenomenon occurs
because these models assign grades that are not
exclusively two-digit grades (such as ’A’, ’B+++’,
etc.), leading to misclassification. Consequently,
we have classified all such instances as zero grades.
It is noteworthy that the incidence of grading er-
Table 6: Number of grading errors (The grade is not a
two-digit number) by different LLMs.
Model
Total Number of Errors
LLaMA2-7B
190
LLaMA2-13B
22
LLaMA2-70B
8
LLaMA2-7B FT
1
LLaMA2-13B FT
0
rors in the LLaMA2 model is significantly reduced
following fine-tuning. Additionally, the GPT-3.5-
Turbo/4 model demonstrates an absence of grade
errors, which can be attributed to the differences
in the capabilities of various LLMs in terms of
understanding and adherence to instructions.
5.2
Analysis of Decision Making
In our study, we utilized the GPT-3.5-Turbo and
GPT-4 models as autonomous HR agents to evalu-
ate the top 10 resumes based on their grades. The
rationale behind their decisions is detailed. As il-
lustrated in Figure 11, both models consistently
identified resume ID 308 as the top candidate. The
justification for this selection was not only the high
grade of resume ID 308 but also its alignment with
the specific needs of an IT company, including rel-
evant work experience and managerial skills. This
analysis demonstrates a remarkable congruence
with the cognitive processes and judgment criteria
typically employed by human HR professionals in
decision-making. Furthermore, these findings un-
derscore the potential of integrating LLM based
HR agents into future automated resume screening
systems.
To further investigate the decision-making ca-
pabilities of the HR agent, particularly in han-
dling complex recruitment requirements, we re-
fined the criteria within this stage and conducted an
additional experiment. This experiment utilized a
dataset of 50 manually annotated resumes, summa-
rized and graded for relevance. We configured the
hiring criteria to target three individuals with ex-
pertise in database development. This requirement


---

## Page 12

(a) Grade Distribution of LLaMA2-7B
(b) Grade Distribution of LLaMA2-13B
(c) Grade Distribution of LLaMA2-70B
Figure 9: Compare the Grade Distribution of LLaMA2-7B/13B/70B models.
(a) Grade Distribution of GPT-3.5-
Turbo
(b) Grade Distribution of GPT-4
(c) Comparison of 6 LLMs in grade
Figure 10: Compare the Grade Distribution of GPT-3.5-Turbo/4 models. And comparison of 6 LLMs in grade.
Selecting just one candidate from such a commendable list
is quite challenging. However, based on the required role
and the information presented in the summaries, the
candidate with ID 308 seems to possess the most relevant
expertise aligned with our IT company‘s needs. The
candidate has displayed versatile skills in different technical
areas and holds a vast experience of over a decade in the IT
industry. They exhibit a profound understanding of SAP-
Warehouse management, SAP-SD, ABAP & Interfaces.
Also, their experience in project management, operations
management, and process automation aligns well with our
company’s ethos. Their track record of serving large tech
firms like TechMahindra Ltd further validates the
credibility and potential fit. Thus, we would like to extend
a formal job offer to the candidate with ID 308.
Based on the grades and summaries of the resumes
provided, I would recommend offering the formal offer
to the candidate with ID 308. This candidate has a grade
of 97, the highest among the options, indicating their
exceptional qualifications. Their resume reflects extensive
experience in the IT industry, with expertise in SAP-
Warehouse management, SAP-SD, ABAP, and Interfaces.
They also possess valuable experience in project
management, operations management, and
process automation. Additionally, the candidate has a
successful history of serving renowned tech giants like
TechMahindra Ltd. and demonstrates strong people
management skills. Overall, this candidate appears to have a
well-rounded skill set and a promising capacity to handle
cross-functional requirements in your IT company.
GPT-4
GPT-3.5-Turbo
Figure 11: The answer text of Decision Making with HR agents (GPT4 and GPT-3.5-Turbo Models).
was incorporated into the input prompt template as
follows: "You are now recruiting three individuals
for database development roles in your company."
As depicted in Figure 12, the HR agent success-
fully identified three candidates, providing detailed
justifications for each selection. Notably, all candi-
dates demonstrated relevant database development
skills and substantial professional experience. The
reasoning for their selection was well-articulated
and convincing. Subsequent manual review of the
candidates’ resumes confirmed that these individu-
als were indeed the most suitable for the positions.
This experiment underscores the adaptability of
the LLM-based resume screening framework, high-
lighting its ability to accommodate a diverse ar-
ray of job specifications. It demonstrates that the
model can be effectively tailored to meet varying
recruitment needs of different companies for vari-
ous positions, thus proving its generalizability and
utility in complex HR scenarios.
5.3
Comparison with Manual Resume
Screening
We conducted a thorough evaluation of various
LLMs by manually annotated 50 resumes to serve
as a benchmark. The results of these tests are de-


---

## Page 13

Given the need for professionals in database development-related roles at your IT company, it's crucial to select
candidates who demonstrate strong database management skills, proficiency in relevant programming languages, and
experience in database-driven projects. Based on the grades and summaries provided:
1. ID: 892 - Grade: 95  
   Summary: This candidate stands out with an extensive 8-year experience in Java/J2EE technologies and expertise
with relational databases like Oracle. The experience in web application development might be directly beneficial for
backend system integration and effective data handling tasks in our projects. The knowledge of cloud deployment using
AWS is also an advantage, as modern database solutions often integrate with cloud services.
2. ID: 30 - Grade: 90 
   Summary: This candidate has a solid background in Oracle SQL and PL/SQL, focusing on database optimization,
maintenance, and implementation. Their experience with companies like Liquidhub and Hewlett Packard, and their
demonstrated technical skills in database management and performance tuning, makes them particularly fitting for
database development roles.
3. ID: 416 - Grade: 90  
   Summary: Though primarily a firmware developer, this candidate's background in Electronics and Communication
Engineering, and their proficiency with real-time operating systems and device driver development, offer useful
crossover skills for database and system architecture projects. Their understanding of hardware protocols might provide
fresh insights into how our database solutions can be optimized for performance at the lowest level.
These selections prioritize a balance of relevant technical skills, proven experience in handling complex databases, and
the ability to contribute uniquely to the development and optimization of advanced database systems at your IT
company.
Figure 12: The text of Decision Making with HR agents (GPT4-Turbo Models).
Table 7: Experimental results of LLMs evaluated based on manually annotated 50 sample datasets (ROUGE-1/2/L).
Model
ROUGE-1
ROUGE-2
ROUGE-L
LLaMA2-7B
27.03
7.11
24.28
LLaMA2-13B
24.96
5.96
22.62
LLaMA2-70B
27.27
7.69
25.00
GPT-3.5-Turbo
34.55
12.37
31.94
GPT-4
39.87
16.44
35.89
Table 8: Experimental results of LLMs evaluated based
on manually annotated 50 sample datasets (BLEU and
Grade Accuracy).
Model
BLEU
Grade Accuracy
LLaMA2-7B
3.28
22.00
LLaMA2-13B
2.71
40.00
LLaMA2-70B
3.73
38.00
GPT-3.5-Turbo
7.16
58.00
GPT-4
11.06
50.00
tailed in Tables 7 and 8, with the GPT-3.5-Turbo
and GPT-4 models demonstrating superior perfor-
mance. Notably, while the accuracy of the grade
assignments was not perfect, a subsequent analysis
of the top ten resumes ranked by grades revealed
significant insights. The resumes that received the
highest grades from GPT-4 exhibited a striking re-
semblance to those scored manually, underscoring
the effectiveness of the model in mimicking human
evaluative patterns.
As depicted in Figure 13, we compiled the IDs
and grades of the top ten resumes according to the
final grades from GPT-4 and manual scoring. In
this figure, underlined text indicates where the two
sets of rankings overlap, highlighting a strong cor-
relation in the evaluation outcomes. Remarkably,
both manually and by GPT-4, resumes ID 801 and
ID 892 received the highest grades. Furthermore,
11 out of the 12 resumes that ranked highly in the
manual assessment also featured prominently in
the GPT-4 rankings, further validating the model’s
evaluative consistency.
Finally, we selected a final qualified resume us-
ing both manual and GPT-4 methods. Both selected
resume ID 801 as the hiring candidate. Detailed
analysis of this candidate’s credentials revealed not
only a robust six years of professional experience
but also a comprehensive repertoire of IT-related
skills. The individual is a versatile full-stack Java
developer, proficient in a range of technologies
spanning from front-end to back-end development,
including networking. This skill set renders the can-
didate highly suitable for a developer role within
an IT organization.


---

## Page 14

Grade of GPT-4
ID 801
95
ID 892
92
ID 30
88
ID 488
88
ID 193
87
ID 189
87
ID 125
86
ID 785
85
ID 604
85
ID 490
85
ID 127
85
ID 514
85
ID 103
85
ID 412
85
ID 242
85
ID 409
85
ID 184
85
ID 416
85
Grade of Manual
ID 801
95
ID 892
95
ID 785
90
ID 490
90
ID 127
90
ID 30
90
ID 103
90
ID 416
90
ID 604
85
ID 125
85
ID 313
85
ID 189
85
Figure 13: Ranking comparison of top 10 GPT-4 rated
resumes and top 10 manually graded resumes. Under-
lining represents the portion where the two overlap (i.e.,
the grades are equivalent).
In conclusion, our findings affirm the efficacy
of the proposed resume screening framework that
leverages LLMs. This comparison with traditional
manual methods substantiates the potential for
LLMs to effectively replace manual resume screen-
ing processes in the future.
Figure 14: The comparison of manual and GPT-4 in
grades distributions (Base 50 samples dataset).
Our analysis also included a comparison be-
tween the score distributions of the most advanced
GPT-4 model and manual grading. Figure 14 illus-
trates this comparison, revealing a high degree of
similarity between the two distributions. We quanti-
fied this similarity by calculating the cosine similar-
ity, which yielded a value of 0.9944, approaching 1.
This high similarity score further supports the con-
sistency between GPT-4-generated grades and man-
ual grades. This consistency is likely attributable
to the model’s use of instruction tuning and rein-
forcement learning with human feedback (RLHF).
We also computed the correlation between the two
rankings using Spearman’s rho (ρ) and Kendall’s
tau (τ). The values obtained were 0.7574 for Spear-
man’s ρ and 0.6252 for Kendall’s τ, indicating
a strong positive correlation between the manual
rankings and the predicted rankings produced by
the LLM.
5.4
Analysis of Long Length Resume
Screening
In addition, for resumes that exceed the LLaMA2
model’s processing limit of 4,096 tokens, we con-
ducted further experiments using more advanced
models from the GPT family. Specifically, we
utilized the GPT-4-Turbo and GPT-3.5-Turbo-16k
models, which are capable of processing up to
128,000 and 16,000 tokens, respectively. These
models are well-suited to handle the length of most
resumes. Due to resource limitations, our experi-
ments were confined to 162 resumes that exceeded
4,000 tokens in length.
We used the results from the GPT-4-Turbo model
as a benchmark for evaluating the performance of
the GPT-3.5-Turbo-16k model. As indicated in Ta-
ble 9, the GPT-3.5-Turbo-16k model demonstrated
promising results, with a notable grade accuracy
of 72.22%. This high level of accuracy can be
attributed to the model’s ability to effectively ana-
lyze content-rich resumes, which typically contain
extensive text detailing numerous skills and work
experiences. Common sense suggests that resumes
with more detailed information about a candidate’s
skills and experiences are likely to score higher, in-
dicating a potentially stronger candidate. This prin-
ciple was affirmed by our findings, which showed
a direct correlation between the depth of resume
content and the accuracy of the model’s grading.


---

## Page 15

Table 9: GPT-3.5-Turbo-16k Model experiment results. Evaluated based on GPT-4-Turbo (Max input length 128K)
annotated 162 over length resume datasets .
Model
ROUGE-1
ROUGE-2
ROUGE-L
GPT-3.5-Turbo-16k
36.05
12.62
32.61
Model
BLEU
Grade Accuracy
GPT-3.5-Turbo-16k
6.78
72.22
5.5
Time comparison between automated and
human resume screening
Our study entailed a meticulous time comparison
of three distinct resume screening methods: Au-
tomated, Semi-Automated, and Manual. To this
end, we deconstructed the automated screening
process into three discrete stages: Classification,
Grading & Summarization, and Decision Making.
We measured the time expenditure for each phase,
culminating in an aggregate duration assessment.
Notably, in the Classification stage, we accounted
for the time span from initiation to conclusion of
the inference process, excluding the fine-tuning du-
ration. This approach mirrors the actual operational
timeline of the automated screening framework. In
the Decision Making stage, our focus was on the
time required to evaluate the top ten resumes.
Additionally, we assessed the time investment
for the semi-automated method, wherein human
HR personnel undertake the final decision-making
step, while preceding stages are managed by LLMs.
For the manual screening conducted by Human HR,
we based our calculations on the average adult read-
ing speed of 238 words per minute, as indicated by
survey literature (Brysbaert, 2019). Consequently,
we deduced that reviewing all 838 resumes, encom-
passing a total of 442,047 words, would approx-
imately take 31 hours (Please note that this is an
estimated time, calculated based on the average
human reading speed.).
Table 10 illustrates that the fully automated re-
sume screening framework, utilizing an LLM agent,
completes the entire process set in approximately
2 hours and 55 minutes. This efficiency represents
a speed 11 times faster than manual resume screen-
ing. Additionally, the semi-automatic approach is
9 times quicker than the manual method. While
this comparison may lack rigorous precision, as it
does not account for the possibility that human HR
personnel might not read every word in a resume to
reach a decision, the significant time reduction ob-
served with the automated framework underscores
its high efficiency.
6
Conclusion
In this study, we explore the feasibility of using an
LLM agent for automated resume screening. We
propose an innovative framework for this purpose
and validate it using a real-world resume dataset,
as well as through simulation of the resume screen-
ing process. Our results, derived from a series of
comparative tests and analyses, demonstrate that
the LLM agent can effectively perform the role of
a human HR professional in resume screening. No-
tably, in terms of time efficiency, the LLM agent
significantly surpasses traditional manual screening
methods.
This work is subject to certain limitations. Pri-
marily, it employs a controlled experimental design
to maximize result accuracy, which restricts the
scope of application to basic requirements of LLMs
agent within IT companies. Consequently, this ap-
proach does not account for the varied requirements
of other industries. Additionally, the collection of
resume data is challenging due to privacy concerns.
In future work, we aim to gather a broader array
of resumes from diverse industries to enhance the
representativeness of our study and further refine
the LLM resume screening framework.
References
Irfan Ali, Nimra Mughal, Zahid Hussain Khand, Javed
Ahmed, and Ghulam Mujtaba. 2022. Resume clas-
sification system using natural language processing
and machine learning techniques. Mehran Univer-
sity Research Journal of Engineering & Technology,
41(1):65–79.
CH Ayishathahira, C Sreejith, and C Raseek. 2018.
Combination of neural networks and conditional ran-
dom fields for efficient resume parsing.
In 2018
International CET Conference on Control, Communi-
cation, and Computing (IC4), pages 388–393. IEEE.
Alessandro Barducci, Simone Iannaccone, Valerio
La Gatta, Vincenzo Moscato, Giancarlo Sperlì, and


---

## Page 16

Table 10: Follow each step to compare the time consumed by automated and manual resume screening.
Model
Classification
Grade & Summary
Decision Making
GPT-4 API
25 min (FT LLaMA2-7B)
2 h 30 min
0.4 min
LLM with
Estimated Human
25 min (FT LLaMA2-7B)
2 h 30 min (GPT-4)
22 min (Manual)
Screening Time
Estimated
Human Screening
—
—
—
Time
Model
Total Time
Multiple
Automatic or Manual
GPT-4 API
2 h 55.4 min
x 11
Automatic
LLM with Estimated
3 h 17 min
x 9
Semi-automatic
Human Screening Time
Estimated Human
x 1
Manual
Screening Time
31 h
Sergio Zavota. 2022. An end-to-end framework for
information extraction from italian resumes. Expert
Systems with Applications, 210:118487.
Markus Bayer, Marc-André Kaufhold, and Christian
Reuter. 2022. A survey on data augmentation for text
classification. ACM Comput. Surv., 55(7).
S Bharadwaj, Rudra Varun, Potukuchi Sreeram Aditya,
Macherla Nikhil, and G Charles Babu. 2022. Resume
screening using nlp and lstm. In 2022 international
conference on inventive computation technologies
(ICICT), pages 238–241. IEEE.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie
Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
Neelakantan, Pranav Shyam, Girish Sastry, Amanda
Askell, et al. 2020. Language models are few-shot
learners. Advances in neural information processing
systems, 33:1877–1901.
Marc Brysbaert. 2019. How many words do we read
per minute? a review and meta-analysis of reading
rate. Journal of memory and language, 109:104047.
Liting Chen, Lu Wang, Hang Dong, Yali Du, Jie Yan,
Fangkai Yang, Shuang Li, Pu Zhao, Si Qin, Saravan
Rajmohan, et al. 2023. Introspective tips: Large lan-
guage model for in-context decision making. arXiv
preprint arXiv:2305.11598.
Fabio Ciravegna and Alberto Lavelli. 2004. Learning-
pinocchio: Adaptive information extraction for real
world applications. Natural Language Engineering,
10(2):145–165.
Chirag Daryani, Gurneet Singh Chhabra, Harsh Patel,
Indrajeet Kaur Chhabra, and Ruchi Patel. 2020. An
automated resume screening system using natural
language processing and similarity. ETHICS AND
INFORMATION TECHNOLOGY [Internet]. VOLK-
SON PRESS, pages 99–103.
Jacob Devlin, Ming-Wei Chang, Kenton Lee, and
Kristina Toutanova. 2018. Bert: Pre-training of deep
bidirectional transformers for language understand-
ing. arXiv preprint arXiv:1810.04805.
Ning Ding, Yujia Qin, Guang Yang, Fuchao Wei,
Zonghan Yang, Yusheng Su, Shengding Hu, Yulin
Chen, Chi-Min Chan, Weize Chen, et al. 2023.
Parameter-efficient fine-tuning of large-scale pre-
trained language models. Nature Machine Intelli-
gence, 5(3):220–235.
Yingpeng Du, Di Luo, Rui Yan, Xiaopei Wang, Hongzhi
Liu, Hengshu Zhu, Yang Song, and Jie Zhang. 2024.
Enhancing job recommendation through llm-based
generative adversarial networks. In Proceedings of
the AAAI Conference on Artificial Intelligence, vol-
ume 38, pages 8363–8371.
Merve Elmas Erdem. 2023. Automatic resume screen-
ing with content matching. In 2023 8th International
Conference on Computer Science and Engineering
(UBMK), pages 554–558.
Chengguang Gan and Tatsunori Mori. 2022.
Con-
struction of english resume corpus and test with
pre-trained language models.
arXiv preprint
arXiv:2208.03219.
Preetam
Ghosh
and
Vaishali
Sadaphal.
2023.
Jobrecogpt–explainable
job
recommendations
using llms. arXiv preprint arXiv:2309.11805.
Tumula Mani Harsha, Gangaraju Sai Moukthika, Dudi-
palli Siva Sai, Mannuru Naga Rajeswari Pravallika,


---

## Page 17

Satish Anamalamudi, and MuraliKrishna Enduri.
2022. Automated resume screener using natural lan-
guage processing (nlp). In 2022 6th international
conference on trends in electronics and informatics
(ICOEI), pages 1772–1777. IEEE.
Jen-tse Huang, Eric John Li, Man Ho Lam, Tian Liang,
Wenxuan Wang, Youliang Yuan, Wenxiang Jiao,
Xing Wang, Zhaopeng Tu, and Michael R Lyu. 2024.
How far are we on the decision-making of llms? eval-
uating llms’ gaming ability in multi-agent environ-
ments. arXiv preprint arXiv:2403.11807.
Bhushan Kinge, Shrinivas Mandhare, Pranali Chavan,
and SM Chaware. 2022. Resume screening using
machine learning and nlp: A proposed system. Inter-
national Journal of Scientific Research in Computer
Science, Engineering and Information Technology
(IJSRCSEIT), 8(2):253–258.
Chin-Yew Lin and Franz Josef Och. 2004.
Auto-
matic evaluation of machine translation quality using
longest common subsequence and skip-bigram statis-
tics. In Proceedings of the 42nd annual meeting of
the association for computational linguistics (ACL-
04), pages 605–612.
Shuai Ma, Qiaoyi Chen, Xinru Wang, Chengbo Zheng,
Zhenhui Peng, Ming Yin, and Xiaojuan Ma. 2024.
Towards human-ai deliberation: Design and evalua-
tion of llm-empowered deliberative ai for ai-assisted
decision-making. arXiv preprint arXiv:2403.16812.
Bonan Min,
Hayley Ross,
Elior Sulem,
Amir
Pouran Ben Veyseh, Thien Huu Nguyen, Oscar Sainz,
Eneko Agirre, Ilana Heintz, and Dan Roth. 2023.
Recent advances in natural language processing via
large pre-trained language models: A survey. ACM
Computing Surveys, 56(2):1–40.
Shervin Minaee, Nal Kalchbrenner, Erik Cambria, Nar-
jes Nikzad, Meysam Chenaghlu, and Jianfeng Gao.
2021. Deep learning–based text classification: A
comprehensive review. ACM Comput. Surv., 54(3).
R Mooney. 1999. Relational learning of pattern-match
rules for information extraction. In Proceedings of
the sixteenth national conference on artificial intelli-
gence, volume 328, page 334.
OpenAI, :, Josh Achiam, Steven Adler, Sandhini Agar-
wal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Ale-
man, Diogo Almeida, Janko Altenschmidt, Sam Alt-
man, Shyamal Anadkat, Red Avila, Igor Babuschkin,
Suchir Balaji, Valerie Balcom, Paul Baltescu, Haim-
ing Bao, Mo Bavarian, Jeff Belgum, Irwan Bello,
Jake Berdine, Gabriel Bernadett-Shapiro, Christo-
pher Berner, Lenny Bogdonoff, Oleg Boiko, Made-
laine Boyd, Anna-Luisa Brakman, Greg Brockman,
Tim Brooks, Miles Brundage, Kevin Button, Trevor
Cai, Rosie Campbell, Andrew Cann, Brittany Carey,
Chelsea Carlson, Rory Carmichael, Brooke Chan,
Che Chang, Fotis Chantzis, Derek Chen, Sully Chen,
Ruby Chen, Jason Chen, Mark Chen, Ben Chess,
Chester Cho, Casey Chu, Hyung Won Chung, Dave
Cummings, Jeremiah Currier, Yunxing Dai, Cory
Decareaux, Thomas Degry, Noah Deutsch, Damien
Deville, Arka Dhar, David Dohan, Steve Dowl-
ing, Sheila Dunning, Adrien Ecoffet, Atty Eleti,
Tyna Eloundou, David Farhi, Liam Fedus, Niko
Felix, Simón Posada Fishman, Juston Forte, Is-
abella Fulford, Leo Gao, Elie Georges, Christian
Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh,
Rapha Gontijo-Lopes, Jonathan Gordon, Morgan
Grafstein, Scott Gray, Ryan Greene, Joshua Gross,
Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse
Han, Jeff Harris, Yuchen He, Mike Heaton, Jo-
hannes Heidecke, Chris Hesse, Alan Hickey, Wade
Hickey, Peter Hoeschele, Brandon Houghton, Kenny
Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu
Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger
Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie
Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser,
Ali Kamali, Ingmar Kanitscheider, Nitish Shirish
Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook
Kim, Christina Kim, Yongjik Kim, Hendrik Kirch-
ner, Jamie Kiros, Matt Knight, Daniel Kokotajlo,
Łukasz Kondraciuk, Andrew Kondrich, Aris Kon-
stantinidis, Kyle Kosic, Gretchen Krueger, Vishal
Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan
Leike, Jade Leung, Daniel Levy, Chak Ming Li,
Rachel Lim, Molly Lin, Stephanie Lin, Mateusz
Litwin, Theresa Lopez, Ryan Lowe, Patricia Lue,
Anna Makanju, Kim Malfacini, Sam Manning, Todor
Markov, Yaniv Markovski, Bianca Martin, Katie
Mayer, Andrew Mayne, Bob McGrew, Scott Mayer
McKinney, Christine McLeavey, Paul McMillan,
Jake McNeil, David Medina, Aalok Mehta, Jacob
Menick, Luke Metz, Andrey Mishchenko, Pamela
Mishkin, Vinnie Monaco, Evan Morikawa, Daniel
Mossing, Tong Mu, Mira Murati, Oleg Murk, David
Mély, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak,
Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh,
Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex
Paino, Joe Palermo, Ashley Pantuliano, Giambat-
tista Parascandolo, Joel Parish, Emy Parparita, Alex
Passos, Mikhail Pavlov, Andrew Peng, Adam Perel-
man, Filipe de Avila Belbute Peres, Michael Petrov,
Henrique Ponde de Oliveira Pinto, Michael, Poko-
rny, Michelle Pokrass, Vitchyr Pong, Tolly Pow-
ell, Alethea Power, Boris Power, Elizabeth Proehl,
Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh,
Cameron Raymond, Francis Real, Kendra Rimbach,
Carl Ross, Bob Rotsted, Henri Roussez, Nick Ry-
der, Mario Saltarelli, Ted Sanders, Shibani Santurkar,
Girish Sastry, Heather Schmidt, David Schnurr, John
Schulman, Daniel Selsam, Kyla Sheppard, Toki
Sherbakov, Jessica Shieh, Sarah Shoker, Pranav
Shyam, Szymon Sidor, Eric Sigler, Maddie Simens,
Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin
Sokolowsky, Yang Song, Natalie Staudacher, Fe-
lipe Petroski Such, Natalie Summers, Ilya Sutskever,
Jie Tang, Nikolas Tezak, Madeleine Thompson, Phil
Tillet, Amin Tootoonchian, Elizabeth Tseng, Pre-
ston Tuggle, Nick Turley, Jerry Tworek, Juan Fe-
lipe Cerón Uribe, Andrea Vallone, Arun Vijayvergiya,
Chelsea Voss, Carroll Wainwright, Justin Jay Wang,
Alvin Wang, Ben Wang, Jonathan Ward, Jason Wei,
CJ Weinmann, Akila Welihinda, Peter Welinder, Ji-


---

## Page 18

ayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner,
Clemens Winter, Samuel Wolrich, Hannah Wong,
Lauren Workman, Sherwin Wu, Jeff Wu, Michael
Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qim-
ing Yuan, Wojciech Zaremba, Rowan Zellers, Chong
Zhang, Marvin Zhang, Shengjia Zhao, Tianhao
Zheng, Juntang Zhuang, William Zhuk, and Barret
Zoph. 2023. Gpt-4 technical report.
Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Car-
roll L. Wainwright, Pamela Mishkin, Chong Zhang,
Sandhini Agarwal, Katarina Slama, Alex Ray, John
Schulman, Jacob Hilton, Fraser Kelton, Luke Miller,
Maddie Simens, Amanda Askell, Peter Welinder,
Paul Christiano, Jan Leike, and Ryan Lowe. 2022.
Training language models to follow instructions with
human feedback.
Alec Radford, Jeffrey Wu, Rewon Child, David Luan,
Dario Amodei, Ilya Sutskever, et al. 2019. Language
models are unsupervised multitask learners. OpenAI
blog, 1(8):9.
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine
Lee, Sharan Narang, Michael Matena, Yanqi Zhou,
Wei Li, and Peter J Liu. 2020. Exploring the limits
of transfer learning with a unified text-to-text trans-
former. The Journal of Machine Learning Research,
21(1):5485–5551.
Amit Singh, Rose Catherine, Karthik Venkat Ramanan,
Vijil Chenthamarakshan, and Nanda Kambhatla.
2010a. Prospect: a system for screening candidates
for recruitment. Proceedings of the 19th ACM inter-
national conference on Information and knowledge
management.
Amit Singh, Catherine Rose, Karthik Visweswariah, Vi-
jil Chenthamarakshan, and Nandakishore Kambhatla.
2010b. Prospect: a system for screening candidates
for recruitment. In Proceedings of the 19th ACM
international conference on Information and knowl-
edge management, pages 659–668.
Amit Singhal et al. 2001. Modern information retrieval:
A brief overview. IEEE Data Eng. Bull., 24(4):35–
43.
Arvind Kumar Sinha, Md Amir Khusru Akhtar, and
Ashwani Kumar. 2021. Resume screening using nat-
ural language processing and machine learning: A
systematic review. Machine Learning and Informa-
tion Processing: Proceedings of ICMLIP 2020, pages
207–214.
Ilya Sutskever, Oriol Vinyals, and Quoc V Le. 2014.
Sequence to sequence learning with neural networks.
Advances in neural information processing systems,
27.
VV Satyanarayana Tallapragada, V Sushma Raj,
U Deepak, P Divya Sai, and T Mallikarjuna. 2023.
Improved resume parsing based on contextual mean-
ing extraction using bert. In 2023 7th International
Conference on Intelligent Computing and Control
Systems (ICICCS), pages 1702–1708. IEEE.
Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier
Martinet, Marie-Anne Lachaux, Timothée Lacroix,
Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal
Azhar, et al. 2023a.
Llama:
Open and effi-
cient foundation language models. arXiv preprint
arXiv:2302.13971.
Hugo Touvron, Louis Martin, Kevin Stone, Peter Al-
bert, Amjad Almahairi, Yasmine Babaei, Nikolay
Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti
Bhosale, et al. 2023b.
Llama 2: Open founda-
tion and fine-tuned chat models.
arXiv preprint
arXiv:2307.09288.
Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
Kaiser, and Illia Polosukhin. 2017. Attention is all
you need. Advances in neural information processing
systems, 30.
Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou,
et al. 2022. Chain-of-thought prompting elicits rea-
soning in large language models. Advances in neural
information processing systems, 35:24824–24837.
Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak
Shafran, Karthik Narasimhan, and Yuan Cao. 2022.
React: Synergizing reasoning and acting in language
models. arXiv preprint arXiv:2210.03629.
Kun Yu, Gang Guan, and Ming Zhou. 2005. Resume
information extraction with cascaded hybrid model.
In Proceedings of the 43rd annual meeting of the
Association for Computational Linguistics (ACL’05),
pages 499–506.
Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang,
Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen
Zhang, Junjie Zhang, Zican Dong, et al. 2023. A
survey of large language models.
arXiv preprint
arXiv:2303.18223.
Shicheng Zu and Xiulai Wang. 2019. Resume informa-
tion extraction with a novel text block segmentation
algorithm. Int J Nat Lang Comput, 8(2019):29–48.
