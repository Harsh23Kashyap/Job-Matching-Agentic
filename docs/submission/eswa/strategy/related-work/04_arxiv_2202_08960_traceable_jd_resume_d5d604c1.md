## Page 1

RESEARCH PROPOSAL
Toward a traceable, explainable, and fair
JD/Resume recommendation system
Amine Barrak
Supervised By:
Professor Amal Zouaq (Research Supervisor)
Professor Bram Adams (Research Supervisor)
Department of Computer and Software Engineering
Polytechnique Montréal, Québec, Canada
March 2021
1
arXiv:2202.08960v1  [cs.IR]  2 Feb 2022


---

## Page 2

Co-Authorship
The following publications include a part of my thesis:
• Amine Barrak, Ellis E. Eghan, Bram Adams. "On the Co-evolution
of ML Pipelines and Source Code". IEEE International Conference on
Software Analysis, Evolution and Reengineering (SANER2021).
The following publication is not directly related to the material presented in
this thesis, but were produced in parallel with the research performed for this
thesis.
• Amine Barrak, Ellis E. Eghan, Bram Adams, Foutse Khomh. "Why do
Builds Fail? – A Conceptual Replication Study". Journal of Systems and
Software (JSS2020).
1


---

## Page 3

Contents
1
Introduction
7
1.1
Context and Motivation . . . . . . . . . . . . . . . . . . . . . . .
7
1.2
Objectives and Contributions . . . . . . . . . . . . . . . . . . . .
9
2
Background
11
2.1
Basic Concepts . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
2.1.1
Job Description (JD) . . . . . . . . . . . . . . . . . . . . .
12
2.1.2
Candidate or Job Seeker . . . . . . . . . . . . . . . . . . .
12
2.1.3
Match a job seeker to a job description
. . . . . . . . . .
12
2.1.4
Data and ML pipeline traceability
. . . . . . . . . . . . .
12
2.1.5
Biases in automated e-recruitment . . . . . . . . . . . . .
13
2.2
Information Retrieval Concepts . . . . . . . . . . . . . . . . . . .
13
2.3
Evaluation Metrics . . . . . . . . . . . . . . . . . . . . . . . . . .
14
2.3.1
Performance Evaluation Metrics
. . . . . . . . . . . . . .
14
2.3.2
Normalized Discounted Cumulative Gain
. . . . . . . . .
15
2.3.3
Average Precision . . . . . . . . . . . . . . . . . . . . . . .
15
2.3.4
MRR (Mean Reciprocal Rank) . . . . . . . . . . . . . . .
16
3
Systematic Literature Review
16
3.1
Methodology
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
3.2
Explainable Model Architectures . . . . . . . . . . . . . . . . . .
19
3.3
Job Description and resume features used for matching . . . . . .
20
3.3.1
Resume Features . . . . . . . . . . . . . . . . . . . . . . .
20
3.3.2
Job Description Features
. . . . . . . . . . . . . . . . . .
22
3.4
Semantic Representation . . . . . . . . . . . . . . . . . . . . . . .
24
3.4.1
Similarity Measures
. . . . . . . . . . . . . . . . . . . . .
24
3.4.2
Ontologies and knowledge bases . . . . . . . . . . . . . . .
25
3.5
Neural Network Architectures . . . . . . . . . . . . . . . . . . . .
28
3.5.1
Recurrent Neural Network (RNN)
. . . . . . . . . . . . .
29
3.5.2
Convolutional Neural Network (CNN) . . . . . . . . . . .
30
3.5.3
Graph Neural Networks (GNN) . . . . . . . . . . . . . . .
31
3.5.4
Transformer architecture (Attention-based components) .
32
3.5.5
Word embeddings and pre-trained language models . . . .
33
3.5.6
Classical Machine Learning . . . . . . . . . . . . . . . . .
34
3.6
Multilingual matching models . . . . . . . . . . . . . . . . . . . .
35
3.7
Biases in the automated e-recruitment Machine Learning algo-
rithms decisions . . . . . . . . . . . . . . . . . . . . . . . . . . . .
37
3.8
Data and Machine Learning traceability . . . . . . . . . . . . . .
37
2


---

## Page 4

4
Research Methodology
38
4.1
What is the state-of-the-art in JD/Resume matching?
. . . . . .
39
4.2
Overview of the Proposed Architecture . . . . . . . . . . . . . . .
40
4.3
Data Sources and pre-processing
. . . . . . . . . . . . . . . . . .
41
4.3.1
The Airudi dataset . . . . . . . . . . . . . . . . . . . . . .
41
4.3.2
Websites scraping
. . . . . . . . . . . . . . . . . . . . . .
42
4.3.3
RecSys Challenge 2017 . . . . . . . . . . . . . . . . . . . .
43
4.3.4
Common data pre-processing . . . . . . . . . . . . . . . .
43
4.4
Resume and job description features . . . . . . . . . . . . . . . .
43
4.4.1
The resume features . . . . . . . . . . . . . . . . . . . . .
43
4.4.2
The job features
. . . . . . . . . . . . . . . . . . . . . . .
44
4.5
Features extractions
. . . . . . . . . . . . . . . . . . . . . . . . .
45
4.5.1
Occupation mapping using deep contextualized word em-
beddings . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
4.5.2
Feature extractions from Resumes
. . . . . . . . . . . . .
48
4.5.3
Feature extraction from Job Description . . . . . . . . . .
49
4.5.4
Features Extraction Validation . . . . . . . . . . . . . . .
50
4.5.5
Language model for annotating features . . . . . . . . . .
50
4.6
Can knowledge base and modern language models improve JD/Re-
sume matching? . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
4.6.1
Baseline model: Job-Resume matching based on language
model transformers . . . . . . . . . . . . . . . . . . . . . .
51
4.6.2
Features similarity and candidates ﬁltering out . . . . . .
55
4.6.3
Matching candidates to job oﬀer
. . . . . . . . . . . . . .
55
4.7
Traceability & Explainability of the matching system . . . . . . .
55
4.7.1
Language model Interpretability and Explainability
. . .
55
4.7.2
How explain the decision of JD/Resume matching to con-
cerned stakeholders? . . . . . . . . . . . . . . . . . . . . .
55
4.7.3
Can traceable models be integrated into a JD/Resume
matching process with low impact on the system com-
plexity? . . . . . . . . . . . . . . . . . . . . . . . . . . . .
59
5
Preliminary results
60
6
Conclusion and Future Work
60
3


---

## Page 5

List of Figures
1
Illustration of Job Description (JD) . . . . . . . . . . . . . . . . .
12
2
Example of the ESCO ontology labeled with a unique URI in
English and French languages . . . . . . . . . . . . . . . . . . . .
28
3
An unrolled Recurrent Neural Network (Original ﬁgure from [1])
29
4
Bidirectional LSTM architecture (Original ﬁgure from [2]) . . . .
29
5
Convolutions Neural Network architecture (Original ﬁgure from
[3]) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
30
6
The Transformer - model architecture [4] . . . . . . . . . . . . . .
32
7
BERT: Pre-training of Deep Bidirectional Transformers for Lan-
guage Understanding architecture (Original ﬁgure from [5]) . . .
34
8
Overview of ﬁne-tuning pre-trained models
. . . . . . . . . . . .
34
9
Overview of the Research methodology of the Thesis . . . . . . .
39
10
Overview of the proposed architecture of matching Resumes to
the Job description . . . . . . . . . . . . . . . . . . . . . . . . . .
40
11
An example of a web developer Resume . . . . . . . . . . . . . .
44
12
An example of a job description for a web developer
. . . . . . .
45
13
The hierarchy structure of the ESCO ontology [6] . . . . . . . . .
46
14
Example of URI of Web Developer occupation in ESCO ontology 1 47
15
Extracting of Candidate features . . . . . . . . . . . . . . . . . .
49
16
Extracting of Job features . . . . . . . . . . . . . . . . . . . . . .
50
17
Proposed matching system . . . . . . . . . . . . . . . . . . . . . .
51
18
The tokens length for the candidates and jobs dataset
. . . . . .
52
19
Architecture of multiple Camembert architecture . . . . . . . . .
53
20
Preliminary overview of the proposed explainable system for the
concerned stakeholders . . . . . . . . . . . . . . . . . . . . . . . .
57
21
The artifacts that should be continuously traceable in the match-
ing JD/Resume environment
. . . . . . . . . . . . . . . . . . . .
59
22
Research timeline . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
1http://data.europa.eu/esco/skill/69bbd53f-fbb0-4476-b4b2-ef7844464e28
4


---

## Page 6

List of Tables
1
Confusion matrix for a binary classiﬁcation
. . . . . . . . . . . .
14
2
Common performance metrics using the confusion matrix. . . . .
14
3
Recommendation base multilingual matching models . . . . . . .
35
4
Dataset labels distribution, the relation between jobs and resumes
are splitted into (unknown, match and unmatch) liaison . . . . .
41
5
Dataset labels distribution, the relation between jobs and resumes
are splitted into (unknown, match and unmatch) liaison . . . . .
42
6
Performance of multiple Camemberts on test set
. . . . . . . . .
54
5


---

## Page 7

Abstract
In the last few decades, companies are interested to adopt an online
automated recruitment process in an international recruitment environ-
ment.
The problem is that the recruitment of employees through the
manual procedure is a time and money consuming process. The manual
recruitment process could also possibly be erroneous in hiring incompetent
individuals. As a result, processing a signiﬁcant number of applications
through conventional methods can lead to the recruitment of clumsy in-
dividuals. Diﬀerent JD/Resume matching model architectures have been
proposed and reveal a high accuracy level in selecting relevant candidates
for the required job positions. However, the development of an automatic
recruitment system is still one of the main challenges. The reason is that
the development of a fully automated recruitment system is a diﬃcult task
and poses diﬀerent challenges. For example, providing a detailed matching
explanation for the targeted stakeholders (candidate recruiter, company
who posted the job) is needed to ensure a transparent recommendation.
There are several ontologies and knowledge bases that represent skills
and competencies (e.g, ESCO, O*NET) that are used to identify the can-
didate and the required job skills for a matching purpose. Besides, modern
pre-trained language models are ﬁne-tuned for this context such as identi-
fying lines where a speciﬁc feature was introduced. Typically, pre-trained
language models use transfer-based machine learning models to be ﬁne-
tuned for a speciﬁc ﬁeld. However, a combination of ontologies knowledge
bases with modern language models is missing. In this proposal, our aim
is to explore how modern language models (based on transformers) can
be combined with knowledge bases and ontologies to enhance the JD/Re-
sume matching process. Our system aims at using knowledge bases and
features to support the explainability of the JD/Resume matching. Fi-
nally, given that multiple software components, datasets, ontology, and
machine learning models will be explored, we aim at proposing a fair, ex-
plainable, and traceable architecture for a Resume/JD matching purpose.
As a ﬁrst step, a systematic literature review is conducted to under-
stand the available models of resume/ job matching architecture, the fea-
tures used to address the matching, and the evaluation metrics used in
the experiences.
Results of this thesis are targeted to make such e-recruitment become
suitable for a fair JD/Resume matching; providing an explanation to the
concerned stakeholders and keep a traceable, scalable JD/Resume rec-
ommendation system environment. The machine learning models’ per-
formance will be evaluated on a gold dataset provided by Airudi, using
the normalized discounted cumulative gain according to the number of
recommended candidates.
Keywords: Job Matching, Traceability, Explainability, Machine Learn-
ing.
6


---

## Page 8

1
Introduction
1.1
Context and Motivation
Determining a suitable candidate for the job is not a simple task. The con-
ventional recruitment process typically follows manual procedures. The manual
recruitment process requires substantial sources such as trained recruiters in
the human resource (HR) department, training expenses, etc. Moreover, these
recruitment processes also require signiﬁcant eﬀorts and time to ﬁnd relevant
candidates for the required job positions. Therefore, ﬁltering the most relevant
candidates manually from a giant list of prospective candidates is troublesome.
Several recent studies have been devoted to addressing the challenges related
to the manual recruitment process. In the advertisement of job descriptions and
recruitment processes, dealing with resumes in multiple languages is not easy.
One of the most crucial challenges in multilingual job oﬀers and resumes is ﬁnd-
ing the most relevant multilingual candidates through the manual recruitment
process.
For example, people speak multiple languages in countries such as
Canada, India, and Belgium. Notably, in Canada, some people speak English,
while others speak French in diﬀerent cities (e.g., Montreal). Similarly, residents
of Flanders communicate in Dutch. Nonetheless, Belgium has three oﬃcial lan-
guages (Dutch, German, and French). Similarly, India has two oﬃcial languages
(English and Hindi). Hence, this implies that a larger pool of candidates in dif-
ferent languages seek job opportunities. Thus, an automatic recruiting system
is required to help job seekers access the recruitment opportunities eﬀectively
and reduce the manual work in the recruitment process.
An eﬀective e-recruiting model frees companies from data overburden and
advertisement cost, since it ﬁlter out incompetent candidates. The e-recruiting
model can also help job seekers eﬀectively access recruitment opportunities and
reduce recruitment work. The key module for a unique e-recruiting model is
the job matching framework that makes an eﬀort to draw in the jobless who
are appropriate to the opportunities to be ﬁlled, where appropriate means that
a considered employer would be keen on perusing the retrieved resumes (cur-
riculum vitae), while job seekers would have a fair chance to be hired. Finally,
an automatic resume matching system can be signiﬁcant in ﬁltering relevant
candidates during the recruitment process.
Moreover, resume screening is a
sensitive subject in biased decision making i.e., ethnic minority application [7].
Since machine learning models are trained using data, and if the data focuses
on speciﬁc features, then machine learning models will make biased predictions
that can have detrimental eﬀects. Therefore, it is vital to ensure that the data
is not biased and contains multifaceted classes. For example, training a model
on people’s resumes in a speciﬁc age range will create a biased model that may
eliminate a qualiﬁed person.
The current job searching systems are unable to understand the semantic
of various resumes and have not kept pace with the ongoing advancement in
ML and natural language processing (NLP) methods. These solutions are com-
monly applied by manually extracted features/attributes and a set of rules with
7


---

## Page 9

predeﬁned weights on keywords that lead to an ineﬀective search experience for
job-seeking candidates. Moreover, these techniques are not scalable. Moreover,
some job seekers or company owners often keep ﬁelds empty in which informa-
tion is required. For example, these ﬁelds can be job title, biography, etc.
The data related to recruitment is usually handled by a relational database
query system [8]. An ideal framework would extract the exact features from
applicant resumes for a job or several jobs possibly reasonable for an applicant.
However, utilizing a relational database system for this job matching problem
will run into two following signiﬁcant barriers: (i) numerous text input ﬁelds
are as free form or informal text by seekers instead of special keywords related
to jobs. That implies that the desired output cannot be reliably matched; this
is more of an information retrieval task, (ii) a number of ﬁelds are missing:
applicants usually do not include all the ﬁelds in an online resume form. For
instance, in the collection of a study, 90% of resumes are missing the Summary
ﬁeld, and 23% of the resumes are without the Resume Body ﬁeld [9].
The job recommendation systems require instantly to recommend accurate
and precise jobs to the applicants and managers and regularly update the strat-
egy of the system to maximize applicants’ fulﬁllment. To accomplish person-
alization, applicants’ explicit data, for instance, applicants’ jobs’ type, skills,
experiences, age, gender, and salary package ought to be adequately utilized.
Therefore, recommendation depends on explicit data that could bring risks of
longer jobless duration or a large number of disappointed employment searchers
[10]. That is one of the reasons that big companies like Microsoft recommend
applicants to submit their implicit information (which is not explicitly present
in a JD), for example, social networking sites (Facebook, LinkedIn, etc.), to con-
sider applicants’ online interactions. Implicit data comprises of all signs about
applicants’ interests that can be concluded by their online actions such as the
sites they explored, the time they spent on a particular page, and the sites they
bookmarked for returning to [10]. A job experience of a candidate had may
contain implicit skills that were not mentioned, therefore, a semantic analysis
of such experience can be understood in, similar context such as the intention
may exist in JD [11].
There are several hurdles in modeling multilingual CV matching systems.
From one perspective, a lack of resources and insuﬃcient data to train machine
learning algorithms, in particular, for a speciﬁc language, can lead a machine-
learning algorithm to provide poor results. Therefore, the development of rele-
vant datasets, especially annotated datasets can help to train a machine learning
algorithm that can learn general hidden patterns in the datasets and obtain good
performance. Such knowledge may be retrieved from structured public ontolo-
gies, which is a graph representation of semantic knowledge information (e.g,
ESCO, O*NET). Annotated domain ontologies contain knowledge i.e., skills,
education, universities that can be reﬁned with the additional dataset by con-
serving its internal associations’ rules (same as, related to) [12].
Context-based transfer learning models [4], such as BERT, XLNet, etc. have
been very beneﬁcial in producing state-of-the-art results in diﬀerent NLP tasks,
such as natural language understanding [5], language inference [13], and machine
8


---

## Page 10

translation [4]. Transfer Learning has also performed extraordinarily in the com-
puter vision ﬁeld where an essential step is to ﬁne-tune the pre-trained models
with ImageNet [14, 15]. Some Simple Transformer models keep on advancing
the ﬁeld of NLP at a great pace, for example, DistilBERT, and RoBERTa [16].
A language model system may identify correctly features in a Job/Resume,
once it is ﬁne-tuned on a large speciﬁc knowledge base.
Traceability and explainability are vital for transparency. Traceability is the
ability to track every aspect of the process to improve product quality, opera-
tional eﬃciency, and the rise in safety awareness. In addition to this, traceability
helps to review the product development ﬂow. Traceability is essential to estab-
lish a communication connection and to promote collaboration with suppliers by
implementing tracking systems. On the other hand, explainability aims to ad-
dress how machine learning algorithms make a decision. Furthermore, explain-
ability is an essential aspect of digital product development because it highlights
the data insights, parameters, and decision point that machine learning algo-
rithm used for decision-making and recommendation process.
Consequently,
Traceability and explainability are signiﬁcant to minimize opaqueness.
1.2
Objectives and Contributions
This project aims to propose an eﬀective e-recruiting tool to suggest the best
candidates for the job postings. We propose to investigate the following objec-
tives:
1. study the State-of-the-art in the JD/Resume matching systems.
2. propose an e-recruiting architecture that considers JD/Resume matching
by combining knowledge bases with a pre-trained transformer-based ma-
chine learning model such as BERT.
3. provide an explainable report to the stakeholders of the recommendations
of the matching decision.
4. adapt an existing traceable model to track the proposed matching and
explainable architecture layers.
This project will be accomplished by collaborating with a startup called
"Airudi" under a Mitacs internship program 2. Airudi aims to develop an e-
recruiting tool that can recommend the best candidates to companies according
to the job requirements. Moreover, Airudi is a third-party company that receives
job oﬀers from companies that require new people to ﬁll various job positions.
So, Airudi advertises the job oﬀers and receives a list of prospective candidates
interested in the job positions. Finally, Airudi is required to provide a list of
the most appropriate candidates to the recruiters to conduct interview sessions.
The e-recruiting system will recommend a list of resumes written in the same
language required in the job description. For example, if a job description is
2https://www.mitacs.ca/en/companies
9


---

## Page 11

written in French, then the e-recruiting system will only ﬁnd the most relevant
candidates having their resume written in French.
To achieve our goal, the following questions are designed to study a traceable,
explainable, and fair JD/Resume recommendation system.
• RQ1: What is the state-of-the-art in JD/Resume matching? In
this research question, we plan to study the state-of-the-art in the JD/Re-
sume matching. A systematic literature review will be conducted on works
not earlier than in 2014 to cover the most recent developments concerning
job description and resume matching.
After studying JD/Resume matching systems, our objectives will be based
on two types of approaches/representations:
1. The Ontologies and knowledge bases: This language model uses a multi-
relational graph that contains connected entities called nodes and relations
called edges to create a structured representation (ESCO[17], DBpedia3,
WordNET4).
2. Transfer learning using language modeling: These language models are
ﬁrst trained on a huge amount of text, known as pre-trained models such
as BERT [5], MUSE 5, and mBART [18]). The pre-trained models can
learn the words, grammar, structure, and other linguistic features of a
language. In addition to this, the pre-trained models can be ﬁne-tuned
on speciﬁc tasks such as classifying sentences in the resume or the job
description if the sentences contain skills features [19].
More speciﬁcally, we also intend to investigate the following research ques-
tion:
• RQ2: Can knowledge base and modern language models improve
JD/Resume matching?
In this research question, our goal is to combine the multilingual knowl-
edge provided by existing ontologies, i.e., ESCO, DBpedia, with ﬁne-tuned
modern pre-trained models to improve the identiﬁcation of the multilin-
gual features. Then, a matching process between the identiﬁed features in
both JD/Resume will be adopted to rank the most appropriate candidates
for the proposed job oﬀer. Moreover, to verify if the proposed JD/Resume
matching model is not biased in the token decisions will be considered.
Once a fair matching model is set up, a matching decision is made. Moreover,
stakeholders need to have an explanation of the models taken decisions. We
consider stakeholders as a job seeker, recruiter, or the company who posted the
job. A detailed explanation of the concerned stakeholders is needed. Therefore,
we formulate the following research question:
3http://mappings.dbpedia.org/index.php/Main_Page
4http://compling.hss.ntu.edu.sg/omw/
5https://github.com/facebookresearch/MUSE
10


---

## Page 12

• RQ3: How explain the decision of JD/Resume matching to con-
cerned stakeholders?
In this research question, we want to explore a way to improve the JD/Re-
sume matching model designed previously to provide an explainable re-
port to the concerned stakeholders.
A report contains the list of the
best-ranked candidates to the recruiter that contain information like
(1) the selection criteria of the candidates and (2) a comparison between
candidates to make a better decision during the interview day. A report
to the job seekers indicates the possible reasons to rank taken decision
(admitted/refused). A report for the company who posted the job
will explain the recruiter evaluation criteria in choosing a person from the
best-ranked candidature nominated for the job.
We will focus on the data cleaning to minimize bias and ensure the stake-
holders’ conﬁdence in our explained reports.
In the previous RQ3, a matching decision between resume and job description
needs to be explained to the concerned stakeholders. During that process, there
is a need to track the diﬀerent stages concerning the evolution of the model’s
decisions by adapting existing traceability modules [20, 21, 22]. Therefore, we
formulate our following research question:
• RQ4: Can traceable models be integrated into a JD/Resume
matching process with low impact on the system complexity?
To answer this research question, a traceable module needs to be adapted
for the current matching JD/Resume challenges described as follows: (1)
Once a fair and explainable model is set up, multiple related submodels
will be generated in the same pipeline (or workﬂow); (2) The most relevant
features of resume and job description can be extracted using semantic
models and/or deep learning methods can be adapted; (3) Experimental
scenarios can be realized with a diﬀerent set of values or hyperparameters
to deploy the selected models; (4) To ﬁnd the accurate models, the au-
tomation of these pipelines is essential and these previous steps must be
repeated with a diﬀerent set of parameters. By knowing that additional
features such as the traceability tools may increase the system’s complex-
ity [23], a case study on the co-evolution of ML pipelines and source code
can be signiﬁcant.
2
Background
2.1
Basic Concepts
We describe in the following subsections the main basic concepts that we will
use during this proposal.
11


---

## Page 13

2.1.1
Job Description (JD)
A job description is a written description of what the person holding a particular
job is expected to do, how they must do it, and the rationale for the required
job procedures [24]. A typical job description includes information about the
company, contact details, job tasks, skills, and educational requirements, and
desired personality. It may contain other details describing speciﬁc requirements
for the job seekers’ candidacy.
Job Summary:  This account Managaer position presents an exciting opportunity to ....
Job Responsabilities:
You will be responsible for the web UI design and implementation for the new products of
the team....
Job Skills & Qualiﬁcation:
1. B.S in computer science or software engineering
2. With at least 2 years of working experience ...
Preferred: 
ERP system knowledge
Figure 1: Illustration of Job Description (JD)
2.1.2
Candidate or Job Seeker
A job seeker is someone who is looking for a job(s). He should present a resume
that contains personal information, educational studies, skills acquired, his job
experiences, languages mastered, etc.
2.1.3
Match a job seeker to a job description
When a job seeker is looking for a speciﬁc job, the candidate will apply for the
job and send his resume to the company that posted the job. Based on the
job seeker’s resume, and the job description details, a matching engine can use
information parsed from the job description requirements and the list of resumes
that applied to the job, such as, skills, education, degree of study, proﬁciency
in languages, etc.
Based on the similarity between a job description and a
list of candidates, the matching engine will automatically recommend a list of
the most similar resumes that meet the requirements. Finally, this automated
process reduces the time to search for candidates and jobs using traditionally
used listing providers and manual search techniques with the keyword.
2.1.4
Data and ML pipeline traceability
Modern ML applications require elaborate pipelines for data engineering, model
building, and releasing [25]. Data engineers use a pipeline of tools to automate
the collection, preprocessing, cleaning, and labeling of data. In contrast, data
scientists use a pipeline to extract the useful features from the data engineers’
data, execute machine learning scripts while experimenting with diﬀerent sets
of values for hyper-parameters, validate the resulting models, and then deploy
12


---

## Page 14

and serve the selected models. Since these steps have to be repeated over and
over whenever the data and/or model scripts or parameters change, in search
of ever more accurate models, automation of these pipelines is essential.
Recently, a variety of data and model versioning tools have appeared to
support data engineers and scientists [26].
Popular tools comprise DVC [4],
MLFlow [5], Pachy-derm [6], ModelDB [7] and Quilt Data [8]. They typically
combine the ability to specify data and/or model pipelines, with advanced ver-
sioning support for data/models, and the ability to deﬁne and manage model
experiments.
One or many of these mentioned tools will be adapted to cover the trace-
ability of the diﬀerent layers of the proposed architecture.
2.1.5
Biases in automated e-recruitment
The biases in the decision of automated e-recruitment that can be linked to the
trained machine learning models. A biased model could be trained on a speciﬁc
type of people, e.g., gender. The model in such a case will prefer a class of
candidates compared to others.
2.2
Information Retrieval Concepts
Traditional word vector
Bag of Words or vector representation. Bag of words (BoW) is a language model
used to represent the presence or absence of a word.
This language model
provides a dictionary of words, but incapable of analyzing the relationships
between words syntactically (structure) and semantically (meaning).
TF-IDF
The term frequency and inverse document frequency (tf-idf) is a weighting
scheme used to assign a numerical statistic that is intended to reﬂect the im-
portance of each word in the document. It is important to highlight that BoW
model only creates vectors of word occurrences (counts). TF-IDF model, on
the other hand, highlights what words are more important words and what
words are less important in the dataset. BoW language model has such limita-
tions such as this model does not take word ordering into account. Similarly,
BoW model considers rare words less important. Therefore, to overcome these
limitations, TF-IDF vectors can be vital. The Tf-idf is calculated as follows:
Wi,j = tfi,j ∗log( N
dfi
)
(1)
Where:
• tfi,j = Number of occurences of i in j
• dfi = Number of documents containing i
• N = Total number of documents
13


---

## Page 15

2.3
Evaluation Metrics
The following section presents some basic common performance metrics used
in literature experiments to evaluate their methodologies in the JD/Resume
matching e.g., performance of the model predicted classes of trained pairs of
<JD, Resume>. Moreover, other classiﬁcation metrics are considered according
to the number of candidates that will be predicted e.g., average precision.
2.3.1
Performance Evaluation Metrics
In binary classiﬁcation, a confusion matrix is commonly used to report perfor-
mance metrics results. The Confusion Matrix (CM) is used in Table 1[27].
• True positive (TP) are positive instances correctly identiﬁed as positive.
• True negative (TN) are negative instances correctly identiﬁed as negative.
• False positive (FP), also known as Type I errors, are negative instances
incorrectly identiﬁed as positive.
• False negative (FN), also known as Type II error, are positive instances
incorrectly identiﬁed as negative.
Labelled positive
Labelled negative
Positive prediction
True Positive (TP)
False Positive (FP)
Negative prediction
False Negative (FN)
True Negative (TN)
Table 1: Confusion matrix for a binary classiﬁcation
From the confusion matrix, we may calculate other performance metrics as
shown in Table 2.
Performance metric
Formula
Recall (R), True Positive Rate (T P R)
T P
T P +F N
True Negative Rate (T N R)
T N
T N+F P
False Positive Rate (F P R)
F P
F P +T N
Precision (P)
T P
T P +F P
Accuracy
T P +T N
T P +T N+F P +F N
F1-score
2∗P ∗T P R
P +T P R
Table 2: Common performance metrics using the confusion matrix.
14


---

## Page 16

Another metric Area Under the ROC curve (AUC) is used to avoid the
usage of (TPR) and (FPR) independently. It is a plot of (TPR) versus (FPR)
at diﬀerent classiﬁcation cut-oﬀs. The Receiver Operating Characteristic (ROC)
curves are usually used when there are roughly equal numbers of instances for
each class, in other words, when the data is balanced [28].
2.3.2
Normalized Discounted Cumulative Gain
The Discounted Cumulative Gain (DCG) is used in rankings with multiple
grades of relevance, e.g., very relevant, relevant, irrelevant and very irrelevant
[29].
The Normalized DCG (NDCG) is a performance metric that has seen in-
creased adoption within the ﬁeld of information retrieval [30]. It has been used
in [31, 32, 33, 34, 35, 36, 37].
DCGn =
n
X
i=1
2reli −1
log2(i + 1)
(2)
NDCGn = DCGn
IDCGn
(3)
IDCGn =
|rel|
X
i=1
2reli −1
log2(i + 1)
(4)
Where:
• Value of rel i is 1 if the item at i in the ranked list is correct recommen-
dation, otherwise rel i is 0.
• n: length of the returned list.
• DCG n : is DCG value of the TopN.
• IDCG n : is ideal DCG value of the TopN.
• |rel| is the size of the jobs.
2.3.3
Average Precision
Average Precision (AP) measurement is used to rank two grades of relevance
(relevant and irrelevant). These measurements determine how accurate the rec-
ommendation system ranks candidates’ applications and the selected candidates.
These methods generate a score according to the rank of actually recommended
applications on the top-k recommendation list.
AP =
Pn
i=1(P(i) ∗rel(i))
#releventitems
(5)
Where:
15


---

## Page 17

• n: the number of recommended jobs for a user.
• rel(i) is 1 if the item at position i in the ranked list is correct recommen-
dation, otherwise it is 0.
• P(i) is precision of top i.
In addition to this, some studies also used a mean average precision to eval-
uate the performance of machine learning models [29, 38, 39, 35].
2.3.4
MRR (Mean Reciprocal Rank)
Reciprocal rank (RR) is a measure that takes into account the ﬁrst position of
the relevant ranked resume list. MRR is the mean of all jobs’ RR values. This
measure was considered in [31, 33, 35, 40, 11].
MRR =
1
|U|
U
X
i=1
1
Ranki
(6)
Where:
• |U|: The number of jobs have recommendation users
• Ranki : The ﬁrst relevant position in recommended users
3
Systematic Literature Review
We designed a Systematic Literature Review (SLR) to cover the existing research
done in the domain of JD/Resume matching. In the beginning, we start by
describing the methodology we followed in our SLR in section3.1. We present
the methods used for artiﬁcial intelligence (IA) explainability in section 3.2
the diﬀerent features used in resume/ job description in section3.3 and the
system knowledge representation in section3.4.
Furthermore, in section 3.5,
we provide an overview of machine learning-based recommendation systems.
Recommendation models are presented in section3.6. Eventually, we talk about
Machine learning traceability systems3.8.
3.1
Methodology
A systematic literature review is considered an eﬀective research methodology
[41] to identify and discover new facts about a research area and to publish
primary results to investigate research questions [42, 41].
This SLR is used to achieve the following ﬁve objectives:
• Understand the JD/Resume matching.
• Identify the features used in the literature to make the matching.
16


---

## Page 18

• Categorise the diﬀerent methodologies used to match JD/Resume.
• Find diﬀerent metrics used to evaluate the matching process.
• Investigate the methods used to cover multilingual JD/Resume
The relation of this SLR with the thesis goal is to create a catalog of the
most used methodologies of multilingual JD/Resume matching and identify the
gaps inside.
To the best of our knowledge, in the literature, there is no systematic lit-
erature review on matching JD/Resume published for the period we covered
between 2014 and 2021.
SLR Planning
We performed an SLR covering matching between resumes and job descriptions
in human resources published from 2014 to 2021. Instead of applying a manual
search, we perform an automated search using Engineering Village 6 to search
for papers related to the matching of resumes and job description. Engineering
Village is an information discovery platform that is connected to several trusted
engineering electronic libraries. Specialized in engineering, it oﬀers many op-
tions to reﬁne the search queries, excludes and inclusion criteria, and provides
the ﬂexibility for the choice of period, language, venues, and authors.
This platform gives users also the ability to search for all recognized journals,
conference, and workshop proceedings together with the same search query [43].
Engineering village includes three data banks Compendex, Inspec, and Knovel.
For our study, we will focus on one data bank, Compendex, to avoid duplicated
papers.
According to our goal which is to study the JD/Resume matching system in
the literature, we assume that the main keywords to make the search query are:
Resume, Job Description and matching. We have used keywords, their
synonyms, and stems to make our search query. Synonyms and truncations are
needed to ensure a complete collection of papers.
1. Resume: resume*, cv, candidate, employee*, job seeker
2. Job: job*, "human resource", recruiter
3. Match: recruitment* OR recommendation* OR hire OR hiring OR match*
Using these keywords, we have combined them with logical operators (AND,
OR). The ﬁnal search query is:
((resume* OR cv OR candidate OR employee* OR "job seeker") AND (job*
OR "human resource" OR recruiter ) AND (recruitment* OR
recommendation* OR hire OR hiring OR match*) AND (ca OR ja) WN DT)
OR ("person-job" AND ﬁt*)
6https://www.engineeringvillage.com/search/quick.url
17


---

## Page 19

"({ca} OR {ja}) WN DT" is an attribute used to allow the server of Com-
pendex to limit results to only documents of type conference articles or journal
articles.
Please note that we validated the query on a set of papers that we knew
already relevant.
SLR Execution
The SLR execution phase was carried out in two steps and executed in August
2020. The ﬁrst one was dedicated to the execution of the search query on the
Engineering village platform.
The query returned 752 papers as primary results. Browsing the research
articles rapidly, we found that unrelated terms needed to be excluded i.e., senti-
ment, behavior, work turnover, sales, work stress, jobseeker satisfaction, crime,
appearance, social network.
We proceeded to add exclusion criteria to exclude papers out of scope.
We used the check-box feature oﬀered by Compendex to make the exclusion
(turnover OR satisfact*, stress*, emotion*, appear*, crime*, sale*, advertis*,
behavior*, "social network", sentiment*). The search was limited also to English
language. Only conference and journal papers were retained.
We analyzed all the research papers and veriﬁed their relevance to our study,
in case we found a relevant one, we included it in our paper catalog (9 papers
were manually added).
Finally, we collected 514 articles with the JD/Resume matching.
The second step was dedicated to the manual analysis of the collected arti-
cles. We performed three rounds:
• The ﬁrst round was reading the abstract, introduction, and conclusion of
the 514 papers and eliminating irrelevant or research articles having page
length of fewer than 4 pages (3 papers). Our data included 85 conference
and journal papers after applying the ﬁrst round.
• The second round was dedicated to the snowball search technique7. We
used it to run through all the paper references and extract if any, articles
that were missed or that the search method was unable to identify. Our
data became 109 papers after the snowball round.
• The third round was committed to particularly focus on the 109 papers.
A complete reading of articles was performed to extract:
– The features used to realize the matching.
– The established methods to extract features.
– The matching process.
– The evaluation metrics.
7to mitigate the fact that we considered only compendex databse
18


---

## Page 20

We present the SLR results and the related work of this thesis in the following
sections, organize as follows. First, we discuss the state-of-the-art of explainable
AI in section 3.2. Next, we describe the diﬀerent features used to deal with
JD/Resume matching in section 3.3. In section 3.4, we present the knowledge
base models and the machine learning architectures in section 3.5. In Section
3.6, we provide a comparison between multilingual matching models. Then, we
present the possible biases in machine learning algorithms in section 3.7. Section
3.8presents the data and machine learning traceability models.
3.2
Explainable Model Architectures
JD/Resume matching models have complex architectures.
The matching or
non-matching decision of these models is diﬃcult to understand. The diﬀerent
stakeholders (recruiter, job poster, job seeker) related to a JD/Resume
matching need a personalised addressed explanation. For example, the company
who opened the job vacancy should receive the reasons that make a list of
candidates more suitable to their job description from the company who posted
the job.
Therefore, any detail (features) in the resume and job description
should be interpreted.
Explainability and interpretability are often used interchangeably to un-
derstand the reasons how artiﬁcial intelligence (IA) models made decisions in
matching JD/Resume matching. Therefore Explainability and interpretability
are vital to understanding the model’s decision-making process. Moreover, the
interpretability is used to understand a cause and eﬀect relationship within
a system. For example, understanding what features are more important and
helpful in matching model decision-making process. Explainability, on the
other hand, is used to study the internal mechanics of a machine or deep learn-
ing system so that the model matching decision can be explained in human
terms [44].
Previous studies [45, 46] used the model’s interpretability to highlight the
most important features given by the attention model in a resume or job post
matching. For example, Le et al. [33] reported that the interpretability could be
summarised using an intention rate model of the job seeker and the employer.
Likewise, another study by Jiang et al. [47] revealed that the features extracted
from resumes as semantics entities are helpful in interpreting the matching re-
sult. Finally, all the machine learning models are trained using data, therefore
insights about data extraction and collection process can be crucial in JD/Re-
sume matching process.
The explanation data extraction process should be explicitly explained to
keep the matching traceability during the whole process. However, deep learn-
ing models are typically diﬃcult to interpret due to complex internal transfor-
mations and considered as a black box [48]. Most importantly, some initiatives
have taken to overcome this issue [49, 50].
According to the best of our knowledge, no JD/Resume matching architec-
ture has been proposed as an explainable model yet. However, diﬀerent studies
have been conducted to highlight the importance of explainability in machine
19


---

## Page 21

learning decision models. For example, a recent study by Danilevsky et al. [51]
realized a survey on the explainability of IA for natural language processing
and reported the operations that enable explainability. These operations are:
(1) Layer-wise relevance propagation [52], (2) input perturbations (3) Attention
base models feature importance [53], (4) LSTM and feature importance explain-
ability [54], and (5) Explainability-aware architecture design [55]. Particularly,
Layer-wise relevance propagation is used to enable feature importance explain-
ability. Similarly, input perturbations usually used for a linear model LIME
and Attention based models are used to highlight important features. Similarly,
another study [54] presented LSTM and feature importance explainability, and
Explainability-aware architecture design [55].
Le et al. [33] tried to overcome the interpretability problem by comparing
the intention of the job seeker and employers. However, this is still far from
having good reasons that explain the matching decision reasons.
3.3
Job Description and resume features used for match-
ing
In the provided literature, features are divided based on their usage in candi-
date resumes and job descriptions from the employers. These are distributed
as education level, skills, personal information, job history, experience, and job
industry information provided by the candidates. On the other hand, the re-
quired information in the job description consists of the same information as for
resumes and salary packages oﬀered and jobs to perform in the speciﬁc industry.
Zhang and Vucetic [56] conducted a case study on Linkedin with graduated
students from the same university where they found that features considered to
be important in the recommendation of resumes to the job oﬀer were not used
i.e., year of graduation, gender, and grade point average. This depicts that
there is a gap of research to be done with respect to the grades and gender of
the candidates.
3.3.1
Resume Features
Education The education section involves education level, specialization in the
relevant ﬁeld, awards or achievements, and research publications. These features
show the candidates’ educational backgrounds.
While conducting the resume analysis, education level or qualiﬁcation infor-
mation has been considered vital because of its role in matching with a suitable
job. Some researchers also included academic awards and achievements as fea-
tures in algorithms’ design [57, 58, 57, 59, 60, 61, 40]. Thus, approximately
every research study has included it as a resume feature. However, some studies
primarily focused on skill analysis [62, 63, 64, 32, 65, 66], and job descriptions’
features [67, 68, 69, 46, 37, 64, 70, 71, 72]. Other educational features include
research paper publications and certiﬁcation in the speciﬁc ﬁelds candidates are
graduated in [73, 74, 75, 59, 46, 76, 77].
20


---

## Page 22

Multiple studies have collected datasets from various ﬁelds such as IT [78, 79,
80, 81, 82, 32], programming languages [45, 61, 40, 68, 31, 83, 84, 85], software
engineering [86, 87, 88, 39], Human Resources [89], Economics [66], Business
[78], and computer sciences [90]. In addition to this, other studies are based on
available datasets from various recruitment sites (indeed, monster, glassdoor,
amrood, careerbuilder, BOSS Zhipin and jobstreet) [58, 91, 88, 92, 34, 93, 94],
social media platforms (LinkedIn and Facebook) [58, 95, 57, 36, 84], government
recruitment departments [40, 69, 37, 96] and university career centers [58, 97,
73, 98, 69, 99, 100, 76]. The datasets collected from universities are based upon
the students’ qualiﬁcations only [58, 97, 69, 99, 100, 76].
Acquired Skills Skills are the natural or learned talents and the expertise
developed by the candidates to perform a task or a job.
There are several
key types of skills: soft skills, hard skills, domain-general, and domain-speciﬁc
skills. However, incorporating skills into resumes is not as simple as it sounds.
There are diﬀerent categories of skills to understand, for instance. Moreover,
it’s essential to select the right skills and to include them in resumes.
The second most important features while conducting the resume analysis
are related to the skills obtained in a speciﬁc ﬁeld. Likewise, technical proﬁ-
ciency while working in a speciﬁc job position, years of experience, and resume
holders language proﬁciency. Some studies only used university datasets, how-
ever, the details such as the students have no relevant practical experience in
their ﬁelds are missing [58, 97, 73, 98, 99, 100, 76]. A feature of the actual posi-
tion is added by various algorithms to enhance the workability of job matching
[57, 101, 75, 95, 35, 102]. Finally, Some frameworks are presented to deﬁne lan-
guage as a resume feature because some jobs require native or foreign-language
speakers. Thus this can play a positive role in job matching and recommenda-
tion [95, 98, 103, 104, 91, 88, 60, 105, 61, 40].
Personal Features In job recommendation and matching systems, researchers
consider unique features in the resume to locate the relevant jobs depending
upon the age, language, location, nationality gender, driving license, mari-
tal and military status.
These features directly impact the job description
requirements, and that is why considered important to be added.
However,
some studies used candidates’ personal details without adding unique features
[73, 106, 80, 36, 82, 70, 32, 107, 108, 109].
The current location feature is required when the job is location speciﬁc, or
the recruitment companies want to consider a candidate from a speciﬁc area
[35, 58, 95, 97, 110, 88, 45, 111, 112, 113, 84, 66, 114]. In addition, the age
of the resume holders is considered as the next personal feature and the jobs
are ﬁltered based on the age requirements by the job matching algorithms set
by the recruiters [58, 110, 103, 115, 116, 60, 96, 117, 114]. Studies have also
considered gender information to ﬁlter gender-speciﬁc jobs and to make it easy
for matching [58, 103, 45, 118, 78, 90, 39, 57, 74, 119, 82, 72, 120, 102]. Marital
status feature of the candidates is also added to the personal feature library
by some researchers [90, 39, 75, 121, 122, 123, 34]. The next personal resume
feature of applying candidate is a nationality, and it holds the same importance
as location feature as it helps in addressing the workplace location and requires
21


---

## Page 23

nationality to avoid any travel sanctions [110, 86, 104, 79, 119, 124, 36, 82, 111,
112, 31, 125, 77, 94, 102]. Only one research framework has included military
status to the personal features library [39] and culture [126].
Features Linked to Jobs Resume features linked to candidates’ job his-
tory, current position, salary scale, actual pay, and industry of the job are
essential as they directly match the job requirements mentioned in the job de-
scription of respective ﬁelds. Actual pay [103, 127, 90, 39, 101, 12, 128, 117]
and salary scale [35, 91, 127, 12] are the resume feature to match the pay pack-
age oﬀered by the company and thus considered by many researchers.
The
industry of the jobs of candidates is from an important feature to be con-
sidered to align with the technical job description features, and this is the
reason nearly all the research studies include it in their matching algorithms
[35, 95, 86, 84, 72, 66, 85, 129, 102, 114]. Furthermore, some researchers used
information about jobs demand in industry to better understand candidate’s in-
terests [86, 103, 88, 128, 96, 82, 111, 112, 92, 83, 102]. The candidate’s experience
is considered by taking two things into account: (i) his previous employment
experience ( history in diﬀerent companies) [116, 130, 131], and (2) the number
of jobs he applied in the past [62, 116, 132, 106, 64, 131, 94] have been taken as
features by the researchers. From the employment point of view, employment
preferences [39] and employee turnover [126] are added as resume features.
3.3.2
Job Description Features
There is ample detail in the job description to identify major roles and important
tasks as they occur today. They are not dependent on any particular qualities
of an incumbent (such as experience, expertise, ability, eﬃciency, commitment,
loyalty, years of service, or degree) [9]. They provide the details required to
identify the job, not the employee.
Personal Requirements The job descriptions issued by recruitment agen-
cies or companies possess a certain format which is based on the primary and
secondary level of important information.
As mentioned earlier, some com-
panies are more intended towards getting technical and qualiﬁcation informa-
tion rather than personal details [73, 57, 133, 12, 37, 106, 108, 66, 85, 109].
Depending upon the vacancy available and suitable gender quota, gender in-
formation is considered to be important in job description analysis by stud-
ies undertaken in existing literature. [57, 74, 119, 61, 40, 134, 135, 130, 123].
The required age for the suitable job is also signiﬁcant to ﬁnd a speciﬁc job
[58, 95, 110, 73, 103, 104, 78, 102, 114]. Some of the studies have also included
civil status [118, 74, 119, 122, 94, 114], military status [39] and needed abil-
ity [12, 123, 65, 136] as personal requirements features. Location of the job
placement should be known for the candidate thus it is added frequently by the
researchers [110, 86, 104, 87, 91, 89, 126, 102].
Educational Requirements This section lists the required level of job
knowledge (such as education, experience, knowledge, skills, and abilities) re-
quired to do the job. This section focuses on the “minimum” level of quali-
ﬁcations for an individual to be productive and successful in this role. In a
22


---

## Page 24

job description, it is essential to identify the educational qualiﬁcations that an
employee must possess to satisfactorily perform the job duties and responsibil-
ities. [137] Thus, the educational qualiﬁcations must be stated well in terms of
areas of study and/or type of degree or concentration that would provide the
knowledge required for entry into this position.
Educational requirements features such as degree names and grades have a
primary signiﬁcance in job recommendation systems and all studies have added
this feature in job description analytic algorithms except a few that are more into
technical skills [62, 63, 64, 32, 65, 66]. The academic awards, i.e. scholarships
and awards, are also considered for the distinctive recruitment of employees
[58, 73, 78, 57, 119, 59, 125].
Oﬀered Position The purpose of job descriptions is to make candidates
understand the nature of their responsibilities depending upon their skills, abil-
ity and qualiﬁcation.
The job description must oﬀer a suitable position for
the candidates considering these requirements. Thus, various studies have dis-
tributed this feature into sub-categories for a better match result and improved
the algorithm’s performance [138]. All studies involving job description anal-
ysis include oﬀered positions and industry types for which jobs are available
[35, 58, 95, 97, 73, 86, 98, 139, 103, 91, 88, 118, 78, 39, 57, 74, 140, 119,
133, 141, 12, 59, 142, 121, 143, 115, 144, 61, 40, 68, 134, 145, 89, 135, 130,
146, 106, 147, 100, 125, 83, 113, 93, 136, 102].
The oﬀered salary is men-
tioned in job descriptions depending on the experience and skills a candidate
brings to the position.
[97, 73, 98, 103, 91, 88, 79, 90, 119, 141, 12, 143,
115, 61, 40, 134, 135, 130, 11, 92, 31, 125, 108, 102].
Depending upon the
seniority of job and responsibilities, years of experience deﬁne the candidates’
suitability, and this is why all the studies have included it as job feature ex-
cept the ones that are considering the university datasets or fresh graduates.
[58, 97, 73, 98, 139, 74, 133, 144, 105, 134, 69, 99, 100, 76].
Companies have certain workplaces for their employees, such as to work in a
team or individually. It is important to highlight that some studies considered
the candidate working experience in a team or individually as a feature, called
as teamwork skills[139, 79, 12, 61, 68, 46, 130, 106, 83, 38, 129] and work length
[95, 98, 139, 91, 88, 75, 123, 81] as requirements for the candidates.
Technical Job Requirements A list of the technical roles and obligations
allocated to the job is given in this section; the basic tasks are also referred
to job requirements. The job requires suﬃcient knowledge of the subject area
to address both unique and normal work challenges, to be able to comment on
technological concerns, and to act as a guide for those within the organization
on the subject. [137] Thus, it is important to list particular abilities and/or
skills needed for the performance of the candidate in this position, including
the designation of any required licenses. Analytical, budget exposure, internal
or external contact, machine, innovative thinking, customer service, decision-
making, variety, critical thinking, multi-tasking, collaboration, problem-solving,
project management, oversight, coordination, are some considerations:
In job description analysis, the technical required information such as tech-
nical information [91, 88, 68, 145, 89, 135, 114], technical categories [86, 133,
23


---

## Page 25

141, 57, 81, 83, 114], and speciﬁc ﬁeld experience [86, 140, 133, 141, 145, 89,
135, 130, 114] are necessary. Thus, these features are found to be essential for
job resume matching algorithms.
Furthermore, all these jobs and personal features are divided among cer-
tain matching and recommendation frameworks to diﬀerentiate among job rec-
ommendation, matching, content-based analysis, and resume analytics.
One
to one job description and resume matching are used in the majority of the
studies [103, 104, 79, 57, 74, 140, 119, 89, 126, 96, 85].
Apart from devel-
oping a matching model of both resume and job description matching, some
researchers are more interested in only one of these, i.e., job recommendation.
[110, 62, 91, 45, 90, 141]. These recommendation systems adopt certain algo-
rithms by combining position description and resume information. These algo-
rithms are content base analysis [58, 139, 144, 130], ontology based [61, 32, 29]
and text base classiﬁcation [144, 132, 102].
3.4
Semantic Representation
Semantic methods are useful to identify linked item ideas, since an idea can
be described in multiple textual ways, relying on implicit knowledge of how
diﬀerent terms relate. This information can be encoded in taxonomies, where
relations between diﬀerent terms are mapped, which then can be used during
job matching.
3.4.1
Similarity Measures
There is some work designed to make the matching based on the text similarity
between the candidate resumes and the job description [101, 148]. This method
is based on transforming the list of features (i.e., education, skills, years of
experience, etc) extracted from the resumes and job descriptions into vectors.
A popular measure in data science is the cosine similarity used to compute
the angle diﬀerence between two vectors. The measure will equal 1 when the
vectors are parallel (they point in the same direction) and 0 when the vectors
are orthogonal. Vectors that point in the same direction are more similar than
vectors that are orthogonal [149].
Cosine Similarity
Wenxing et al. [150] proposed a mobile reciprocal job recommender based on
computing the cosine similarity between feature vectors of the job seekers and
the recruiters. Duan et al. [101] used the vector space model (VSM) to cluster
the resumes based on their similarity to reduce the number of matching the job
resume to each position by addressing only the match between clusters and job
description. Rodrigues et al. [122] classiﬁed candidates by feature similarity i.e.,
work experience, education, etc. In contrast, Gubta and Garg [90] proposed
a personalized recommendation to the candidate according to his proﬁle i.e.,
preferring the company that has the same current location [151]. Kenthapadi
24


---

## Page 26

et al. [152] discussed the personalized job recommendation strategy at LinkedIn
where the job seekers receive personalized job postings based on the context
data present in their proﬁles, activities and similar members. However, Nigam
et al. [64] demonstrated that if some candidate applies for similar jobs according
to their interests, this will be a subject of candidates motivation. For example,
if some candidates applied for a job, the same candidates can also be interested
in applying for other similar jobs.
Jaro Winkler distance
Jaro Winkler distance [153] is a measure of similarity between two strings, the
higher the Jaro distance for two strings is, the more similar the strings are.
Maree et al. [154] used this technique to compare the sense of a term used
in resumes and job descriptions if it has a close distance based on the term
surroundings words. Çelik [77] measured the similarity between two terms to
eliminate mi-spelling errors from resumes and jobs description in the parsing
process.
LSI & LDA
The clustering of text and the calculation of similarity should be calculated on
the basis of the text model. The commonly used models are latent semantic
index (LSI) and Latent Dirichlet allocation (LDA).
Latent semantic indexing (LSI) is used to reduce the dimension for classiﬁ-
cation. The idea is that words will occur in similar pieces of text if they have
similar meanings. It is an indexing and retrieval method that uses a mathemat-
ical technique called singular value decomposition (SVD) to identify patterns in
the relationships between the terms and concepts contained in an unstructured
collection of text [155].
On the other hand, Latent Dirichlet allocation (LDA) has been used to
identify the main topic (meaning) of a text. LDA works by creating a normal
distribution of words by randomly choosing topics and then checks for the prob-
ability of the word to belong to a topic regarding all the documents [76]. the
highest score is chosen as the ﬁnal topic. This method has been used in several
works to extract the topic distribution from jobs or resumes [45, 100, 76, 31].
3.4.2
Ontologies and knowledge bases
We found in the literature of JD/Resume matching several approaches that
improve or use the knowledge of existing ontologies or taxonomies to extract
the list of skills in JD/Resume. For example, the ontology Occupational Infor-
mation Network (O*NET)8 database in the USA, the multilingual European
Dictionary of Skills and Competencies (DISCO)9, the ’European Skills, Compe-
tences, Qualiﬁcations and Occupations’ (ESCO)10 have been extended or served
8https://www.onetcenter.org/
9http://disco-tools.eu/
10https://ec.europa.eu/esco/portal/home
25


---

## Page 27

as a base model to create a new ontology/taxonomy. The ontologies are made
in a way that can be updated at any time and adapted to the dynamics of the
labor market [156].
More ontologies were used to extract semantics from the parsed JD/Re-
sume, such as WordNet [157] which is a lexical resource of diﬀerent domains
that contains synonyms and hyponym relations between words. YAGO [158]
is a crowdsourced platform containing structured and relational information
extracted from Wikipedia and other sources in multiple languages. Similarly,
DBpedia [159] ontologies in diﬀerent domains have been created based on the
most commonly used infoboxes within Wikipedia.
Taxonomy
In natural language processing, a taxonomy provides machines ordered represen-
tations and hierarchical relationships among concepts and the words employed
to describe those concepts. For example, a basic NLP taxonomy would have
concepts such as machine learning, which is a subset of AI, and deep learning,
which is a subset of machine learning. In other words, a taxonomy is a collection
of hierarchically classifying concepts in an automatic manner from text corpora.
Gugnani and Hemant [11] created a taxonomy of skills in multiple ﬁelds that
was mined from public online web dataset resources and then used four mod-
ules to split them (Named Entity Recognition, grammatical tagging, embedded
word2vec space of skill-term, skills-term dictionary), they generate a binary
probability equation that determines if the parsed item is a skill-term.
The
probability equations combine the models decision including ONet11, Hope12
and Wikipedia dictionaries. After preparing the taxonomy skills, they use it
to extract explicit skills, and the implicit skills (interpreted from similar jobs).
Finally, Cosine similarity and TF-IDF were used to match skills and explicit-
implicit skills.
Singh et al. [65] used a job-role taxonomy that describes the job roles in-
side the organizations that typically have various job roles, where the hierarchy
describes job categories and job roles at the top, until reaching the individual
skills needed to satisfy the jobs category at lower levels of the taxonomy. The
goal of this work is to determine the target skill that a candidate needed to
learn. Javed et al. [60] used the common ontologies O*NET to associate the job
ads and resumes to the CareerBuilder 13 job title taxonomy.
Ontology
An Ontology is a representation of a set of concepts within a domain and the
relationships between those concepts [160].
Several approaches that are doing the matching JD/Resume chose to cre-
ate their skills base ontology. Balachander et al. [32] built a custom technical
11https://www.onetonline.org/
12https://www.computerhope.com/
13https://www.careerbuilder.com/
26


---

## Page 28

skills ontology by crawling DBpedia and then used to compute the similari-
ty/ dissimilarity between these features to show the relationship between skills
in the ontology. Besides, Celik [77] deployed an ontology-based resume parser
(ORP) that is constructed from many domain ontologies where each ontology
has its domain-based concepts, properties, and relationships according to the
segments of a personal resume (education, location, abbreviations, occupations,
organizations, resume). Their ORP is based on six modules that treat resumes
(converter, segmenter, parser engine, normalization, classiﬁcation and cluster-
ing of concepts, and generating personal résumé ontologies for individuals). The
resumes are analyzed semantically using the framework and a Jaro-Winkler dis-
tance algorithm was used to reform the misspelled parsed terms.
A resume
ontology was proposed also by Mohamed et al. [113] where they considered
personal information, skills, educational qualiﬁcations, certiﬁcations, and work
experience. They proposed a manual update of the ontology in case the new
skills feature is not recognized.
Guo et al. [34] presented in their methodology RésuMatcher a system that
generates a domain-speciﬁc ontology. To compute the similarity and relationship
between skills, DBpedia knowledge taxonomy was used. Corde et al. [63] created
a skill ontology, where they consider the skill similarity of the job seeker and a
job description by computing the path distance between two skills.
Maree et al. [87] built a semantic network from reﬁned concepts of job of-
fers and resumes where words’ semantic relationships are mapped in a network.
They utilize ontologies, WordNet [157], and YAGO [158] to enrich the knowl-
edge with semantic resources and occupational classiﬁcations. The produced
networks from the resume segments were matched with their corresponding net-
works that are extracted from the job oﬀer using Jaro–Winkler distance. The
same idea was applied by Nimbekar et al. [59], where they derived the relat-
edness between skills from both resumes and job posts to construct a semantic
network. The semantic network was used as input to the matching algorithm
to measure the closeness JD/Resume.
In the context of our thesis, we will consider the ESCO ontology to be
used. Since, it contains skills, competencies, qualiﬁcations, and occupations.
ESCO is bridging language barriers by providing terms for each concept in
26 European languages and Arabic. To map between the diﬀerent languages,
each occupation, knowledge, skill/competence provides with a unique universal
URI over the web. ESCO provides a short explanation of the meaning of the
occupations and clariﬁes its semantic boundaries.
27


---

## Page 29

Python
C++
Computer 
Programming
Digital 
Content 
Creation
Broader Skill
Broader Skill
C++
Python
Programmation 
Informatique
Création de 
Contenus 
Numériques
Broader Skill
Broader Skill
http://data.europa.eu/esco/skill/b633eb55-8f1f-
4ae6-ab4c-2022ffe2cb7f
Concept URI
http://data.europa.eu/esco/skill/21d2f96d-35f7-
4e3f-9745-c533d2dd6e97
Concept URI
ESCO 
English Label
ESCO 
French Label
http://data.europa.eu/esco/skill/f5369f2f-e52b-
43d8-8d31-79a6c11188d8
Concept URI
Figure 2: Example of the ESCO ontology labeled with a unique URI in English
and French languages
We present in Figure 2 an example of the ESCO ontology. We can notice
that the skills are listed in a hierarchy. Each skill (or ESCO concept) has a
unique concept URI which is used to identify and map the same skill in diﬀerent
languages. For instance, Software Developer (EN) and Développeur de Logiciels
(FR) share the same concept URI. 14 A real-life example of mapping a resume
skill to a job description required skill would be as follows: (i) If a resume skill
(e.g. C++) directly matches with a skill listed in the job description (e.g. c++),
it will be a perfect match. (ii) However, the model is also beneﬁcial to map
the skills indirectly. e.g., mapping can also be done when resume skill is more
speciﬁc (C++) but the job description skill is broader (computer programming),
or vice versa. Since, C++ is a narrower skill of Computer Programming, it will
be picked up for mapping because the model connects these two as parent-child.
3.5
Neural Network Architectures
Diﬀerent deep learning methods have been used in JD/Resume matching and
advanced the performance and ﬂexibility of solving text mining problems. Some
previous studies used deep learning methods to address NLP tasks [116]. Among
14http://data.europa.eu/esco/occupation/f2b15a0e-e65a-438a-aﬀb-29b9d50b77d1
28


---

## Page 30

various deep learning models, Recurrent Neural Network (RNN), Convolutional
Neural Network (CNN) are widely-used architectures, that can provide eﬀective
ways for NLP problems [46].
3.5.1
Recurrent Neural Network (RNN)
Recurrent Neural Network (RNN) architecture is widely used in many NLP
tasks, it is designed to process sequential information of varying lengths. An
RNN performs the same task for every element of a sequence, with the output
depending on the previous computations, which enables the model to predict
the current output conditioned on long-distance features. Figure 3 shows the
architecture of the Recurrent Neural Network.
Figure 3: An unrolled Recurrent Neural Network (Original ﬁgure from [1])
Qiao et al. [125] created a competency analysis model, where it has a job
description or a resume as input and provided the job requirements and the job
seekers’ competency as outputs.
RNNs have a feedback loop in the recurrent layer of the previous computa-
tion. However, it can be diﬃcult to train them to solve problems that require
learning long-term temporal dependencies, due to the vanishing and exploding
gradient when computing the loss function [161].
The Long Short-Term Memory network (LSTMs) was introduced [162] which
is a variation of RNN that uses special units in addition to standard units.
LSTM units include a ’memory cell’ that can maintain information in memory
for long periods of time to understand the meaning. A set of gates is used to
control when information enters the memory when it’s output, and when it’s
forgotten. As a variant of LSTM, Bi-directional LSTM (BiLSTM) is composed
of a forward LSTM and backward LSTM [163] that can preserve information
from both past and future.
Figure 4: Bidirectional LSTM architecture (Original ﬁgure from [2])
29


---

## Page 31

BiLSTM architecture as shown in Figure 4, has been used in diﬀerent ways
in the matching between resumes and job descriptions to better understand the
context of the text. For example, Qin et al. [45] used BiLSTM to model the
word-level representation of job posting and resumes. In contrast, Luo et al. [38]
provided aggregated representation for resume experiences embedding words.
However, Nigam et al. [64] used a BiLSTM to capture candidates’ interactions
with jobs and get an idea about their preferences by leveraging both past as
well as future candidate-job interactions of the latent job preferences.
Similar to LSTM, Gated recurrent units (GRUs) is a gating mechanism in
RNN to track long-term dependencies eﬀectively while mitigating the vanish-
ing/exploding gradient problems. The GRU operates using a reset gate and an
update gate. The reset gate sits between the previous activation and the next
candidate activation to forget the previous state, and the update gate decides
how much of the candidate activation to use in updating the cell state [164].
Bian et al. [145] employed a bi-directional recurrent neural network with
gated recurrent unit (BiGRU) to model both sentences and documents in a job
posting or a resume.
3.5.2
Convolutional Neural Network (CNN)
Convolutional Neural Network CNN aims at modeling hierarchical relationships
and elicit local semantics. The eﬀort of applying CNN in text mining can date
back to Kalchbrenner et al. [165] where they proposed a Dynamic Convolutional
Neural Network (DCNN) to model sentences.
In the main use of the CNN
architecture in the context of resume and job description matching is to extract
the features [105].
Le et al. [33] deployed a CNN to identify the skills and
characteristics that are important for the matching between job postings and
resumes. Figure 5 shows the architecture of the Convolution Neural Network.
Figure 5: Convolutions Neural Network architecture (Original ﬁgure from [3])
Zhu et al. [107] proposed a framework called PJFNN, based on CNN. They
used a Person-Job Fit Neural Network to learn the joint representations of
Person-Job ﬁtness from historical job applications. They justiﬁed the use of
CNN architecture rather than RNN for textual data modeling for better hierar-
chical relationships and local semantics between a job posting (resume) and its
30


---

## Page 32

requirement (work experience) items. Jiang et al. [47] used word embeddings
by utilizing Zhu et al. [107] model and created a matrix for each resume where
each row is a ﬁxed-length sentence. The matrix used as input for a conventional
neural network that is supposed to extract explicit features.
He et al. [116] presented a model to predict the career trajectory of talents
based on their features inside their resumes. They classiﬁed the features on
numerical and textual features; they applied one-hot encoding to represent the
numerical features and word2vec to represent the textual ones. They used these
datasets as input to the ﬁve layers CNN model (input layer, convolution layer
with a ReLU activation, max-pooling and dropout, Dense layer, and softmax
layer).
Luo et al. [38] used CNN in the job description. This was aimed to get fewer
parameters than multilayer perception which reduced the model complexity.
They represented job requirements by embeddings with an attention layer to
identify important job requirements. Finally, the embeddings were fed to the
convolutional neural network.
3.5.3
Graph Neural Networks (GNN)
Graph Neural Networks (GNN) are developed to directly learn on networks or
graphs, where nodes are represented as propagated along with edges and updat-
ing node representations with the combination with its neighbors to generate
node embeddings through the design of multiple graph convolution layers [166].
Bian et al. [167] proposed a predictive JD/Resume matching network that
consists of a decision taken by two components that capture semantic com-
patibility of JD/Resume in two diﬀerent views, (1) text-based matching model
between JD/Resume and (2) relation-based matching model that link seman-
tics between similar JDs and Resumes. In the text-based matching model, they
represent the sentences of resumes and jobs using the BERT encoder and feed
them to a transformer-based architecture where the output represents the over-
all document. An explicit explanation of the transformers is provided in the
subsequent section 3.5.4. In the relation-based matching model, they made a
graph to represent the interaction between resumes and jobs (job-to-resume,
resume-to-resume, and job-to-job) where job-to-job and resume-to-resume are
linked by categories labeling and job-to-resume are linked based on keywords
importance. Then, they create a matching model based on a relational graph
convolutional network of the JD/Resume relation graph. After creating both
models in diﬀerent ways, they proposed to update the model weights using
stochastic gradient descent (SGD) to penalize the instances where there is a
disagreement and ﬁltering the poor learned instances.
In a similar context, Zhang et al. [168] leveraged a graph convolutional net-
work to match a query (short text) and a long text document. They create a
keyword graph from the text document via three steps: document preprocess-
ing with NLP method, Keyword extraction using the TF-IDF technique, and
construction of the edges between the keywords. To capture the structural in-
formation, they presented a graph attention network mechanism to learn the
31


---

## Page 33

representations and model the local interactions to handle the short-long text
matching problem.
3.5.4
Transformer architecture (Attention-based components)
In 2017, a deep learning technique was introduced known as the Transformer. In
natural language processing, transformers were presented to deal with the tasks
in which the data is sequential data. For example, tasks like translation and
text summarization are handled using transformers. More speciﬁcally, BERT is
a transformer-based model that has been used in a wide variety of NLP tasks.
Most importantly, BERT has outperformed many traditional nonneural network
models.
The attention mechanism is a part of a neural architecture that was intro-
duced to enhance encoder-decoder models to alleviate the fact that the context
vector of an RNN becomes an information bottleneck. It allows focusing on
certain parts of the input sequence by assigning higher values to more relevant
elements when predicting a certain part of the output sequence, enabling easier
learning and of high quality [169].
Figure 6: The Transformer - model architecture [4]
Qin et al. [45] proposed a framework called TAPJFNN to predict a person-
job ﬁt based on the topic of the job description. They applied the attention
mechanism using the softmax function in diﬀerent stages in their architecture
for the purpose to calculate the weight of word embeddings and improve the
interpretability of the relationships between job postings and resumes. They
apply it to the job requirements, candidate experiences, and hidden layers of
their proposed neural network. Same with Bian et al. [145], where they applied
32


---

## Page 34

an attention-based RNN encoder to derive the sentence representation of the
job posting and a resume.
Luo et al. [38] used a word embedding technique to provide a meaningful
representation of the words/phrase and their context in the job posting and re-
sume. They considered three major groups of features in the resume (experience,
skills, and talent ﬁeld) and the recruiter job post. They adopted the hierarchy of
attention architecture to assign high values ( weights) to the important features
of words.
3.5.5
Word embeddings and pre-trained language models
Word embedding is a feature learning techniques in natural language processing
where words or phrases from the vocabulary are mapped to vectors of real
numbers. Fernandez and Suraj [40] used a hybrid Average Word Embedding
AWE representation of the resumes and job description. They created it by
combining a trained word embedding from CV/JD with pre-trained Spanish
word embeddings.
Word2vec [170] is a method to obtain distributed representations for a word
by using neural networks with one hidden layer. It was implemented in multiple
cases to represent job oﬀers and proﬁles [81, 40, 64, 130, 127, 111, 11, 125].
Doc2vec [171] is a feature vector representation of a document. It has been
used in [31, 11, 102]. luo et al. [38] implementing the ELMo word embedding
to represent each word/phrase in both the resumes and job-posts.
BERT is a method of pre-training language representation, where it gener-
ates multiple, contextual, bidirectional word representations. BERT only im-
plements the transformer encoder part [167]. Diﬀerent studies used BERT to
solve various NLP tasks. For example, Jiang et al. [47] used BERT to predict
the university index from a predeﬁned university list. Devlin et al. [5] adopt
BERT as encoder layer of the sentences corresponding to the skill requirements
of job post.
The following Figure 7 show an example of BERT transformer usage. The
BERT was trained on diﬀerent down-stream tasks and then ﬁne-tuned to the
speciﬁc task of questions/answers.
33


---

## Page 35

Figure 7: BERT: Pre-training of Deep Bidirectional Transformers for Language
Understanding architecture (Original ﬁgure from [5])
In the following Figure 8, a simpliﬁed overview of the way that a language
model can be pre-trained on a large text corpus, and then ﬁne-tuned using a
dataset for a speciﬁc task.
Task
datasets
Pre-trained
Language Models
Task speciﬁc Model
Large-scale text
corpus
Pre-training
Fine-tuning
Figure 8: Overview of ﬁne-tuning pre-trained models
3.5.6
Classical Machine Learning
In several works of JD/Resume matching in literature have been using classical
machine learning, Logistic Regression (LR), Factorized Machine (FM), GBM
(gradient boosting), RF (random forest), VOBN (variable-order Bayesian net-
works), SVM (support vector machine), C4.5, Naive Bayes, Adaboost (AB),
Random Forests (RF), Gradient Boosting Decision Tree (GBDT), Linear Dis-
criminant Analysis (LDA), and Quadratic Discriminant Analysis (QDA), as
base models in their experiments to validate the performance of their proposed
architecture models to solve the JD/Resume matching [38, 126, 107, 146, 64].
In a particular case, Ozcan and Oguducu [39] applied diﬀerent classiﬁcation
techniques in the job recommender system to deal with the cold and non-cold
start of candidates recommendation.
Qin et al. [45] created a mean vector
of word embedding vectors of ability requirements and candidate experiences
to run their experiments on the classical machine learning (LR, DT, AB, RF,
GBDT).
34


---

## Page 36

3.6
Multilingual matching models
Table 3: Recommendation base multilingual matching models
celik[77]
malherbeet al. [143]
Tamburriet al. [19]
Shakurova [172]
Method used
Ontology based
parsing of resumes
create graph
of skill base knowledge
identify skills from
parsed resumes
bilingual dictionary
from parsing CV
Learnt Language
labeled (English + Turkish)
French & English
English
English
Test Language
english & Turkish
French & English
Dutch-Flemish
English/German &
English/Dutch
Match based on
ontology labeling
Skills extracted from
JD/candidates
Skills lines
labeling
cross-lingual learn
Experiment
(resume/job)
Only one resume case study
100 Jobs
10K jobs
Compare (200
and 500 CV)
Precision(P)/Recall(R)
extraction
-
P(0.81)
P(0.73) / R(0.94)
0.81 (f1 measure)
External knowledge
-
French/English DBpedia,
StackOverFlow tags
Pre-trained
Bert
Pre-trained
embedding layer
Features used
Skills, education,
location, occupation,
concepts, organisation
Skills
Skills
Skills
year publication
2016
2016
2020
2019
Multilingual systems have received the special attention of many researchers.
Multilingualism plays a very important role in these systems because we don’t
have one language to deal with, in regard to resumes and job-seeking activities
[173]. Resumes to job description matching systems in a are diﬃcult to ﬁnd
especially when they have to deal with a single language. To ﬁgure out inter-
pretable ﬁgures, and make the best use of multilingual text, one major focus
of the project is to derive useful and semantic knowledge. Table 3 show the
recommendation base, multilingual matching models.
Lexicon diﬀers with respect to the languages and learning the lexicon from
one language to another is a diﬃcult task i.e., English lexicons are diﬀerent than
Turkish [104]. Bal et al. [104] analyzed Turkish job advertisements and tried to
identify the structure of the common sentences to create some rule patterns to
extract. They addressed the diﬃculties encountered such as the Turkish verbs
are at the end of the sentence, whereas in English, verbs are at the middle of the
sentence. Multiple solutions for JD/Resume matching were proposed to treat
several individual languages in the literature i.e., , Indonesian [68], Vietnamese
[97], Brazilian [81], Belgium [37], Spanish [40], Chinese [127]. Cross-lingual may
be a solution.
Cross-lingual embedding represents words in multiple languages, they are
crucial for task scaling of multiple languages by transferring knowledge from
high resource languages i.e., English to low resource language i.e., German
and Dutch [172]. Lena et al. [172] evaluated the embeddings that are on the
sequence labeling tasks of parsing CV and they also show the size of a bilingual
35


---

## Page 37

dictionary, frequency of dictionary words along with performance measures.
The researchers have conducted an experiment on Dutch-English and German-
English cross-lingual embeddings. They used Canonical Correlation Analysis
(CCA) linear projection in a monolingual vector to estimate Dutch/German
embeddings in terms of English space.
Subsequently, these embeddings are
used for the sequence model. The sequence model is always trained in terms of
English space. The data used for training is either English data along with the
Dutch/German training data or just English training data. Once the model is
created to support multilingualism, it is tested Dutch/German test data. Several
other factors have been considered for experimenting with bilingual dictionaries
like size, data source, and bilingual dictionary frequency.
The French and English multilingual aspect was considered by Malherbe and
Aufaure [143] proposed a knowledge base architecture (English and French) of
skills that is extracted (job oﬀer, resumes) from the job oﬀer website.
The
crawled data was ﬁltered to include skills data based on the term frequency
in the corpus. After formalizing these documents, the system is coupled with
external sources of information that are named as Stack-Overﬂow and DBpedia.
A normalization technique was applied to associate each job oﬀer and proﬁle
with the corresponding skills base. The link was based on having the same alias
between the tags of Stack-Overﬂow and the concepts in DBpedia. The very 1st
step was to process the skill terminologies obtained from English and French
sources for which a hypothesis “to use an expression that appears frequently in
the skills ﬁeld content of the proﬁles” was proposed. The 2nd step of the frame-
work is based on extracting the related concepts in specially chosen knowledge
graphs, namely DBpedia and Stack-Overﬂow tags. Most of the data uploaded
by a candidate are in unstructured text form. Their extraction of multilingual
skills using their proposed approach was able to reach 80% [143].
Celik [77] presented a semantic-based extraction system for matching re-
sumes for any job opening to gather important information from the resumes.
The study proposed an ontology-o=based resume Parser (ORP) system for
Turkish and English language used in resumes along with concept-matching
tasks, the data is analyzed semantically, and then it is parsed with important
information like education, experience, business, and features. The study was
divided into 6 major steps, starting with the conversion of the resume, parti-
tioning it into segments, then parsing important data from input, normalizing
that data, after that applying clustering and classiﬁcation tasks to focus on the
important sections of the resumes.
The framework used is based on SWRL
and provides a formal OWL ontology with rules in the abstract syntax. Jaro-
Winkler distance algorithm was used to detect incorrectly spelled words. Added
to that, they ensure multilingualism in this research by translating items from
the diﬀerent ontologies and assigning tags labels of English or Turkish languages.
Tamburri et al. [19] presented a DataOps model based on agile practice
in skills extraction from resumes and jobs, featuring machine learning models.
The researchers have applied a DataOps pipeline for skills extraction constructed
from ﬁve steps (Data Pre-processing, Sentences Annotation for Learning, Model
Training, ﬁne-tuning training, and prediction). Their experiment is directed on
36


---

## Page 38

using BERT cloud base-model pre-trained in English [174] and ﬁne-tuned with
annotated sentences extracted from vacancies. They applied their model to a
Dutch-Flemish cross-border labor market for job seekers.
Linkedin proposed a method to make users proﬁles in other languages and
create another proﬁle in the preferred language. Moreover, users can set the
language that their proﬁle will be displayed, and Linkedin does not translate
the content or messages. People viewing a proﬁle can choose from the language
a proﬁle owner setup before 15.
To summarise, with the growth of powerful pretrained language models
i.e., BERT, the need to ﬁne-tune in a speciﬁc ﬁeld or even in a speciﬁc required
language to train such model to identify the features i.e., skills. To do so, a
dataset needs to be labeled to ﬁne-tune a pretrained model. Tamburri et al. [19]
used a speciﬁc dataset gathered from parsing JD/Resume and labeled manually
via a domain expert and this labeled dataset became the standards dataset
used in the ﬁne-tuning. However, such sources are not enough to cover enough
knowledge, also, expensive for manual labeling. In our proposed method, the
use of reach multilingual ontology/knowledge base is required to be used in
labeling JD/Resume for ﬁne-tuning BERT language model purposes.
3.7
Biases in the automated e-recruitment Machine Learn-
ing algorithms decisions
The machine learning algorithms used in automated programs of hiring usually
train their models on a pair of matched JD/Resume. These algorithm decisions
have been shown a bias decision i.e., cognitive bias, coworkers, demographic
subgroup, etc [175]. For example, Amazon created a hiring tool in 2014, that
has to parse resumes and infer the best candidates using their own workforce
over the past 10 years, where they trained their models on a large majority of its
existing workforce of white and male persons [176] which lead to systematical
bias against female applicants [177].
Pessach et al. [126] consider dealing with the biases that may happen in the
e-recruitment prediction model. They attentively consider including a dataset
that represents a wide range of the heterogeneous populations through a math-
ematical programming model.
In this thesis, we will consider dealing with the potential biases we may
have in the model by considering a wide range of the JD/Resume per topic in
the training phase, including various diversiﬁed features. A collaboration with
Airudi will open access to a wide range of multivarious datasets (JD/Resume).
3.8
Data and Machine Learning traceability
In the JD/Resume matching workﬂow, common steps are realized (parsing,
feature extraction, model training, experimentation, and validation) and re-
15https://www.linkedin.com/pulse/20140710185825-25298675-multilingual-create-a-
secondary-language-proﬁle-on-linkedin/
37


---

## Page 39

peated over time. Since JD/Resume matching models and workﬂows are cen-
tered around data, it is important to keep track of the data used at each step,
machine learning models, and iteration of the workﬂow, i.e., recording the his-
tory of the diﬀerent ML stages, to ensure the reproducibility of the ML pipeline
(same inputs, same outputs) and to track data provenance. JD/Resume match-
ing pipelines need to be automatically tracked in a way that guarantees that
all the ﬁles and metrics will be reproducible or fetch the full context of an
experiment or to perform a new iteration.
The versioning of ML data and models is a young and growing practice, with
several tools created to help developers with tracking the various aspects of their
workﬂow. Airﬂow [178] is used to create, schedule, and monitor machine learn-
ing workﬂows as a directed acyclic graph (DAG) that may be composed of mul-
tiple tasks. Similarly, Luigi [179] is a workﬂow engine framework that helps to
write static and fault-tolerant data pipelines in Python. Miguel et al. [180] pre-
sented the Marvin engine that supports the exploration and model development
of distributed computing systems for data-intensive applications. It provides a
standard interface to allow other applications access to shared model artifacts
and to support high throughput and processing of large datasets. MLﬂow [20]
is a platform to streamline machine learning development. It is divided into
three components for (1) tracking experiments, (2) packaging the code into re-
producible runs, and (3) sharing and deploying models trained using diverse
ML frameworks. Kedro [181] provides a development workﬂow framework that
implements software engineering best-practice for data pipeline construction,
basically leveraging data abstraction and clear code organization to bring mod-
els into production. Pachyderm [182] is a data science platform aimed at an
enterprise that combines data lineage [26] with end-to-end pipelines on Kuber-
netes, with a graphical pipeline builder and data versioning.
DVC [21] is a data/model versioning tool that is integrated with git reposi-
tories, such that the history of data, models, and code can evolve together in an
eﬃcient manner. It is designed to handle large ﬁles, data sets, machine learning
models, metrics, and code. DVC was designed to support the gradual adoption
of ML capabilities in traditional software projects.
In our thesis, we will consider studying the need to propose system trace-
ability based on one or more versioning tools.
Therefore, studying the best
practices of applying such tools in software repositories is required. A study in
this context has been proposed and sent to SANER2021.
4
Research Methodology
We will describe in this section our methodology and steps that we will follow
to address the following research questions:
RQ1: What is the state-of-the-art in JD/Resume matching?
RQ2: Can knowledge base and modern language models improve JD/Re-
sume matching?
38


---

## Page 40

RQ3: How explain the decision of JD/Resume matching to concerned
stakeholders?
RQ4: Can traceable models be integrated into a JD/Resume matching
process with low impact on the system complexity?
We propose a general methodology to achieve the thesis goal shown in Figure
9.
Figure 9: Overview of the Research methodology of the Thesis
4.1
What is the state-of-the-art in JD/Resume matching?
As a ﬁrst objective, we created a systematic literature review to address the
following requirements related to JD/Resume matching (methodology and pre-
liminary results are shared in Section III):
• Understand the challenges of JD/Resume matching.
• Identify the features used in the literature that may help to make the
matching.
39


---

## Page 41

• Categorize the diﬀerent methodologies to extract features from JD/Re-
sume used in literature.
• Categorize the diﬀerent methodologies for matching between resumes and
job descriptions.
• Identify the diﬀerent metrics used to evaluate the matching process.
4.2
Overview of the Proposed Architecture
During our PhD, we propose the architecture presented in Figure 10 as a path-
way to be proven to improve the matching between jobs and resumes.
The
proposed architecture is supposed to resolve the thesis research questions re-
lated to the JD/Resume matching:
• Can knowledge base and modern language models improve JD/Resume
matching?
• How explain the decision of JD/Resume matching to concerned stakehold-
ers?
• Can traceable models be integrated into a JD/Resume matching process
with low impact on the system complexity?
Figure 10: Overview of the proposed architecture of matching Resumes to the
Job description
The proposed architecture of matching Resumes to the Job description is
based on processing the following points:
1. Dataset sources and pre-processing
2. Resume and job description features
3. Features extractions
4. The matching system
5. Traceability & Explainability of the matching system
40


---

## Page 42

4.3
Data Sources and pre-processing
In this section, we describe the diﬀerent sources and alternatives of the dataset
and the possible preprocessing steps that may be applied.
4.3.1
The Airudi dataset
During our internship, we received ethics approval to have access to the company
databases of resumes and Job descriptions of our industry partner Airudi. Such
a dataset is considered critical and the most important part to initiate this
project since companies do not share such conﬁdential data (resumes of persons
who applied to their proposed jobs).
Airudi collects their dataset from its clients (companies looking to hire ef-
fective persons), where they apply an anonymization protocol of the candidates
and hide their personal information (ﬁrst name, birth date, etc).
The provided dataset contains French and English resumes and job descrip-
tion, and contains the following features:
• Resume features: education, degree, university, work experience(skills,
professional competencies, personnel competencies).
• JD features: the job title, post description, requirements (required educa-
tion, required skills, required experience), job responsibilities, and the job
advantages.
• List of matched JD/Resume that is manually constructed from recruiter
clients (gold standard) with diﬀerent recruitment processes i.e., accepted,
refused, waiting for candidate decision, send oﬀer to candidate.
The dataset provided by Airudi requires preprocessing steps. We applied
Regex functions for impurities cleaning, for example blank areas and extra bois-
terous characters. We also ﬁxed typos related to french language i.e., è, oe.
We transformed the list of recruitment process information between candi-
dates and the jobs to a binary classiﬁcation (match or unmatch). For example,
we assigned a match in the status of “Accepted Jobs Skills” and an unmatch for
the case of “Not retained - Physical interview”. There were other cases where it
is not possible to determine the matching status such as “interested candidate”
or “stopped process”. We removed the empty cells from the dataset that were
missing a job description or a resume. We recorded the remaining cases number
in Table 4.
Table 4: Dataset labels distribution, the relation between jobs and resumes are
splitted into (unknown, match and unmatch) liaison
Data cells
Unknown label:0
match:1
unmatch:2
total
<jobID, CandID, match-status>
38839
7656
21033
67528
41


---

## Page 43

We classiﬁed (38839/67528) 57% of the cases as unknown, most of them
are noted as "stopped interviews process" (35446 cases). In the following, we
consider only the labeled dataset as (match, unmatch) with a total of 28689
pairs of <job, resume>. We made an additional ﬁlter of cases, where the same
job exists with diﬀerent IDs (1576/2500 jobs). Similarly, we removed duplicates
where the same job is assigned to the same candidate having diﬀerent IDs.
We removed cases (8 matches) having contradictory recruitment processes i.e.,
"candidate accepted" and "candidate refused". We ﬁlter out candidates having
less than 50 word (771 candidates), all the removed candidates were conﬁrmed
and veriﬁed manually. Table 5 show details related to the remaining jobs and
resumes.
Table 5: Dataset labels distribution, the relation between jobs and resumes are
splitted into (unknown, match and unmatch) liaison
Unique total
Unique Match label
Unique Unmatch label
candidates
16194
5776
12107
jobs
909
872
472
total pairs
<candidate, job>
27257
7090
20167
4.3.2
Websites scraping
We will proceed to have additional datasets from public websites, to enrich the
actual dataset with the updated skills and nowadays requirements.
We will
consider adding job description (JD) in both languages French and English, for
example, from the oﬃcial Canadian job bank 16 or public job posting website
17. Such a public website represents a rich source of job oﬀers, where the job
poster describes his oﬀer in two languages French and English. The Jobbank
website is designed to ﬁlter the jobs by features (province, city, posted date,
full/part-time, period of employment, salary, years of experience, job source,
education or training, language, employment group, job categories).
Moreover, there is another section recommending top related job categories.
A list of skills and knowledge are provided to job seekers, so they can ﬁll a list of
skills they have and knowledge. Such a dataset is the reach of real and updated
features.
The indeed website oﬀers the possibility to ﬁnd candidates that are appro-
priate to a speciﬁc query that can be turned to advanced search 18 to include
(keywords, work experience, speciﬁc experience with required years of experi-
ences, education institution with the study ﬁeld). There is an additional option
(not for free) to download the job seeker proﬁles.
16https://www.jobbank.gc.ca/
17https://ca.indeed.com/
18https://resumes.indeed.com/advanced-search
42


---

## Page 44

Starting from that purpose, we plan to assign job seekers to a job description
based on the following scenarios:
1- Choose a job description and via the advanced candidates research, we
can specify the diﬀerent ﬁelds and consider the best ranked proﬁles that indeed
engine search proposes as our ground truth that should be assigned to the job,
and the less ranked resumes as non match.
2- We can search for multiple candidates using job title or skills, then using
the candidate work history, we can ﬁnd the job description that he was assigned
to in the past.
4.3.3
RecSys Challenge 2017
The challenge dataset contains user proﬁles, job postings, interactions that users
performed on job posts, and interaction of the recruiter to the users proﬁles. It
also contains the user job impressions, i.e., information about job postings that
were shown to users. The total dataset includes 1,367,057 users and 1,358,098
jobs. Users and jobs were described by several similar attributes such as job
categories, career level, industry, location, etc. In addition, the users have the
educational background and details about work experience. The dataset was
carried out through an anomization procedure [183].
4.3.4
Common data pre-processing
A data preprocessing analysis and cleaning veriﬁcation should be realized. The
language model should receive a clean text as input since it is performed to
learn the context of a given text.
The Word Sense Disambiguation (WSD)
can be used to specify the correct sense for terms used in resumes and jobs
description (i.e., typos, missing values, etc) according to its surrounding textual
content. The WSD module is integrated with NLTK python API 19, where it
can be linked with the WordNet lexical database. Moreover, we will attempt
to eliminate bias when addressing the three research questions of the thesis. To
identify the dataset quality against biases, a detailed analysis to categorize the
features is necessary. For example, the consideration or not of a feature (age)
can increase or decrease the cases of bias during the execution of an existing
matching algorithm.
4.4
Resume and job description features
In this section, we show the features that characterise both resumes and jobs.
4.4.1
The resume features
The resume is generally composed essentially of at least 3 sections: (1)Name and
contact information; (2) Education (degree, school name, certiﬁcations, awards);
(3) Work experience (company name, job title, accomplishments, period).
19http://www.nltk.org/howto/wsd.html
43


---

## Page 45

In a resume, we may ﬁnd additional information that usually occurs: (1) Career
Summary or Objective Statement; (2) knowledge or hard skills; (3) Language
skills; (4) Attitudes and values and (5) others (nationality, gender, marital sta-
tus, etc). Figure 11 shows the diﬀerent sections a job description can have.
Figure 11: An example of a web developer Resume
4.4.2
The job features
The job description is composed of a main 3 sections: (1)Job title; (2) Job
responsibilities; (3) Qualiﬁcations and skills.
There is additional information that may be included in a job description: (1)
Job summary (overview of your company and expectations for the position) (2)
Compensation and beneﬁts and (3) others (gender, age range, marital status,
location, etc). Figure 12 show the diﬀerent section a job description can have.
44


---

## Page 46

Figure 12: An example of a job description for a web developer
4.5
Features extractions
There are diﬀerent features in a resume and a job description, we propose a
feature extraction method that is based on the ESCO (European Skills, Com-
petences, qualiﬁcations, and Occupations) ontology. The ESCO ontology is a
multilingual classiﬁcation system of European that considers three pillars: (1)
Occupation; (2) Skill (and competences) and (3) Qualiﬁcation. Figure 13 shows
hierarchy structure of the ESCO ontology.
The purpose of this section is to ﬁnd a way how we can disambiguate a part
from a text that describes the information in the Resume/Job, and how to relate
it to a concept which is described in a knowledge base (ontology).
Since the ESCO ontology has linked pillars that describe occupations, we will
proceed to interpret semantically the occupation that describes the closest pos-
sible JD/Resume based on the ontology’s occupation. The ontology occupation
has a short explanation of the occupation’s meaning and a speciﬁc clariﬁcation
of its semantic boundaries.
However, the ESCO ontology is not perfect to cover all the ﬁelds and their
interactions. The O*Net ontology and knowledge bases such as DICE have been
used in several related studies [87, 86] to identify the skills feature; O*Net
ontology is the US’s primary source of occupational information and it covers
more domain i.e., (medical and artistic), but other skills acronyms may not
be recognized that may be covered with lexical ontology WordNet or YAGO3.
Moreover, to cover more domains, additional sources of knowledge (tags from
StackOverﬂow, quora, etc) may be added using the associations’ rules (same as
related to)[87]. Although, expanding ontologies knowledge bases and labeling
45


---

## Page 47

diﬀerent multilingual categories will be a future work, due to the task complexity
challenges.
Figure 13: The hierarchy structure of the ESCO ontology [6]
The occupation pillar organises the occupation concepts in ESCO. It uses
hierarchical relationships between them, metadata as well as mapping to the
International Standard Classiﬁcation of Occupations (ISCO) to structure the
occupations.
Each occupation concept contains alternative labels terms that have the
same meaning of the main concept and hidden terms in each of the ESCO lan-
guages. Each occupation also comes a description, scope note and deﬁnition.
Furthermore, they list the knowledge, skills, and competences that experts con-
sidered relevant terminology for this occupation on a European scale [6]. Figure
14 show a shorted example of a web developer occupation in the ESCO ontology.
46


---

## Page 48

Figure 14: Example of URI of Web Developer occupation in ESCO ontology 20
The ESCO system presented in its last version "ESCO v1.0.8" published
in August 2020 provides a web service API to make queries on the ontology.
They also provide an RDF (Resource Description Framework) format of their
data to be downloaded, such a format will be useful during the mapping of the
Resume/JD to the closest occupation.
4.5.1
Occupation mapping using deep contextualized word embed-
dings
In this subsection, we describe our proposition to a possible way for semantic
mapping using word deep conceptualization.
A query using the job title or the resume career on ESCO API can result
in an exact match or to a list of possible occupations that may match with. In
the case of nonexistence of the job title, the resume career, or even there is no
exact match, we need to run a deeper semantic mapping.
To compare semantically between two textual parts (concept from the ontol-
ogy and section parts of the JD/Resume), the contextualized word embeddings
can be used to capture the word semantics in diﬀerent contexts.
Language models i.e., BERT, ELMo, have been used for transfer learning in
several natural language processing applications. In our case, we will use transfer
learning to extract the knowledge embedded in a pre-trained machine learning
model. For example, the BERT model takes in consideration three aspects to
47


---

## Page 49

represent a word and keep its meaning inside a phrase, (1) Position Embeddings
to express the position of words in a sentence; (2) Segment Embeddings to
distinguish between diﬀerent input sentences i.e., pair sentences for a matching
purpose; (3) Token Embeddings that represent the word pieces vocabulary [5].
We plan to investigate the contextualized word embeddings from language
models and compare the similarity i.e., cosine distance, between the ontology
occupations concepts and the section parts inside a JD/Resume. This process
can be applied in occupation mapping, skills and knowledge validation.
Depending on the task and the context, we need to run an experimentation
to compare and explore the most appropriate word deep contextualized language
models to our context.
4.5.2
Feature extractions from Resumes
A resume is usually divided into separate sections, where every section has a
message to present. To extract features, we need to start by separating these
sections by using, for example regex functions. Figure 15 shows the sections
that may be identiﬁed in a resume. The purpose is to create a graph proﬁle of
a resume candidate that contains all the useful information inside the resume.
Once the sections identiﬁed, we can use the experience section and link it to the
possible occupations the candidate may have during his working curriculum.
The occupations can be validated With the help of other sections
(knowledge and skills, summary).
In the education section, we need to
determine the degrees and the university of the candidate. To unify the degree
terminology, we may use the lexical ontologies i.e., WordNet or YAGO3. For
example, if you search for the word "phd", the wordnet returns the diﬀerent
lexical ways it may be written, including hyponyms, hypernyms, and derived
words.
From the summary section, we may determine attitudes and values
where we can be linked to the attitude and values ESCO taxonomy. It describes
individual work styles, preferences, and behaviour. After this step, we should
have a graph proﬁle of a candidate.
48


---

## Page 50

Figure 15: Extracting of Candidate features
4.5.3
Feature extraction from Job Description
A job description can be represented by an occupation in the ESCO ontology,
where it can be validated with diﬀerent sections (job title, job summary, respon-
sibilities, qualiﬁcations, etc). As shown in Figure 14, where a representation of a
web developer is presented, we can assign the following mapping to job descrip-
tion using semantic similarities of deep conceptualized word embeddings, (1)
the job summary with the job title can be linked to the description of the occu-
pation; (2) the required responsibilities can be linked to the essential skills; (3)
the required qualiﬁcations can be linked to the essential knowledge; (4) attitude
and values; (5) the language skills.
Similar to the resume, we can determine the requirements of the education
degree/ university.
49


---

## Page 51

Figure 16: Extracting of Job features
4.5.4
Features Extraction Validation
After extracting the features and making the graph proﬁles that represent the
sources of JD/Resume, we will validate the feature extraction results by ensuring
if the JD/Resume graph proﬁle meets the knowledge, skills that describe the
JD/Resume. An additional manual validation can be applied to a sampled case
of the dataset.
4.5.5
Language model for annotating features
To reduce the cost of feature extraction, we plan to automate this task once
we have enough labeled dataset, by applying the advanced existing pre-trained
language models i.e., BERT and ﬁne-tune it to determine the diﬀerent entities
(dataset labeling) in resumes and job descriptions [184].
4.6
Can knowledge base and modern language models im-
prove JD/Resume matching?
During this section, we present the matching system that is based on (1) deeply
textual matching using language model transformer; (2) ﬁltering out the non-
conform candidates using feature similarity; (3) feature matching models. Fig-
ure 17 shows the diﬀerent parts of the proposed matching system.
50


---

## Page 52

Figure 17: Proposed matching system
4.6.1
Baseline model: Job-Resume matching based on language model
transformers
We designed a baseline model to match resumes with job description. The model
will be used as a reference point to evaluate the evolution of the proposed ar-
chitecture performance. The proposed model is based on a BERT transformer
that aims to classify a pair of <job, resume> as a match or not. BERT is a
powerful language understanding model. It is characterized by a deeply bidirec-
tional text learning, and that it can use a large amount of plain text data for
training. However, BERT has a length limit on the input text, e.g., 512 words,
which prevents the accurate modeling of long documents.
Since we have a French dataset, we need a model that was pre-trained in the
51


---

## Page 53

same language. The CamemBERT was introduced as a state-of-the-art language
model that was pre-trained on the French subcorpus [185]. Given the limit size
of words a BERT model can support, we plotted the number of tokens of the
textual dataset (jobs and candidates). Figure 18 shows the tokens distribution
of the candidates and jobs.
Candidates
Jobs
102
103
104
Tokens Length
Figure 18: The tokens length for the candidates and jobs dataset
In the proposed architecture, we use multiple Camembert models to encode
the input job description and resume. Figure 19 illustrates the detailed archi-
tecture of the model.
Approach: We propose a job-resume matching architecture where the number
of Camembert models to consider is calculated depending on the training/test
dataset (tokens size). We choose the architecture which at most results in losing
10% (This threshold can be modiﬁed) of the input text content. The architecture
structure is therefore dynamic and solely depends on the threshold we set and
the dataset. By decreasing the loss threshold, we may use a high number of
Camembert models and that would result in a high number of parameters which
will be diﬃcult to train and converge to the right spot given the data size and
computation power. Using a small number of Camembert models will result in
loss of information which in turn would aﬀect the performance. It’s therefore a
trade-oﬀ, and the threshold should be chosen wisely.
52


---

## Page 54

Figure 19: Architecture of multiple Camembert architecture
We keep an overlap of 50 tokens between consecutive chunks in order to
prevent context information loss (see text highlighted with green in Figure 19).
The ﬁnal job description/resume representation is given by averaging the rep-
resentations of each chunk as shown in Equations 7 and 8:
job_embeds =
1
nbr_job_chunks
nbr_job_chunks
X
i=1
job_embedsi
(7)
resume_embeds =
1
nbr_resume_chunks
nbr_resume_chunks
X
i=1
resume_embedsi
(8)
The ﬁnal job description and resume contextualized vectors (i.e., embeddings
of length 768) are concatenated (resulting in a vector of length 2*768) and fed
to a feed forward neural network for ﬁnal classiﬁcation. It’s composed of one
hidden layer of 768 neurons (can be tuned later) and ReLU activation function
shown in Equation 9 to get an intermediary representation of the input of size
768 (i.e., hidden_output):
hidden_output = ReLU(W t
768.concatenated_embeds + b768)
(9)
The resulting vector representation of the full input is then fed to a ﬁnal
output layer of 2 neurons. The output logits shown in Equation 10 represent
scores for the ‘match’ and ‘not match’ output classes.
logits = W t
2.hidden_output + b2
(10)
We then apply Softmax function shown in Equation 11 to the output logits
to get the probabilities of the input job description and resume to ‘match’ or
53


---

## Page 55

‘not match’. The output class associated with the highest probability is the
predicted class.
pmatch =
elogits1
Pi=1
i=0 elogitsi
pnot_match =
elogits0
Pi=1
i=0 elogitsi
(11)
During training, we ﬁnally compute Binary Cross Entropy loss shown in
Equation 12 and run backpropagation and optimization steps towards mini-
mization of the loss function. During inference we only output the probabilities
as the model is already trained.
Bi_Cross_Entropy = −qmatch log(pmatch) −qnot_match log(pnot_match) (12)
Where p is the predicted probability and q is the ground truth probability.
Results: We used a stratiﬁed split of our initial data into 80% for training and
20% for testing. The training set is then split to 80% for actual training and
20% for validation.
We set a maximum threshold of data loss of 10%. The model dynamically
chose 1 Camembert for encoding job descriptions (resulting in loss of 4.72% of
job description data) and 2 Camembert models for encoding resumes (resulting
in loss of 6.74% of data).
With the high number of model parameters, we
encounter Out Of Memory issues with batch size higher than 8, on a Tesla T4
GPU (from Google Colab). Therefore, we run training with batches of size 4.
Each epoch took around 30min for training and 7min for validation.
Starting from the third Epoch, the model performance did not improve.
We therefore stopped at the third epoch and saved the dedicated model. The
model achieves 78% accuracy and an F1-score of 65%. The full metrics values
are reported in Table 6. We can conclude that the model is predicting better
the non-match label. Thus, additional improvement can be applied i.e., using
weighted loss function or augmented data, where the best combinations can be
validated empirically.
Table 6: Performance of multiple Camemberts on test set
Label
precision
recall
F1-score
CamemBERT
Windowing
not match (0)
0.8
0.93
0.86
match (1)
0.63
0.34
0.44
CamemBert
Windowing + Overlap
not match (0)
0.78
0.99
0.87
match (1)
0.87
0.20
0.33
54


---

## Page 56

4.6.2
Features similarity and candidates ﬁltering out
At this stage of the project, we want to ﬁlter out the candidates that don’t
ﬁt the job exclusive requirements, i.e., required experience years. Using Regex
functions, we will determine if there are required years of experience of using a
tool, or having speciﬁc skills (language, technical hard skills, etc).
4.6.3
Matching candidates to job oﬀer
We will create a ranking method based on the matching models. Typically, the
JD/Resume matching can be (1) related to text mining and natural language
processing techniques such as text classiﬁcation; (2) sentence matching based on
vector similarities ; (3) sentence pair modeling matching; (4) neural network via
encoding the JD and resume into a shared space and compute their matching
using cosine similarity.
4.7
Traceability & Explainability of the matching system
In this section, we present the possible traceability and explainability ways of
the proposed models to the diﬀerent stakeholders concerned with the matching
system.
4.7.1
Language model Interpretability and Explainability
After optimization of the model to get the best performing version given our
data, we are willing to focus more on the interpretability and explainability
aspects of the model.
For that, we aim to run experiments to understand how the model takes de-
cisions to accept/refuse candidates given their resumes and the job description.
We will also investigate the parts of resume/job description to which the model
pays more attention. This will help understand what the model has learned and
its limitations. Which in turn help to tweak the model for better performance.
Recently, the Language Interpretability Tool (LIT) [186] was published with
an open-source implementation for assessing the explainability of AI models
(especially in NLP) through diﬀerent graphs and functionalities. Using it would
be of great help for our use case.
4.7.2
How explain the decision of JD/Resume matching to con-
cerned stakeholders?
At this stage of the project, we will propose explainability reports speciﬁcally
for the JD/Resume matching we suggested in RQ2. We believe that the better
explanation we can have of the matching decision, the more valuable the feature
we should have.
The Explainability is about trust. It’s important for the three stakehold-
ers (candidates, job poster, recruiter) of the matching decision to understand
its behavior.
Depending if the good or bad decisions the model makes, it’s
55


---

## Page 57

important to have visibility into how they were made. However, the decision
models based on deep neural networks behave as black-boxes and fail to pro-
vide total explanations for their predictions. The state of the art still advances
to provide closer explanations of the model decision, such as the LIME (Lo-
cal Interpretable Model-Agnostic Explanations) model-agnostic [187] that has
a principle of perturbing the input around its neighborhood and seeing how
the model’s predictions behave. Similarly, Rationalizing Neural Predictions is
trying to predict what part of a paragraph a model is used to make a decision
[188].
In our case, we would ﬁrst like to use such a model-agnostic as a baseline
to determine if there are certain sections, keywords, attributes that help the
language model make its decision.
However, to be able to explain this, we
would like to see how the ontology can contribute to better explain a decision of
a neuronal network based model. We suppose that a uniﬁed ontology for both
resume and job description will help us to assign an explanation of the behavior
of our language model algorithms. Such experimentation can be validated with
qualitative analysis collaborated with the airudi clients (sources of our dataset).
We present an overview of the proposed explainable reports we plan to pro-
vide to the concerned three stakeholders (candidates, job poster, recruiters) of
the matching decisions in Figure 20.
56


---

## Page 58

Figure 20: Preliminary overview of the proposed explainable system for the
concerned stakeholders
4.7.2.1
Explanation for a candidates
The process is enabled, when the third-party company (Airudi) receives a
job vacancy from a recruiter. Airudi publishes the job online, and the persons
apply for the job, including existing persons already sending their resumes look-
ing for a job vacancy. The matching engine should compute the most eligible
candidatures to the posted job, and then prepare an explainable report for the
candidates: (1) that are eliminated in the early stage because they do not match
the explicit features i.e., age, years of experiences, etc. (2) that matched the
explicit features, but they have been ranked among the last. A special report
will be generated including the details of the trained models and how their skills
57


---

## Page 59

were not enough to be retained. A comparison between the list of recommended
persons for the job with each refused candidate will be made, to include a list
of requirements in the report. (3) The persons who were recommended to the
recruiter (to be interviewed), but not oﬀered the job will be compared to the
chosen candidate, and a similar report indicating the diﬀerences characterizing
the hired person.
4.7.2.2
Explanation for a recruiter
The recruiter will receive: (1) a list of the recommended candidates from the
matching engine, including a highlighted reasons of each person with the rea-
sons that make him matching the job; (2) A features comparison between the
candidates will help him to choose easily the most appropriate person needed
for the job. Then, the recruiter will evaluate the candidates for the highlighted
features that made them eligible for the job.
4.7.2.3
Explanation for a job poster
The job poster needs to be updated with the reasons a person was accepted from
the proposed list of candidates. The accepted person can be anyone from the
recommended list. In that case, a comparison with the candidates will highlight
the hidden reason that someone other than the ﬁrst ranked person was chosen.
The company that posted the job will update its recommendation model engine.
58


---

## Page 60

4.7.3
Can traceable models be integrated into a JD/Resume match-
ing process with low impact on the system complexity?
Figure 21: The artifacts that should be continuously traceable in the matching
JD/Resume environment
To respond to this research question, there is a need to understand the existing
traceability tools in order to choose the most appropriate one(s) that ﬁt our
proposed architecture. Subsequently, a comparison and a set of best practice
usage of ML traceability tools need to be addressed. The traceability module
has to be adapted to include the following requirements as shown in Figure 21:
• Tracking continuously the saved dataset with their diﬀerent evolution from
their unstructured sources to include (cleaning, transformation, labeling).
• Ensure an up-to-date recommendation pipeline evolution, e.g., in case a
candidate will ask an audit of decisions made by the system. The system
should be able to pinpoint exact model version, data set versions used for
training, etc.
• Updating the diﬀerent knowledge bases, due to their continuous evolution,
once a new feature (skill, education, etc ) appears and needs to be included.
• Taking in consideration that we have an ontology that can be evolved and
can be used particularly with certain models or having transformations
59


---

## Page 61

(i.e., embeddings). Our learning models will be dependent on some parts
of the text and other parts of the ontology.
We will try to model all
system elements that evolve continuously with diﬀerent compatibility (new
ontology release, updated dataset, models’ hyperparameters) to be able
to trace back and reproduce the system decisions.
• Traceability can also be useful for debugging a language model.
Tracking data and machine learning in a software repository will introduce
new ﬁles describing the workﬂow evolution at the diﬀerent stages of a project
lifetime. This new data may lead to a complexity growth in the case of wrong
usage, which opens the door to analyze the co-evolution of such traceability
tools with the source code.
We can evaluate the system eﬀectiveness traceability by trying to recover
back the system at a random point of its pipeline evolution.
5
Preliminary results
We share our preliminary results regarding a case study on open source GitHub
projects that are using DVC and how the complexity of the traceability pipelines
co-evolution with source code ﬁles.
Best practice lessons of such tool usage
are provided. However, traceability and explainability are two complementary
methods in such an environment.
The following study will help us to learn the best practices of integrating
such traceability tools in our system. We have this work accepted in Saner2021
[189].
6
Conclusion and Future Work
An explainable, traceable automated e-recruitment is a need in the cross-border
labor market to ﬁnd the appropriate candidate that matches a proposed job.
This project aims to propose an eﬀective e-recruiting tool to suggest the best
candidates for the job postings. We will review and provide the State-of-the-
art in the JD/Resume matching systems. This study proposes an e-recruiting
architecture that considers JD/Resume matching by combining knowledge bases
with a pretrained transformer-based machine learning model such as BERT.
Furthermore, the system will generate an explainable report that can be useful
for the stakeholders to know the JD/Resume matching system decision. Finally,
this research will help to automatize the e-recruitment systems by making them
suitable for fair, explainable, and traceable JD/Resume matching.
The on-going SLR presented in the section 3.1 is the ﬁrst step to achieve our
thesis: (1) study the state-of-the-art in the JD/Resume matching ; (2) explore
the performance of training an accurate JD/Resume models by combining a
knowledge base with modern language models for recommendation purposes;
(3) provide an explainable report to the stakeholders of the matching decisions
60


---

## Page 62

recommendations; (4) adapt a traceable existing model to be able to track the
diﬀerent layers of the proposed matching and explainable architecture. We aim
to continue this research to achieve the following short and long-term goals
which will allow concluding our thesis.
We summarize our thesis research timeline in Figure 22. It shows the evolu-
tion of the research in time during the past and next two years. The academic
requirements include course activities, literature review, and the synthesis exam,
written and oral part of the research proposal. The deliverable phase includes
the preparation for one journal paper and three conference papers. Finally, the
Ph.D. dissertation phase includes the Ph.D. thesis preparation and revision and
defense. We plan to ﬁnish this thesis work by the Winter session of 2022.
All results will be published in Q1 ranked journals and NLP conferences
(ASE, CICLING, CIKM, ESWC)
Figure 22: Research timeline
61


---

## Page 63

References
[1] “Understanding
rnn
and
lstm.
what
is
neural
network?
|
by
aditi mittal | towards data science.” https://towardsdatascience.
com/understanding-rnn-and-lstm-f7cdf6dfc14e.
(Accessed
on
11/18/2020).
[2] “Bi-lstm. what is a neural network?
just like our. . .
| by raghav
aggarwal
|
medium.”
https://medium.com/@raghavaggarwal0089/
bi-lstm-bc3d68da8bd0. (Accessed on 11/18/2020).
[3] “convolutional neural network.” http://www.wildml.com/wp-content/
uploads/2015/11/Screen-Shot-2015-11-06-at-8.03.47-AM.png.
(Accessed on 11/18/2020).
[4] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
Ł. Kaiser, and I. Polosukhin, “Attention is all you need,” in Advances in
neural information processing systems, pp. 5998–6008, 2017.
[5] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training
of deep bidirectional transformers for language understanding,” arXiv
preprint arXiv:1810.04805, 2018.
[6] S. A. Directorate-General for Employment and I. E. Commission), “Three
tools to facilitate online job matching throughout europe,” 2011.
[7] E. Derous, H.-H. D. Nguyen, and A. M. Ryan, “Reducing ethnic discrimi-
nation in resume-screening: a test of two training interventions,” European
Journal of Work and Organizational Psychology, pp. 1–15, 2020.
[8] A. L. Paoletti, J. Martinez-Gil, and K.-D. Schewe, “Top-k matching
queries for ﬁlter-based proﬁle matching in knowledge bases,” in Interna-
tional Conference on Database and Expert Systems Applications, pp. 295–
302, Springer, 2016.
[9] X. Yi, J. Allan, and W. B. Croft, “Matching resumes and jobs based on
relevance models,” in Proceedings of the 30th annual international ACM
SIGIR conference on Research and development in information retrieval,
pp. 809–810, 2007.
[10] M. Reusens, W. Lemahieu, B. Baesens, and L. Sels, “A note on explicit
versus implicit information for job recommendation,” Decision Support
Systems, vol. 98, pp. 26–35, 2017.
[11] A. Gugnani and H. Misra, “Implicit skills extraction using document em-
bedding and its use in job recommendation.,” in AAAI, pp. 13286–13293,
2020.
62


---

## Page 64

[12] A. Chaudhary, M. Jobanputra, S. Shah, R. Gandhi, S. Chaudhary, and
R. Goswami, “Automated human capital management system,” in 2018
Annual IEEE International Systems Conference (SysCon), pp. 1–8, IEEE,
2018.
[13] A. Conneau, D. Kiela, H. Schwenk, L. Barrault, and A. Bordes, “Super-
vised learning of universal sentence representations from natural language
inference data,” ArXiv Preprint ArXiv:1705.02364, 2017.
[14] J. Yosinski, J. Clune, Y. Bengio, and H. Lipson, “How transferable are
features in deep neural networks?,” in Advances in Neural Information
Processing Systems, pp. 3320–3328, 2014.
[15] J. Deng, W. Dong, R. Socher, L.-J. Li, K. Li, and L. Fei-Fei, “Imagenet:
A large-scale hierarchical image database,” in 2009 IEEE Conference on
Computer Vision and Pattern Recognition, pp. 248–255, Ieee, 2009.
[16] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy, M. Lewis,
L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly optimized bert
pretraining approach,” ArXiv Preprint ArXiv:1907.11692, 2019.
[17] J. De Smedt, M. le Vrang, and A. Papantoniou, “Esco: Towards a semantic
web for the european labor market.,” in LDOW@ WWW, 2015.
[18] Y. Liu, J. Gu, N. Goyal, X. Li, S. Edunov, M. Ghazvininejad, M. Lewis,
and L. Zettlemoyer, “Multilingual denoising pre-training for neural ma-
chine translation,” arXiv preprint arXiv:2001.08210, 2020.
[19] D. A. Tamburri, W. J. V. D. Heuvel, and M. Garriga, “Dataops for so-
cietal intelligence: a data pipeline for labor market skills extraction and
matching,” in 2020 IEEE 21st International Conference on Information
Reuse and Integration for Data Science (IRI), pp. 391–394, 2020.
[20] “Mlﬂow - a platform for the machine learning lifecycle | mlﬂow.” https:
//mlflow.org/. (Accessed on 06/05/2020).
[21] “Data
version
control
·
dvc.”
https://dvc.org/.
(Accessed
on
06/05/2020).
[22] “Apache atlas – data governance and metadata framework for hadoop.”
https://atlas.apache.org/#/. (Accessed on 11/13/2020).
[23] K. Karlsen and P. Olsen, “3 - problems and implementation hurdles in
food traceability,” in Advances in Food Traceability Techniques and Tech-
nologies (M. Espiñeira and F. J. Santaclara, eds.), Woodhead Publishing
Series in Food Science, Technology and Nutrition, pp. 35 – 46, Woodhead
Publishing, 2016.
[24] V. M. Catano, Recruitment and selection in Canada. Cengage Learning,
2009.
63


---

## Page 65

[25] S. Amershi, A. Begel, C. Bird, R. DeLine, H. Gall, E. Kamar, N. Nagap-
pan, B. Nushi, and T. Zimmermann, “Software engineering for machine
learning: A case study,” in 2019 IEEE/ACM 41st International Confer-
ence on Software Engineering: Software Engineering in Practice (ICSE-
SEIP), pp. 291–300, IEEE, 2019.
[26] H. Atwal, “Dataops technology,” in Practical DataOps, pp. 215–247,
Springer, 2020.
[27] T. Hasanin, T. M. Khoshgoftaar, J. L. Leevy, and R. A. Bauder, “Investi-
gating class rarity in big data,” Journal of Big Data, vol. 7, no. 1, pp. 1–17,
2020.
[28] T. Saito and M. Rehmsmeier, “The precision-recall plot is more informa-
tive than the roc plot when evaluating binary classiﬁers on imbalanced
datasets,” PloS one, vol. 10, no. 3, p. e0118432, 2015.
[29] L. A. Cabrera-Diego, M. El-Bèze, J.-M. Torres-Moreno, and B. Durette,
“Ranking résumés automatically using only résumés: A method free of job
oﬀers,” Expert Systems with Applications, vol. 123, pp. 91–107, 2019.
[30] C. Loﬁ, “Measuring semantic similarity and relatedness with distributional
and knowledge-based approaches,” Information and Media Technologies,
vol. 10, no. 3, pp. 493–501, 2015.
[31] M. Dehghan, H. A. Rahmani, A. A. Abin, and V.-V. Vu, “Mining shape
of expertise: A novel approach based on convolutional neural network,”
Information Processing & Management, vol. 57, no. 4, p. 102239, 2020.
[32] Y. Balachander and T.-S. Moh, “Ontology based similarity for information
technology skills,” in 2018 IEEE/ACM International Conference on Ad-
vances in Social Networks Analysis and Mining (ASONAM), pp. 302–305,
IEEE, 2018.
[33] R. Le, W. Hu, Y. Song, T. Zhang, D. Zhao, and R. Yan, “Towards eﬀec-
tive and interpretable person-job ﬁtting,” in Proceedings of the 28th ACM
International Conference on Information and Knowledge Management,
pp. 1883–1892, 2019.
[34] S. Guo, F. Alamudun, and T. Hammond, “Résumatcher: A personalized
résumé-job matching system,” Expert Systems with Applications, vol. 60,
pp. 169–182, 2016.
[35] M.-L. Tran, A.-T. Nguyen, Q.-D. Nguyen, and T. Huynh, “A compari-
son study for job recommendation,” in 2017 International Conference on
Information and Communications (ICIC), pp. 199–204, IEEE, 2017.
[36] A. Grover, D. Arya, and G. Venkataraman, “Latency reduction via deci-
sion tree based query construction,” in Proceedings of the 2017 ACM on
Conference on Information and Knowledge Management, pp. 1399–1407,
2017.
64


---

## Page 66

[37] M. Reusens, W. Lemahieu, B. Baesens, and L. Sels, “Evaluating recom-
mendation and search in the labor market,” Knowledge-Based Systems,
vol. 152, pp. 62–69, 2018.
[38] Y. Luo, H. Zhang, Y. Wen, and X. Zhang, “Resumegan: An optimized
deep representation learning framework for talent-job ﬁt via adversarial
learning,” in Proceedings of the 28th ACM International Conference on
Information and Knowledge Management, pp. 1101–1110, 2019.
[39] G. Özcan and S. G. Ögüdücü, “Applying diﬀerent classiﬁcation techniques
in reciprocal job recommender system for considering job candidate pref-
erences,” in 2016 11th International Conference for Internet Technology
and Secured Transactions (ICITST), pp. 235–240, IEEE, 2016.
[40] F. C. Fernández-Reyes and S. Shinde, “Cv retrieval system based on job
description matching using hybrid word embeddings,” Computer Speech
& Language, vol. 56, pp. 73–79, 2019.
[41] B. Kitchenham and S. Charters, “Guidelines for performing systematic
literature reviews in software engineering,” 2007.
[42] M. Staples and M. Niazi, “Experiences using systematic review guidelines,”
J. Syst. Softw., vol. 80, pp. 1425–1437, Sept. 2007.
[43] Z. Sharaﬁ, Z. Soh, and Y.-G. Guéhéneuc, “A systematic literature review
on the usage of eye-tracking in software engineering,” Inf. Softw. Technol.,
vol. 67, pp. 79–107, Nov. 2015.
[44] “Machine learning explainability vs interpretability: Two concepts that
could help restore trust in ai.” https://www.kdnuggets.com/2018/
12/machine-learning-explainability-interpretability-ai.html.
(Accessed on 11/21/2020).
[45] C. Qin, H. Zhu, T. Xu, C. Zhu, C. Ma, E. Chen, and H. Xiong, “An
enhanced neural network approach to person-job ﬁt in talent recruitment,”
ACM Transactions on Information Systems (TOIS), vol. 38, no. 2, pp. 1–
33, 2020.
[46] C. Qin, H. Zhu, T. Xu, C. Zhu, L. Jiang, E. Chen, and H. Xiong, “Enhanc-
ing person-job ﬁt for talent recruitment: An ability-aware neural network
approach,” in The 41st International ACM SIGIR Conference on Research
& Development in Information Retrieval, pp. 25–34, 2018.
[47] J. Jiang, S. Ye, W. Wang, J. Xu, and X. Luo, “Learning eﬀective rep-
resentations for person-job ﬁt by feature fusion,” in Proceedings of the
29th ACM International Conference on Information & Knowledge Man-
agement, pp. 2549–2556, 2020.
[48] Z. C. Lipton, “The mythos of model interpretability,” Queue, vol. 16, no. 3,
pp. 31–57, 2018.
65


---

## Page 67

[49] R. Haﬀar, J. Domingo-Ferrer, and D. Sánchez, “Explaining misclassiﬁca-
tion and attacks in deep learning via random forests,” in International
Conference on Modeling Decisions for Artiﬁcial Intelligence, pp. 273–285,
Springer, 2020.
[50] D. Bau, B. Zhou, A. Khosla, A. Oliva, and A. Torralba, “Network dis-
section: Quantifying interpretability of deep visual representations,” in
Proceedings of the IEEE conference on computer vision and pattern recog-
nition, pp. 6541–6549, 2017.
[51] M. Danilevsky, K. Qian, R. Aharonov, Y. Katsis, B. Kawas, and P. Sen,
“A survey of the state of explainable ai for natural language processing,”
arXiv preprint arXiv:2010.00711, 2020.
[52] N. Poerner, B. Roth, and H. Schütze, “Evaluating neural network expla-
nation methods using hybrid documents and morphological agreement,”
arXiv preprint arXiv:1801.06422, 2018.
[53] L. Luo, X. Ao, F. Pan, J. Wang, T. Zhao, N. Yu, and Q. He, “Beyond po-
larity: Interpretable ﬁnancial sentiment analysis with hierarchical query-
driven attention.,” in IJCAI, pp. 4244–4250, 2018.
[54] R. Ghaeini, X. Z. Fern, and P. Tadepalli, “Interpreting recurrent and
attention-based neural models: a case study on natural language infer-
ence,” arXiv preprint arXiv:1808.03894, 2018.
[55] N. Liu, X. Huang, J. Li, and X. Hu, “On interpretation of network
embedding via taxonomy induction,” in Proceedings of the 24th ACM
SIGKDD International Conference on Knowledge Discovery & Data Min-
ing, pp. 1812–1820, 2018.
[56] S. Zhang and S. Vucetic, “Sampling bias in linkedin: A case study,” in
Proceedings of the 25th International Conference Companion on World
Wide Web, pp. 145–146, 2016.
[57] M. Ramannavar and N. S. Sidnal, “A proposed contextual model for big
data analysis using advanced analytics,” in Big Data Analytics, pp. 329–
339, Springer, 2018.
[58] B. Gupta, S. Kanodia, N. Khanna, et al., “A comprehensive recommender
system for fresher and employer,” in Progress in Advanced Computing and
Intelligent Engineering, pp. 119–127, Springer, 2019.
[59] R. Nimbekar, Y. Patil, R. Prabhu, and S. Mulla, “Automated resume eval-
uation system using nlp,” in 2019 International Conference on Advances in
Computing, Communication and Control (ICAC3), pp. 1–4, IEEE, 2019.
[60] F. Javed, Q. Luo, M. McNair, F. Jacob, M. Zhao, and T. S. Kang,
“Carotene: A job title classiﬁcation system for the online recruitment
domain,” in 2015 IEEE First International Conference on Big Data Com-
puting Service and Applications, pp. 286–293, IEEE, 2015.
66


---

## Page 68

[61] U. P. K. Kethavarapu and S. Saraswathi, “Concept based dynamic ontol-
ogy creation for job recommendation system,” Procedia computer science,
vol. 85, pp. 915–921, 2016.
[62] A. Qodad, A. El Kenz, A. Benyoussef, and M. El Yadari, “An adaptive
learning system based on a matching jobs and resumes engine,” in Pro-
ceedings of the 4th International Conference on Big Data and Internet of
Things, pp. 1–7, 2019.
[63] S. Corde, V. R. Chifu, I. Salomie, E. S. Chifu, and A. Iepure, “Bird mating
optimization method for one-to-n skill matching,” in 2016 IEEE 12th In-
ternational Conference on Intelligent Computer Communication and Pro-
cessing (ICCP), pp. 155–162, IEEE, 2016.
[64] A. Nigam, A. Roy, H. Singh, and H. Waila, “Job recommendation through
progression of job selection,” in 2019 IEEE 6th International Conference
on Cloud Computing and Intelligence Systems (CCIS), pp. 212–216, IEEE,
2019.
[65] M. Singh, K. N. Ramamurthy, and S. Vasudevan, “Propensity modeling
for employee re-skilling,” in 2017 IEEE Global Conference on Signal and
Information Processing (GlobalSIP), pp. 893–897, IEEE, 2017.
[66] V. Gatteschi, F. Lamberti, G. Paravati, A. Raso, and C. Demartini,
“Which learning outcomes should i acquire? a bar chart-based semantic
system for visually comparing learners’ acquirements with labor market
requirements,” in 2016 IEEE 40th Annual Computer Software and Appli-
cations Conference (COMPSAC), vol. 1, pp. 774–779, IEEE, 2016.
[67] Q. Liu, F. Javed, and M. Mcnair, “Companydepot: Employer name nor-
malization in the online recruitment industry,” in Proceedings of the 22nd
ACM SIGKDD International Conference on Knowledge Discovery and
Data Mining, pp. 521–530, 2016.
[68] K. Kusnawi, J. Ipmawati, and D. Kusumandaru, “Decision support sys-
tem employee recommendation using fuzzy sugeno method as a job search
service,” in 2019 International Conference on Information and Commu-
nications Technology (ICOIACT), pp. 539–542, IEEE, 2019.
[69] R. Liu, Y. Ouyang, W. Rong, X. Song, W. Xie, and Z. Xiong, “Employer
oriented recruitment recommender service for university students,” in In-
ternational Conference on Intelligent Computing, pp. 811–823, Springer,
2016.
[70] M. Papoutsoglou, N. Mittas, and L. Angelis, “Mining people analytics
from stackoverﬂow job advertisements,” in 2017 43rd Euromicro Con-
ference on Software Engineering and Advanced Applications (SEAA),
pp. 108–115, IEEE, 2017.
67


---

## Page 69

[71] S. Ahuja, J. Mondal, S. S. Singh, and D. G. George, “Similarity com-
putation exploiting the semantic and syntactic inherent structure among
job titles,” in International Conference on Service-Oriented Computing,
pp. 3–18, Springer, 2017.
[72] C. S. Namahoot and M. Brückner, “Standard-based bidirectional decision
making for job seekers and employers,” in International Conference on
Cooperative Design, Visualization and Engineering, pp. 10–20, Springer,
2017.
[73] R. Liu, W. Rong, Y. Ouyang, and Z. Xiong, “A hierarchical similarity
based job recommendation service framework for university students,”
Frontiers of Computer Science, vol. 11, no. 5, pp. 912–922, 2017.
[74] Y. Zhang, C. Yang, and Z. Niu, “A research of job recommendation system
based on collaborative ﬁltering,” in 2014 Seventh International Symposium
on Computational Intelligence and Design, vol. 1, pp. 533–538, IEEE,
2014.
[75] T. Sandanayake, G. Limesha, T. Madhumali, W. Mihirani, and M. Peiris,
“Automated cv analyzing and ranking tool to select candidates for job po-
sitions,” in Proceedings of the 6th International Conference on Information
Technology: IoT and Smart City, pp. 13–18, 2018.
[76] L. Jain, M. H. Vardhan, G. Kathiresan, and A. Narayan, “Optimizing peo-
ple sourcing through semantic matching of job description documents and
candidate proﬁle using improved topic modelling techniques,” in Advances
in Artiﬁcial Intelligence and Data Engineering, pp. 899–908, Springer,
2020.
[77] D. Celik, “Towards a semantic-based information extraction system for
matching résumés to job openings,” Turkish Journal of Electrical Engi-
neering & Computer Sciences, vol. 24, no. 1, pp. 141–159, 2016.
[78] C. Chanavaltada, P. Likitphanitkul, and M. Phankokkruad, “An improve-
ment of recommender system to ﬁnd appropriate candidate for recruit-
ment with colloborative ﬁltering,” in 2015 International Conference on
Informative and Cybernetics for Computational Social Systems (ICCSS),
pp. 72–77, IEEE, 2015.
[79] J. Martinez-Gil, A. L. Paoletti, and M. Pichler, “A novel approach for
learning how to automatically match job oﬀers and candidate proﬁles,”
Information Systems Frontiers, pp. 1–10, 2019.
[80] C.-O. Truică and A. Barnoschi, “Innovating hr using an expert system for
recruiting it specialists–esrit,” arXiv preprint arXiv:1906.04915, 2019.
[81] J. C. Valverde-Rebaza, R. Puma, P. Bustios, and N. C. Silva, “Job recom-
mendation based on job seeker skills: An empirical study.,” in Text2Story@
ECIR, pp. 47–51, 2018.
68


---

## Page 70

[82] E. Espenakk, M. J. Knalstad, and A. Kofod-Petersen, “Lazy learned
screening for eﬃcient recruitment,” in International Conference on Case-
Based Reasoning, pp. 64–78, Springer, 2019.
[83] B. Walek, O. Pektor, and R. Farana, “Proposal of the web application
for selection of suitable job applicants using expert system,” in Computer
Science On-line Conference, pp. 363–373, Springer, 2016.
[84] E. A. K. Zaman, A. F. A. Kamal, A. Mohamed, A. Ahmad, and R. A. Z.
R. M. Zamri, “Staﬀemployment platform (step) using job proﬁling ana-
lytics,” in International Conference on Soft Computing in Data Science,
pp. 387–401, Springer, 2018.
[85] A. L. Paoletti, J. Martinez-Gil, and K.-D. Schewe, “Extending knowledge-
based proﬁle matching in the human resources domain,” in Database and
Expert Systems Applications, pp. 21–35, Springer, 2015.
[86] A. Zaroor, M. Maree, and M. Sabha, “A hybrid approach to conceptual
classiﬁcation and ranking of resumes and their corresponding job posts,”
in International Conference on Intelligent Decision Technologies, pp. 107–
119, Springer, 2017.
[87] M. Maree, A. B. Kmail, and M. Belkhatir, “Analysis and shortcomings
of e-recruitment systems: Towards a semantics-based approach address-
ing knowledge incompleteness and limited domain coverage,” Journal of
Information Science, vol. 45, no. 6, pp. 713–735, 2019.
[88] A. B. Kmail, M. Maree, M. Belkhatir, and S. M. Alhashmi, “An automatic
online recruitment system based on exploiting multiple semantic resources
and concept-relatedness measures,” in 2015 IEEE 27th International Con-
ference on Tools with Artiﬁcial Intelligence (ICTAI), pp. 620–627, IEEE,
2015.
[89] R. Susanto and A. Andriana, “Employee recruitment analysis using com-
puter based weighted product model,” in IOP Conference Series: Mate-
rials Science and Engineering, vol. 662, p. 022049, IOP Publishing, 2019.
[90] A. Gupta and D. Garg, “Applying data mining techniques in job recom-
mender system for considering candidate job preferences,” in 2014 In-
ternational Conference on Advances in Computing, Communications and
Informatics (ICACCI), pp. 1458–1465, IEEE, 2014.
[91] X. Guo, H. Jerbi, and M. P. O’Mahony, “An analysis framework for
content-based job recommendation,” in 22nd International Conference on
Case-Based Reasoning (ICCBR), Cork, Ireland, 29 September-01 October
2014, 2014.
[92] A. B. Kmail, M. Maree, and M. Belkhatir, “Matchingsem: Online recruit-
ment system based on multiple semantic resources,” in 2015 12th Interna-
tional Conference on Fuzzy Systems and Knowledge Discovery (FSKD),
pp. 2654–2659, IEEE, 2015.
69


---

## Page 71

[93] P. Bafna, S. Shirwaikar, and D. Pramod, “Task recommender system us-
ing semantic clustering to identify the right personnel,” VINE Journal of
Information and Knowledge Management Systems, 2019.
[94] W. Chen, P. Zhou, S. Dong, S. Gong, M. Hu, K. Wang, and D. Wu, “Tree-
based contextual learning for online job or candidate recommendation
with big data support in professional social networks,” IEEE Access, vol. 6,
pp. 77725–77739, 2018.
[95] N. D. Almalis, G. A. Tsihrintzis, and N. Karagiannis, “A content based
approach for recommending personnel for job positions,” in IISA 2014,
The 5th International Conference on Information, Intelligence, Systems
and Applications, pp. 45–49, IEEE, 2014.
[96] L. Mrsic, H. Jerkovic, and M. Balkovic, “Interactive skill based labor mar-
ket mechanics and dynamics analysis system using machine learning and
big data,” in Asian Conference on Intelligent Information and Database
Systems, pp. 505–516, Springer, 2020.
[97] Q.-D. Nguyen, T. Huynh, and T.-A. Nguyen-Hoang, “Adaptive methods
for job recommendation based on user clustering,” in 2016 3rd National
Foundation for Science and Technology Development Conference on In-
formation and Computer Science (NICS), pp. 165–170, IEEE, 2016.
[98] P. Yi, C. Yang, C. Li, and Y. Zhang, “A job recommendation method op-
timized by position descriptions and resume information,” in 2016 IEEE
Advanced Information Management, Communicates, Electronic and Au-
tomation Control Conference (IMCEC), pp. 761–764, IEEE, 2016.
[99] D. Lee and C. Ahn, “Industrial human resource management optimization
based on skills and characteristics,” Computers & Industrial Engineering,
p. 106463, 2020.
[100] A. Jacobsen and G. Spanakis, “It’s a match!
reciprocal recommender
system for graduating students and jobs.,” in EDM, 2019.
[101] L. Duan, X. Gui, M. Wei, and Y. Wu, “A resume recommendation algo-
rithm based on k-means++ and part-of-speech tf-idf,” in Proceedings of
the 2019 International Conference on Artiﬁcial Intelligence and Advanced
Manufacturing, pp. 1–5, 2019.
[102] S. Maheshwary and H. Misra, “Matching resumes to jobs via deep siamese
network,” in Companion Proceedings of the The Web Conference 2018,
pp. 87–88, 2018.
[103] P. K. Roy, S. S. Chowdhary, and R. Bhatia, “A machine learning approach
for automation of resume recommendation system,” Procedia Computer
Science, vol. 167, pp. 2318–2327, 2020.
70


---

## Page 72

[104] G. Bal, A. Karakaş, T. Güngör, F. Süzen, and K. C. Kara, “A matching
approach based on term clusters for erecruitment,” in Industrial Confer-
ence on Data Mining, pp. 394–404, Springer, 2016.
[105] Q. Guohao, W. Bin, W. Bai, and Z. Baoli, “Competency analysis in hu-
man resources using text classiﬁcation based on deep neural network,”
in 2019 IEEE Fourth International Conference on Data Science in Cy-
berspace (DSC), pp. 322–329, IEEE, 2019.
[106] N. D. Almalis, G. A. Tsihrintzis, N. Karagiannis, and A. D. Strati, “Fo-
dra—a new content-based job recommendation algorithm for job seeking
and recruiting,” in 2015 6th International Conference on Information, In-
telligence, Systems and Applications (IISA), pp. 1–7, IEEE, 2015.
[107] C. Zhu, H. Zhu, H. Xiong, C. Ma, F. Xie, P. Ding, and P. Li, “Person-
job ﬁt: Adapting the right talent for the right job with joint representa-
tion learning,” ACM Transactions on Management Information Systems
(TMIS), vol. 9, no. 3, pp. 1–17, 2018.
[108] S. Amin, N. Jayakar, S. Sunny, P. Babu, M. Kiruthika, and A. Gurjar,
“Web application for screening resume,” in 2019 International Conference
on Nascent Technologies in Engineering (ICNTE), pp. 1–7, IEEE, 2019.
[109] S. Charleer, F. Gutiérrez, and K. Verbert, “Supporting job mediator and
job seeker through an actionable dashboard,” in Proceedings of the 24th In-
ternational Conference on Intelligent User Interfaces, pp. 121–131, 2019.
[110] S. Pahari, D. Ghosh, and A. Pal, “A framework for personal selection pro-
cess using trapezoidal intuitionistic fuzzy sets,” in Computational Science
and Engineering: Proceedings of the International Conference on Compu-
tational Science and Engineering (Beliaghata, Kolkata, India, 4-6 October
2016), p. 159, CRC Press, 2016.
[111] Q. Luo, M. Zhao, F. Javed, and F. Jacob, “Macau: Large-scale skill sense
disambiguation in the online recruitment domain,” in 2015 IEEE Inter-
national Conference on Big Data (Big Data), pp. 1324–1329, IEEE, 2015.
[112] P. Xu and D. Barbosa, “Matching résumés to job descriptions with stacked
models,” in Canadian Conference on Artiﬁcial Intelligence, pp. 304–309,
Springer, 2018.
[113] A. Mohamed,
W. Bagawathinathan,
U. Iqbal,
S. Shamrath,
and
A. Jayakody, “Smart talents recruiter-resume ranking and recommenda-
tion system,” in 2018 IEEE International Conference on Information and
Automation for Sustainability (ICIAfS), pp. 1–5, IEEE, 2018.
[114] P. R. Chaudhari, P. C. Gangurde, and N. L. Kulkarni, “Design of an ex-
pert system for competence and performance management using sanskrit
computational linguistics,” in 2015 International Conference on Green
Computing and Internet of Things (ICGCIoT), pp. 90–92, IEEE, 2015.
71


---

## Page 73

[115] N. Fatma, V. Choudhary, N. Sachdeva, and N. Rajput, “Canonicalizing
knowledge bases for recruitment domain,” in Paciﬁc-Asia Conference on
Knowledge Discovery and Data Mining, pp. 500–513, Springer, 2020.
[116] M. He, D. Shen, Y. Zhu, R. He, T. Wang, and Z. Zhang, “Career tra-
jectory prediction based on cnn,” in 2019 IEEE International Conference
on Service Operations and Logistics, and Informatics (SOLI), pp. 22–26,
IEEE, 2019.
[117] S. Dong, Z. Lei, P. Zhou, K. Bian, and G. Liu, “Job and candidate rec-
ommendation with big data support: A contextual online learning ap-
proach,” in GLOBECOM 2017-2017 IEEE Global Communications Con-
ference, pp. 1–7, IEEE, 2017.
[118] X. XXXX, “An neural information retrieval approach for résumé searching
in a recruitment agency,”
[119] Z. Wang, X. Tang, and D. Chen, “A resume recommendation model for
online recruitment,” in 2015 11th International Conference on Semantics,
Knowledge and Grids (SKG), pp. 256–259, IEEE, 2015.
[120] M. Liu, J. Wang, K. Abdelfatah, and M. Korayem, “Tripartite vec-
tor representations for better job recommendation,”
arXiv preprint
arXiv:1907.12379, 2019.
[121] G. R. Leah, P. C. Enrico, and A. R. Christopher, “A vectorization model
for job matching application of a government employment service oﬃce,”
International Workshop on Computer Science and Engineering, 2019.
[122] L. G. Rodriguez and E. P. Chavez, “Feature selection for job matching
application using proﬁle matching model,” in 2019 IEEE 4th International
Conference on Computer and Communication Systems (ICCCS), pp. 263–
266, IEEE, 2019.
[123] H. Wenxing, C. Yiwei, Q. Jianwei, and H. Yin, “ihr+: A mobile recipro-
cal job recommender system,” in 2015 10th International Conference on
Computer Science & Education (ICCSE), pp. 492–495, IEEE, 2015.
[124] S. Chala, S. Harrison, and M. Fathi, “Knowledge extraction from online
vacancies for eﬀective job matching,” in 2017 IEEE 30th Canadian Con-
ference on Electrical and Computer Engineering (CCECE), pp. 1–4, IEEE,
2017.
[125] G. Qiao, B. Wu, B. Wang, and B. Zhang, “Mlca: A multi-label competency
analysis method based on deep neural network,” in International Confer-
ence on Advanced Data Mining and Applications, pp. 805–814, Springer,
2019.
72


---

## Page 74

[126] D. Pessach, G. Singer, D. Avrahami, H. C. Ben-Gal, E. Shmueli, and
I. Ben-Gal, “Employees recruitment: A prescriptive analytics approach
via machine learning and mathematical programming,” Decision Support
Systems, p. 113290, 2020.
[127] Y. Deng, H. Lei, X. Li, and Y. Lin, “An improved deep neural network
model for job matching,” in 2018 International Conference on Artiﬁcial
Intelligence and Big Data (ICAIBD), pp. 106–112, IEEE, 2018.
[128] W. Chen, X. Zhang, H. Wang, and H. Xu, “Hybrid deep collaborative
ﬁltering for job recommendation,” in 2017 2nd IEEE International Con-
ference on Computational Intelligence and Applications (ICCIA), pp. 275–
280, IEEE, 2017.
[129] A. Cernian and V. Sgarciu, “Boosting the recruitment process through
semi-automatic semantic skills identiﬁcation,” in Proceedings of The World
Congress on Engineering 2017, pp. 605–607, 2017.
[130] W. Shalaby, K. Al Jadda, M. Korayem, and T. Grainger, “Entity type
recognition using an ensemble of distributional semantic models to en-
hance query understanding,” in 2016 IEEE 40th Annual Computer Soft-
ware and Applications Conference (COMPSAC), vol. 1, pp. 631–636,
IEEE, 2016.
[131] A. Zaroor, M. Maree, and M. Sabha, “Jrc: A job post and resume classi-
ﬁcation system for online recruitment,” in 2017 IEEE 29th International
Conference on Tools with Artiﬁcial Intelligence (ICTAI), pp. 780–787,
IEEE, 2017.
[132] F. Borisyuk, K. Kenthapadi, D. Stein, and B. Zhao, “Casmos: A frame-
work for learning candidate selection models over structured queries and
documents,” in Proceedings of the 22nd ACM SIGKDD International Con-
ference on Knowledge Discovery and Data Mining, pp. 441–450, 2016.
[133] D. Lee, M. Kim, and I. Na, “Artiﬁcial intelligence based career matching,”
Journal of Intelligent & Fuzzy Systems, vol. 35, no. 6, pp. 6061–6070,
2018.
[134] S. K. Chanda, M. S. Areﬁn, R. Karim, and Y. Morimoto, “Developing a
technique to select potential candidates using a combination of rough sets
and fuzzy sets,” in International Conference on Intelligent Computing &
Optimization, pp. 45–60, Springer, 2019.
[135] O. Manad, M. Bentounsi, and P. Darmon, “Enhancing talent search by
integrating and querying big hr data,” in 2018 IEEE International Con-
ference on Big Data (Big Data), pp. 4095–4100, IEEE, 2018.
[136] Y. Kino, H. Kuroki, T. Machida, N. Furuya, and K. Takano, “Text anal-
ysis for job matching quality improvement,” Procedia computer science,
vol. 112, pp. 1523–1530, 2017.
73


---

## Page 75

[137] “Writing
an
eﬀective
job
description
|
human
resources
|
wright
state
university.”
https://www.wright.edu/human-resources/
policies-and-resources/writing-an-effective-job-description.
(Accessed on 10/31/2020).
[138] “Understanding
educational
requirements
for
job
listings.”
https://www.thebalancecareers.com/
educational-requirements-for-employment-2059799.
(Accessed
on 10/31/2020).
[139] J. Nguyen, G. Sánchez-Hernández, A. Armisen, N. Agell, X. Rovira, and
C. Angulo, “A linguistic multi-criteria decision-aiding system to support
university career services,” Applied Soft Computing, vol. 67, pp. 933–940,
2018.
[140] Y.-C. Chou, C.-Y. Chao, and H.-Y. Yu, “A résumé evaluation system based
on text mining,” in 2019 International Conference on Artiﬁcial Intelli-
gence in Information and Communication (ICAIIC), pp. 052–057, IEEE,
2019.
[141] M. Mehta, R. Derasari, S. Patel, A. Kakadiya, R. Gandhi, S. Chaud-
hary, and R. Goswami, “A service-oriented human capital management
recommendation platform,” in 2019 IEEE International Systems Confer-
ence (SysCon), pp. 1–8, IEEE, 2019.
[142] G. K. Palshikar, R. Srivastava, M. Shah, and S. Pawar, “Automatic short-
listing of candidates in recruitment.,” in ProfS/KG4IR/Data: Search@
SIGIR, pp. 5–11, 2018.
[143] E. Malherbe and M.-A. Aufaure, “Bridge the terminology gap between
recruiters and candidates: A multilingual skills base built from social
media and linked data,” in 2016 IEEE/ACM International Conference on
Advances in Social Networks Analysis and Mining (ASONAM), pp. 583–
590, IEEE, 2016.
[144] B. Patel, V. Kakuste, and M. Eirinaki, “Capar: a career path recommen-
dation framework,” in 2017 IEEE Third International Conference on Big
Data Computing Service and Applications (BigDataService), pp. 23–30,
IEEE, 2017.
[145] S. Bian, W. X. Zhao, Y. Song, T. Zhang, and J.-R. Wen, “Domain adap-
tation for person-job ﬁt with transferable deep global match network,” in
Proceedings of the 2019 Conference on Empirical Methods in Natural Lan-
guage Processing and the 9th International Joint Conference on Natural
Language Processing (EMNLP-IJCNLP), pp. 4812–4822, 2019.
[146] E. Malherbe, M. Diaby, M. Cataldi, E. Viennet, and M.-A. Aufaure, “Field
selection for job categorization and recommendation to social network
74


---

## Page 76

users,” in 2014 IEEE/ACM International Conference on Advances in So-
cial Networks Analysis and Mining (ASONAM 2014), pp. 588–595, IEEE,
2014.
[147] E. EP et al., “Framework of an intelligent job recommendation system,”
in Proceedings of International Conference on Sustainable Computing in
Science, Technology and Management (SUSCOM), Amity University Ra-
jasthan, Jaipur-India, 2019.
[148] P. Neculoiu, M. Versteegh, and M. Rotaru, “Learning text similarity with
siamese recurrent networks,” in Proceedings of the 1st Workshop on Rep-
resentation Learning for NLP, pp. 148–157, 2016.
[149] D. Widdows, “Orthogonal negation in vector spaces for modelling word-
meanings and document retrieval,” in Proceedings of the 41st annual meet-
ing of the association for computational linguistics, pp. 136–143, 2003.
[150] H. Wenxing, C. Yiwei, Q. Jianwei, and H. Yin, “ihr+: A mobile recipro-
cal job recommender system,” in 2015 10th International Conference on
Computer Science & Education (ICCSE), pp. 492–495, IEEE, 2015.
[151] H. Yu, C. Liu, and F. Zhang, “Reciprocal recommendation algorithm for
the ﬁeld of recruitment,” Journal of Information & Computational Sci-
ence, vol. 8, no. 16, pp. 4061–4068, 2011.
[152] K. Kenthapadi, B. Le, and G. Venkataraman, “Personalized job recom-
mendation system at linkedin: Practical challenges and lessons learned,”
in Proceedings of the Eleventh ACM Conference on Recommender Sys-
tems, pp. 346–347, 2017.
[153] W. E. Winkler, “Overview of record linkage and current research direc-
tions,” in Bureau of the Census, Citeseer, 2006.
[154] M. Maree, A. B. Kmail, and M. Belkhatir, “Analysis and shortcomings
of e-recruitment systems: Towards a semantics-based approach address-
ing knowledge incompleteness and limited domain coverage,” Journal of
Information Science, vol. 45, p. 713–735, Nov 2018.
[155] S. Deerwester, S. Dumais, T. Landauer, G. Furnas, and L. Beck, “Improv-
ing information-retrieval with latent semantic indexing,” in Proceedings of
the ASIS annual meeting, vol. 25, pp. 36–40, INFORMATION TODAY
INC 143 OLD MARLTON PIKE, MEDFORD, NJ 08055-8750, 1988.
[156] R. Rentzsch and M. Staneva, “Skills-matching and skills intelligence
through curated and data-driven ontologies,” Proceedings of the DELFI
Workshops, 2020.
[157] G. A. Miller, WordNet: An electronic lexical database. MIT press, 1998.
75


---

## Page 77

[158] F. M. Suchanek, G. Kasneci, and G. Weikum, “Yago: a core of semantic
knowledge,” in Proceedings of the 16th international conference on World
Wide Web, pp. 697–706, 2007.
[159] J. Lehmann, R. Isele, M. Jakob, A. Jentzsch, D. Kontokostas, P. N.
Mendes, S. Hellmann, M. Morsey, P. Van Kleef, S. Auer, et al., “Dbpedia–
a large-scale, multilingual knowledge base extracted from wikipedia,” Se-
mantic web, vol. 6, no. 2, pp. 167–195, 2015.
[160] M. Ivanović and Z. Budimac, “An overview of ontologies and data re-
sources in medical domains,” Expert Systems with Applications, vol. 41,
no. 11, pp. 5158–5166, 2014.
[161] S. Hochreiter, “The vanishing gradient problem during learning recurrent
neural nets and problem solutions,” International Journal of Uncertainty,
Fuzziness and Knowledge-Based Systems, vol. 6, no. 02, pp. 107–116, 1998.
[162] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural
computation, vol. 9, no. 8, pp. 1735–1780, 1997.
[163] A. Graves and J. Schmidhuber, “Framewise phoneme classiﬁcation with
bidirectional lstm and other neural network architectures,” Neural net-
works, vol. 18, no. 5-6, pp. 602–610, 2005.
[164] K. Cho, B. Van Merriënboer, C. Gulcehre, D. Bahdanau, F. Bougares,
H. Schwenk, and Y. Bengio, “Learning phrase representations using
rnn encoder-decoder for statistical machine translation,” arXiv preprint
arXiv:1406.1078, 2014.
[165] N. Kalchbrenner, E. Grefenstette, and P. Blunsom, “A convolutional neu-
ral network for modelling sentences,” arXiv preprint arXiv:1404.2188,
2014.
[166] M. Shi, D. A. Wilson, X. Zhu, Y. Huang, Y. Zhuang, J. Liu, and
Y. Tang, “Evolutionary architecture search for graph neural networks,”
arXiv preprint arXiv:2009.10199, 2020.
[167] S. Bian, X. Chen, W. X. Zhao, K. Zhou, Y. Hou, Y. Song, T. Zhang,
and J.-R. Wen, “Learning to match jobs with resumes from sparse inter-
action data using multi-view co-teaching network,” in Proceedings of the
29th ACM International Conference on Information & Knowledge Man-
agement, pp. 65–74, 2020.
[168] T. Zhang, B. Liu, D. Niu, K. Lai, and Y. Xu, “Multiresolution graph at-
tention networks for relevance matching,” in Proceedings of the 27th ACM
International Conference on Information and Knowledge Management,
pp. 933–942, 2018.
76


---

## Page 78

[169] A. Galassi, M. Lippi, and P. Torroni, “Attention in natural language pro-
cessing,” IEEE Transactions on Neural Networks and Learning Systems,
2020.
[170] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean, “Dis-
tributed representations of words and phrases and their compositional-
ity,” in Advances in neural information processing systems, pp. 3111–3119,
2013.
[171] Q. Le and T. Mikolov, “Distributed representations of sentences and doc-
uments,” in International conference on machine learning, pp. 1188–1196,
2014.
[172] L. Shakurova,
B. Nyari,
C. Li,
and M. Rotaru,
“Best practices
for learning domain-speciﬁc cross-lingual embeddings,” arXiv preprint
arXiv:1907.03112, 2019.
[173] C. J. Baaij, “The eu policy on institutional multilingualism: Between prin-
ciples and practicality,” JLL, vol. 1, p. 14, 2012.
[174] T. Pires, E. Schlinger, and D. Garrette, “How multilingual is multilingual
bert?,” arXiv preprint arXiv:1906.01502, 2019.
[175] M. Langenkamp, A. Costa, and C. Cheung, “Hiring fairly in the age of
algorithms,” arXiv preprint arXiv:2004.07132, 2020.
[176] R. Mac, “Amazon releases diversity numbers for the ﬁrst time and surprise,
it’s mostly male and white,” 2014.
[177] R. Goodman, “Why amazon’s automated hiring tool discriminated against
women.(2018),” 2018.
[178] “Apache
airﬂow.”
http://airflow.apache.org/.
(Accessed
on
06/04/2020).
[179] “spotify/luigi.”
https://github.com/spotify/luigi.
(Accessed on
06/04/2020).
[180] L. B. Miguel, D. Takabayashi, J. R. Pizani, T. Andrade, and B. West,
“Marvin-from exploratory models to production,” Journal of Machine
Learning Research, pp. 33–44, 2017.
[181] “quantumblacklabs/kedro: A python library that implements software en-
gineering best-practice for data and ml pipelines..” https://github.com/
quantumblacklabs/kedro. (Accessed on 06/05/2020).
[182] “Pachyderm | version-controlled data science.” https://www.pachyderm.
com/. (Accessed on 06/05/2020).
77


---

## Page 79

[183] F. Abel, A. Benczúr, D. Kohlsdorf, M. Larson, and R. Pálovics, “Recsys
challenge 2016: Job recommendations,” in Proceedings of the 10th ACM
Conference on Recommender Systems, RecSys ’16, (New York, NY, USA),
p. 425–426, Association for Computing Machinery, 2016.
[184] J. Li, A. Sun, J. Han, and C. Li, “A survey on deep learning for named
entity recognition,” IEEE Transactions on Knowledge and Data Engineer-
ing, 2020.
[185] L. Martin, B. Muller, P. J. O. Suárez, Y. Dupont, L. Romary, É. V. de la
Clergerie, D. Seddah, and B. Sagot, “Camembert: a tasty french language
model,” arXiv preprint arXiv:1911.03894, 2019.
[186] I. Tenney, J. Wexler, J. Bastings, T. Bolukbasi, A. Coenen, S. Gehrmann,
E. Jiang, M. Pushkarna, C. Radebaugh, E. Reif, et al., “The language
interpretability tool: Extensible, interactive visualizations and analysis
for nlp models,” arXiv preprint arXiv:2008.05122, 2020.
[187] M. T. Ribeiro, S. Singh, and C. Guestrin, “"why should i trust you?"
explaining the predictions of any classiﬁer,” in Proceedings of the 22nd
ACM SIGKDD international conference on knowledge discovery and data
mining, pp. 1135–1144, 2016.
[188] T. Lei, R. Barzilay, and T. Jaakkola, “Rationalizing neural predictions,”
arXiv preprint arXiv:1606.04155, 2016.
[189] A. Barrak, E. E. Eghan, and B. Adams, “On the co-evolution of ml
pipelines and source code – empirical study of dvc projects,” in Proceed-
ings of the 28th IEEE International Conference on Software Analysis,
Evolution, and Reengineering (SANER), (Hawaii, USA), March 2021. To
appear.
78
