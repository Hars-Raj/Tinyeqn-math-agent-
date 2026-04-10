# MathQualityGrader: Singapore MOE Math Evaluation Agent

MathQualityGrader is an intelligent, multi-agent AI pipeline designed to evaluate student math answers. It acts like an experienced secondary-school mathematics teacher, providing targeted, syllabus-aligned feedback rather than just marking answers "Right" or "Wrong".

## 🌟 Overview
The primary goal of this platform is to help students learn from their mistakes. The agent traces the student's methodology, checks for conceptual vs. careless mistakes, assigns partial credit where appropriate, and provides constructive, actionable feedback tailored to the official MOE Singapore Math curriculum.

## 🏗️ Architecture & Agent Roles

The system is built using Google's Agent Development Kit (`google.adk`) and operates sequentially through four specialized `LlmAgent`s:

### 1. Parser Agent
- **Role:** Data structurer.
- **Action:** Takes the raw text of the math question and the student's answer, parsing it into a structured JSON format. It breaks down the student's dense workings into a clear, step-by-step array.

### 2. QuestionLevel Agent
- **Role:** Syllabus mapping & Method validation.
- **Action:** Leverages official curriculum knowledge (`moe_math_syllabus.json`) and specific guardrails (`moe_math_guardrails.json`) to determine the educational level of the question (e.g., Primary 5, Secondary 2). 
- It assesses the student's chosen methodology to see if it is valid for their academic level (e.g., ensuring algebra isn't unfairly expected of a primary school student), and decides the most appropriate method to solve the problem.

### 3. MathSolver Agent
- **Role:** Ground-truth generator.
- **Action:** Before marking, the system needs the correct answer. The Solver solves the math problem step-by-step using the syllabus-approved method recommended by the QuestionLevel agent. It produces the verified final answer and detailed step explanations to act as the gold-standard reference.

### 4. MathAnswerEvaluator Agent
- **Role:** The "Experienced Teacher".
- **Action:** Compares the student's structured workings against the MathSolver's ground truth. It simulates realistic marking behaviors:
  - **Diagnostic Tracing:** Works backward from the student's final line to find exactly where the logic or arithmetic broke.
  - **Error Classification:** Distinguishes between transcription errors, conceptual misunderstandings, and careless arithmetic slips.
  - **Credit Allocation:** Mimics real exam marking schemes by awarding method marks, accuracy marks, and follow-through marks.
  - **Constructive Feedback:** Starts with strengths, pinpoints the specific breakdown in logic, and provides an encouraging, forward-looking hint for self-correction.

## 🚀 Pipeline Flow
`Parse Input` &rarr; `Identify Level & Validate Method` &rarr; `Generate Perfect Solution` &rarr; `Evaluate Student Work`

## 📂 Requirements
- `google.adk` (Agent Development Kit framework)
- Python 3.10 and above (to match the ADK requirements)
- Required JSON knowledge bases (`moe_math_syllabus.json` and `moe_math_guardrails.json`) placed within the `data/` directory.

## 🧠 Educational Philosophy
The hallmark of `MathQualityGrader` is its natural, teacher-like voice. It recognizes that learning math is progressive. By avoiding robotic phrasing and focusing on the *why* alongside the *what*, it encourages resilience and genuine conceptual mastery.
