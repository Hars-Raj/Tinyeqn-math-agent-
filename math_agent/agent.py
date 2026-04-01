from typing import Dict, Any
from google.adk.agents.sequential_agent import SequentialAgent
from google.adk.agents.llm_agent import LlmAgent
import json
from pathlib import Path


parser_agent = LlmAgent(
    name="Parser",
    model="gemini-2.5-flash",
    instruction="""
    You are a parser. Given a math question and student answer, parse it into a structured format.
    Divide each step of the student's answer into a list of strings.
    Output JSON:
    {
      "question": str,
      "answer": list[str],
    }
    """
)


# 1. Load the files FIRST (outside the agent)
def load_syllabus_knowledge():
    # Use Path(__file__).parent to ensure it runs correctly from any working directory
    data_dir = Path(__file__).parent / "data"
    syllabus_path = data_dir / "moe_math_syllabus.json"
    guardrails_path = data_dir / "moe_math_guardrails.json"
    
    with open(syllabus_path, encoding="utf-8") as f:
        syllabus = json.load(f)
    with open(guardrails_path, encoding="utf-8") as f:
        guardrails = json.load(f)
    
    return syllabus, guardrails

# Load once
syllabus_kb, guardrails = load_syllabus_knowledge()

# 2. Now define the agent with clean f-string
question_level_agent = LlmAgent(
    name="QuestionLevel",
    model="gemini-2.5-flash",
    instruction=f"""
    You are an experienced MOE Singapore Math Leveling Agent (Primary 1-6 and Secondary 1-4).

    OFFICIAL SYLLABUS KNOWLEDGE BASE:
    {json.dumps(syllabus_kb, indent=2)}

    HIGH-RISK GUARDRAILS AND VALIDATION RULES:
    {json.dumps(guardrails, indent=2)}

    Follow this exact multi-stage teacher chain-of-thought when leveling any question:

    1. Topic & Skill Extraction
    2. Syllabus Mapping (use the knowledge base above)
    3. Intended Method Check
    4. Minimum Level Calculation
    5. Bidirectional Validation (use the guardrails)

    If the student's method is provided:
    - Check if it is valid as a solution (like using Algebra for a model question).
    - If valid → set "validity": "Valid" and use the student's preferred method.
    - If invalid or not provided → set "validity": "Invalid" and recommend the most suitable method for that level.

    Output **only** valid JSON (no extra text):
    {{
      "level": "Primary 5" or "Secondary 2" etc.,
      "method": "short description of method",
      "validity": "Valid" or "Invalid"
    }}
"""
)

math_solver_agent = LlmAgent(
    name="MathSolver",
    model="gemini-2.5-flash",
    instruction="""
    You are a math problem solver. Given a math question, provide the correct final answer and a step-by-step Explanation.

    1. Read the question carefully and identify what is being asked.
    2. Solve the problem step-by-step, showing all work and reasoning using the method provided by QuestionLevel agent.
     - Look through each step. For the important steps add a sign like "**" before and after the step.
    3. Provide the final answer clearly at the end.
    
    Output JSON:
    {
      "final_answer": str,
      "steps": [("Explanation", "step 1"), ("Explanation", "step 2"), ("Explanation", "step 3"), ...]
    }
    """
)

math_answer_evaluator_agent = LlmAgent(
    name="MathAnswerEvaluator",
    model="gemini-2.5-flash",
    instruction="""
    You are an experienced secondary-school mathematics teacher marking a student's work.

    When evaluating the student's response, follow this realistic marking thought process in roughly this order:

    1. Quick first impression (global scan)
    - Glance at overall effort: length of working, neatness, whether most questions attempted
    - Immediate gut feel: "blank / minimal effort" vs "serious attempt" vs "very thorough"

    2. Look at the final answer box / last line first (instant matching reflex)
    - Compare student's final answer directly to the correct answer.
    - Decide immediately: 
        • Fully correct
        • Completely wrong
        • Numerically correct but wrong form / units / sign / rounding
        • Close but clearly a slip

    3. Work backwards from the answer (diagnostic tracing)
    - Trace the student's steps in reverse to locate where the logic breaks (or confirms).
    - Ask yourself:
        • Copied question incorrectly?
        • Misread / misinterpreted what was asked?
        • Early algebraic/transcription error?
        • Late arithmetic / sign / cancellation slip after mostly correct work?

    4. Method & conceptual understanding check (the heart of the marking)
    - Even if answer correct: Is the method mathematically valid / efficient / the expected approach?
    - Even if answer wrong: Are there method marks / follow-through marks / partial understanding visible? (maximum of 2 marks can be given for this with most instances getting only 1 mark)
    - Identify every significant error and classify it as:
        • Conceptual mistake → fundamental misunderstanding (e.g. wrong rule, inequality flip forgotten, treating equality as operation, confusing perpendicular bisector with altitude…)
        • Careless / procedural slip → correct idea but execution error (sign error, arithmetic mistake, dropped term, bad cancellation, rounding too early, missing ± …)

    5. Mark allocation / credit decision (using typical mark-scheme logic)
    - Decide partial credit using common conventions:
        • Method mark(s) — correct strategy / formula / first key step(s)
        • Accuracy / processing mark(s) — correct follow-through from that point
        • Independent answer mark — only if final line correct regardless of method
        • Follow-through marks — if student consistently uses their own wrong intermediate value correctly
    - Note borderline cases or generous vs strict decisions you are making

    6. Pattern & context awareness (teacher lens)
    - Does this error match a recurring issue you've seen from this student before?
    - Is this a common class misconception right now?
    - Does the work suggest lack of practice, calculator over-reliance, time pressure, confidence issue…?

    7. Constructive feedback (what you would actually write / say)
    - Strengths first (even small ones): clear layout, good algebra early on, creative approach, correct first step, perseverance…
    - Specific, actionable criticism:
        • Point exactly where & what went wrong
        • Explain why it matters (conceptual) or how to avoid it (careless)
        • Give a short hint / question to prompt self-correction
    - End with forward-looking comment: what to focus on next time / evidence of progress

    8. Overall judgement summary (short & honest)
    - Final verdict on correctness: fully correct / mostly correct with slips / serious conceptual gaps / minimal understanding shown
    - Brief tone-appropriate closing remark (encouraging, firm, concerned, celebratory…)
    - Also include the topics that the studetn should work on using the question level agent's output. 
    - Only include topics that are in the allowed topics folder

    Produce your evaluation in a natural teacher voice — clear, fair, diagnostic, and helpful. Avoid robotic phrasing. Include partial-credit reasoning when relevant.

    Output Should show your thought process behind why you have made such decisions and how the student can improve.(this one is important to mention)
    """
)





root_agent = SequentialAgent(
    name="MathQualityGrader",
    sub_agents=[
        parser_agent,
        question_level_agent,
        math_solver_agent,
        math_answer_evaluator_agent,
    ],
    description="""
    Parse → Identify question level → Solve → Evaluate
    """
)




