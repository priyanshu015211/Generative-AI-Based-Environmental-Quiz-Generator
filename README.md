# EcoQuiz AI — Approximately 40% First-Review Prototype

**Project title:** Generative AI-Based Environmental Quiz Generator

This project version intentionally represents an early milestone, not the complete proposed system. It provides a basic interactive prototype to demonstrate during the first review.

## Working in this version
- A Streamlit-based quiz interface.
- Selection from seven environmental topics.
- Preferred difficulty selection (Easy, Medium, Hard).
- A local prepared sample question bank containing MCQ, True/False, and scenario-based questions.
- Basic structure and duplicate checks for quiz items.
- Answer submission, score calculation, correct-answer display, and explanations.
- A restart control to run another quiz.

## Not implemented yet
- LLM/API-based creation of new questions. The current app selects from prepared sample questions.
- Difficulty adaptation based on user scores.
- Database storage, accounts, and cross-session quiz history.
- Retrieval from trusted environmental sources or fact-checking of generated content.
- Full evaluation, deployment, and production hardening.

## Run on Windows
1. Install Python 3.10 or newer.
2. Extract this ZIP and open a terminal in the extracted folder.
3. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install dependencies and run the app:

   ```powershell
   pip install -r requirements.txt
   streamlit run app.py
   ```

No API key is needed for this milestone.

## Run tests

```powershell
pytest -q
```

## Suggested first-review explanation

"We have completed the initial interface and quiz workflow. Users can choose an environmental topic and preferred difficulty, answer questions from our sample question bank, and receive a score with explanations. We have added basic checks to reject malformed or duplicate questions. This is our approximately 40% milestone. In the next stage, we plan to integrate an LLM for dynamic question generation, add adaptive difficulty, and store quiz results."

## Important limitation

The project title mentions Generative AI, but this early version does **not yet call an LLM**. The current quiz is based on prepared sample data so the user interface and scoring can be demonstrated reliably. Do not present LLM-based question generation or adaptive learning as completed features at this review.
