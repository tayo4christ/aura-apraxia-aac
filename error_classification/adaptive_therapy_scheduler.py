import csv
import random

# Define example exercises for each error type
EXERCISES = {
    0: ["Say 'cat'", "Say 'dog'", "Say 'ball'"],  # Normal: reinforce correct practice
    1: [
        "Say 'sunshine'",
        "Say 'hospital'",
        "Say 'calendar'",
    ],  # Omission: target multisyllabic
    2: [
        "Say 'fish'",
        "Say 'ship'",
        "Say 'cheese'",
    ],  # Substitution: target minimal pairs
}


def load_latest_predictions(csv_path):
    try:
        with open(csv_path, "r") as f:
            reader = list(csv.reader(f))[1:]  # skip header
            predictions = [int(row[2]) for row in reader if row]
            return predictions
    except Exception as e:
        print("Error reading predictions:", e)
        return []


def choose_adaptive_task(predictions):
    if not predictions:
        return "No recent predictions found. Default task: Say 'apple'."
    latest = predictions[-1]
    exercise = random.choice(EXERCISES.get(latest, ["Say 'apple'"]))
    return f"Suggested exercise based on last error type ({latest}): {exercise}"


if __name__ == "__main__":
    log_path = "adaptive_therapy_logs/speech_error_predictions.csv"
    preds = load_latest_predictions(log_path)
    task = choose_adaptive_task(preds)
    print("🧠 Adaptive Therapy Task:")
    print(task)
