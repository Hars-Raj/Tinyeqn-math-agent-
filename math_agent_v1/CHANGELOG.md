# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
*No unreleased changes at this time.*

## [0.7.0] - 31-03-2026
### Added
- **Focus Topic Recommendations:** Upgraded the Evaluator Agent to actively suggest specific topics for the student to practice. It now leverages the Question Level Agent's output to dynamically recommend targeted improvement areas strictly based on an allowed list of topics.

## [0.6.0] - 30-03-2026
### Added
- **Accuracy Guardrails:** Implemented guardrails due to lingering method mismatch errors. This significantly improved the precision of the identified question levels and the expected mathematical methods.

## [0.5.1] - 28-03-2026
### Added
- **Syllabus Knowledge Base:** Created and integrated `moe_math_syllabus.json`. This provides the Question Level Agent with a dedicated reference to correctly identify textbook methods directly tied to the student's educational tier.

## [0.5.0] - 27-03-2026
### Added
- **Question Level Agent:** Discovered a method mismatch where the agent solved questions using advanced techniques not appropriate for the student's level. Implemented the Question Level Agent to strictly map syllabus expectations to the corresponding question.

## [0.4.0] - 24-03-2026
### Added
- **Parser Agent:** Integrated a dedicated parsing agent at the start of the pipeline. This parses and structures incoming questions and answers to make them significantly more readable for downstream agents.

## [0.3.1] - 23-03-2026
### Changed
- **Evaluator Improvements:** Improved the Evaluator Agent using Chain-of-Thought (CoT) prompting to accurately replicate a teacher's diagnostic feedback process.
- **Definitive Grading Response:** Enhanced the Evaluator to generate a clear, definitive response format, bringing the quality of feedback extremely close to that of a real human educator.

## [0.3.0] - 17-03-2026
### Added
- **Evaluator Agent:** Implemented a new agent directly into the sequential pipeline designed to compare the student's structured answer against the pure output of the Solver Agent.

## [0.2.0] - 16-03-2026
### Changed
- **Sequential Agents Migration:** Transitioned from a tool-based architecture into a multi-agent sequential pipeline using `MathQualityGrader`.
- **Solver Agent Output:** Replaced the SymPy algebraic tool with a dedicated Solver Agent. This upgrade enables the system to inherently solve a far wider range of mathematical questions beyond basic algebra.

## [0.1.0] - 12-03-2026
### Added
- **Initial Prototype:** Successfully created a working single-agent math solver.
- **SymPy Tool:** Implemented a tool utilizing the `SymPy` Python library to programmatically solve algebraic equations.
