"""
Utility for printing a text-based confusion matrix.

This version avoids any heavy plotting libraries so it runs anywhere,
including CI and simple CPU environments.
"""

from __future__ import annotations
from typing import List


def confusion_matrix_to_text(matrix: List[List[int]], labels: List[str]) -> str:
    """
    Convert a confusion matrix into a neatly formatted text table.

    Args:
        matrix: 2D list of confusion counts
        labels: class names in order

    Returns:
        Multiline formatted string.
    """
    col_widths = [max(len(label), 10) for label in labels]

    header = " " * 12 + "".join(
        f"{label:>{w+4}}" for label, w in zip(labels, col_widths)
    )

    rows = []
    for i, (row, label) in enumerate(zip(matrix, labels)):
        row_str = f"{label:<12}"
        for j, val in enumerate(row):
            w = col_widths[j]
            row_str += f"{val:>{w+4}}"
        rows.append(row_str)

    return header + "\n" + "\n".join(rows)
