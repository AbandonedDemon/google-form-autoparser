# Google Forms Auto-Filler

A lightweight Python tool to parse public Google Forms and submit automated responses. Supports CLI and Streamlit web UI.

## Supported Question Types

- Short text
- Paragraph
- Radio buttons
- Dropdowns
- Checkboxes
- Linear scale

## Setup

```bash
pip install -r requirements.txt
```

## CLI Usage

```bash
# Parse form and preview a sample response (no submission)
python -m formbot.main --url "https://docs.google.com/forms/d/e/FORM_ID/viewform" --dry-run

# Submit 10 responses (default)
python -m formbot.main --url "https://docs.google.com/forms/d/e/FORM_ID/viewform"

# Submit 50 responses with custom delay
python -m formbot.main --url "https://docs.google.com/forms/d/e/FORM_ID/viewform" --count 50 --min-delay 2 --max-delay 5
```

### CLI Options

| Option | Default | Description |
|---|---|---|
| `--url` | *(required)* | Google Form URL |
| `--count` | 10 | Number of responses to submit |
| `--min-delay` | 1.5 | Minimum delay between submissions (seconds) |
| `--max-delay` | 4.0 | Maximum delay between submissions (seconds) |
| `--dry-run` | off | Parse and generate one sample without submitting |
| `--verbose` | off | Print detailed output |

## Streamlit UI

```bash
streamlit run streamlit_app.py
```

1. Enter a Google Form URL in the sidebar
2. Click **Parse Form** to extract questions
3. Click **Preview Sample** to see a generated response
4. Click **Submit Responses** to start batch submission with live progress

### Deploy on Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main file path to `streamlit_app.py`
4. Deploy

## Testing Without a Form

Use the included example fixture to test the generator offline:

```bash
python -c "
import json
from formbot.generator import generate_response

with open('tests/example_form.json') as f:
    questions = json.load(f)

for entry_id, value in generate_response(questions):
    print(f'  {entry_id} = {value}')
"
```

## Project Structure

```
├── streamlit_app.py       # Streamlit entry point (for deployment)
├── requirements.txt       # Dependencies
│
├── formbot/
│   ├── config.py          # Constants and type mapping
│   ├── parser.py          # Form HTML fetcher + question extractor
│   ├── generator.py       # Response generator (Faker + random)
│   ├── submitter.py       # POST submission engine with rate limiting
│   └── main.py            # CLI entry point
│
└── tests/
    └── example_form.json  # Sample form fixture for offline testing
```

## How It Works

1. Fetches the Google Form HTML page
2. Extracts the `FB_PUBLIC_LOAD_DATA_` JavaScript variable containing form metadata
3. Parses the nested structure to identify questions, types, entry IDs, and options
4. Generates realistic responses using Faker (text) and random selection (choices)
5. Submits via POST to the Google Forms `formResponse` endpoint with rate limiting

## Limitations

- Only works with **public** forms (no login required)
- Does not support multiple choice grid, file upload, or date/time question types
- Does not handle "Other" option fields
- High volume submissions may trigger rate limiting from Google
