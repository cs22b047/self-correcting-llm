from transformers import pipeline

# Load model
llm = pipeline("text2text-generation", model="google/flan-t5-base", max_length=512)

# Prompts
GENERATOR_PROMPT = "You are a legal assistant. Explain the following legal clause in simple, plain English:\nClause: {clause}"
CRITIC_PROMPT = (
    "You are a legal reviewer. Review the following explanation of a legal clause.\n\n"
    "Clause: {clause}\n\n"
    "Explanation: {explanation}\n\n"
    "Evaluate for: factual accuracy, clarity, completeness, and legal precision.\n\n"
    "Your output format:\n\n[Critique]\n...\n\n[Suggested Correction]\n..."
)
REWRITE_PROMPT = (
    "You previously explained the clause:\n{clause}\n\n"
    "Your explanation was:\n{explanation}\n\n"
    "A reviewer suggested improvements:\n{critique}\n\n"
    "Based on this feedback, write an improved explanation."
)

def call_flan(prompt: str) -> str:
    result = llm(prompt)
    return result[0]["generated_text"].strip()

def generate_explanation(clause: str) -> str:
    return call_flan(GENERATOR_PROMPT.format(clause=clause))

def generate_critique(clause: str, explanation: str) -> str:
    return call_flan(CRITIC_PROMPT.format(clause=clause, explanation=explanation))

def rewrite_explanation(clause: str, explanation: str, critique: str) -> str:
    return call_flan(REWRITE_PROMPT.format(clause=clause, explanation=explanation, critique=critique))