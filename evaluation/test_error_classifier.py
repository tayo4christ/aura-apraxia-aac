"""
Evaluate AURA's error-classification module using precision, recall,
F1-score, and a text-based confusion matrix.

Usage:
    python -m evaluation.test_error_classifier --csv path/to/results.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, List

from evaluation.text_confusion_matrix import confusion_matrix_to_text


LABELS = ["substitution", "omission", "distortion"]


def load_pairs(csv_path: Path) -> List[tuple[str, str]]:
    """
    Load (true_label, predicted_label) pairs from CSV.

    CSV format:
        true_label,predicted_label
    """
    pairs = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if (
            "true_label" not in reader.fieldnames
            or "predicted_label" not in reader.fieldnames
        ):
            raise ValueError("CSV must contain columns: true_label,predicted_label")
        for row in reader:
            pairs.append((row["true_label"], row["predicted_label"]))
    return pairs


def compute_confusion_matrix(
    pairs: List[tuple[str, str]], labels: List[str]
) -> List[List[int]]:
    label_to_idx = {label: i for i, label in enumerate(labels)}
    matrix = [[0 for _ in labels] for _ in labels]

    for true, pred in pairs:
        if true in label_to_idx and pred in label_to_idx:
            ti = label_to_idx[true]
            pi = label_to_idx[pred]
            matrix[ti][pi] += 1

    return matrix


def compute_precision_recall_f1(
    matrix: List[List[int]], labels: List[str]
) -> Dict[str, Dict[str, float]]:
    metrics = {}

    for i, label in enumerate(labels):
        tp = matrix[i][i]
        fp = sum(matrix[j][i] for j in range(len(labels)) if j != i)
        fn = sum(matrix[i][j] for j in range(len(labels)) if j != i)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )

        metrics[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }

    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate error classification metrics."
    )
    parser.add_argument(
        "--csv",
        type=Path,
        required=True,
        help="CSV with true_label and predicted_label columns.",
    )
    args = parser.parse_args()

    pairs = load_pairs(args.csv)
    if not pairs:
        raise SystemExit("No evaluation samples found in CSV.")

    matrix = compute_confusion_matrix(pairs, LABELS)
    metrics = compute_precision_recall_f1(matrix, LABELS)

    print("\n=== AURA Error Classification Evaluation ===")
    print(f"Samples: {len(pairs)}\n")

    # Print metrics per class
    for label in LABELS:
        m = metrics[label]
        print(
            f"{label.capitalize():<12} | P={m['precision']:.3f}  R={m['recall']:.3f}  F1={m['f1']:.3f}"
        )

    print("\nConfusion Matrix:")
    print(confusion_matrix_to_text(matrix, LABELS))


if __name__ == "__main__":
    main()
