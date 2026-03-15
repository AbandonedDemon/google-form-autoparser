# Response generator — produces fake form payloads as list[tuple[str, str]].
import random

from faker import Faker

from formbot.config import FAKER_LOCALE

fake = Faker(FAKER_LOCALE)


def _generate_short_text(question):
    return [(question["entry_id"], fake.sentence())]


def _generate_paragraph(question):
    return [(question["entry_id"], fake.paragraph())]


def _generate_radio(question):
    return [(question["entry_id"], random.choice(question["options"]))]


def _generate_dropdown(question):
    return [(question["entry_id"], random.choice(question["options"]))]


def _generate_checkbox(question):
    options = question["options"]
    selected = random.sample(options, k=random.randint(1, len(options)))
    return [(question["entry_id"], value) for value in selected]


def _generate_linear_scale(question):
    value = str(random.randint(question["scale_min"], question["scale_max"]))
    return [(question["entry_id"], value)]


_GENERATORS = {
    "short_text": _generate_short_text,
    "paragraph": _generate_paragraph,
    "radio": _generate_radio,
    "dropdown": _generate_dropdown,
    "checkbox": _generate_checkbox,
    "linear_scale": _generate_linear_scale,
}


def generate_response(questions: list[dict]) -> list[tuple[str, str]]:
    payload: list[tuple[str, str]] = []
    for question in questions:
        qtype = question["type"]
        handler = _GENERATORS.get(qtype)
        if handler is None:
            print(f"Warning: unsupported question type '{qtype}', skipping.")
            continue
        payload.extend(handler(question))
    return payload
