## Page 1

arXiv:2505.20312v1  [cs.CY]  22 May 2025
Let’s Get You Hired: A Job Seeker’s Perspective on Multi-Agent
Recruitment Systems for Explaining Hiring Decisions
Aditya Bhattacharya
aditya.bhattacharya@kuleuven.be
KU Leuven
Leuven, Belgium
Katrien Verbert
katrien.verbert@kuleuven.be
KU Leuven
Leuven, Belgium
Figure 1: High-level design of our multi-agent recruitment system. The agentic architecture was designed through an iterative,
user-centric process involving active job seekers, ensuring that the system aligns with their needs and expectations.
ABSTRACT
During job recruitment, traditional applicant selection methods
often lack transparency. Candidates are rarely given sufficient justi-
fications for recruiting decisions, whether they are made manually
by human recruiters or through the use of black-box Applicant
Tracking Systems (ATS). To address this problem, our work intro-
duces a multi-agent AI system that uses Large Language Models
(LLMs) to guide job seekers during the recruitment process. Us-
ing an iterative user-centric design approach, we first conducted
a two-phased exploratory study with four active job seekers to
inform the design and development of the system. Subsequently,
we conducted an in-depth, qualitative user study with 20 active job
seekers through individual one-to-one interviews to evaluate the
developed prototype. The results of our evaluation demonstrate
that participants perceived our multi-agent recruitment system
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for components of this work owned by others than the
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or
republish, to post on servers or to redistribute to lists, requires prior specific permission
and/or a fee. Request permissions from permissions@acm.org.
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
© 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM ISBN 978-x-xxxx-xxxx-x/YY/MM...$15.00
https://doi.org/10.1145/nnnnnnn.nnnnnnn
as significantly more actionable, trustworthy, and fair compared
to traditional methods. Our study further helped us uncover in-
depth insights into factors contributing to these perceived user
experiences. Drawing from these insights, we offer broader design
implications for building user-aligned, multi-agent explainable AI
systems across diverse domains.
CCS CONCEPTS
• Human-centered computing →Human computer interac-
tion (HCI); Systems and tools for interaction design; • Com-
puting methodologies →Artificial intelligence.
KEYWORDS
Explainable AI, XAI, LLM, Conversational Explanations, Agentic
AI, Multi-Agent System
ACM Reference Format:
Aditya Bhattacharya and Katrien Verbert. 2025. Let’s Get You Hired: A Job
Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining
Hiring Decisions. In Proceedings of the 38th Annual ACM Symposium on
User Interface Software and Technology (UIST ’25), September 28 – October
1, 2025, Busan, South Korea. ACM, New York, NY, USA, 16 pages. https:
//doi.org/10.1145/nnnnnnn.nnnnnnn


---

## Page 2

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
1
INTRODUCTION
Despite technological advancements, the conventional job applica-
tion process lacks transparency, particularly in the initial candidate
shortlisting phase. Traditional approaches, whether relying on the
algorithmic ‘black box’ of Applicant Tracking Systems (ATS) or
the subjective evaluations of human recruiters, often fail to pro-
vide applicants with constructive and personalised feedback for
explaining the hiring decision [31]. The lack of clarity in hiring deci-
sions negatively impacts job seekers’ experiences. When decisions
seem arbitrary, trust erodes, engagement declines, and uncertainty
persists [27, 31].
Recent advancements in Large Language Model (LLM)-based
conversational AI systems have transformed the ability of decision
support systems to explain their predicted outcomes [12, 51]. Ad-
ditionally, the emergence of AI agents, i.e., autonomous systems
that leverage LLMs’ reasoning capabilities to perceive, analyse,
and act, presents a new opportunity to increase transparency in
candidate shortlisting and provide clearer explanations for hiring
decisions [19]. This is due to the inherent ability of agentic systems
to integrate diverse data sources and perform complex reasoning
of user queries, allowing for the generation of context-aware and
personalised explanations [16, 39]. For instance, in a recruitment
scenario, an applicant can query an AI agent for company back-
ground information before an interview. The AI agent can utilise
web search tools to retrieve relevant company details and suggest
ways for the applicant to highlight their strengths during the inter-
view, aligning with the company’s core values. This capability to
tailor explanations to individual user needs holds immense promise
for improving the job application experience.
To effectively meet the diverse needs of end users interacting
with agentic systems, prior research has emphasised the signifi-
cance of multi-agent systems [16]. Unlike single AI agents, which
often struggle with context switching and generate inaccurate or
irrelevant responses when tasked with multiple roles, multi-agent
systems distribute responsibilities among specialised agents, im-
proving both the accuracy and relevance of the generated responses
[21]. However, the effective design of these systems remains a signif-
icant challenge, particularly due to the limited user-centred research
in this area [24]. Key obstacles include designing simplified system
architectures with clearly defined agent roles and capabilities, es-
tablishing efficient communication protocols between agents, and
developing strategies for resolving disagreements between multiple
agents [16, 21, 22, 61].
Our research seeks to bridge these gaps by introducing a user-
centric multi-agent system designed to provide actionable explana-
tions that clarify hiring decisions for job applicants. This system
enables applicants to engage in a conversational dialogue, evaluate
their job profile against specific openings and obtain tailored sug-
gestions for profile improvement and interview preparation. We
adopted an iterative, user-centred design approach (UCD) [48] to
develop the system. We started with a two-phased exploratory user
study involving four active job seekers to capture key user require-
ments and co-design the system. This was followed by an in-depth
qualitative study using one-to-one semi-structured interviews with
20 participants. This study focused on addressing the following
research questions:
RQ1. How do job applicants perceive the actionability of multi-
agent AI feedback for improving their job applications?
RQ2. How do job applicants develop trust and confidence in a
multi-agent system for hiring decisions?
RQ3. How do job applicants perceive the fairness and potential
biases of multi-agent AI in hiring decisions and guidance?
In general, this work highlights the importance of a user-centred
approach when designing multi-agent Explainable AI (XAI) sys-
tems [2]. Our evaluation showed that participants perceived the
multi-agent recruitment system as significantly more actionable,
trustworthy, and fair compared to conventional hiring methods. Ad-
ditionally, the study offered valuable insights into how job seekers
perceive and interpret multi-agent systems used to explain hiring
decisions in comparison to conventional methods. Accordingly, this
work makes three key contributions:
(1) Theoretical Contributions: We introduce an iterative user-
centric design approach specifically tailored for developing
multi-agent XAI systems. Furthermore, by synthesising in-depth
insights from our qualitative user study, we contribute broader
design implications applicable to the creation of explainable and
user-aligned multi-agent AI systems across various domains.
(2) Artifact Contributions: We present a tangible instantiation
of our UCD approach into a multi-agent recruitment chatbot
that provides actionable feedback to job applicants. The source
code, user-centric system architecture, and system prompts are
open-sourced on GitHub.
(3) Empirical Contributions: We present findings from a quali-
tative evaluation with 20 active job seekers, highlighting that
users perceived the system as more actionable, trustworthy,
and fair compared to traditional recruitment methods. We also
collected complementary quantitative data, revealing that eval-
uation scores for perceived actionability, trust, and fairness
were significantly higher for our system than for traditional
methods. These insights can inform future research on build-
ing user-centric multi-agent systems beyond the recruitment
domain.
2
BACKGROUND AND RELATED WORK
2.1
AI Agents
AI agents are autonomous entities that leverage LLMs to perceive,
think, and act in a certain environment to accomplish specific ob-
jectives [12, 16]. These agents typically consist of three core com-
ponents: (1) an LLM-based reasoning engine, (2) a suite of external
tools for interfacing with external data sources (e.g., databases,
APIs), and (3) a memory module for retaining contextual infor-
mation [22]. These systems offer distinct advantages, including
automated task execution based on dynamic conditions, better
decision-making through reasoned analysis, and personalised rec-
ommendations tailored to specific user contexts [22, 61].
To further improve the relevance and utility of agentic conversa-
tions, integrating techniques like Retrieval-Augmented Generation
(RAG) enables the retrieval of real-time information [20]. Moreover,
a variety of prompting techniques, including ReAct [67] and Chain-
of-Thought (CoT) [62], are essential for assuring intended results
and directing agent behaviour. These diverse strategies were selec-
tively applied throughout the design and experimentation phases


---

## Page 3

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
to steer agents toward producing more accurate, explainable, and
user-aligned recommendations.
Prior work has shown the importance of having multiple AI
agents, rather than a single agent, when designing systems to meet
diverse user needs [16, 22]. Single-agent systems excel at specialised
tasks, while multi-agent systems coordinate multiple agents to ad-
dress complex and varied tasks, where each agent fulfils a specific
role. Multi-agent architectures have demonstrated significant bene-
fits in contexts that require collaboration, distributed knowledge, or
a combination of specialised skills [16]. By distributing workloads
and integrating their outputs, multi-agent systems are essential to
execute tasks that exceed the capacity of individual agents.
Prior studies on AI agent system architecture reveal diverse
designs, ranging from simple to complex [35]. These include hierar-
chical systems, where a central planner directs subordinate agents,
decentralised networks allowing autonomous agent collaboration,
and supervised structures with a lead agent overseeing sub-agents
[16]. However, the design process of agentic systems by AI experts
often overlooks the real needs of end-users. Consequently, this
oversight leads to agentic systems that are unnecessarily complex
and poorly aligned with user expectations.
Our work involves a user-centric process for designing the multi-
agent architecture and profiling individual agents. This includes
defining agent roles and goals, developing prompting strategies
to control their behaviour, designing toolkits, managing memory,
and overall user interface (UI). The system aims to deliver conver-
sational explanations to end users by engaging them in natural,
dialogue-based conversations.
2.2
User Interfaces for Conversational
Explanation
Conversational explanations are explanations that are delivered
through free-form natural language dialogues to improve user un-
derstanding of AI systems [32, 37, 42, 55, 69]. Recent developments
in LLM-powered AI agents have necessitated the integration of
reasoning and explanation capabilities into traditional Conversa-
tional User Interfaces (CUIs), such as chatbots and voice assistants
[32, 52, 55, 69]. Additionally, prior research has highlighted the
importance of CUIs in delivering dynamic, personalised responses
tailored to users’ backgrounds, needs, and preferences [32].
In this work, we refer to CUIs designed for conversational expla-
nations as Explanation-driven CUIs (xCUIs). Our research investi-
gates how job seekers interact with an iteratively designed xCUI to
understand hiring decisions and improve their job prospects. While
our study focuses on recruitment, its implications extend to other
domains where xCUIs can enhance the transparency of decision
support systems.
3
APPLICATION IMPLEMENTATION: MULTI
AGENTIC RECRUITMENT SYSTEM
3.1
Usage Scenario
We developed our multi-agentic xCUI using a user-centred de-
sign methodology [48] (as illustrated in Figure 2) to support job
seekers mostly in the early stages of the hiring process. The de-
mand for xCUI systems during job recruitment is particularly high,
as traditional candidate shortlisting methods are deemed to lack
transparency [31]. Whether through manual assessment by human
recruiters or black-box ATS platforms, candidates rarely receive
adequate explanations for hiring decisions [27]. This lack of trans-
parency underscores the need for XAI solutions to increase the
fairness and clarity of the decision-making process for job seekers.
Furthermore, applicants often require individualised feedback to re-
fine their resumes, acquire relevant skills, and improve their overall
chances of being hired. Our xCUI system directly addresses these
needs by evaluating a job seeker’s profile suitability for specific
openings and delivering tailored suggestions for profile enhance-
ment and interview preparation during the hiring process.
3.2
Exploratory User Study
The application was implemented through an iterative UCD ap-
proach, beginning with a two-phased exploratory user study to
identify key user requirements and inform the preliminary ap-
plication design. This study was conducted online in two phases
using Microsoft Teams (as the online meeting platform) and Miro (a
real-time collaborative whiteboard). Ethical approval for the study
was obtained from KU Leuven (Approval Number: G-2024-8652-
R3(MAR)). This study involved voluntary, pro-bono participation
from four active job seekers, all of whom had recent experience in
the job application process. The participants were evenly distributed
by gender and ranged in age from 25 to 41 years (𝑀= 31,𝑆𝐷= 5.1).
Recruitment was conducted via LinkedIn.
The first phase of the study involved individual think-aloud and
co-design sessions. During the think-aloud sessions, we explored
the key challenges job seekers face in the recruitment process and
the types of support they would expect from an AI system. In the
co-design component, participants engaged with existing AI tools
(ChatGPT and Gemini web applications) and reimagined the de-
sign of a new support system by creating sketches on Miro. Each
session lasted approximately one hour. These sessions helped us
uncover participants’ core needs during the job application process
and collect initial system design ideas grounded in their lived ex-
periences. Informed by their input and chatbot design principles
from prior research [24, 63, 66], we created a low-fidelity proto-
type. In the subsequent phase, the same four participants assessed
this prototype during approximately 30-minute semi-structured
interview sessions. Their feedback was crucial in refining and devel-
oping a high-fidelity prototype. Moreover, their insights extended
beyond the design of the UI. We utilised their feedback to design
the multi-agent system architecture and defined the specific roles
and responsibilities of each agent as discussed in Section 3.4.
To facilitate qualitative analysis, all meetings have been recorded
and transcribed. To derive key user requirements and inform the
user-driven design of the multi-agent architecture, including agent
roles and behaviour through prompt engineering, we adopted Braun
and Clarke’s thematic analysis method [11]. This approach enabled
us to extract meaningful themes grounded in participants’ expe-
riences and expectations for the design and development of our
system.


---

## Page 4

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
Figure 2: Iterative user-centric design and development approach for our multi-agentic recruitment system.
3.3
User Requirements
The following user requirements were confirmed after analysing
the feedback captured from our exploratory study:
1. Provide applicants with a concise evaluation of their fit
for a desired job position: Our participants highlighted the
need for a nuanced, quantitative evaluation of their resume’s
alignment with target job descriptions. They underscored the
critical importance of an additional explanation that unpacks
the rationale behind the matching score. One of the participants
mentioned: “the most frustrating aspect of job applications is
the complete lack of meaningful feedback after rejections. I want
to understand the real probability of my selection and receive
clear, specific guidance on improving my profile. Sometimes, I feel
that the opening is not an actual opening but rather for internal
hiring when the rejection message is very vague.” This explanatory
feedback would not only quantify their hiring chances but also
provide actionable insights, highlighting specific strengths to
leverage and precise skill gaps to address.
2. Recommend necessary changes in applicant’s profile to
increase hiring prospects: Participants said that, in contrast
to conventional ATS-based candidate screening, they needed
a system that offers practical advice on how to modify their
CV or resume for a particular position in order to improve
their chances of getting shortlisted. For instance, one of them
mentioned: “When transitioning between job roles, not all of my
previous experience is equally important for the new role. I need
the AI to tell me the most useful skills and projects that align with
the new position, rather than including all of my past experiences.”
3. Include a recruiter’s perspective to clarify job expecta-
tions: Participants consistently struggled with the absence of
recruiter feedback, which hindered their understanding of a
role’s key responsibilities. They expressed the need for recruiter-
like insights to evaluate their readiness, identify skill gaps, and
obtain motivating feedback to better prepare for desired posi-
tions. One of them mentioned: “Once, I was rejected thrice for a
manager role, even though I knew I was a good fit. When I directly
reached out to the hiring manager through LinkedIn, I was told
that the HR recruiter thought I lacked prior people management
experience, even though I was a senior staff engineer with people
management experience. The recruiter responsible for the short-
listing process did not fully understand the role of a staff engineer.
So, if the AI can think like a real recruiter, it will help to identify
changes needed [in the resume] to clear the screening stage”.
4. Include a mentor perspective for better interview prepa-
ration: Participants highlighted the desired role of the AI as a
mentor, suggesting it could offer career guidance by recommend-
ing suitable roles, companies, and seniority levels based on their
profiles. They emphasised the need for constructive feedback
delivered in a positive tone to foster confidence throughout the
application process. For instance, one of them stated: “Reaching
out to a real [human] mentor is not always easy. My questions
might be too basic and silly for them. Whereas the AI can mentor
me and highlight my strengths so that I feel confident during
interviews. I can also ask my silly questions without the fear of
being judged.”
5. Provide candidates with balanced comments to help them
prepare for interviews: Every participant emphasised the im-
portance of study materials and possible interview questions, as
well as assistance with interview preparation. They also voiced
worries about AI systems giving answers that are excessively
acceptable or positive. For instance, one of them mentioned: “I
tried ChatGPT [for evaluating their resume]. It is too positive most
of the time. AI shouldn’t shield us from the harsh reality, and they
need to be critical sometimes to help us improve.” They like candid
criticism that takes into account both strengths and weaknesses.
Some participants proposed using a moderator to settle disputes
between the viewpoints of recruiters and mentors, much like in
a formal debate style: “I like getting multiple perspectives. But to
get the main [takeaway] messages, perhaps another AI can act as
a debate moderator when there is a conflicting opinion between an
AI mentor and an AI recruiter.” Such a method would guarantee
a more fair and helpful assessment, giving the candidate concise
and useful takeaways.
3.4
Multi-Agentic System Design
To meet the identified user requirements, a multi-agentic system de-
sign is necessary, as participants expressed the need for the system
to function simultaneously as a recruiter, mentor, and moderator.
This justifies our choice of a multi-agent system over a single agent


---

## Page 5

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
performing multiple tasks, as the latter presents several challenges,
including hallucinations caused by rapid context switching [61].
3.4.1
Agent Roles and Responsibilities. To overcome these limi-
tations while fulfilling user requirements, we formulated a multi-
agent design consisting of the following three specialised agents,
each with dedicated roles and responsibilities. The specific num-
ber of agents and the definition of these distinct roles were not
based on pre-existing HR frameworks or arbitrary selection. In-
stead, they were carefully derived from a thorough analysis of the
feedback gathered during our initial exploratory study with active
job seekers. This user-centred approach ensured that the agentic
composition directly aimed to address the key information needs
and perspectives identified by our target users.
(1)
Recruiter : The recruiter agent simulates the role of a hir-
ing manager by evaluating a candidate’s suitability for a given
position based on their academic background, professional
experience, and relevant skill sets. It delivers objective, ana-
lytical feedback using structured scores and ratings to assess
candidate-job fit. Rather than offering overly positive or generic
responses, the recruiter agent focuses on constructive and ac-
tionable feedback, highlighting key areas for improvement and
skill gaps. To enhance clarity and readability, its outputs are
presented in a concise tabular format, avoiding long, text-heavy
explanations.
(2)
Mentor : The mentor agent functions as a supportive coach,
guiding candidates in enhancing their job profiles and prepar-
ing for the recruitment process. It delivers constructive and
actionable feedback by suggesting improvements for resumes,
interview strategies, and skill development. In cases where re-
cruiter feedback may appear overly critical, the mentor agent
provides balancing perspectives by emphasising the candidate’s
strengths. Adopting a friendly, conversational, and encouraging
tone, the agent provides examples and explanations to guide
candidates in taking action to improve their hiring prospects.
(3)
Moderator : The moderator agent functions as the final
decision-maker, orchestrating the interaction between the re-
cruiter and mentor agents to ensure fair, consistent, and well-
reasoned hiring recommendations. It critically evaluates the
perspectives offered by both agents, mediates disagreements,
and provides transparent justifications for its decisions. The
moderator maintains a neutral stance, avoiding overly positive
or negative feedback, and summarises key points in a balanced
manner to deliver an objective and comprehensive assessment
to the applicant. To enhance reliability, the moderator lever-
ages the LLM-as-a-Judge approach [71], ensuring that final
responses are contextually relevant and minimise hallucina-
tions. Furthermore, the moderator agent presents its feedback
in a concise and accessible format, incorporating graphical ele-
ments such as emoticons to clearly highlight strengths, gaps,
and actionable next steps for the candidate.
3.4.2
Architectural Design Pattern. Based on insights from our
exploratory study, we implemented a supervisory multi-agent ar-
chitecture [16, 35]. In this framework, a central moderator agent
serves as the primary interface for user interactions while oversee-
ing the recruiter and mentor agents. Although these sub-agents
operate under the moderator’s supervision, they function inde-
pendently, processing user queries and generating responses au-
tonomously. To enable constructive argumentation and ensure bal-
anced recommendations, responses generated by the sub-agents are
shared among them. This mechanism allows for counter-arguments
and justifications, particularly when discrepancies arise in hiring
assessments. Upon receiving a user query, the moderator deter-
mines whether to engage the recruiter agent, the mentor agent, or
both, depending on the context. It then validates and synthesises
the sub-agents’ responses into a cohesive, structured output before
presenting it to the user. Figure 1 illustrates the high-level design
of our multi-agent architecture.
3.4.3
Agent Tools. As the central supervisory agent, the modera-
tor exclusively manages access to the system’s toolkit, a suite of
functionalities designed to enhance decision-making and ensure
the overall accuracy of the agentic responses. This toolkit com-
prises modules for extracting and interpreting information from
applicant resumes and job descriptions, performing web searches
to gather contextual data about the hiring company or job role,
and applying moderation mechanisms to prevent hallucinations or
the generation of harmful content. In contrast, the recruiter and
mentor agents do not directly access these tools. This design choice
was made to optimise response latency and ensure consistent, reli-
able tool usage. Our experiments showed that less capable LLMs,
when deployed as sub-agents, were more error-prone in invoking
tools. Centralising tool access within the moderator agent not only
streamlined the communication pipeline but also improved the
consistency and dependability of responses. Sub-agents rely on the
moderator to supply the contextual information required for their
individual responses. In situations where key details are unclear or
incomplete, these agents can initiate clarification requests to the
moderator. This coordination mechanism enables iterative refine-
ment and facilitates the generation of more contextually grounded
and refined recommendations.
3.4.4
Agent Memory Management. While every agent maintains a
log of all conversational exchanges that include the user inputs and
generated responses, the moderator agent centrally manages the
overall conversation history to ensure consistency and preserve
contextual understanding throughout interactions. This centralised
memory allows for coherent dialogues with users and seamless in-
formation flow across agents. The individual memory of sub-agents
is particularly useful for generating responses to follow-up user
queries that require detailed reasoning behind the recommenda-
tions. This ensures that suggestions for improving hiring prospects
or interview preparation remain contextually relevant and informed
by prior exchanges.
3.5
High-Fidelity Prototype
Building on insights from our exploratory study, we developed a
high-fidelity prototype of an xCUI that integrates the multi-agent
system design outlined in Section 3.4. This prototype was imple-
mented as an interactive web application designed for job seekers
navigating the recruitment process. For front-end development, we
utilised Streamlit [58], a Python-based framework for creating web
applications. The moderator agent was powered by GPT-4-Turbo


---

## Page 6

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
Figure 3: Screenshot of our multi-agent xCUI application with the different UI components marked: (a) UI control to upload
the resume and job requirement documents, (b) this component illustrates the matching score with summarised explanations,
(c) configuration controls to alter the display of certain UI components, (d) personalised agent introduction, (e) quick questions
to help users start the chatbot conversation and (f) agentic AI responses presented in a simplified format with necessary visual
aids along with input text box for user queries.
from OpenAI [44], chosen for its advanced reasoning capabilities
required to oversee and coordinate the sub-agents. Meanwhile,
the recruiter and mentor agents leveraged GPT-4o-Mini, which
offered faster response times while maintaining strong analytical
performance. Additionally, we integrated LangChain [33], an open-
source middleware framework that accelerates the development of
LLM applications. The user interface (UI) was constructed based on
an improved version of the low-fidelity prototype, incorporating
feedback from the initial exploratory study. It includes matching
scores accompanied by concise justifications, as well as a quick
questions feature allowing users to initiate interaction without man-
ual typing (similar to previous research [18, 55]). The job fit score
was computed as the average of the individual scores provided
by each sub-agent, based on the extent to which the applicant’s
experiences and qualifications aligned with the specified job re-
quirements. Users also have the option to customise their app view
to display their resume, the job description, quick questions, and a
detailed overview of the individual sub-agents (recruiter and men-
tor) through a configuration option. Figure 3 illustrates a screenshot
of our multi-agent xCUI application.
4
QUALITATIVE USER STUDY
4.1
Study Setup
We conducted an in-depth qualitative user study through semi-
structured interviews with 20 active job seekers. Ethical approval
was obtained from the KU Leuven Ethics Committee (approval
number G-2024-8652-R3(MAR)). The study was conducted online,
with each participant participating in a one-on-one interview that
lasted between 40 and 55 minutes, averaging approximately 45
minutes. Interviews were recorded and transcribed using Microsoft
Teams. In addition to qualitative insights, we collected quantitative
data through pre-task and post-task surveys to complement our
findings. This approach allowed us to gather both qualitative and
quantitative evidence to address our research questions.
4.2
Participants
This study involved 20 participants who were active job seekers
currently going through the application process. An initial cohort
was recruited through LinkedIn, with subsequent participants iden-
tified via snowball sampling. To mitigate potential bias, individuals
who participated in the exploratory user study were excluded from
this phase. The final participant group comprised a diverse range


---

## Page 7

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Table 1: Summarised demographic information of the quali-
tative user study participants.
Demographics
Participant Groups
Age
Groups
18 - 30 years: 9
31 - 40 years: 6
41 - 50 years: 5
Gender
Male: 11
Female: 9
Highest
Education Level
Bachelor: 13
Master: 7
Overall
Work Experience
Early to Mid Career Professionals (0-5 years): 8
Experienced Professionals (More than 5 years): 12
AI
Knowledge
No experience: 1
Novice (Knowledge of using AI tools like ChatGPT, Gemini): 15
Intermediate (Knowledge of developing AI applications): 3
Advance (Developed AI Applications): 1
Country of Origin
United States: 9, India: 5
Canada: 3, Belgium: 2, China: 1
of demographic backgrounds, including variations in gender, age,
education level, country of origin, and job experience level. The
summarised demographic information for all participants is pre-
sented in Table 1. To ensure anonymity when presenting the study’s
findings and quoting participants, each participant is referred to as
P(N), where N represents a unique identifier from 1 to 20.
4.3
Evaluation Measures
To address our research questions, this section describes the vari-
ous evaluation measures captured during our user study. For each
evaluation measure, we captured quantitative data through vali-
dated questionnaires from prior work. Additionally, we had semi-
structured interview questions to gather more in-depth qualitative
feedback from the participants. We included the complete set of
study questionnaires as part of the supplementary material.
Perceived Actionability: Based on insights from our exploratory
study, where participants consistently emphasised the need for
actionable feedback during the candidate shortlisting and inter-
view process, we aimed to evaluate the perceived actionability of
our system. Specifically, we aimed to compare its effectiveness
with conventional methods, such as ATS or manual assessments
conducted by human recruiters. Building on Shoemaker et al.’s def-
inition of actionability [53], we define perceived actionability as
the extent to which users believe the system delivers clear, feasible,
and valuable actions that help them achieve their primary goals.
To quantitatively measure perceived actionability, we utilised the
assessment toolkit developed by Singh et al. [54]. Additionally, to
gain qualitative insights, we designed semi-structured interview
questions informed by Bhattacharya et al. [4]. From the qualitative
responses, we aimed to explore which aspects of the multi-agent
system’s feedback users found most valuable and actionable, as
well as potential improvements, particularly in the context of job
recruitment.
Perceived Trust: Given that a lack of transparency in conventional
candidate shortlisting is a significant concern in the recruitment
process, we aimed to evaluate how the explanations generated by
our agentic system influence users’ perceived trust. We adopted the
definition of perceived trust in automated systems provided by Jian
et al. [28], who define it as a user’s confidence in the reliability, com-
petence, and integrity of an automated system in providing relevant
responses to achieve their goals. To quantitatively assess perceived
trust, we utilised their validated questionnaire. Furthermore, our
interview questions explored factors that could impact trust in
multi-agent systems (informed by prior work such as [5, 6, 41]) and
how users might react if their trust diminished due to issues with
agent responses.
Perceived Fairness: Due to the well-known pitfalls of LLMs [17, 30,
50, 60], such as hallucinations and biased responses, we sought to as-
sess how participants perceived the fairness of our system. Drawing
from methodologies in previous studies [38, 43], we quantitatively
evaluated the fairness of our agentic system and compared it with
traditional applicant shortlisting methods. Additionally, through
semi-structured interviews, we aimed to understand how users
would respond when they encountered biased responses or fairness
issues within the agentic system’s outputs.
We also logged the conversation history for each participant
to observe patterns in user queries and to evaluate the generated
responses for instances of hallucination or other common issues
generally observed in LLM outputs.
4.4
Study Procedure
Upon recruitment, participants were provided with comprehensive
information regarding the study’s objectives, their roles, respon-
sibilities, and rights. In adherence to our ethical guidelines, they
were required to provide informed consent prior to participation.
Following consent, participants completed a pre-task question-
naire. This instrument served to gather demographic data and de-
tails about their prior experiences with conventional candidate
shortlisting methods, whether manual (via human recruiters) or
automated (via ATS). Specifically, participants were asked to reflect
on their experiences in relation to our evaluation measures used to
address our research questions (perceived actionability, trust, and
fairness). This process allowed us to establish essential baseline
scores for a direct comparison with the user experiences derived
from our multi-agent xCUI system.
After completing the pre-task questionnaires, participants en-
gaged in a task where they uploaded their resume or CV, along with
a job description for a position of interest, through our application.
Subsequently, the AI system evaluated their hiring chances for that
specific role, displaying a matching score accompanied by justifica-
tions in the quick insights section. Participants could then interact
with the chatbot to ask questions, discuss their hiring prospects
and necessary resume improvements, and explore other relevant
queries. Concurrent with this task, they participated in one-on-one
semi-structured interviews to provide in-depth feedback on their
overall experience.
After interacting with our application, each participant com-
pleted a post-task questionnaire, where they provided feedback on
the system’s actionability, trustworthiness, and fairness. The quan-
titative data was analysed alongside qualitative interview insights
to address our research questions. An overview of the study flow is
illustrated in Figure 4.


---

## Page 8

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
Figure 4: Study flow of our qualitative user study with 20 active job seekers.
4.5
Data Analysis
Quantitative Data: For the quantitative analysis, we first evaluated
the normality of our collected data using the Shapiro-Wilk test [40].
Given that the data violated normality assumptions, we applied non-
parametric statistical test, such as the Mann-Whitney U test [40], to
compare the performance of our application against conventional
methods used in job recruitment.
Qualitative Data: We analysed the qualitative data using Braun and
Clarke’s six-phase thematic analysis method [11]. This involved
an initial review of the recorded interview transcripts, followed
by the generation of a list of preliminary codes derived from the
data. Through several iterative cycles, we then grouped these initial
codes into potential overarching themes. After carefully reviewing
and refining these preliminary themes, we established a final set
of themes. These themes provided deeper insights into the overall
user experience across our evaluation measures, enabling us to ad-
dress our research questions effectively. Additionally, they informed
potential refinements for the next iterative development phase of
our system. While the quantitative data from the 20 participants
provided an exploratory overview of their perceptions, the primary
focus and strength of this research lie in the rich, nuanced insights
gained from the qualitative analysis of the interview data, which
aimed to uncover the underlying factors driving these perceptions.
5
RESULTS
5.1
How do job applicants perceive the
actionability of multi-agent AI feedback for
improving their job applications? (RQ1)
5.1.1
Quantitative insights: Our analysis revealed a statistically
significant increase in perceived actionability for our system com-
pared to participants’ prior experiences with conventional methods
using the Mann-Whitney U-test (𝑈= 26, 𝑝< .001). Specifically, as
shown in Figure 5, the median actionability score for our system
was 34% higher than that of conventional methods. This finding
not only underscores the actionable nature of our multi-agent xCUI
but also highlights a substantial lack of actionable feedback in cur-
rent candidate shortlisting and recruitment processes. Our system
demonstrates considerable potential to address this critical gap by
providing job seekers with actionable recommendations, thereby
significantly improving their overall experience during recruitment.
Through qualitative data analysis, we gained a deeper understand-
ing of job seekers’ perspectives on the actionability of our system.
Figure 5: Box plots showing an increase in the perceived
actionability of our multi-agentic AI feedback compared to
conventional methods
5.1.2
What aspects of our multi-agent system’s feedback made it
seem more actionable than traditional methods? The following in-
sights derived from our qualitative analysis offer a comprehensive
understanding of the factors influencing the high perceived ac-
tionability of our system. Additionally, we report the number of
participants supporting each identified theme.
Improved understanding of alignment between candidate
profile and job requirements <16  >: Participants found our
multi-agent system’s feedback more actionable due to its clear
understanding of alignment between their resume and the job de-
scription of their target role. They highly valued how our system
identified the most critical gaps between their current profiles and
the job requirements, specifically in terms of experience and skills,
and clearly outlined the necessary steps to address these discrep-
ancies. For instance, P3 mentioned: “It’s really insightful to see how
this app differentiates between must-have and good-to-have skills.
Sometimes I even wonder if I still have a chance with a company if I
lack a skill they’re looking for. But this app clearly tells me just how
important that missing skill is for the specific role and tells me how
to acquire it.”
Personalised feedback to increase hiring prospects <14  >:
Participants acknowledged the effectiveness of our system in pro-
viding personalised feedback for tailoring resumes to specific roles.


---

## Page 9

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
This feature was particularly beneficial for candidates transitioning
to new job roles, as it helped them identify transferable skills and
relevant experiences while also highlighting essential skills they
needed to acquire to improve their hiring prospects. For example, P2
stated: “There are many transferable skills between data engineering
and data science like knowledge of ETL and using data pipelines. This
chatbot can actually help in identifying the most relevant projects
I should highlight in my resume for getting selected.” Additionally,
participants appreciated the system’s ability to recommend relevant
courses and learning resources, including external web links for
interview preparation: “Wow, this application not only tells me what
I am missing in my resume, but it is suggesting online courses and
videos I can watch to learn them!” (P1).
Importance of response format and xCUI components <17
 >: A majority of participants appreciated the chatbot’s concise,
visually enhanced summaries, which effectively highlighted their
strengths, identified key gaps, and pointed out job requirements
not explicitly mentioned in their resumes through the use of visual
icons. As P14 noted: “I love this concise tabular response. I can see
assessment areas, recommended actions to take, their impact on the
selection process, and these green ticks and red crosses that tell me
which aspects to improve and which aspects I am good at.” Partici-
pants also emphasised the value of the quick insights component,
which enabled them to rapidly grasp the actions required and as-
sess their overall chances of success at a glance. This feature was
particularly beneficial for candidates with limited work experience
(such as recent graduates), who often apply to a wide range of
positions and need to quickly determine job relevance. For instance,
P9 stated: “Recent graduates like me believe in shooting a thousand
arrows to hit the target once! This score and the explanations [in quick
insights] are enough to give me the confidence I need to apply for
openings.” Additionally, participants highlighted the importance
of the quick questions feature. Notably, 16 out of 20 participants
initiated their interaction with the system using the provided quick
questions, while the remaining four formulated their own queries.
These latter participants, who bypassed the generic suggested ques-
tions, expressed a desire for more in-depth clarification on specific
gaps identified in the quick insights.
Importance of both mentor and recruiter perspective for
increasing hiring prospects <13  >: The majority of our partici-
pants particularly valued the inclusion of both mentor and recruiter
perspectives for gaining a comprehensive understanding of nec-
essary improvements. For example, P16 mentioned: “I like getting
more perspectives as it helps me decide what is truly important and
what I can de-prioritise”. However, most of those who expressed
a preference for both (9 out of 13) found the recruiter feedback
more useful. They explained that the critical nature of this feedback
provided a realistic assessment of their shortcomings and the level
of effort required for improvement. For instance, P8 stated: “The
critical feedback is more useful. Even if it could make me feel worried,
the harsh feedback can actually motivate me to take that extra step
to improve my hiring chances”. Participants who did not explicitly
value the distinct perspectives of the mentor and recruiter agents
frequently perceived minimal divergence in their responses, largely
due to the alignment of the generated feedback. This observation
suggests that the individual presentation of both mentor and re-
cruiter perspectives may hold greater significance than exclusive
reliance on a synthesised response from the moderator, particularly
in instances where the sub-agents exhibit contradictory opinions.
Nevertheless, the moderator fulfilled a critical function in synthe-
sising actionable steps for the user and resolving any ambiguities
arising from the sub-agents’ responses.
5.1.3
How would users react when they perceive multi-agent AI
feedback as insufficiently actionable? While the majority of partici-
pants characterised the feedback and recommendations from our
multi-agent xCUI as highly actionable, a subset expressed a desire
for more granular explanations (6 out of 20). This deeper curiosity
centred on a more thorough understanding of identified gaps, strate-
gies for their mitigation, and the relevance of specific skills and
experiences to their target job role. The following insights help us
understand what users can do if the xCUI feedback is insufficiently
actionable for them.
Ask detailed follow-up questions for better clarification <6
 >: Participants who desired more detailed, granular feedback from
the system initiated multiple follow-up questions. Initially, these
follow-ups were often brief and sometimes vague. However, when
participants perceived a need for more comprehensive explanations,
their subsequent questions became well-articulated, clearly specify-
ing the information they sought in the response. For instance, P12
stated: “The explanations are good and useful, particularly because
an ATS will never generate such explanations. However, I would want
to know more about the missing 25% score [the matching score for
this participant was 75%], not just to validate my strengths but also
to prepare well to cover my weaknesses.” However, we also observed
a reluctance among some participants (8 out of 20) to pose detailed
and well-articulated questions, highlighting the potential benefit
of question chaining. This approach, where the moderator agent
proactively suggests relevant follow-up questions the user might
find pertinent, could address this reluctance and provide further
clarification without requiring the user to formulate the queries
themselves.
Steer the agent behaviour for personalised response formats
<3  >: A small proportion of participants indicated a tendency
to steer the AI feedback towards greater perceived actionability.
This behaviour may stem from their prior familiarity with prompt
engineering techniques for LLM-based chatbots: “Since I am a person
who loves more information, I will instruct the chatbot to give more
details to understand why this [missing] skill is relevant and what
can I do in a short time. As I’ve seen in ChatGPT, giving detailed
instructions generates more detailed answers” (P17).
5.1.4
How to make multi-agent AI feedback more actionable? Be-
yond understanding why users perceived our xCUI system as action-
able, we also identified several insights that could further enhance
its actionability. Although these suggestions fall outside the imme-
diate scope of this study, we include them in our results as potential
future enhancements that our system could support.
Consider personal situations for contextually robust rec-
ommendations <5  >: An interesting finding from our study
highlights that contextual knowledge extends beyond a nuanced
understanding of candidate profiles and job descriptions to encom-
pass the candidate’s personal situation. For instance, P5 received a
system suggestion to pursue a PhD to enhance his chances of secur-
ing a senior position they were targeting. However, P5’s personal


---

## Page 10

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
and family circumstances rendered a long-term commitment to a
PhD program unsuitable. This indicates the importance of incorpo-
rating personal context to refine the relevance and practicality of
AI-driven recommendations. He mentioned: “I know that getting a
PhD would be nice, but considering that I have a family to take care
of, a PhD at this point of my career is not an option.” Additionally,
P3 suggested that if a particular skill is realistically unattainable,
the system should explicitly indicate the negative impact of lacking
that skill. This information could empower candidates to make
informed decisions about whether to pursue the position or explore
alternative openings that are a better fit for their current capabili-
ties: “If getting this skill is not possible, I would be curious to know if
I’m completely out of chance for applying for this job”.
Provide examples of successful candidates for similar roles
<4  >: Many participants expressed a desire to compare their pro-
file and hiring prospects against individuals who were successfully
recruited for comparable positions within the same company. For
instance, P1 suggested: “It would be great to know some informa-
tion of candidates who successfully landed similar jobs within this
company, such as the skills they had, their overall years of experience,
their job title or previous employers”. While the comprehensive data
collection required to implement this feature across all companies
presents a considerable challenge, individual organisations could
consider maintaining a database of successful hires for specific
roles. Integrating the multi-agentic system with such an internal
database could effectively provide this comparative insight to job
seekers.
Simplified follow-up questioning <3  >: A few participants
suggested having a UI element adjacent to each recommendation
that would allow them to pose clarifying questions to the agentic
system with a simple click, eliminating the need for manual typing.
This feature could potentially reduce their perceived task load and
enhance the overall user experience. This feature could further
improve their perceived task load and improve the overall user
experience. For example, P20 stated: “It would be cool to just select
or click these suggestions and automatically a question could be asked
to the chatbot for getting a more detailed answer into how to execute
the recommendations”.
Integrate with popular external platforms <3  >: A few par-
ticipants also suggested the integration of our system with external
platforms commonly used by candidates to showcase their portfo-
lios, such as LinkedIn, GitHub, and personal websites. They noted
that human recruiters often review these supplementary platforms
alongside resumes or CVs to gain a more comprehensive under-
standing of a candidate’s profile. As mentioned by P2: “It would
be useful for me if this chatbot can connect to my GitHub and sug-
gest projects from my portfolio that I should definitely include in my
resume for this job”.
Key-takeaways: Job seekers perceived the multi-agent xCUI
as significantly more actionable than their prior experiences
with conventional methods, attributing this to the system’s
ability to clearly explain profile-job alignment and provide
personalised, targeted feedback. Key elements such as the
structured response format with visual icons and the inclu-
sion of both mentor and recruiter perspectives facilitated
a better understanding of necessary actions for increasing
their hiring prospects.
5.2
How do job applicants develop trust and
confidence in a multi-agent system for
hiring decisions? (RQ2)
5.2.1
Quantitative insights: Our quantitative analysis of perceived
trust in our multi-agent xCUI revealed significantly higher trust
scores compared to participants’ prior experiences with conven-
tional hiring methods (𝑈= 38.5, 𝑝< .001). As shown in Figure 6,
trust scores for our system were 30% higher than those of con-
ventional approaches. Furthermore, Spearman’s correlation test
indicated a significant positive correlation between perceived trust
and perceived actionability (𝑟= 0.54, 𝑝= .013), suggesting that en-
hancing the actionability of agentic feedback can further strengthen
user trust. These findings underscore the widespread lack of trust
in traditional hiring processes among job seekers and demonstrate
how xCUI can foster trust through transparent explanations and
actionable recommendations.
Figure 6: Box plots showing an increase in the perceived trust
of our multi-agentic AI feedback compared to conventional
methods
5.2.2
What are the factors that contribute to building trust? Quali-
tative analysis of our user study data revealed themes that help us
understand the factors contributing to building trust.
Perceived trust rooted in understanding profile-job align-
ment <18  >: The majority of participants indicated that their trust
in the AI feedback stemmed from the system’s ability to elucidate
the alignment between their job profile and the specific require-
ments of the job. Participants reported that the system’s assessment
of their suitability and the subsequent suggestions provided often
corroborated their own understanding of their qualifications in
relation to the role. This congruence between the AI’s evaluation
and their self-assessment developed a greater sense of trust in the
system’s recommendations. For example, P15 stated: “Yes, I do trust
this [xCUI] feedback. The suggestions make sense; some of them are
spot-on, as I am aware of these flaws. I will definitely try to follow these
[recommendations].” This insight further explains why we observed
a significant positive correlation between perceived actionability
and trust.


---

## Page 11

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Multiple agentic perspective helps in building trust <13  >:
Most participants expressed that feedback from both recruiter and
mentor perspectives was valuable, as it increased transparency of
the entire process by considering multiple aspects. For instance,
P13 remarked: “I do like both the mentor and recruiter feedback. The
recruiter being more critical helps me self-reflect on what I need to
improve upon. Whereas, the mentor feedback encourages me to try
out the suggestions despite knowing what [skills and experiences] I
lack.”
Holistic nature of agentic feedback <4  >: Several partici-
pants noted that feedback from human mentors and career coaches
is often perceived as generic and influenced by personal biases
or limited experiences. In contrast, they highlighted that the AI-
generated feedback from our system was more specific, context-
aware, and closely aligned with their individual profiles and job
requirements. Participants appreciated the system’s ability to pro-
vide holistic and forward-looking recommendations, describing
them as more comprehensive and pre-emptive than the typically
narrow or subjective advice offered by human advisors. For exam-
ple, P10 mentioned: “The career [human] mentors whom I have ever
reached out to, often gave generic feedback based on what they have
seen. I understand their time is often limited when assessing my CV,
but their generic feedback hasn’t helped me so far. The AI feedback
appears to be more specific, and I think it’s more useful.”
5.2.3
How could users react when they experience less trustworthy
agentic responses? While our study did not reveal any instances of
hallucinated responses (factually fabricated information), we did ob-
serve occasional short-term memory lapses within the multi-agent
system, particularly during extended interactions where it appeared
to forget previously captured details from candidate profiles or job
descriptions. Recognising that the complete elimination of all po-
tential issues, such as short-term memory loss, hallucinations, or
irrelevant responses, may be practically challenging, we sought to
understand potential user reactions to less trustworthy responses,
which are summarised in the subsequent part.
Empathy towards AI feedback <18  >: Most participants ex-
pressed empathy toward the AI system rather than disappointment
or frustration, acknowledging that they did not expect the AI to be
infallible or consistently accurate. For instance, P12 remarked: “You
know it’s AI, I don’t expect it to know everything. It’s fine if it makes
some mistakes, I still wouldn’t mind using it.” Additionally, several
participants noted that when the AI misinterpreted certain infor-
mation, they were inclined to guide or correct it through follow-up
queries, treating the interaction as a collaborative process.: “If it
[the system] fails to recognise that I’ve already mentioned a particu-
lar skill in my resume, I would explicitly point it out. Then, ask how
having that skill improves my chances of getting hired”, as stated by
P15.
Motivation towards using agentic feedback would remain
same <17  >: Most participants did not express any form of dis-
trust toward our xCUI system. Even those who were initially more
sceptical demonstrated curiosity and a willingness to engage with
the system, reflecting a baseline level of confidence in its capabili-
ties. For example, P18 mentioned: “Even if the app tells me that I have
a 100% chance of getting selected, I would not blindly trust it. I will
always trust but verify the information.” Interestingly, contrary to
recent concerns about users’ over-reliance on LLM-generated feed-
back [46, 68], the majority of our participants expressed a healthy
scepticism. They acknowledged the fallibility of AI and demon-
strated a balanced approach toward its use. As P8 explained: “I
always take AI suggestions with a pinch of salt. But it doesn’t bother
me if it is wrong; anyway, I won’t get my hopes up even if the AI says
that I am the perfect match for this role. Similarly, it’ll not make me
emotional if I get a poor score.”
Key-takeaways: Job applicants demonstrated significantly
greater trust in the xCUI compared to their prior experiences
with conventional methods, largely attributed to the system’s
transparent explanations of profile-job alignment. This trust
is likely sustained by the positive correlation we observed
between perceived trust and actionability, suggesting that
the usefulness and clarity of recommendations reinforce user
trust and confidence over time. Interestingly, participants also
expressed a degree of empathy towards the agentic system,
acknowledging its AI nature and thus not expecting absolute
error-free performance.
5.3
How do job applicants perceive the fairness
and potential biases of multi-agent AI in
hiring decisions and guidance? (RQ3)
5.3.1
Quantitative insights: Our analysis of perceived fairness scores
showed a significantly higher rating for our multi-agent xCUI com-
pared to participants’ prior experiences with conventional hiring
methods (𝑈= 16.0, 𝑝< .001). Figure 7 presents a box plot illustrat-
ing the difference in perceived fairness scores between our system
and traditional recruitment approaches. We found that fairness
scores for our system were 40% higher than those of conventional
methods. Moreover, Spearman’s correlation test revealed a sig-
nificant positive correlation between perceived fairness and trust
(𝑟= 0.52, 𝑝= .018), as well as between perceived fairness and
actionability (𝑟= 0.67, 𝑝= .001). These findings suggest that in-
creasing actionability can enhance both user trust and the overall
perception of fairness in a multi-agentic recruitment system.
Figure 7: Box plots showing an increase in the perceived
fairness of our multi-agentic AI feedback compared to con-
ventional methods


---

## Page 12

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
5.3.2
What factors contributed to the perception of our multi-agent
system feedback as fairer compared to conventional methods? The
following themes help us understand why the participants deemed
our system as fairer compared to conventional approaches.
Importance of transparency and actionability of responses
<19  >: Most participants described our xCUI system as trans-
parent, noting that it provided a clear and honest picture of their
hiring prospects. They appreciated that the feedback was construc-
tive rather than overly optimistic or vague. As P19 stated: “I liked
how the system is neutral. Mentioning the gaps is very helpful, and
yet it does so in a neutral tone, without being rude or authoritative.” In
addition, some participants actively tested the system for potential
biases by posing sensitive or hypothetical queries. For example, P9
asked: “Suppose I am a female applicant with two years of career
break due to childbirth, would that change my selection chances?”
The absence of biased or discriminatory responses in such cases
enhanced participants’ perceptions of fairness and trustworthiness.
The combination of constructive, actionable feedback and the ability
to perform ’what-if’ analyses contributed to participants viewing
the system as both fair and transparent.
Human bias is more concerning <14  >: A significant number
of participants expressed greater concern regarding potential bias
in human recruiters compared to AI systems. They suggested that
human recruiters may overlook nuanced aspects of a candidate’s
past roles and responsibilities. Consequently, due to their narrow
perspective and lack of sufficient reasoning, applicants may doubt
the fairness of the recruitment process. For example, P13 mentioned:
“Sometimes it’s hard for me to find out if I am getting rejected because
I lack something or they [recruiters] already have a candidate from
their network. So, I would say [human] recruiters are more biased
and unfair than AI”. This perspective provides insight into the
observed significant difference in perceived fairness between our
xCUI system and conventional recruitment approaches.
5.3.3
How could users react if they observe fairness issues in the
agentic responses? As previously mentioned, we did not observe
any instances of hallucinated responses. However, we did note
evidence of short-term memory loss in the agentic system. Fur-
thermore, we found no indications of biased responses based on
demographic factors. Nevertheless, when P4 attempted to probe
the system by initially uploading a job description for one role and
subsequently asking questions about a related but distinct role, the
agentic system continued to respond while referencing the initial
role, exhibiting a hesitation to fully switch context. These observa-
tions prompted further investigation into potential user reactions
upon encountering fairness issues in agentic responses.
Steer towards the fair response through follow-up prompts
without expressing any negative emotions <15  >: Consistent
with user behaviour observed in response to untrustworthy outputs,
participants indicated a tendency to guide the system towards fairer
responses through iterative follow-up prompts when encountering
potentially unfair or biased feedback. For instance, as P3 mentioned:
“I wouldn’t take it [unfair response] personally knowing its AI. I don’t
think I will be angry. Instead, I would keep on asking questions till I
get a fair answer”. Similarly, P9 mentioned: “Since its AI, it’s meant
to give you information. There is nothing to be emotional about if the
information is inaccurate. I would rely on my own judgement at the
end of the day.” These responses suggest a pragmatic user approach
to perceived unfairness in agentic feedback, characterised by a
willingness to refine the responses through continued interaction
rather than an emotional reaction for disregarding it.
Key-takeaways: Job applicants perceived our xCUI system
as significantly fairer than their prior experiences with tra-
ditional methods, attributing this to its transparent and ac-
tionable feedback. They expressed greater concern about
inherent human recruiter bias as they believed that agen-
tic systems could be designed to maintain a neutral stance.
Participants also indicated a willingness to guide the system
towards fairer responses even if they observed any form of
bias.
6
DISCUSSION
6.1
Issues Beyond Hallucination: Amnestic
Syndrome of LLM Agents
As briefly discussed, we did not observe traditional hallucinations,
i.e., instances where LLMs fabricate information based on unsup-
ported assumptions [65]. This suggests that our hallucination-
mitigation strategies, including the LLM-as-a-Judge technique, mod-
eration tools, and limiting the context to specific information, such
as candidate resumes and job descriptions, were effective. These
strategies successfully filtered unreliable outputs before presenting
the final moderator response. However, we acknowledge that some
potential for hallucination may still exist, particularly through exter-
nal web resource recommendations, which are less tightly scoped.
Surprisingly, we observed a different kind of failure: short-term
memory lapses, where the system temporarily forgot information
explicitly mentioned earlier in the same interaction (such as specific
candidate skills or job requirements). Upon reviewing conversation
logs, we found that each agent correctly extracted the relevant
information, but this knowledge was not consistently retained or
recalled across the dialogue. We refer to this phenomenon as the
amnestic syndrome of LLM agents, a term inspired by similar pat-
terns of temporary memory loss in human cognition. While prior
work has extensively studied hallucinations in LLMs [26, 65], our
findings suggest that memory failures represent a distinct class of
limitations in multi-agent or ExCUI-based systems. Although earlier
research has begun exploring memory management strategies for
LLM agents [25, 70], our work highlights the practical implications
of amnestic syndrome of LLMs particularly for the recruitment
domain. We encourage future research to investigate both the un-
derlying causes and potential design remedies for this syndrome to
ensure more reliable and coherent agentic interactions.
6.2
Reduced Risk of Over-Reliance
While prior research has raised concerns regarding potential user
over-reliance on generative AI and LLM-based applications [7, 10,
13, 29, 68], our findings suggest a comparatively lower risk of such
over-reliance within the context of our multi-agentic xCUI. This
reduced tendency toward blind trust could be attributed to two key
factors. Firstly, a significant portion of our participants appeared to
be experienced users of LLM chatbots such as ChatGPT, potentially


---

## Page 13

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
cultivating a degree of scepticism and a heightened awareness of
the inherent limitations and potential inaccuracies associated with
LLM-generated content. This pre-existing understanding aligns
with the concept of warranted trust, which is posited to be crucial in
fostering an appropriate calibration of trust and reliance among end-
users [41]. Secondly, the design of our system, which incorporates
multiple agent perspectives (i.e., recruiter, mentor, and moderator)
to provide actionable explanations, likely fostered a more balanced
pattern of engagement. This multi-faceted explanation approach
likely helped calibrate users’ trust and reliance as it provided diverse,
sometimes contrasting, viewpoints. As also noted in prior work
[34], LLM applications that serve as pre-application support tools
are less likely to cause over-reliance compared to systems that fully
automate tasks on behalf of the user.
6.3
Including Recruiter Perspective
Although our xCUI system is primarily designed to support job
applicants, we recognise the critical importance of incorporating
recruiter perspectives in the subsequent phases of our iterative, user-
centred development process. Engaging recruiters can help surface
additional design opportunities and system features that cater to
the needs of hiring teams, ultimately enhancing the overall utility
of the platform. By involving both stakeholders (applicants and re-
cruiters), we envision the system evolving into a more collaborative
tool that facilitates mutual understanding and alignment. After all,
the recruitment process should not be treated as a zero-sum game
[45], where gains for one party imply losses for the other. Instead,
fostering transparency and collaboration can create a positive-sum
outcome, where both applicants and recruiters benefit from more
informed, efficient, and equitable hiring decisions.
6.4
Steering of Multi-Agent Systems
Our study highlights the proactive role that end-users are willing
to take in steering the responses of multi-agent systems, particu-
larly when the AI-generated feedback is perceived as insufficiently
actionable, trustworthy, or fair. This reinforces the growing interest
in user-centric control over LLM agents [47, 56, 64], with ongoing
research exploring various prompting and interaction techniques
to support such steering. While prior work has largely focused on
single-agent systems, our findings suggest new opportunities for ex-
amining how users can effectively influence or guide multi-agentic
systems. In particular, future research should explore mechanisms
that allow users to selectively engage, prioritise, or reconfigure
agent roles in real-time, tailoring system behaviour to meet indi-
vidual needs and contextual demands more effectively.
6.5
Ethical Considerations for Agentic Systems
Even though participants in our study did not raise explicit concerns
regarding fairness, bias, or trust in our agentic system, our user
study primarily explored potential user reactions to problematic
responses in a research setting. In real-world deployments, users
may express reservations about being evaluated by AI agents, espe-
cially in high-stakes contexts that can impact life or livelihood [15].
Additionally, concerns around data privacy and security of user in-
formation remain paramount [15]. To promote the responsible use
of agentic systems, we advocate for the implementation of informed
consent mechanisms, ensuring users are aware of how their data
is used, stored and safeguarded. Such systems must also comply
with relevant regulatory frameworks, such as the GDPR, the EU
AI Act, and similar policies, which emphasise accountability, trans-
parency, and risk mitigation. Furthermore, while we recognise the
research value of enabling user-driven steering in agentic systems,
this functionality also opens potential vectors for misuse, including
adversarial attacks like prompt injection and jailbreak attempts
[36]. As the use of multi-agent systems becomes more prevalent,
we encourage future work to not only advance their capabilities but
also develop robust safeguards and ethical frameworks to ensure
their safe and responsible deployment.
6.6
Limitations
Before discussing the broader implications of our work across mul-
tiple domains, we would like to acknowledge the following known
limitations:
(1) Limited evaluation across diverse LLMs for agentic system design:
Our implementation of the multi-agentic system exclusively re-
lied on OpenAI’s GPT models as the underlying LLM-based rea-
soning engines. While these models have demonstrated strong
performance in various tasks, we acknowledge that different
LLMs may exhibit varying behaviours, strengths, and limita-
tions depending on the task and domain. Recent research has
increasingly emphasised the importance of carefully selecting
LLMs for specific use cases, as model choice can significantly
impact response quality, alignment, and reasoning capabilities
[1, 9, 49]. Future work should include a comparative empiri-
cal analysis of multiple LLMs to evaluate their suitability for
different agent roles within a multi-agentic architecture.
(2) Latency in multi-agent response generation: For certain queries,
we observed that the response time of our multi-agent system
extended up to a minute. Such latency may negatively affect
the user experience, particularly in real-time conversational
settings where users expect prompt responses. This delay was
often a result of some agents over-thinking on certain user
queries requiring in-depth reasoning. This syndrome can be
considered similar to the analysis paralysis syndrome in hu-
mans [59], in which over-thinking restricts from taking prompt
actions. Similar properties of LLM agents have also been noted
in prior work [14]. Future research should investigate the user
experience implications of these delayed responses from over-
thinking LLM agents, using tools such as NASA-TLX [23] or
through comprehensive qualitative evaluations.
(3) Potential presence of subjective recall bias in our quantitative
comparisons: In our study, participants were not exposed to a
standardised “conventional hiring system.” Instead, their com-
parisons were based on personal memory and prior experiences
with traditional hiring practices. As a result, our quantitative
findings may be influenced by subjective recall bias [57]. While
our qualitative findings provide rich context that supports
and explains these perception-based trends, the comparative
feedback should not be interpreted as objective performance
data. Future work could involve controlled A/B testing or ran-
domised between-subject studies to more rigorously assess the


---

## Page 14

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
perceived and actual effectiveness of multi-agent recruitment
systems at scale.
6.7
Design Implications Considering Broader
Applicability
Although our work focuses specifically on the recruitment domain,
the following design implications derived from our findings offer
broader applicability across diverse domains involving multi-agent
systems.
• User-centric design of multi-agent architectures: Our findings
emphasise the value of adopting a user-centred design approach
in developing complex multi-agent system architectures. We
advocate for involving end-users early in the design process to
collaboratively determine the number of agents, their distinct
roles and behaviours, appropriate communication protocols,
and memory management strategies. An iterative user-centred
development process ensures that the system aligns closely with
real-world user needs.
• UI elements to support actionable conversations: Findings from
our study advocate the importance of simplified user interac-
tions for having engaging and actionable conversations. We
found the importance of the quick questions and quick insights
components, especially for initiating conversations. We further
recommend implementing question chaining, either via agent-
generated follow-ups or interactive UI components to scaffold
deeper conversations (e.g., exploring how-to, why, or what-if
queries) without requiring users to manually articulate complex
follow-up questions, which can often be cognitively taxing.
• Adaptive abstraction of agentic responses: Our study highlighted
a divergence in user preferences regarding the level of detail in
agentic responses. While some participants appreciated gran-
ular explanations, others found overly detailed outputs over-
whelming and difficult to process. This variation underscores
the challenge of determining a one-size-fits-all approach to ex-
planation depth. To accommodate diverse cognitive preferences,
we recommend integrating UI controls that allow users to dy-
namically adjust the level of detail through simple visual aids,
such as icons or buttons. This feature can allow users to eas-
ily modify the level of detail in subsequent interactions with
a single action, fostering a more personalised and cognitively
accessible interaction experience.
• Inclusion and validation of situational information of end-users
for producing context-aware recommendations: As observed in
our study findings, awareness of end-users’ situational informa-
tion is crucial for generating context-aware recommendations.
For example, participants suggested incorporating information
regarding their willingness to pursue higher education, the prac-
tical feasibility of undertaking side projects, certification courses,
or even internships. Considering these personal constraints can
lead to more realistic and useful recommendations. Therefore,
we recommend proactively gathering such situational informa-
tion through a pre-questionnaire, which could be implemented
via interactive UI elements or through direct questioning by
the chatbot prior to recommendation generation. Furthermore,
drawing an analogy to moderation check tools, we suggest in-
tegrating agent tools to validate the alignment of final agentic
recommendations with the end-users’ stated situational infor-
mation.
• Integration with external platforms via RAG for enhanced contex-
tual knowledge: Some participants from our user study expressed
a need for the system to integrate with external platforms for in-
formation retrieval. We posit that in other application domains,
such as healthcare, finance, and education, accessing specific,
validated information from pre-defined sources could be even
more critical for facilitating robust context-aware conversations.
Therefore, we recommend implementing Retrieval-Augmented
Generation (RAG) pipelines [20] to establish a relevant and reli-
able contextual knowledge base derived from pertinent external
platforms such as LinkedIn, GitHub, and other personal web-
sites. Integrating this knowledge base as a tool for the LLM
agents would enable more accurate information retrieval and
the synthesis of highly context-aware responses.
• UI indicators for warranted trust and response latency in over-
thinking agents: While our study found a low risk of over-reliance
on the multi-agentic xCUI system in the recruitment domain,
this may not generalise to other high-stakes contexts such as
healthcare or finance, where users might place unwarranted
trust in AI-generated outputs. Drawing from prior research on
calibrated trust and transparency [29, 41], we recommend in-
corporating visual cues within the interface, such as warning
messages, icons, or tooltips, to proactively alert users to potential
limitations in the agents’ reasoning or coverage. Additionally,
in cases where agents require extended processing time due
to complex reasoning tasks (i.e., over-thinking), explicit latency
indicators or progress animations can help manage user expec-
tations and reduce frustration. These interface features would
support more informed and trust-calibrated interactions across
diverse usage scenarios.
7
CONCLUSION
In this work, we introduced a multi-agent conversational AI system
designed to support job applicants with transparent and actionable
feedback during the recruitment process. Through an iterative user-
centred design approach and a qualitative study involving 20 active
job seekers, we demonstrated that our system was perceived as
more trustworthy, fair, and actionable compared to conventional
hiring methods. Our findings highlight the potential of multi-agent
LLM systems in enhancing user experience, not only by offering
diverse perspectives but also by providing actionable, trustworthy
and fair feedback. Beyond the recruitment domain, we provide
broader design implications for building explainable, user-aligned
multi-agent systems across multiple application domains.
ACKNOWLEDGMENTS
Many thanks to Yizhe Zhang, Grzegorz Meller, Robin De Croon and
Maxwell Szymanski for their helpful suggestions that improved
this work. We also extend our gratitude to all the participants for
taking part in our user studies. This research was supported by the
Researcher Access Program from Open AI, Flanders AI Research
Program (FAIR) and Research Foundation–Flanders (FWO grants
G0A4923N and G067721N) [3, 8].


---

## Page 15

A Job Seeker’s Perspective on Multi-Agent Recruitment Systems for Explaining Hiring Decisions
UIST ’25, September 28 – October 1, 2025, Busan, South Korea
REFERENCES
[1] Omer Aydin, Enis Karaarslan, Fatih Safa Erenay, and Nebojsa Bacanin. 2025.
Generative AI in Academic Writing: A Comparison of DeepSeek, Qwen, ChatGPT,
Gemini, Llama, Mistral, and Gemma. arXiv:2503.04765 [cs.CY] https://arxiv.org/
abs/2503.04765
[2] Aditya Bhattacharya. 2022. Applied Machine Learning Explainability Techniques.
In Applied Machine Learning Explainability Techniques. Packt Publishing, Birm-
ingham, UK. https://www.packtpub.com/product/applied-machine-learning-
explainability-techniques/9781803246154
[3] Aditya Bhattacharya. 2024. Towards Directive Explanations: Crafting Explainable
AI Systems for Actionable Human-AI Interactions. In Extended Abstracts of the
CHI Conference on Human Factors in Computing Systems (CHI EA ’24) (Honolulu,
HI, USA) (CHI EA ’24). ACM, New York, NY, USA, 6. https://doi.org/10.1145/
3613905.3638177
[4] Aditya Bhattacharya, Jeroen Ooge, Gregor Stiglic, and Katrien Verbert. 2023.
Directive Explanations for Monitoring the Risk of Diabetes Onset: Introducing
Directive Data-Centric Explanations and Combinations to Support What-If Ex-
plorations. In Proceedings of the 28th International Conference on Intelligent User
Interfaces (Sydney, NSW, Australia) (IUI ’23). Association for Computing Machin-
ery, New York, NY, USA, 204–219. https://doi.org/10.1145/3581641.3584075
[5] Aditya Bhattacharya, Simone Stumpf, Robin De Croon, and Katrien Verbert.
2025. Explanatory Debiasing: Involving Domain Experts in the Data Generation
Process to Mitigate Representation Bias in AI Systems. In CHI Conference on
Human Factors in Computing Systems (CHI ’25) (Yokohama, Japan). ACM, New
York, NY, USA, 20. https://doi.org/10.1145/3706598.3713497
[6] Aditya Bhattacharya, Simone Stumpf, Lucija Gosak, Gregor Stiglic, and Katrien
Verbert. 2024. EXMOS: Explanatory Model Steering Through Multifaceted Expla-
nations and Data Configurations. In Proceedings of the CHI Conference on Human
Factors in Computing Systems (Honolulu, HI, USA) (CHI ’24). Association for Com-
puting Machinery, New York, NY, USA. https://doi.org/10.1145/3613904.3642106
[7] Aditya Bhattacharya, Tim Vanherwegen, and Katrien Verbert. 2025. “Show Me
How”: Benefits and Challenges of Agent-Augmented Counterfactual Explanations
for Non-Expert Users. In Proceedings of the 33rd ACM Conference on User Modeling,
Adaptation and Personalization (UMAP ’25) (New York City, NY, USA). ACM, 11
pages. https://doi.org/10.1145/3699682.3728321
[8] Aditya Bhattacharya and Katrien Verbert. 2024. "How Good Is Your Explana-
tion?": Towards a Standardised Evaluation Approach for Diverse XAI Methods
on Multiple Dimensions of Explainability. In Adjunct Proceedings of the 32nd
ACM Conference on User Modeling, Adaptation and Personalization (Cagliari, Italy)
(UMAP Adjunct ’24). Association for Computing Machinery, New York, NY, USA,
513–515. https://doi.org/10.1145/3631700.3664911
[9] Muhammad Shahrul Zaim bin Ahmad and Kazuhiro Takemoto. 2024. Large-scale
moral machine experiment on large language models. arXiv:2411.06790 [cs.CY]
https://arxiv.org/abs/2411.06790
[10] Jessica Y. Bo, Sophia Wan, and Ashton Anderson. 2025. To Rely or Not to Rely?
Evaluating Interventions for Appropriate Reliance on Large Language Models.
arXiv:2412.15584 [cs.HC] https://arxiv.org/abs/2412.15584
[11] Virginia Braun and Victoria Clarke. 2012. Thematic Analysis. In APA Handbook
of Research Methods in Psychology, Vol 2: Research Designs: Quantitative, Quali-
tative, Neuropsychological, and Biological. American Psychological Association,
Washington, DC, US, 57–71. https://doi.org/10.1037/13620-004
[12] Arthur Caetano, Kavya Verma, Atieh Taheri, Radha Kumaran, Zichen Chen,
Jiaao Chen, Tobias Höllerer, and Misha Sra. 2025. Agentic Workflows for Con-
versational Human-AI Interaction Design.
arXiv:2501.18002 [cs.HC] https:
//arxiv.org/abs/2501.18002
[13] Valerie Chen, Q. Vera Liao, Jennifer Wortman Vaughan, and Gagan Bansal. 2023.
Understanding the Role of Human Intuition on Reliance in Human-AI Decision-
Making with Explanations. arXiv:2301.07255 [cs.HC] https://arxiv.org/abs/2301.
07255
[14] Konstantina Christakopoulou, Shibl Mourad, and Maja Matarić. 2024.
Agents
Thinking
Fast
and
Slow:
A
Talker-Reasoner
Architecture.
arXiv:2410.08328 [cs.AI] https://arxiv.org/abs/2410.08328
[15] N’yoma Diamond and Soumya Banerjee. 2024. On the Ethical Considerations of
Generative Agents. arXiv:2411.19211 [cs.CY] https://arxiv.org/abs/2411.19211
[16] Adam Fourney, Gagan Bansal, Hussein Mozannar, Cheng Tan, Eduardo Salinas,
Erkang, Zhu, Friederike Niedtner, Grace Proebsting, Griffin Bassman, Jack Gerrits,
Jacob Alber, Peter Chang, Ricky Loynd, Robert West, Victor Dibia, Ahmed Awadal-
lah, Ece Kamar, Rafah Hosn, and Saleema Amershi. 2024. Magentic-One: A Gen-
eralist Multi-Agent System for Solving Complex Tasks. arXiv:2411.04468 [cs.AI]
https://arxiv.org/abs/2411.04468
[17] Arturo Fredes and Jordi Vitria. 2024.
Using LLMs for Explaining Sets of
Counterfactual Examples to Final Users.
arXiv:2408.15133 [cs.LG]
https:
//arxiv.org/abs/2408.15133
[18] A. Freed and an O’Reilly Media Company Safari. 2021. Conversational AI. Man-
ning Publications. https://books.google.be/books?id=wtKAzwEACAAJ
[19] Chengguang Gan, Qinghao Zhang, and Tatsunori Mori. 2024.
Application
of LLM Agents in Recruitment: A Novel Framework for Resume Screening.
arXiv:2401.08315 [cs.CL] https://arxiv.org/abs/2401.08315
[20] Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi
Dai, Jiawei Sun, Meng Wang, and Haofen Wang. 2024. Retrieval-Augmented
Generation for Large Language Models: A Survey. arXiv:2312.10997 [cs.CL]
https://arxiv.org/abs/2312.10997
[21] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V.
Chawla, Olaf Wiest, and Xiangliang Zhang. 2024. Large Language Model based
Multi-Agents: A Survey of Progress and Challenges. arXiv:2402.01680 [cs.CL]
https://arxiv.org/abs/2402.01680
[22] Shanshan Han, Qifan Zhang, Yuhang Yao, Weizhao Jin, Zhaozhuo Xu, and
Chaoyang He. 2024. LLM Multi-Agent Systems: Challenges and Open Prob-
lems. arXiv:2402.03578 [cs.MA] https://arxiv.org/abs/2402.03578
[23] Sandra G. Hart and Lowell E. Staveland. 1988. Development of NASA-TLX
(Task Load Index): Results of Empirical and Theoretical Research. In Human
Mental Workload, Peter A. Hancock and Najmedin Meshkati (Eds.). Advances
in Psychology, Vol. 52. North-Holland, 139–183. https://doi.org/10.1016/S0166-
4115(08)62386-9
[24] Gaole He, Gianluca Demartini, and Ujwal Gadiraju. 2025. Plan-Then-Execute:
An Empirical Study of User Trust and Team Performance When Using LLM
Agents As A Daily Assistant. In CHI Conference on Human Factors in Computing
Systems (CHI ’25) (Yokohama, Japan) (CHI ’25). ACM, New York, NY, USA, 22.
https://doi.org/10.1145/3706598.3713218
[25] Yuki Hou, Haruki Tamoto, and Homei Miyashita. 2024. "My agent understands
me better": Integrating Dynamic Human-like Memory Recall and Consolidation
in LLM-Based Agents. In Extended Abstracts of the CHI Conference on Human
Factors in Computing Systems (Honolulu, HI, USA) (CHI EA ’24). Association for
Computing Machinery, New York, NY, USA, Article 7, 7 pages. https://doi.org/
10.1145/3613905.3650839
[26] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian
Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin, and Ting
Liu. 2023. A Survey on Hallucination in Large Language Models: Principles,
Taxonomy, Challenges, and Open Questions. arXiv:2311.05232 [cs.CL] https:
//arxiv.org/abs/2311.05232
[27] Anna-Lena Hunkenschroer and Christoph Luetge. 2022. Ethics of AI-Enabled
Recruiting and Selection: A Review and Research Agenda. Journal of Business
Ethics 178 (2022), 977–1007. https://doi.org/10.1007/s10551-022-05049-6
[28] Jiun-Yin Jian, Ann Bisantz, and Colin Drury. 2000. Foundations for an Empirically
Determined Scale of Trust in Automated Systems. International Journal of Cogni-
tive Ergonomics 4 (03 2000), 53–71. https://doi.org/10.1207/S15327566IJCE0401_04
[29] Sunnie S. Y. Kim, Jennifer Wortman Vaughan, Q. Vera Liao, Tania Lombrozo, and
Olga Russakovsky. 2025. Fostering Appropriate Reliance on Large Language
Models: The Role of Explanations, Sources, and Inconsistencies. In Proceedings
of the CHI Conference on Human Factors in Computing Systems (CHI ’25). ACM,
Yokohama, Japan, 1–26. https://doi.org/10.1145/3706598.3714020
[30] Jenny Kunz and Marco Kuhlmann. 2024. Properties and Challenges of LLM-
Generated Explanations. In Proceedings of the Third Workshop on Bridging Human–
Computer Interaction and Natural Language Processing, Su Lin Blodgett, Amanda
Cercas Curry, Sunipa Dev, Michael Madaio, Ani Nenkova, Diyi Yang, and Ziang
Xiao (Eds.). Association for Computational Linguistics, Mexico City, Mexico,
13–27. https://doi.org/10.18653/v1/2024.hcinlp-1.2
[31] Andreas Köchling and Marius C. Wehner. 2020. Discriminated by an algorithm: a
systematic review of discrimination and fairness by algorithmic decision-making
in the context of HR recruitment and HR development. Business Research 13
(2020), 795–848. https://doi.org/10.1007/s40685-020-00134-w
[32] Himabindu Lakkaraju, Dylan Slack, Yuxin Chen, Chenhao Tan, and Sameer Singh.
2022. Rethinking Explainability as a Dialogue: A Practitioner’s Perspective.
arXiv:2202.01875 [cs.LG]
[33] LangChain. 2025. . LangChain. https://www.langchain.com Accessed: 2025-01-
21.
[34] Brenna Li, Ofek Gross, Noah Crampton, Mamta Kapoor, Saba Tauseef, Mohit Jain,
Khai N. Truong, and Alex Mariakakis. 2024. Beyond the Waiting Room: Patient’s
Perspectives on the Conversational Nuances of Pre-Consultation Chatbots. In
Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems
(Honolulu, HI, USA) (CHI ’24). Association for Computing Machinery, New York,
NY, USA, Article 438, 24 pages. https://doi.org/10.1145/3613904.3641913
[35] X. Li, S. Wang, S. Zeng, et al. 2024. A survey on LLM-based multi-agent systems:
workflow, infrastructure, and challenges. Vicinagearth 1, 9 (2024). https://doi.
org/10.1007/s44336-024-00009-2
[36] Yi Liu, Gelei Deng, Yuekang Li, Kailong Wang, Zihao Wang, Xiaofeng Wang,
Tianwei Zhang, Yepang Liu, Haoyu Wang, Yan Zheng, and Yang Liu. 2024. Prompt
Injection attack against LLM-integrated Applications. arXiv:2306.05499 [cs.CR]
https://arxiv.org/abs/2306.05499
[37] Jieting Luo, Thomas Studer, and Mehdi Dastani. 2023. Providing personalized
Explanations: a Conversational Approach.
arXiv:2307.11452 [cs.MA] https:
//arxiv.org/abs/2307.11452
[38] Lin Luo, Yuri Nakao, Mathieu Chollet, Hiroya Inakoshi, and Simone Stumpf.
2025. EARN Fairness: Explaining, Asking, Reviewing, and Negotiating Artificial
Intelligence Fairness Metrics Among Stakeholders. Proceedings of the ACM on


---

## Page 16

UIST ’25, September 28 – October 1, 2025, Busan, South Korea
Bhattacharya and Verbert
Human-Computer Interaction 9, 2 (April 2025), 37. https://doi.org/10.1145/3710908
[39] Marcello M. Mariani, Novin Hashemi, and Jochen Wirtz. 2023. Artificial in-
telligence empowered conversational agents: A systematic literature review
and research agenda. Journal of Business Research 161 (2023), 113838.
https:
//doi.org/10.1016/j.jbusres.2023.113838
[40] Evie McCrum-Gardner. 2008. Which is the correct statistical test to use? British
Journal of Oral and Maxillofacial Surgery 46, 1 (Jan. 2008), 38–41. https://doi.
org/10.1016/j.bjoms.2007.09.002
[41] Siddharth Mehrotra, Chadha Degachi, Oleksandra Vereschak, Catholijn M. Jonker,
and Myrthe L. Tielman. 2024. A Systematic Review on Fostering Appropriate
Trust in Human-AI Interaction: Trends, Opportunities and Challenges. ACM J.
Responsib. Comput. 1, 4, Article 26 (Nov. 2024), 45 pages. https://doi.org/10.1145/
3696449
[42] Tim Miller. 2017. Explanation in Artificial Intelligence: Insights from the Social
Sciences. https://doi.org/10.48550/ARXIV.1706.07269
[43] Yuri Nakao, Simone Stumpf, Subeida Ahmed, Aisha Naseer, and Lorenzo Strap-
pelli. 2022. Toward Involving End-users in Interactive Human-in-the-loop AI
Fairness. ACM Trans. Interact. Intell. Syst. 12, 3, Article 18 (July 2022), 30 pages.
https://doi.org/10.1145/3514258
[44] OpenAI. 2025. . OpenAI.
https://openai.com/index/openai-api/ Accessed:
2025-01-21.
[45] Oxford University Press. 2014. Zero-sum game. https://www.oxfordreference.
com/display/10.1093/acref/9780199670840.001.0001/acref-9780199670840-e-
1491 Accessed: 2025-03-29.
[46] Samir Passi and Mihaela Vorvoreanu. 2022.
Overreliance on AI: Literature
Review.
Microsoft Technical Report MSR-TR-2022-12. Microsoft Corpora-
tion. https://www.microsoft.com/en-us/research/uploads/prod/2022/06/Aether-
Overreliance-on-AI-Review-Final-6.21.22.pdf
[47] Nate Rahn, Pierluca D’Oro, and Marc G. Bellemare. 2024. Controlling Large Lan-
guage Model Agents with Entropic Activation Steering. arXiv:2406.00244 [cs.CL]
https://arxiv.org/abs/2406.00244
[48] Frank Ritter, Gordon Baxter, and Elizabeth Churchill. 2014. User-Centered Systems
Design: A Brief History. Springer, 33–54.
https://doi.org/10.1007/978-1-4471-
5134-0_2
[49] Seyed Amir Ahmad Safavi-Naini, Shuhaib Ali, Omer Shahab, Zahra Shahho-
seini, Thomas Savage, Sara Rafiee, Jamil S Samaan, Reem Al Shabeeb, Farah
Ladak, Jamie O Yang, Juan Echavarria, Sumbal Babar, Aasma Shaukat, Samuel
Margolis, Nicholas P Tatonetti, Girish Nadkarni, Bara El Kurdi, and Ali Soroush.
2024. Vision-Language and Large Language Model Performance in Gastroen-
terology: GPT, Claude, Llama, Phi, Mistral, Gemma, and Quantized Models.
arXiv:2409.00084 [cs.CL] https://arxiv.org/abs/2409.00084
[50] Christian A. Schiller. 2024. The Human Factor in Detecting Errors of Large Lan-
guage Models: A Systematic Literature Review and Future Research Directions.
arXiv:2403.09743 [cs.CL] https://arxiv.org/abs/2403.09743
[51] Ashish Sharma, Sudha Rao, Chris Brockett, Akanksha Malhotra, Nebojsa Jojic, and
Bill Dolan. 2024. Investigating Agency of LLMs in Human-AI Collaboration Tasks.
In Proceedings of the 18th Conference of the European Chapter of the Association for
Computational Linguistics (Volume 1: Long Papers), Yvette Graham and Matthew
Purver (Eds.). Association for Computational Linguistics, St. Julian’s, Malta, 1968–
1987. https://aclanthology.org/2024.eacl-long.119/
[52] Hua Shen, Chieh-Yang Huang, Tongshuang Wu, and Ting-Hao ’Kenneth’ Huang.
2023. ConvXAI: Delivering Heterogeneous AI Explanations via Conversations to
Support Human-AI Scientific Writing. arXiv:2305.09770 [cs.HC] https://arxiv.
org/abs/2305.09770
[53] S. J. Shoemaker, M. S. Wolf, and C. Brach. 2014. Development of the patient educa-
tion materials assessment tool (PEMAT): a new measure of understandability and
actionability for print and audiovisual patient information. Patient Education and
Counseling 96, 3 (Sep 2014), 395–403. https://doi.org/10.1016/j.pec.2014.05.027
[54] Ronal Singh, Tim Miller, Liz Sonenberg, Eduardo Velloso, Frank Vetere, Piers
Howe, and Paul Dourish. 2024. An Actionability Assessment Tool for Explainable
AI. arXiv:2407.09516 [cs.HC] https://arxiv.org/abs/2407.09516
[55] Dylan Slack, Satyapriya Krishna, Himabindu Lakkaraju, and Sameer Singh.
2023. Explaining machine learning models with interactive natural language
conversations using TalkToModel. Nature Machine Intelligence (27 Jul 2023).
https://doi.org/10.1038/s42256-023-00692-8
[56] Bingqing Song, Boran Han, Shuai Zhang, Hao Wang, Haoyang Fang, Bonan
Min, Yuyang Wang, and Mingyi Hong. 2025. Effectively Steer LLM To Follow
Preference via Building Confident Directions. https://doi.org/10.48550/arXiv.
2503.02989
[57] Arthur A. Stone and Saul Shiffman. 2002. Capturing momentary, self-report data:
A proposal for reporting guidelines. Annals of Behavioral Medicine 24, 3 (2002),
236–243. https://doi.org/10.1207/S15324796ABM2403_09
[58] Streamlit. 2025. . Streamlit. https://streamlit.io Accessed: 2025-01-21.
[59] Bonnie Talbert. 2017. Overthinking and Other Minds: The Analysis Paralysis.
Social Epistemology 31 (07 2017), 1–12. https://doi.org/10.1080/02691728.2017.
1346933
[60] Lindia Tjuatja, Valerie Chen, Tongshuang Wu, Ameet Talwalkwar, and Graham
Neubig. 2024. Do LLMs Exhibit Human-like Response Biases? A Case Study in
Survey Design. Transactions of the Association for Computational Linguistics 12
(2024), 1011–1026. https://doi.org/10.1162/tacl_a_00685
[61] Khanh-Tung Tran, Dung Dao, Minh-Duong Nguyen, Quoc-Viet Pham, Barry
O’Sullivan, and Hoang D. Nguyen. 2025. Multi-Agent Collaboration Mechanisms:
A Survey of LLMs. arXiv:2501.06322 [cs.AI] https://arxiv.org/abs/2501.06322
[62] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei
Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. Chain-of-thought prompting
elicits reasoning in large language models. In Proceedings of the 36th International
Conference on Neural Information Processing Systems (New Orleans, LA, USA)
(NIPS ’22). Curran Associates Inc., Red Hook, NY, USA, Article 1800, 14 pages.
[63] Justin D. Weisz, Jessica He, Michael Muller, Gabriela Hoefer, Rachel Miles, and
Werner Geyer. 2024. Design Principles for Generative AI Applications. In Pro-
ceedings of the CHI Conference on Human Factors in Computing Systems. ACM,
New York, NY, USA, 1–22. https://doi.org/10.1145/3613904.3642466
[64] Liwenhan Xie, Chengbo Zheng, Haijun Xia, Huamin Qu, and Chen Zhu-Tian. 2024.
WaitGPT: Monitoring and Steering Conversational LLM Agent in Data Analysis
with On-the-Fly Code Visualization. https://doi.org/10.48550/arXiv.2408.01703
[65] Ziwei Xu, Sanjay Jain, and Mohan Kankanhalli. 2024. Hallucination is Inevitable:
An Innate Limitation of Large Language Models.
arXiv:2401.11817 [cs.CL]
https://arxiv.org/abs/2401.11817
[66] Xi Yang and Marco Aurisicchio. 2021. Designing Conversational Agents: A Self-
Determination Theory Approach. In Proceedings of the 2021 CHI Conference on
Human Factors in Computing Systems (Yokohama, Japan) (CHI ’21). Association
for Computing Machinery, New York, NY, USA, Article 256, 16 pages.
https:
//doi.org/10.1145/3411764.3445445
[67] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language
Models. In International Conference on Learning Representations (ICLR).
[68] Cheng Zhai, Syamsul Wibowo, and L.D. Li. 2024. The effects of over-reliance on
AI dialogue systems on students’ cognitive abilities: a systematic review. Smart
Learning Environments 11 (2024). https://doi.org/10.1186/s40561-024-00316-7
[69] Tong Zhang, X. Jessie Yang, and Boyang Li. 2024. May I Ask a Follow-up Question?
Understanding the Benefits of Conversations in Neural Network Explainability.
arXiv:2309.13965 [cs.HC] https://arxiv.org/abs/2309.13965
[70] Zeyu Zhang, Xiaohe Bo, Chen Ma, Rui Li, Xu Chen, Quanyu Dai, Jieming Zhu,
Zhenhua Dong, and Ji-Rong Wen. 2024. A Survey on the Memory Mechanism of
Large Language Model based Agents. arXiv:2404.13501 [cs.AI] https://arxiv.org/
abs/2404.13501
[71] Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu,
Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang,
Joseph E. Gonzalez, and Ion Stoica. 2023. Judging LLM-as-a-Judge with MT-Bench
and Chatbot Arena. arXiv:2306.05685 [cs.CL] https://arxiv.org/abs/2306.05685
