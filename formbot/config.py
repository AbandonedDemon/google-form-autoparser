# Question type mapping from Google Forms internal codes
QUESTION_TYPES = {
    0: "short_text",
    1: "paragraph",
    2: "radio",
    3: "dropdown",
    4: "checkbox",
    5: "linear_scale",
}

# Default CLI settings
DEFAULT_COUNT = 10
DEFAULT_MIN_DELAY = 1.5
DEFAULT_MAX_DELAY = 4.0

# HTTP settings
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 30

# Faker settings
FAKER_LOCALE = "en_US"
