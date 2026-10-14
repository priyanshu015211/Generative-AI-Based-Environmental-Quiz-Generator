import streamlit as st
from src.question_bank import get_quiz
from src.validator import validate_questions

st.set_page_config(page_title="EcoQuiz AI | First Review", page_icon="🌱", layout="wide")

TOPICS = [
    "Climate Change", "Biodiversity", "Waste Management", "Pollution",
    "Renewable Energy", "Water Conservation", "Sustainable Development"
]
LEVELS = ["Easy", "Medium", "Hard"]

st.markdown("""
<style>
.stApp { background: #f5f8f1; }
.hero { padding: 1.2rem 1.4rem; border-radius: 14px; background: #1f6b45; color: white; }
.note { color: #526354; font-size: 0.92rem; }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero"><h1>EcoQuiz AI</h1>'
    '<p>Generative AI-Based Environmental Quiz Generator — First-Review Prototype</p></div>',
    unsafe_allow_html=True,
)
st.write("Choose an environmental topic and test your understanding through an interactive quiz.")
st.info(
    "Current milestone (approximately 40%): this demo selects questions from a prepared sample bank. "
    "LLM-based question generation and adaptive difficulty are planned next, not implemented yet."
)

with st.sidebar:
    st.header("Quiz settings")
    topic = st.selectbox("Environmental topic", TOPICS)
    preferred_level = st.selectbox("Preferred difficulty", LEVELS, index=0)
    number = st.slider("Number of questions", min_value=3, max_value=5, value=3)
    st.caption("Questions are currently selected from local sample data; no API key is required.")

if "questions" not in st.session_state:
    st.session_state.questions = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""

if st.button("Generate quiz", type="primary", use_container_width=True):
    for response_key in [f"response_{i}" for i in range(5)]:
        st.session_state.pop(response_key, None)
    questions = get_quiz(topic, preferred_level, number)
    questions, issues = validate_questions(questions)
    st.session_state.questions = questions
    st.session_state.submitted = False
    st.session_state.quiz_topic = topic
    st.session_state.quiz_level = preferred_level
    st.session_state.validation_issues = issues
    st.rerun()

if st.session_state.questions:
    questions = st.session_state.questions
    st.subheader(f"Quiz: {st.session_state.quiz_topic}")
    left, middle, right = st.columns(3)
    left.metric("Questions", len(questions))
    middle.metric("Preferred level", st.session_state.get("quiz_level", "Easy"))
    right.metric("Question source", "Local sample bank")
    if st.session_state.get("validation_issues", 0):
        st.caption(f"Validation filtered {st.session_state.validation_issues} malformed or duplicate item(s).")

    if not st.session_state.submitted:
        with st.form("environmental_quiz_form"):
            answers = {}
            for idx, question in enumerate(questions):
                st.markdown(f"**Q{idx + 1}. {question['question']}**")
                options = question.get("options") or ["True", "False"]
                answers[idx] = st.radio(
                    "Select one answer", options,
                    index=None,
                    key=f"response_{idx}",
                    label_visibility="collapsed",
                )
                st.caption(f"Format: {question.get('type', 'MCQ')}")
                st.write("")
            submitted = st.form_submit_button("Submit answers", type="primary")

        if submitted:
            score = sum(answers.get(i) == q["answer"] for i, q in enumerate(questions))
            st.session_state.responses = answers
            st.session_state.score = score
            st.session_state.submitted = True
            st.rerun()
    else:
        score = st.session_state.score
        total = len(questions)
        st.success(f"Your score: {score}/{total} ({score / total:.0%})")
        st.subheader("Answer review")
        for idx, question in enumerate(questions):
            selected = st.session_state.responses.get(idx)
            correct = selected == question["answer"]
            st.markdown(f"**Q{idx + 1}. {question['question']}**")
            if correct:
                st.markdown(f":green[Correct] — **{question['answer']}**")
            else:
                shown = selected if selected is not None else "Not answered"
                st.markdown(f":red[Incorrect] — Your answer: {shown}. Correct answer: **{question['answer']}**")
            st.caption(question.get("explanation", "Review this concept with a trusted environmental source."))
            st.divider()
        if st.button("Start another quiz", type="primary"):
            for response_key in [f"response_{i}" for i in range(5)]:
                st.session_state.pop(response_key, None)
            st.session_state.questions = []
            st.session_state.submitted = False
            st.session_state.pop("responses", None)
            st.session_state.pop("score", None)
            st.rerun()

st.markdown("---")
st.markdown(
    '<p class="note">Prototype note: this milestone demonstrates topic-based quiz delivery and scoring. '
    'It does not yet generate new questions with an LLM, adapt difficulty using performance, '
    'or save results to a database.</p>',
    unsafe_allow_html=True,
)
