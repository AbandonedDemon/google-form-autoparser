# CLI entry point for Google Forms auto-filler.
import argparse
import sys

from formbot.parser import parse_form
from formbot.generator import generate_response
from formbot.submitter import submit_batch
from formbot.config import DEFAULT_COUNT, DEFAULT_MIN_DELAY, DEFAULT_MAX_DELAY


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Auto-fill Google Forms with generated responses.")
    p.add_argument("--url", required=True, help="Google Form URL")
    p.add_argument("--count", type=int, default=DEFAULT_COUNT, help=f"Number of responses (default: {DEFAULT_COUNT})")
    p.add_argument("--min-delay", type=float, default=DEFAULT_MIN_DELAY, help=f"Min delay between submissions in seconds (default: {DEFAULT_MIN_DELAY})")
    p.add_argument("--max-delay", type=float, default=DEFAULT_MAX_DELAY, help=f"Max delay between submissions in seconds (default: {DEFAULT_MAX_DELAY})")
    p.add_argument("--dry-run", action="store_true", help="Parse and generate one sample response without submitting")
    p.add_argument("--verbose", action="store_true", help="Print detailed output")
    return p


def main():
    args = create_parser().parse_args()

    print(f"Parsing form: {args.url}")
    try:
        form_id, questions = parse_form(args.url)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"Found {len(questions)} question(s):\n")
    for i, q in enumerate(questions, 1):
        line = f"  {i}. [{q['type']}] {q['question']}"
        if q["options"]:
            line += f"  ({len(q['options'])} options)"
        if q["scale_min"] is not None:
            line += f"  (scale {q['scale_min']}-{q['scale_max']})"
        print(line)
    print()

    if args.dry_run:
        print("--- Dry run: generating one sample response ---\n")
        sample = generate_response(questions)
        for entry_id, value in sample:
            print(f"  {entry_id} = {value}")
        print("\nNo submissions made.")
        return

    print(f"Submitting {args.count} response(s) with {args.min_delay}-{args.max_delay}s delay...\n")
    result = submit_batch(form_id, questions, args.count, args.min_delay, args.max_delay)
    print(f"\nDone: {result['success']} succeeded, {result['failed']} failed out of {result['total']}")


if __name__ == "__main__":
    main()
