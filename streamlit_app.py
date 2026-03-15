# Streamlit UI for Google Forms Auto-Filler
import time
import random

import streamlit as st

from formbot.parser import parse_form
from formbot.generator import generate_response
from formbot.submitter import build_submit_url, submit_response
from formbot.config import (
    DEFAULT_COUNT,
    DEFAULT_MIN_DELAY,
    DEFAULT_MAX_DELAY,
    USER_AGENT,
    REQUEST_TIMEOUT,
)

import requests

st.set_page_config(page_title="Google Forms Auto-Filler", page_icon="📝", layout="wide")
st.title("📝 Google Forms Auto-Filler")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    form_url = st.text_input("Form URL", placeholder="https://docs.google.com/forms/d/e/.../viewform")
    count = st.number_input("Response Count", min_value=1, value=DEFAULT_COUNT, step=1)
    col1, col2 = st.columns(2)
    with col1:
        min_delay = st.number_input("Min Delay (s)", min_value=0.1, value=DEFAULT_MIN_DELAY, step=0.5)
    with col2:
        max_delay = st.number_input("Max Delay (s)", min_value=0.1, value=DEFAULT_MAX_DELAY, step=0.5)
    parse_btn = st.button("🔍 Parse Form", use_container_width=True, type="primary")

# --- Session state ---
if "questions" not in st.session_state:
    st.session_state.questions = None
if "form_id" not in st.session_state:
    st.session_state.form_id = None

# --- Parse form ---
if parse_btn:
    if not form_url.strip():
        st.error("Please enter a Google Form URL.")
    else:
        with st.spinner("Parsing form..."):
            try:
                form_id, questions = parse_form(form_url.strip())
                st.session_state.form_id = form_id
                st.session_state.questions = questions
            except ValueError as e:
                st.error(f"Parse error: {e}")
                st.session_state.questions = None
                st.session_state.form_id = None
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                st.session_state.questions = None
                st.session_state.form_id = None

# --- Main area ---
if st.session_state.questions is None:
    st.info("Enter a Google Form URL in the sidebar and click **Parse Form** to get started.")
    st.stop()

questions = st.session_state.questions
form_id = st.session_state.form_id

st.success(f"Found **{len(questions)}** question(s)")

# Display parsed questions
st.subheader("📋 Parsed Questions")
for i, q in enumerate(questions, 1):
    type_badge = q["type"]
    line = f"**{i}.** `{type_badge}` — {q['question']}"
    if q["options"]:
        line += f" *({len(q['options'])} options)*"
    if q["scale_min"] is not None:
        line += f" *(scale {q['scale_min']}–{q['scale_max']})*"
    st.markdown(line)

st.divider()

# --- Preview / Submit buttons ---
col_preview, col_submit = st.columns(2)

with col_preview:
    preview_btn = st.button("👁️ Preview Sample", use_container_width=True)

with col_submit:
    submit_btn = st.button("🚀 Submit Responses", use_container_width=True, type="primary")

# --- Preview ---
if preview_btn:
    st.subheader("📝 Sample Response")
    sample = generate_response(questions)
    data = [{"Entry ID": eid, "Value": val} for eid, val in sample]
    st.table(data)

# --- Submit ---
if submit_btn:
    st.subheader("📤 Submitting Responses")

    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://docs.google.com/forms/d/e/{form_id}/viewform",
    })
    submit_url = build_submit_url(form_id)

    progress_bar = st.progress(0)
    status_text = st.empty()
    log_container = st.container()

    success = 0
    failed = 0

    for i in range(1, count + 1):
        payload = generate_response(questions)
        ok = submit_response(session, submit_url, payload)
        if ok:
            success += 1
        else:
            failed += 1

        progress_bar.progress(i / count)
        status_text.markdown(f"**Progress:** {i}/{count} — ✅ {success} succeeded, ❌ {failed} failed")

        with log_container:
            st.text(f"[{i}/{count}] {'OK' if ok else 'FAILED'}")

        if i < count:
            time.sleep(random.uniform(min_delay, max_delay))

    progress_bar.progress(1.0)
    st.divider()
    if failed == 0:
        st.success(f"Done! All **{success}** responses submitted successfully.")
    else:
        st.warning(f"Done: **{success}** succeeded, **{failed}** failed out of **{count}**.")
