"""
Command-line utility to evaluate AURA's speech recognition outputs.

Usage:
    python -m evaluation.evaluate_speech_recognition \
        --csv path/to/results.csv

The CSV file is expected to have a header row with at least:
    reference,hypothesis

Where:
    - reference  = ground-truth transcription
    - hypothesis = model/system transcription

This script will compute:
    - Average Word Error Rate (WER)
    - Average Character Error Rate (CER)
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable, Tuple

from evaluation.metrics import (
    average_metric,
    character_error_rate,
    word_error_rate,
)


def load_pairs(csv_path: Path) -> Iterable[Tuple[str, str]]:
    """
    Load (reference, hypothesis) pairs from a CSV file.

    Args:
        csv_path: Path to a CSV file with 'reference' and 'hypothesis' columns.

    Yields:
        Tuples of (reference, hypothesis) strings.
    """
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if (
            "reference" not in reader.fieldnames
            or "hypothesis" not in reader.fieldnames
        ):
            raise ValueError(
                "CSV file must contain 'reference' and 'hypothesis' columns."
            )

        for row in reader:
            reference = row["reference"] or ""
            hypothesis = row["hypothesis"] or ""
            yield reference, hypothesis


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate speech recognition outputs using WER and CER.",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        required=True,
        help="Path to CSV file with 'reference' and 'hypothesis' columns.",
    )
    args = parser.parse_args()

    if not args.csv.exists():
        raise SystemExit(f"CSV file not found: {args.csv}")

    references: list[str] = []
    hypotheses: list[str] = []

    for ref, hyp in load_pairs(args.csv):
        references.append(ref)
        hypotheses.append(hyp)

    if not references:
        raise SystemExit("No rows found in CSV; nothing to evaluate.")

    avg_wer = average_metric(references, hypotheses, word_error_rate)
    avg_cer = average_metric(references, hypotheses, character_error_rate)

    print("=== AURA Speech Recognition Evaluation ===")
    print(f"Number of samples: {len(references)}")
    print(f"Average WER: {avg_wer:.4f}")
    print(f"Average CER: {avg_cer:.4f}")


if __name__ == "__main__":
    main()
