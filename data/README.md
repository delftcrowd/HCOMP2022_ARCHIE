***Description of the data in this dataset***
The dataset consists of generated analogies and expert evaluation of generated analogies: 

Analogies are collected from the Prolific Platform. The analogies are stored as CSV.
- generated_analogies.csv:
  - `participant_id`, anonymized participant id used in our data collection 
  - `task_id`, task ID. It includes two topics calorie prediction (T001, T002, T006) and room prediction (T008_2, T009_1, T010_2)
  - `concept`, the main concept that appeared in each task
  - `label`, ground truth label associated with each task
  - `analogy`, generated analogy-based explanation

The expert conducted a structured evaluation for analogy-based explanations. 
There is substantial overlap between the five experts (E1, E2, E3, E4, E5).

These files contain the following columns:
- `Analogy_evaluation_expert - {expert ID}.csv`
  - `participant_id`, anonymized participant id used in our data collection 
  - `task_id`, task ID. It includes two topics calorie prediction (T001, T002, T006) and room prediction (T008_2, T009_1, T010_2)
  - `concept`, the main concept that appeared in each task
  - `label`, ground truth label associated with each task
  - `analogy`, generated analogy-based explanation
  - `valid`, whether this analogy can be used to explain the model prediction. [Yes | No]
  - `Syntactic correctness`: Whether the analogy sentence is syntactically correct?  [Yes | No]
  - `Factual Correctness`: Whether it describes a fact about real world? Can we switch it to make it factual? (switch concept A and concept B in template) [Yes | No]
  - `Misunderstanding`: whether the generated analogy can cause misunderstanding. [Yes w/o switch | Yes & switch | No]
  - `structural correspondence`: How well can you align the properties of the explanation concepts to the properties of the concepts in the target sentence? 5-point Likert scale
  - `Relational similarity`: How similar do you perceive the relationship between concepts in the explanation and the relationship between concepts in the target sentence? 5-point Likert scale
  - `Familiarity`: How familiar are you with the concepts in the explanation? 5-point Likert scale
  - `Helpfulness`: How helpful is this explanation for you to understand the target sentence? 5-point Likert scale
  - `Transferability`: How well can the explanation be used in other contexts? 5-point Likert scale
  - `Simplicity`: Do you think the explanation is simple enough for others to understand? 5-point Likert scale
  - `Domain`: The domain of generated analogies.
  - `Relation Type`: The relation reflected in the generated analogies.

More details about the annotation manual can be found at [here](https://github.com/delftcrowd/HCOMP2022_ARCHIE/tree/main/annotation_manual)
