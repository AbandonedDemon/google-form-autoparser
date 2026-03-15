# Plan: Google Forms Auto-Filler Tool

## Context

Build a lightweight Python CLI tool that parses a Google Form URL, extracts question metadata from the embedded `FB_PUBLIC_LOAD_DATA_` structure, generates realistic responses, and submits them automatically. This is for survey testing and thesis data simulation. The project is fresh — only `docs/build_guide.md` exists.

---

## Project Structure

```
formbot/
├── config.py        # Constants, type mapping, defaults
├── parser.py        # Fetch HTML + extract questions from FB_PUBLIC_LOAD_DATA_
├── generator.py     # Generate responses per question type
├── submitter.py     # POST submissions with rate limiting
├── main.py          # CLI entry point (argparse)
└── requirements.txt
```

---

## Implementation Steps

### Step 1: `formbot/config.py`
- Question type mapping: `{0: "short_text", 1: "paragraph", 2: "radio", 3: "dropdown", 4: "checkbox", 5: "linear_scale"}`
- Defaults: count=10, delay 1.5–4.0s, timeout=30s
- User-Agent string mimicking a real browser
- Faker locale setting

### Step 2: `formbot/requirements.txt`
```
requests>=2.31.0
faker>=22.0.0
beautifulsoup4>=4.12.0
```

### Step 3: `formbot/parser.py` (most complex module)
- `fetch_form_html(url)` — GET the form, detect login-required forms by checking for `freebirdFormviewerViewFormRequiresLogin`
- `extract_fb_data(html)` — Use BeautifulSoup to find `<script>` tags, then regex `FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?)\s*;\s*</script>` to extract the JS array, parse with `json.loads()` (with trailing-comma cleanup fallback)
- `parse_questions(fb_data)` — Walk nested list structure:
  - Questions at `fb_data[1][1]`
  - Each question `q`: title=`q[1]`, type=`q[3]`, entry_id=`q[4][0][0]` (prefix with `"entry."`), options=`q[4][0][1]` (each option at `[i][0]`)
  - For linear scale: extract min/max from options list length
  - Wrap index access in try/except, skip unparseable questions with warning
- `get_form_id(url)` — Extract form ID from URL path
- `parse_form(url)` — Orchestrator returning `(form_id, questions)`
- Output format per question: `{"question": str, "type": str, "type_code": int, "entry_id": str, "options": list|None, "scale_min": int|None, "scale_max": int|None}`

### Step 4: `formbot/generator.py`
- **Critical design choice**: Return `list[tuple[str, str]]` not dict — checkboxes need repeated keys
- Dispatch table mapping type names to handler functions
- Handlers:
  - `short_text` → `fake.sentence()`
  - `paragraph` → `fake.paragraph()`
  - `radio` / `dropdown` → `random.choice(options)`
  - `checkbox` → `random.sample(options, k=randint(1, len))` — returns **multiple tuples with same entry_id**
  - `linear_scale` → `random.randint(min, max)`

### Step 5: `formbot/submitter.py`
- `build_submit_url(form_id)` → `https://docs.google.com/forms/d/e/{form_id}/formResponse`
- `submit_response(url, payload)` — POST with `requests.Session()`, pass payload as list of tuples to `data=` param, set User-Agent + Referer headers, accept 200/302 as success
- `submit_batch(form_id, questions, count, min_delay, max_delay)` — Loop: generate → submit → print progress → sleep random delay. Returns `{"success": int, "failed": int, "total": int}`

### Step 6: `formbot/main.py`
- argparse CLI: `--url` (required), `--count` (default 10), `--min-delay`, `--max-delay`, `--dry-run`, `--verbose`
- Flow: parse form → print question summary → submit batch (or dry-run) → print results
- `--dry-run` generates one sample response and prints without submitting

---

## Key Pitfalls to Watch

1. **FB_PUBLIC_LOAD_DATA_ nesting** — Structure is undocumented and may vary. Use defensive indexing with try/except.
2. **Checkbox encoding** — Must use list-of-tuples for `requests.post(data=...)`, not a dict.
3. **Login-required forms** — Detect early in parser and abort with clear error.
4. **"Other" option fields** — Skip in v1, these use a separate entry ID pattern.
5. **Rate limiting** — 1.5–4.0s random delay is reasonable for up to ~200 submissions.

---

## Verification

1. `pip install -r formbot/requirements.txt`
2. `python formbot/main.py --url <test_form_url> --dry-run --verbose` — Verify parsing + generation without submitting
3. `python formbot/main.py --url <test_form_url> --count 3` — Submit 3 test responses to a form you control
4. Check the Google Form responses sheet to confirm data arrived correctly
5. Test with forms containing different question types (radio, checkbox, text, dropdown, linear scale)
