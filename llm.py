from transformers import pipeline

# Load model
llm = pipeline("text2text-generation", model="google/flan-t5-base", max_length=512)

# Prompts
# GENERATOR_PROMPT = "You are a legal assistant. Explain the following legal clause in simple, plain English:\nClause: {clause}"
# CRITIC_PROMPT = (
#     "You are a legal reviewer. Review the following explanation of a legal clause.\n\n"
#     "Clause: {clause}\n\n"
#     "Explanation: {explanation}\n\n"
#     "Evaluate for: factual accuracy, clarity, completeness, and legal precision.\n\n"
#     "Output Corrected Explanation"
# )
REWRITE_PROMPT = (
    "You previously explained the clause:\n{clause}\n\n"
    "Your explanation was:\n{explanation}\n\n"
    "A reviewer suggested improvements:\n{critique}\n\n"
    "Based on this feedback, write an improved explanation."
)
GENERATOR_PROMPT = (
    "You are a legal assistant. Your task is to explain legal clauses in plain, everyday English. "
    "Here is how you should do it:\n\n"
    "Example:\n"
    "Clause: The employee shall not disclose confidential information to third parties.\n"
    "Plain English: The employee must not share private company info with people outside the company.\n\n"
    "Now do the same for this clause:\n\n"
    "Clause: {clause}\n"
    "Plain English:"
)
CRITIC_PROMPT = (
    "You are a legal reviewer. The following explanation is too close to the original legal clause. "
    "Your task is to rewrite it in clearer, more understandable language.\n\n"
    "Clause:\n{clause}\n\n"
    "Current Explanation:\n{explanation}\n\n"
    "Improved Plain English Explanation:"
)



def call_flan(prompt: str) -> str:
    result = llm(prompt)
    print(result)
    return result[0]["generated_text"].strip()

def generate_explanation(clause: str) -> str:
    return call_flan(GENERATOR_PROMPT.format(clause=clause))

def generate_critique(clause: str, explanation: str) -> str:
    return call_flan(CRITIC_PROMPT.format(clause=clause, explanation=explanation))

def rewrite_explanation(clause: str, explanation: str, critique: str) -> str:
    return call_flan(REWRITE_PROMPT.format(clause=clause, explanation=explanation, critique=critique))