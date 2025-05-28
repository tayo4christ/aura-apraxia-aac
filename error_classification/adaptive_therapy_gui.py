import tkinter as tk
import csv
import random
import os
from datetime import datetime

# Define example tasks for each error class
EXERCISES = {
    0: ["Say 'cat'", "Say 'dog'", "Say 'ball'"],
    1: ["Say 'sunshine'", "Say 'hospital'", "Say 'calendar'"],
    2: ["Say 'fish'", "Say 'ship'", "Say 'cheese'"]
}

def load_latest_prediction(csv_path):
    try:
        with open(csv_path, "r") as f:
            reader = list(csv.reader(f))[1:]
            if not reader:
                return None
            last_row = reader[-1]
            return int(last_row[2])
    except Exception as e:
        print("Error reading predictions:", e)
        return None

def get_next_task():
    pred = load_latest_prediction("adaptive_therapy_logs/speech_error_predictions.csv")
    if pred is None:
        return "No prediction found. Please classify speech first."
    return random.choice(EXERCISES.get(pred, ["Say 'apple'"]))

# GUI setup
root = tk.Tk()
root.title("AURA Adaptive Therapy")
root.geometry("450x200")

title_label = tk.Label(root, text="🧠 Adaptive Speech Therapy", font=("Helvetica", 18, "bold"))
title_label.pack(pady=10)

task_label = tk.Label(root, text="Press 'Next Task' to begin...", font=("Helvetica", 14))
task_label.pack(pady=20)

def update_task():
    task = get_next_task()
    task_label.config(text=f"Suggested Task:{task}")

next_button = tk.Button(root, text="Next Task", font=("Helvetica", 12), command=update_task)
next_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", font=("Helvetica", 12), command=root.quit)
exit_button.pack()

root.mainloop()