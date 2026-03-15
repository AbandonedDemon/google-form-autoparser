# Google Forms parser — extracts questions from public form URLs.

import re
import json
import requests

from formbot.config import QUESTION_TYPES, USER_AGENT, REQUEST_TIMEOUT


def fetch_form_html(url: str) -> str:
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        raise ValueError(f"Failed to fetch form: HTTP {resp.status_code}")
    html = resp.text
    if "freebirdFormviewerViewFormRequiresLogin" in html:
        raise ValueError("This form requires login and cannot be auto-parsed")
    return html


def extract_fb_data(html: str) -> list:
    match = re.search(
        r"FB_PUBLIC_LOAD_DATA_\s*=\s*(.+?)\s*;\s*</script>",
        html,
        re.DOTALL,
    )
    if not match:
        raise ValueError("Could not find FB_PUBLIC_LOAD_DATA_ in HTML")
    raw = match.group(1)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        cleaned = re.sub(r",\s*([}\]])", r"\1", raw)
        return json.loads(cleaned)


def parse_questions(fb_data: list) -> list[dict]:
    questions = []
    for q in fb_data[1][1]:
        try:
            title = q[1]
            type_code = q[3]
            entry_id = f"entry.{q[4][0][0]}"
            type_name = QUESTION_TYPES.get(type_code, "unknown")

            options = None
            scale_min = None
            scale_max = None

            try:
                raw_options = q[4][0][1]
                if raw_options:
                    options = [opt[0] for opt in raw_options]
            except (IndexError, TypeError):
                pass

            if type_code == 5 and options:
                scale_min = 1
                scale_max = len(options)

            questions.append({
                "question": title,
                "type": type_name,
                "type_code": type_code,
                "entry_id": entry_id,
                "options": options,
                "scale_min": scale_min,
                "scale_max": scale_max,
            })
        except (IndexError, TypeError, KeyError) as e:
            print(f"Warning: skipping unparseable question: {e}")
    return questions


def get_form_id(url: str) -> str:
    match = re.search(r"/d/e/([^/]+)", url)
    if not match:
        raise ValueError(f"Could not extract form ID from URL: {url}")
    return match.group(1)


def parse_form(url: str) -> tuple[str, list[dict]]:
    form_id = get_form_id(url)
    html = fetch_form_html(url)
    fb_data = extract_fb_data(html)
    questions = parse_questions(fb_data)
    return form_id, questions
