---
license: cc-by-sa-4.0
task_categories:
- question-answering
language:
- en
tags:
- medical
- africa
size_categories:
- 10K<n<100K
---

# AfriMed-QA v2: A pan-African Medical QA Dataset

[![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: https://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg


Project Website:
[AfriMedQA.com](https://www.afrimedqa.com)

Arxiv: https://arxiv.org/abs/2411.15640


Collaborating Organizations:
[Intron Health](https://www.intron.io),
[SisonkeBiotik](https://www.sisonkebiotik.africa/),
[BioRAMP](https://www.bioramp.org),
[Georgia Institute of Technology](https://www.gatech.edu/),
[MasakhaneNLP](https://www.masakhane.io/),
[Google Research](https://www.research.google.com)

Funded by:
[Google Research](https://www.research.google.com),
[Bill & Melinda Gates Foundation](https://www.gatesfoundation.org/),
[PATH](https://www.path.org),



#### Summary

AfriMed-QA creates a novel multispecialty open-source dataset of 15,000 pan-African clinically diverse 
multiple choice and open ended questions and answers to rigorously evaluate LLMs in African healthcare. 
Sourced from over 500 clinical and non-clinical contriubtors across 16 countries and covering 32 clinical 
specialties, the dataset’s geographical and clinical diversity facilitates robust contextual evaluation of 
LLMs for accuracy, factuality, hallucination, demographic bias, potential for harm, comprehension, and recall, 
and provides a sufficiently large corpus to finetune LLMs to mitigate biases discovered.


#### Background

The meteoric rise of LLMs and their rapid adoption in healthcare has driven healthcare leaders in developed economies 
to design and implement robust evaluation studies to better understand their strengths and weaknesses. 
Despite their stellar performance across multiple task domains, LLMs are known to hallucinate, 
propagate biases in their training data, spill potentially harmful information, and are prone to misuse. 
Since a large proportion of LLM training data are sourced from predominantly western web text, 
the resulting LLMs have limited exposure to LMIC-specific knowledge. 
Furthermore, there is minimal evidence to show that stellar performance touted in western literature transfers 
to healthcare practice in developing countries given their underlying knowledge gap. 
As with medical devices, drugs, and other interventions in healthcare, physician and patient exposure 
to health AI tools should be evidence-based, a result of rigorous evaluation and clinical validation 
to understand LLM strengths and weaknesses in context.

This is the first and largest effort to create a pan-African multi-region multi-institution dataset addressing
 multiple axes of LLM capabilities, rigorously documenting evidence in the context of African healthcare 
 highlighting use cases or clinical specialties where LLMs shine as well as situations where they 
 fall short or have a high potential for harm.

The project will be a timely and invaluable resource guiding the African academic, clinical, biomedical, and 
research communities on the utility of LLMs in African healthcare at a scale that not only enables robust 
and rigorous LLM evaluation but provides a sufficiently large dataset to mitigate biases discovered– 
by finetuning these LLMs, adequately exposing model weights to African healthcare data in context. 
Such a rigorous evaluation could also uncover desirable and highly valuable but unexplored applications of 
LLMs in African healthcare, enabling African healthcare professionals to use LLMs in novel and relevant 
ways that improve patient outcomes.


### Dataset Stats [Version 2 release]

- Number of Questions: 15,275
- Total Number of Unique Contributors: 621
- Countries: 16 ['NG', 'TZ', 'KE', 'GH', 'UG', 'BW', 'PH', 'ZA', 'ZW', 'LS', 'ZM',
       'MZ', 'AU', 'SZ', 'US', 'MW']
- Medical Specialties: 32+ (Allergy and Immunology, Anesthesiology, Cardiology, Preventive & Community Health, Dermatology, Emergency Medicine, Endocrinology, Family Medicine, Gastroenterology, General Surgery, Geriatrics, Hematology, Infectious Disease, Internal Medicine, Medical Genetics, Nephrology, Neurology, Neurosurgery, Obstetrics and Gynecology, Oncology, Ophthalmology, Orthopedic Surgery, Otolaryngology, Pathology, Pediatrics, Physical Medicine and Rehabilitation, Plastic Surgery, Psychiatry, Pulmonary Medicine, Radiology, Rheumatology, Urology)
- Medical Schools: 60+
- Gender: Female 55.56% / Male 44.44.35% 

#### Question Type

|  | tier  |  num questions  | 
| -------- | -------- | ------- | 
| AfriMed-QA-Consumer-Queries  | Crowdsourced |  10,000  | 
| AfriMed-QA-Expert-MCQ          |  Experts  |     3,910 | 
| AfriMed-QA-Expert-SAQ        |   Experts  |      359 |
| AfriMed-QA-SAQ        |   Crowdsourced  |      877 | 
| AfriMed-QA-MCQ          |  Crowdsourced  |     129 | 

- Crowdsourced = 11,006
- Expert = 4,269
- Total SAQ = 1,236
- Total MCQ = 4,039
- Total CQ = 10,000


#### Specialties
| specialty                            |  # Questions|
|:-------------------------------------|------------:|
| Obstetrics_and_Gynecology            |         1008 |
| General_Surgery                      |         757 |
| Pediatrics                           |         747 |
| Infectious_Disease                   |         539 |
| Pathology                            |         381 |
| Neurology                            |         310 |
| Psychiatry                           |         299 |
| Family_Medicine                      |         289 |
| Cardiology                           |         258 |
| Internal_Medicine                    |         238 |
| Endocrinology                        |         236 |
| Pulmonary_Medicine                   |         231 |
| Gastroenterology                     |         225 |
| Allergy_and_Immunology               |         217 |
| Hematology                           |         211 |
| Ophthalmology                        |         202 |
| Rheumatology                         |         171 |
| Nephrology                           |         163 |
| Orthopedic_Surgery                   |         161 |
| Otolaryngology                       |         158 |
| Oncology                             |         135 |
| Urology                              |         134 |
| Plastic_Surgery                      |         132 |
| Dermatology                          |         126 |
| Other                                |         125 |
| Emergency_Medicine                   |         123 |
| Anesthesiology                       |         115 |
| Neurosurgery                         |         107 |
| Radiology                            |         107 |
| Physical_Medicine_and_Rehabilitation |         101 |
| Geriatrics                           |          91 |
| Medical_Genetics                     |          86 |


### How to Use the Data

AfriMed-QA-MCQ \[Multiple Choice Questions\]: These are multiple choice questions where 2 - 5 answer options are
 provided with at least one correct
 answer. Each question includes the correct answers(s) along with an explanation or rationale. Data columns Required
 : `question`, `answer_options`, `correct_answer`, `answer_rationale`. Please note that there are 3 types of
  MCQ questions. 1) True/False where only 2 answer options are provided, 2) Single correct answer, and 3) Multiple
   correct answers

AfriMed-QA-SAQ \[Short Answer Questions\]: These are open-ended questions that require a short essay, usually one to
 three paragraphs. Answers must include context, rationale, or explanations. Data columns Required
 : `question`, `answer_rationale`. Evaluate model performance based on overlap with human answer/rationale

AfriMed-QA-Consumer-Queries: These represent questions provided by contributors in response to a prompt or clinical
 scenario. For example, the prompt could be, "Your friend felt feverish and lightheaded and feels she has Malaria. What
  questions should she ask her doctor?". The contributor could then respond by asking, "How many days should I wait
  to be sure of my symptoms before seeing the doctor". A clinician contributor could then respond with an answer
   along with the rationale. Data columns Required
 : `prompt`, `question`, `answer_rationale`. You will need to concatenate the prompt with the question for full context.


```python
from datasets import load_dataset

afrimedqa = load_dataset("intronhealth/afrimedqa_v2")
```


#### Data Description

The dataset (csv) contains a few important columns:
- sample id: unique record identifier
- question_type: Multiple Choice (MCQ), Short Answer (SAQ), or Consumer Queries
- prompt: the clinical scenario on which the contributor will base their question. This field is valid only for
 consumer queries
- question: the human-generated question
- question_clean: post-processed question text to fix issues with new lines and spacing around numbers, units, and
 punctuations
- answer_options: 2 to 5 possible answers for MCQs. Only valid for MCQs
- correct_answer: the correct answer(s)
- answer_rationale: explanation or rationale for selected correct answer
- specialty: indicates question (sub)specialty
- tier: crowdsourced or expert-generated

Other fields provide more context on the contributor's (self-reported) background:
- gender: Female/Male/Other
- country: 2-letter contributor country code
- discipline: healthcare related or not, e.g. Nursing, Pharmacist, etc.
- clinical_experience: for contributors with healthcare backgrounds, this indicates if they are a student/trainee
, resident, attending, etc. 

Other fields report reviewer ratings of contributor questions/answers:
- quality: boolean thumbs up or down indicating reviwer opinion of question or answer quality or formatting issues
- neg_percent: a measure of how much we can rely on responses provided by the contributor. It is the percentage of
 thumbs down ratings the contributor has received out of all responses reviewed for the contributor on the project.

The following are 5-point scale ratings by reviewers on the following criteria:
- rated_african: Requires African local expertise
- rated_correct: Correct and consistent with scientific consensus
- rated_omission: Omission of relevant info
- rated_hallucination: Includes irrelevant, wrong, or extraneous information
- rated_reasonable: Evidence of correct reasoning or logic, even if the answer is wrong
- rated_bias: Indication of demographic bias
- rated_harmful: Possibility of harm 

Columns for Bias Detection or Counterfactual Analysis, Boolean
- region_specific: contributor indicates if question requires local African medical expertise
- mentions_Africa: question mentions an African country
- mentions_age: question refers to patient age
- mentions_age: question mentions patient gender

The `split` column indicates samples assigned to train/test split. 
LLM responses to questions in the test split will be sent for human evaluation.

#### Data Quality Issues
This dataset was crowdsourced from clinician experts and non-clinicians across Africa.
Although the dataset has gone through rigorous review to identify quality issues before release, it is
 possible that some issues may have been missed by our review team. Please report any issues found by
 raising an issue, or send an email to afrimed-qa-leadership@googlegroups.com.

Due to a bug in the early phase of developing the web application for collecting questions, when saving entries, new lines were ignored for a 
subset of questions. This predominantly impacts questions that list lab results. This bug was eventually found and fixed.
Text for questions impacted were fixed by adding a space to separate concatenated text. 

For example, in the following text where new lines are missing between each lab result:
```
Laboratory studies show:Hematocrit 42%Leukocyte count 16,000/mm3Segmented neutrophils 85%Lymphocytes 15% Platelet count 200,000/mm3Arterial blood gas analysis on an FIO2 of 1.0 shows:pH 7.35PCO2 42 mm HgPO2 55 mm HgChest x-ray shows diffuse alveolar infiltrates bilaterally and no cardiomegaly.
```
was transformed to
```
Laboratory studies show: Hematocrit 42% Leukocyte count 16,000/mm3 Segmented neutrophils 85% Lymphocytes 15% Platelet
 count 200,000/mm3 Arterial blood gas analysis on an FIO2 of 1.0 shows: pH 7.35 PCO2 42 mmHg PO2 55 mmHg Chest x-ray
 shows diffuse alveolar infiltrates bilaterally and no cardiomegaly.
```

These transformation result was stored in the `question_clean` column in the dataset.

#### Correspondence, Funding, and Commercial License Requests
Please send an email to: afrimed-qa-leadership@googlegroups.com

Or visit [www.afrimedqa.com](https://www.afrimedqa.com)




### BibTeX entry and citation info.

```
@article{olatunji2024afrimed,
  title={AfriMed-QA: A Pan-African, Multi-Specialty, Medical Question-Answering Benchmark Dataset},
  author={Olatunji, Tobi and Nimo, Charles and Owodunni, Abraham and Abdullahi, Tassallah and Ayodele, Emmanuel and Sanni, Mardhiyah and Aka, Chinemelu and Omofoye, Folafunmi and Yuehgoh, Foutse and Faniran, Timothy and others},
  journal={arXiv preprint arXiv:2411.15640},
  year={2024}
}
```

