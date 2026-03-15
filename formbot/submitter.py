# POST submission engine for Google Forms auto-filler.
import time
import random
import requests
from formbot.config import USER_AGENT, REQUEST_TIMEOUT, DEFAULT_MIN_DELAY, DEFAULT_MAX_DELAY
from formbot.generator import generate_response


def build_submit_url(form_id: str) -> str:
    return f"https://docs.google.com/forms/d/e/{form_id}/formResponse"


def submit_response(session: requests.Session, submit_url: str, payload: list[tuple[str, str]]) -> bool:
    try:
        resp = session.post(submit_url, data=payload, timeout=REQUEST_TIMEOUT)
        return resp.status_code == 200
    except requests.RequestException:
        return False


def submit_batch(
    form_id: str,
    questions: list[dict],
    count: int,
    min_delay: float = DEFAULT_MIN_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
) -> dict:
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://docs.google.com/forms/d/e/{form_id}/viewform",
    })

    submit_url = build_submit_url(form_id)
    success = 0
    failed = 0

    for i in range(1, count + 1):
        payload = generate_response(questions)
        ok = submit_response(session, submit_url, payload)
        if ok:
            success += 1
        else:
            failed += 1
        print(f"[{i}/{count}] {'OK' if ok else 'FAILED'}")
        if i < count:
            time.sleep(random.uniform(min_delay, max_delay))

    return {"success": success, "failed": failed, "total": count}
