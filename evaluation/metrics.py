"""
Reusable evaluation metrics for AURA.

Includes:
- Word Error Rate (WER)
- Character Error Rate (CER)

These functions are model-agnostic and can be used across different
experiments (offline evaluation scripts, notebooks, etc.).
"""

from typing import Iterable, Sequence


def _edit_distance(reference: Sequence[str], hypothesis: Sequence[str]) -> int:
    """
    Compute Levenshtein edit distance between two token sequences.

    Uses a dynamic-programming implementation with O(len(ref) * len(hyp)) time.
    """
    m = len(reference)
    n = len(hypothesis)

    # dp[i][j] = distance between reference[:i] and hypothesis[:j]
    dp: list[list[int]] = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i  # deletions
    for j in range(n + 1):
        dp[0][j] = j  # insertions

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if reference[i - 1] == hypothesis[j - 1] else 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost,  # substitution
            )

    return dp[m][n]


def word_error_rate(reference: str, hypothesis: str) -> float:
    """
    Compute Word Error Rate (WER).

    WER = edit_distance(ref_words, hyp_words) / len(ref_words)

    Returns:
        A float in [0, +inf), where 0.0 means perfect match.
    """
    ref_tokens = reference.split()
    hyp_tokens = hypothesis.split()

    if not ref_tokens:
        # Define WER(∅, hyp) as 0.0 to avoid division by zero.
        return 0.0

    distance = _edit_distance(ref_tokens, hyp_tokens)
    return distance / len(ref_tokens)


def character_error_rate(reference: str, hypothesis: str) -> float:
    """
    Compute Character Error Rate (CER).

    CER = edit_distance(ref_chars, hyp_chars) / len(ref_chars)

    Returns:
        A float in [0, +inf), where 0.0 means perfect match.
    """
    ref_chars = list(reference)
    hyp_chars = list(hypothesis)

    if not ref_chars:
        return 0.0

    distance = _edit_distance(ref_chars, hyp_chars)
    return distance / len(ref_chars)


def average_metric(
    references: Iterable[str],
    hypotheses: Iterable[str],
    metric_fn,
) -> float:
    """
    Compute the average of a metric over multiple (ref, hyp) pairs.

    Args:
        references: iterable of reference strings.
        hypotheses: iterable of hypothesis strings.
        metric_fn: callable taking (reference, hypothesis) -> float.

    Returns:
        Mean metric value over all pairs. Returns 0.0 if there are no pairs.
    """
    total = 0.0
    count = 0

    for ref, hyp in zip(references, hypotheses):
        total += metric_fn(ref, hyp)
        count += 1

    if count == 0:
        return 0.0

    return total / count
