# Streamlit UI Design

## Overview

A single-file Streamlit app (`ui/streamlit_app.py`) that wraps the existing `formbot` CLI modules in a browser-based GUI. Sidebar + Main layout.

## Sidebar

- **Form URL** — `st.text_input`
- **Response Count** — `st.number_input` (default 10, min 1)
- **Min Delay** — `st.number_input` (default 1.5, min 0.1, step 0.5)
- **Max Delay** — `st.number_input` (default 4.0, min 0.1, step 0.5)
- **"Parse Form" button** — `st.button`, triggers `parse_form(url)`

## Main Area (progressive sections)

### 1. Parsed Questions
- Shown after successful parse, stored in `st.session_state`
- Display as list: `"{index}. [{type}] {question} ({N} options)"` or similar
- `st.success("Found N questions")`

### 2. Sample Preview
- "Preview Sample" button → calls `generate_response(questions)`
- Shows result in a `st.dataframe` or `st.table` with entry_id and value columns

### 3. Submission
- "Submit Responses" button → runs `submit_batch` logic inline with `st.progress()` updates
- Cannot use `submit_batch` directly (it blocks and prints to stdout), so replicate the loop in Streamlit with progress bar and `st.empty()` placeholders
- Final summary: `st.success/st.error` with success/fail counts

## Error Handling
- `ValueError` from parser → `st.error(str(e))`
- Network errors → `st.error("Failed to connect")`

## Dependencies
- Add `streamlit` to requirements or document separately
- Reuses `formbot.parser`, `formbot.generator`, `formbot.submitter` modules

## Run Command
```
streamlit run ui/streamlit_app.py
```
