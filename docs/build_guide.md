# Google Forms Auto Filler Tool

Lightweight automation tool for generating and submitting responses to a Google Form.
Designed for survey testing and thesis data simulation.

---

# 1. Goal

Build a lightweight tool that:

1. Accepts a **Google Form URL**
2. Automatically **parses the form structure**
3. Generates **realistic survey responses**
4. Submits **N automated responses**
5. Supports:
   - Radio buttons
   - Checkboxes
   - Dropdowns
   - Text inputs

---

# 2. Core Workflow

```
User provides Google Form URL
        ↓
Fetch form HTML
        ↓
Extract FB_PUBLIC_LOAD_DATA_ JSON
        ↓
Parse questions and entry IDs
        ↓
Generate answers for each question
        ↓
POST responses to formResponse endpoint
        ↓
Repeat N times with delay
```

---

# 3. Project Structure

```
formbot/
│
├── main.py
├── parser.py
├── generator.py
├── submitter.py
├── config.py
│
└── requirements.txt
```

Optional UI layer:

```
ui/
 └── streamlit_app.py
```

---

# 4. Required Libraries

```
requests
faker
beautifulsoup4
streamlit (optional)
```

Install:

```
pip install -r requirements.txt
```

---

# 5. Form Parser

Purpose: Extract question metadata from the Google Form page.

Steps:

1. Download form HTML
2. Locate `FB_PUBLIC_LOAD_DATA_`
3. Parse JSON structure
4. Extract:
   - question text
   - question type
   - answer options
   - entry IDs

Output example:

```json
[
  {
    "question": "Gender",
    "type": "radio",
    "entry": "entry.123456",
    "options": ["Male", "Female"]
  },
  {
    "question": "Feedback",
    "type": "text",
    "entry": "entry.654321"
  }
]
```

---

# 6. Question Type Mapping

Google Form types:

| Code | Type                    |
| ---- | ----------------------- |
| 0    | short text              |
| 1    | paragraph               |
| 2    | radio / multiple choice |
| 3    | dropdown                |
| 4    | checkbox                |
| 5    | linear scale            |

Supported types for automation:

```
text
radio
checkbox
dropdown
```

---

# 7. Response Generator

Generate answers depending on question type.

Strategies:

### Radio

Random choice from options.

```
random.choice(options)
```

### Checkbox

Random subset.

```
random.sample(options, k=random_count)
```

### Text

Generate natural sentences.

Using Faker:

```
faker.sentence()
faker.paragraph()
```

Alternative:

Use predefined comment pools for realism.

---

# 8. Submission Engine

Google Form submissions go to:

```
https://docs.google.com/forms/d/e/FORM_ID/formResponse
```

Example POST payload:

```
{
 "entry.123456": "Male",
 "entry.654321": "Staff were friendly and helpful"
}
```

Send using:

```
requests.post(url, data=payload)
```

---

# 9. Rate Limiting

To avoid detection:

```
sleep(random.uniform(1.5,4.0))
```

Optional improvements:

- random delays
- random text lengths
- weighted answer distributions

---

# 10. CLI Usage

Example:

```
python main.py --url FORM_URL --count 200
```

Output:

```
Parsing form...
Found 8 questions

Submitting responses...
Progress: 1/200
Progress: 2/200
...
Completed
```

---

# 11. Optional UI

Simple UI with Streamlit:

Features:

- Paste form URL
- Select number of responses
- Start automation
- Progress display

Launch:

```
streamlit run streamlit_app.py
```

---

# 12. Future Improvements

Possible enhancements:

- Auto-detect question weights
- Statistical distribution control
- Proxy / IP rotation
- Multi-threaded submission
- Export generated dataset
- GUI desktop tool

---

# 13. Ethical Notes

This tool is intended for:

- survey testing
- form automation experiments
- dataset simulation

Avoid misuse that violates research integrity or platform policies.

---

# 14. Example Run

```
Input Form URL:
https://docs.google.com/forms/d/e/FORM_ID/viewform

Responses Requested:
200

Questions Detected:
- Gender
- Age Group
- Satisfaction Level
- Comments

Execution Time:
~8 minutes
```

---

# End
