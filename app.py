import html
import streamlit as st
from src.question_bank import get_quiz
from src.validator import validate_questions

st.set_page_config(
    page_title="EcoQuiz AI | Environmental Learning",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TOPICS = [
    "Climate Change", "Biodiversity", "Waste Management", "Pollution",
    "Renewable Energy", "Water Conservation", "Sustainable Development"
]
LEVELS = ["Easy", "Medium", "Hard"]
TOPIC_ICONS = {
    "Climate Change": "◌",
    "Biodiversity": "✳",
    "Waste Management": "↻",
    "Pollution": "⌁",
    "Renewable Energy": "ϟ",
    "Water Conservation": "≈",
    "Sustainable Development": "◎",
}

st.markdown(
    r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
      --forest: #174d3b;
      --forest-deep: #103b2d;
      --leaf: #2f7856;
      --lime: #d7ef9b;
      --ink: #18372d;
      --muted: #687b72;
      --line: #e1e9e2;
      --paper: #ffffff;
      --canvas: #f5f8f4;
    }

    html, body, [class*="css"], .stApp {
      font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      color: var(--ink);
    }
    .stApp { background: var(--canvas); }
    [data-testid="stHeader"] { background: rgba(245,248,244,0.88); }
    [data-testid="stMainBlockContainer"] {
      max-width: 1160px;
      padding-top: 1.8rem;
      padding-bottom: 3.2rem;
    }
    #MainMenu, footer { visibility: hidden; }

    .brandbar {
      display: flex; align-items: center; justify-content: space-between;
      gap: 1rem; margin-bottom: 1.15rem;
    }
    .brand-left { display: flex; align-items: center; gap: 0.75rem; }
    .brand-mark {
      width: 43px; height: 43px; border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      color: #f5ffe8; background: var(--forest); font-size: 1.45rem;
      font-weight: 800; font-family: 'Manrope', sans-serif;
      box-shadow: 0 6px 18px rgba(23,77,59,.12);
    }
    .brand-name { font: 800 1.17rem 'Manrope', sans-serif; color: var(--ink); letter-spacing: -.04em; line-height: 1.15; }
    .brand-name span { color: var(--leaf); }
    .brand-caption { color: #809087; font-size: .67rem; letter-spacing: .13em; font-weight: 700; margin-top: .24rem; }
    .review-pill {
      border: 1px solid #dce8dd; border-radius: 999px; padding: .48rem .8rem;
      color: #547162; background: #edf4ec; font-size: .73rem; font-weight: 700;
      letter-spacing: .04em; white-space: nowrap;
    }

    .hero {
      position: relative; overflow: hidden; display: flex; align-items: center;
      justify-content: space-between; gap: 2rem;
      padding: 2.4rem 2.65rem; border-radius: 25px;
      background: radial-gradient(circle at 80% 8%, rgba(215,239,155,.18), transparent 27%),
                  linear-gradient(120deg, #103b2d 0%, #1b6045 70%, #2b7552 100%);
      color: white; box-shadow: 0 16px 38px rgba(22,67,49,.13);
    }
    .hero-copy { max-width: 700px; position: relative; z-index: 1; }
    .eyebrow { color: #d8edae; font-size: .73rem; text-transform: uppercase; letter-spacing: .17em; font-weight: 800; margin-bottom: .9rem; }
    .hero h1 { color: white; font: 800 clamp(2.05rem, 4vw, 3rem)/1.1 'Manrope', sans-serif; letter-spacing: -.055em; margin: 0 0 .85rem 0; }
    .hero p { color: #d6e8dc; max-width: 590px; line-height: 1.7; font-size: 1rem; margin: 0; }
    .hero-badge {
      min-width: 142px; width: 142px; height: 142px; border-radius: 50%;
      background: rgba(245,255,229,.10); border: 1px solid rgba(234,249,218,.35);
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      box-shadow: inset 0 0 0 8px rgba(234,249,218,.04); flex-shrink: 0; text-align: center;
    }
    .hero-badge strong { color: #e5f7bd; font: 800 2.3rem 'Manrope', sans-serif; letter-spacing: -.06em; }
    .hero-badge span { font-size: .65rem; text-transform: uppercase; letter-spacing: .14em; color: #d9e8dc; font-weight: 800; margin-top: .25rem; }

    .milestone {
      display: flex; align-items: flex-start; gap: .8rem; margin: 1.1rem 0 1.65rem;
      padding: .95rem 1.1rem; border: 1px solid #e1e9df; background: #edf3ea; border-radius: 14px;
      color: #546d5e; font-size: .86rem; line-height: 1.55;
    }
    .milestone-dot { width: 9px; height: 9px; border-radius: 50%; background: #6e9c59; margin-top: .34rem; flex-shrink: 0; }
    .section-kicker { color: #638171; font-size: .72rem; text-transform: uppercase; letter-spacing: .14em; font-weight: 800; margin: .1rem 0 .45rem; }
    .section-title { font: 800 1.55rem 'Manrope', sans-serif; letter-spacing: -.04em; color: var(--ink); margin: 0 0 .35rem; }
    .section-desc { color: var(--muted); line-height: 1.6; margin: 0 0 1.1rem; font-size: .92rem; }
    .field-label { color: #496454; font-size: .78rem; font-weight: 800; margin: .15rem 0 .5rem; }
    .topic-summary {
      padding: 1rem 1.05rem; border-radius: 14px; border: 1px solid var(--line);
      background: #f8faf7; margin: .55rem 0 1.1rem; display: flex; gap: .8rem; align-items: center;
    }
    .topic-icon { height: 42px; width: 42px; border-radius: 13px; display: flex; align-items: center; justify-content: center; background: #e6f0df; color: #316c4b; font: 800 1.55rem 'Manrope', sans-serif; }
    .topic-summary strong { font: 700 1rem 'Manrope', sans-serif; display: block; color: var(--ink); }
    .topic-summary span { display: block; font-size: .81rem; color: var(--muted); margin-top: .2rem; }
    .mini-stat {
      padding: .95rem 1rem; border-radius: 14px; background: white;
      border: 1px solid var(--line); min-height: 86px;
    }
    .mini-stat span { color: #72847a; font-size: .75rem; display: block; }
    .mini-stat strong { color: var(--ink); font: 800 1.18rem 'Manrope', sans-serif; display: block; margin-top: .38rem; }

    div[data-baseweb="select"] > div { border-radius: 11px; border-color: #dce5dc; background: #fff; min-height: 45px; }
    div[data-baseweb="select"] > div:focus-within { border-color: #6a9978; box-shadow: 0 0 0 1px #6a9978; }
    div[data-testid="stSlider"] [data-baseweb="slider"] { padding-top: .55rem; }
    .stButton > button, div[data-testid="stFormSubmitButton"] > button {
      border-radius: 12px; min-height: 3rem; font-weight: 800; transition: all .18s ease;
      border: 1px solid #d9e4da; background: #fff; color: #294c3b;
    }
    .stButton > button[kind="primary"], div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
      background: var(--forest); border-color: var(--forest); color: white;
      box-shadow: 0 7px 15px rgba(23,77,59,.12);
    }
    .stButton > button[kind="primary"]:hover, div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
      background: #23664a; border-color: #23664a; color: white; transform: translateY(-1px);
    }
    .stButton > button:hover { border-color: #8eaf98; color: var(--forest); }
    div[data-testid="stRadio"] > label { color: #6d8175; font-size: .8rem; font-weight: 700; }
    div[role="radiogroup"] { gap: .4rem; }
    div[role="radiogroup"] label {
      border: 1px solid #e1e9e2; background: #fbfcfa; border-radius: 10px;
      padding: .48rem .65rem; margin-right: .12rem;
    }
    div[role="radiogroup"] label:hover { border-color: #abc6b0; background: #f3f8f1; }
    [data-testid="stMetric"] { background: #fff; padding: 1rem 1.05rem; border: 1px solid var(--line); border-radius: 14px; }
    [data-testid="stMetricLabel"] { color: #6f8277; }
    [data-testid="stMetricValue"] { color: var(--ink); font-family: 'Manrope', sans-serif; }
    [data-testid="stProgressBar"] > div { background: #dfe9df; border-radius: 999px; }
    [data-testid="stProgressBar"] > div > div { background: #3b8058; border-radius: 999px; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--line); border-radius: 18px; background: #fff; }
    .quiz-topline { display:flex; align-items:center; justify-content:space-between; gap:1rem; margin-bottom:.5rem; }
    .quiz-name { font: 800 1.55rem 'Manrope', sans-serif; letter-spacing: -.04em; color: var(--ink); }
    .soft-chip { display:inline-block; color:#38634a; background:#edf5e9; border:1px solid #dbe9d6; border-radius:999px; padding:.35rem .65rem; font-size:.72rem; font-weight:800; }
    .question-number { color: #789081; font-size: .72rem; letter-spacing: .13em; font-weight: 800; text-transform: uppercase; margin-bottom: .55rem; }
    .question-text { color: var(--ink); font: 700 1.08rem/1.55 'Manrope', sans-serif; margin-bottom: .8rem; }
    .result-banner { padding:1.4rem 1.5rem; border-radius:18px; background:linear-gradient(110deg,#eaf4e4,#f5f8ed); border:1px solid #dce9d4; margin:.75rem 0 1rem; }
    .result-label { font-size:.72rem; text-transform:uppercase; letter-spacing:.15em; font-weight:800; color:#557760; }
    .result-score { font:800 2.25rem 'Manrope',sans-serif; color:#214f37; letter-spacing:-.06em; margin:.2rem 0; }
    .result-copy { color:#5c7665; font-size:.9rem; }
    .review-heading { font:800 1rem 'Manrope',sans-serif; color:var(--ink); line-height:1.5; }
    .answer-good { padding:.65rem .8rem; border-radius:10px; background:#eef7ea; border:1px solid #dcebd6; color:#306243; font-size:.86rem; }
    .answer-bad { padding:.65rem .8rem; border-radius:10px; background:#fff3ef; border:1px solid #f3ded5; color:#954d3b; font-size:.86rem; }
    .explanation { color:#65786d; font-size:.88rem; line-height:1.65; margin-top:.65rem; }
    .footer-note { margin-top:2rem; padding-top:1rem; border-top:1px solid #e0e8df; color:#829087; font-size:.76rem; line-height:1.6; }

    @media (max-width: 700px) {
      [data-testid="stMainBlockContainer"] { padding-left: 1rem; padding-right: 1rem; padding-top: 1rem; }
      .hero { padding: 1.5rem; border-radius: 19px; }
      .hero-badge { min-width: 86px; width: 86px; height: 86px; }
      .hero-badge strong { font-size: 1.55rem; }
      .hero-badge span { font-size: .5rem; }
      .review-pill { display: none; }
      .hero p { font-size: .9rem; }
      .brand-caption { font-size: .57rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Consistent page header
st.markdown(
    """
    <div class="brandbar">
      <div class="brand-left">
        <div class="brand-mark">E</div>
        <div>
          <div class="brand-name">EcoQuiz <span>AI</span></div>
          <div class="brand-caption">ENVIRONMENTAL LEARNING STUDIO</div>
        </div>
      </div>
      <div class="review-pill">FIRST REVIEW &nbsp;·&nbsp; MILESTONE 01</div>
    </div>
    <section class="hero">
      <div class="hero-copy">
        <div class="eyebrow">Learn a little. Change a lot.</div>
        <h1>Small questions.<br>Greener thinking.</h1>
        <p>Explore the environmental issues shaping our world with short, focused quizzes designed to make learning practical and engaging.</p>
      </div>
      <div class="hero-badge"><strong>40%</strong><span>Project milestone</span></div>
    </section>
    <div class="milestone"><span class="milestone-dot"></span><div><strong>First-review prototype</strong><br>Topic-based quizzes, answer checking, and scoring are working. This version uses a prepared sample question bank; live Generative AI and adaptive difficulty are planned for a later milestone.</div></div>
    """,
    unsafe_allow_html=True,
)

# Keep application state simple and explicit.
if "questions" not in st.session_state:
    st.session_state.questions = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "quiz_topic" not in st.session_state:
    st.session_state.quiz_topic = ""


def clear_quiz():
    for key in [f"response_{i}" for i in range(10)]:
        st.session_state.pop(key, None)
    for key in ["responses", "score", "questions", "quiz_topic", "quiz_level", "quiz_type", "validation_issues"]:
        st.session_state.pop(key, None)
    st.session_state.questions = []
    st.session_state.submitted = False
    st.rerun()

if not st.session_state.questions:
    st.markdown('<div class="section-kicker">01 / Make it yours</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Build your quiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Pick a subject, one question format, a starting difficulty, and exactly 3, 4, or 5 questions from the current sample bank.</div>', unsafe_allow_html=True)

    with st.container(border=True):
        top_left, top_right = st.columns([1.45, 1], gap="large")
        with top_left:
            st.markdown('<div class="field-label">ENVIRONMENTAL TOPIC</div>', unsafe_allow_html=True)
            topic = st.selectbox(
                "Environmental topic", TOPICS,
                format_func=lambda item: f"{TOPIC_ICONS[item]}   {item}",
                label_visibility="collapsed",
            )
            st.markdown(
                f'<div class="topic-summary"><div class="topic-icon">{TOPIC_ICONS[topic]}</div><div><strong>{html.escape(topic)}</strong><span>Explore key concepts and everyday choices</span></div></div>',
                unsafe_allow_html=True,
            )
        with top_right:
            st.markdown('<div class="field-label">QUESTION FORMAT</div>', unsafe_allow_html=True)
            question_type = st.selectbox(
                "Question format", ["MCQ", "True/False", "Scenario-based"],
                format_func=lambda value: "Multiple-choice (MCQ)" if value == "MCQ" else value,
                label_visibility="collapsed",
                help="Choose one format for every question in this quiz.",
            )
            difficulty_col, count_col = st.columns([1, 1], gap="medium")
            with difficulty_col:
                st.markdown('<div class="field-label">STARTING DIFFICULTY</div>', unsafe_allow_html=True)
                preferred_level = st.selectbox(
                    "Preferred difficulty", LEVELS, index=0, label_visibility="collapsed",
                    help="This chooses which questions are selected first. The app does not adapt difficulty based on results yet.",
                )
            with count_col:
                st.markdown('<div class="field-label">NUMBER OF QUESTIONS</div>', unsafe_allow_html=True)
                number = st.select_slider("Number of questions", options=[3, 4, 5], value=3, label_visibility="collapsed")
            st.caption("Choose one format and 3, 4, or 5 questions · No sign-in required")

        st.markdown("<div style='height:.35rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="field-label">WHAT’S INCLUDED</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3, gap="small")
        for col, value, label in [
            (s1, "7", "Environmental topics"),
            (s2, "3", "Question formats"),
            (s3, "Instant", "Score & feedback"),
        ]:
            with col:
                st.markdown(f'<div class="mini-stat"><span>{label}</span><strong>{value}</strong></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:.65rem'></div>", unsafe_allow_html=True)
        if st.button("Create my quiz  →", type="primary", use_container_width=True):
            clear_quiz_state = [f"response_{i}" for i in range(10)]
            for response_key in clear_quiz_state:
                st.session_state.pop(response_key, None)
            questions = get_quiz(topic, preferred_level, number, question_type=question_type)
            questions, issues = validate_questions(questions)
            if len(questions) != number:
                st.error(f"The sample bank returned {len(questions)} valid questions, but {number} were requested. Please choose another format or count.")
            else:
                st.session_state.questions = questions
                st.session_state.submitted = False
                st.session_state.quiz_topic = topic
                st.session_state.quiz_level = preferred_level
                st.session_state.quiz_type = question_type
                st.session_state.validation_issues = issues
                st.rerun()

else:
    questions = st.session_state.questions
    total = len(questions)
    topic = st.session_state.quiz_topic
    level = st.session_state.get("quiz_level", "Easy")
    quiz_type = st.session_state.get("quiz_type", "MCQ")

    if not st.session_state.submitted:
        st.markdown('<div class="section-kicker">02 / Your quiz</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="quiz-topline"><div class="quiz-name">{html.escape(topic)}</div><span class="soft-chip">{html.escape(level)} level</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="section-desc">Take your time. Choose one answer for each question, then submit to see your score and explanations.</div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        a.metric("Questions", total)
        b.metric("Question format", "MCQ" if quiz_type == "MCQ" else quiz_type)
        c.metric("Selected level", level)
        st.progress(0.0, text="Ready when you are · 0% complete")

        if st.session_state.get("validation_issues", 0):
            st.caption(f"The basic validation step filtered {st.session_state.validation_issues} malformed or duplicate item(s).")

        with st.form("environmental_quiz_form"):
            answers = {}
            for idx, question in enumerate(questions):
                with st.container(border=True):
                    col_num, col_type = st.columns([1, 1])
                    with col_num:
                        st.markdown(f'<div class="question-number">QUESTION {idx + 1:02d} <span style="color:#b2c0b4">/ {total:02d}</span></div>', unsafe_allow_html=True)
                    with col_type:
                        qtype = html.escape(question.get("type", "MCQ"))
                        st.markdown(f'<div style="text-align:right"><span class="soft-chip">{qtype}</span></div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="question-text">{html.escape(question["question"])}</div>', unsafe_allow_html=True)
                    options = question.get("options") or ["True", "False"]
                    answers[idx] = st.radio(
                        f"Answer for question {idx + 1}", options,
                        index=None, key=f"response_{idx}", label_visibility="collapsed",
                    )
            st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
            submitted = st.form_submit_button("Submit answers and see results  →", type="primary", use_container_width=True)

        if submitted:
            score = sum(answers.get(i) == question["answer"] for i, question in enumerate(questions))
            st.session_state.responses = answers
            st.session_state.score = score
            st.session_state.submitted = True
            st.rerun()
    else:
        score = st.session_state.score
        total = len(questions)
        pct = score / total if total else 0
        if pct >= .8:
            headline, feedback = "Great work!", "You’ve built a strong understanding of this topic."
        elif pct >= .5:
            headline, feedback = "Good start.", "Review the explanations below to strengthen your understanding."
        else:
            headline, feedback = "Keep exploring.", "Every question is a chance to learn something new. Review the answers and try again."

        st.markdown('<div class="section-kicker">03 / Your results</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-banner"><div class="result-label">Quiz complete</div><div class="result-score">{score} <span style="font-size:1.2rem;color:#6b8c73">/ {total}</span></div><div style="font-weight:800;color:#315d41;font-size:1.06rem">{headline}</div><div class="result-copy">{feedback}</div></div>',
            unsafe_allow_html=True,
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("Final score", f"{score}/{total}")
        m2.metric("Accuracy", f"{pct:.0%}")
        m3.metric("Question format", "MCQ" if quiz_type == "MCQ" else quiz_type)
        st.progress(pct, text=f"You answered {score} out of {total} correctly")

        st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">Review your answers</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-desc">Check what you selected and read the short explanation for each question.</div>', unsafe_allow_html=True)

        for idx, question in enumerate(questions):
            selected = st.session_state.responses.get(idx)
            correct = selected == question["answer"]
            with st.container(border=True):
                st.markdown(f'<div class="question-number">QUESTION {idx + 1:02d}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="review-heading">{html.escape(question["question"])}</div>', unsafe_allow_html=True)
                if correct:
                    st.markdown(f'<div class="answer-good">Correct · <strong>{html.escape(question["answer"])}</strong></div>', unsafe_allow_html=True)
                else:
                    shown = "Not answered" if selected is None else html.escape(str(selected))
                    st.markdown(f'<div class="answer-bad">Your answer: <strong>{shown}</strong><br>Correct answer: <strong>{html.escape(question["answer"])}</strong></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="explanation">{html.escape(question.get("explanation", "Review this concept with a trusted environmental source."))}</div>', unsafe_allow_html=True)

        st.markdown("<div style='height:.45rem'></div>", unsafe_allow_html=True)
        if st.button("← Build another quiz", type="primary", use_container_width=True):
            clear_quiz()

st.markdown(
    '<div class="footer-note"><strong>About this milestone</strong><br>EcoQuiz AI is currently an early prototype. This version demonstrates quiz delivery and scoring from a prepared local question bank. LLM-based question generation, score-based adaptive difficulty, and database-backed progress tracking are future development stages.</div>',
    unsafe_allow_html=True,
)
