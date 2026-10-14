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
