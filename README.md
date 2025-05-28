# Self-Correcting LLM System

## Project Setup Instructions

1. clone the repo

```
git clone https://github.com/cs22b047/self-correcting-llm.git
cd self-correcting-llm
```
2. Install dependencies

```
pip install -r requirements.txt
```

3. Start the web server

```
python app.py
```

## Use Case Chosen

**Legal Clause Explanation**  
I focused on interpreting complex legal clauses into plain English and ensuring the explanation is both correct and clear through a self-correcting LLM pipeline.


## System Architecture & Prompt Strategy

### Pipeline Structure

1. **Input:** Legal Clause
2. **Stage 1 – Generator (LLM-1):**
   - Role: Legal assistant
   - Task: Explain the clause in plain English
3. **Stage 2 – Critic (LLM-2):**
   - Role: Legal reviewer
   - Task: Identify inaccuracies or ambiguities in the explanation
4. **Stage 3 – Rewriter:**
   - Applies suggested corrections for improved output

### Prompt Design

#### Generation Prompt (LLM-1)

> You are a legal assistant. Explain the following legal clause in simple, plain English:
>
> Clause: "{{LEGAL_CLAUSE}}"

#### Critique Prompt (LLM-2)

> You are a legal reviewer. Review the following explanation of a legal clause.
>
> Clause: "{{LEGAL_CLAUSE}}"
>
> Explanation: "{{LLM1_OUTPUT}}"
>
> Evaluate for: factual accuracy, clarity, completeness, and legal precision.
>
> Your output format:
>
> ```
> [Critique]
> ...
> [Suggested Correction]
> ...
> ```

#### Feedback Loop Prompt

> You previously explained the clause:
> "{{LEGAL_CLAUSE}}"
>
> Your explanation was:
> "{{LLM1_OUTPUT}}"
>
> A reviewer suggested improvements:
> "{{CRITIQUE}}"
>
> Based on this feedback, write an improved explanation.


## Error Types: What It Can and Can’t Catch

### Can Catch:
- Misinterpretation of legal terminology
- Over-simplification of important legal concepts
- Ambiguities or lack of clarity
- Incomplete explanations

### Cannot Catch:
- Errors in the original clause itself
- Highly domain-specific legal subtleties requiring expert judgment
- Hallucinated corrections from the critic model


## Test Runs
| **#** | **Legal Clause** | **Initial Explanation** | **Self-Corrected Explanation** | **User-Suggested Correction** | **Final Explanation (Post User Feedback)** |
|------:|------------------|--------------------------|-------------------------------|-------------------------------|---------------------------------------------|
| 1 | The lessee shall not sublet the premises without the prior written consent of the lessor. |  The tenant cannot allow another person to live in or use the rental property unless they first get written permission from the landlord. | The tenant cannot rent the property to someone else unless the landlord agrees in writing. The tenant cannot allow another person to live in or use the rental property unless they first get written permission from the landlord. | Add a note that subletting without consent may violate the lease terms. | The tenant is not allowed to let someone else use the property unless they have written permission from the landlord; doing so without consent could break the lease agreement. |
| 2 | This agreement shall be governed by the laws of the State of California. | The rules of California will be used to handle this agreement. | This agreement will follow and be interpreted under the laws of the State of California. | Explain what "governed by" means legally. | This agreement must follow the legal system of California, meaning any legal issues will be resolved under California law. |
| 3 | The party in breach shall indemnify and hold harmless the non-breaching party from all liabilities arising therefrom. | The person who breaks the agreement must protect the other person from any responsibility that comes from it. | If one party breaks the agreement, they must cover any costs or legal responsibilities the other party faces because of it. | Clarify “liabilities” and provide an example. | If someone breaks the agreement, they must pay for any costs or legal troubles the other person faces, such as lawsuits or fines. |
| 4 | Any disputes shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association. | All arguments will be settled using arbitration under AAA rules. | Any legal disputes will be settled by binding arbitration, where a neutral third party makes a final decision, based on AAA rules. | Mention that court appeals are not possible in binding arbitration. | Disputes will be settled by binding arbitration, meaning a third party decides the outcome and the decision cannot be appealed in court. |
| 5 | Time is of the essence in the performance of each party’s obligations. | Everyone must do their part on time. | It is crucial that each party meets deadlines and timing requirements, as delays may breach the contract. | Add consequences of missing deadlines. | Each party must meet all deadlines exactly; if not, it could lead to legal consequences like a breach of contract or termination. |

#### Edge cases tested for:
- Legally Ambiguous Clauses
- Clause with Legal Jargon and Embedded References
- Double Negatives or Unusual Legal Phrasing

## Evaluation

### Accuracy
I compared the initial explanation generated by the LLM with the self-corrected explanation to assess:

- Whether factual errors were resolved
- Whether key legal terms were preserved or clarified
- Whether clarity improved without loss of legal meaning

Across 5 test runs, the self-corrected output improved the initial response in 4/5 cases.

###  Overcorrection

In this system, overcorrection occured when the model hallucinated critique content. 

Because flan-t5-base is not domain-specific, some corrections slightly altered legal phrasing without introducing factual errors.

The feedback loop helped reduce this effect to a certain level.

## Code Implementation

### Tech stack used

Model: google/flan-t5-base via transformers

Pipeline type: text2text-generation

Environment: CPU-based local execution (works without API keys)

Language: Python 3.10

### Reasoning for model selection, limitations, and alternate options

#### 1. Reasoning:

flan-t5 is a model that is trained on a diverse set of instructions, making it effective for tasks like explanation, summarization, and critique.

flan-t5 is relatively small (~250M parameters) and is easy to run on CPUs without requiring GPUs or cloud services.

Unlike OpenAI's APIs, google's flan-t5 is open source. So, using it here, in the context of an assesment, makes sense for me.

#### 2. Limitations

flan-t5 is not trained specifically on legal text. So, its interpretations may lack domain-specific precision.

Limited context window makes it unsuitable for long or multi-clause legal texts.

Runs slowly on CPU for longer prompts or multi-step pipelines, making it a bad choice in a production setting.

#### 3. Alternate options

LexLM : It is a legal domain fine-tuned version of LLaMA. Trained on US case law, contracts, statutes. And is also open-source!

Spellbook : GPT-based assistant for contract drafting and review. Not open-source.


## Web Interfce

I have also implemented a basic web interface that uses a flask backend to run the above LLM logic.

#### Features:

- Chat style interaction
- Step by step output display
- Real-Time feedback loop
- Option to start over with a new clause

![Screenshot from 2025-05-27 20-56-33](https://github.com/user-attachments/assets/94fd60fd-e110-446e-aa40-a64a52360474)
