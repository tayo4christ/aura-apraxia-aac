import torch
import csv
from datetime import datetime
import os

# Simulate classifier output: batch of 8, 3-class logits
output = torch.randn(8, 3)

# Get predicted class labels (e.g., 0 = normal, 1 = omission, 2 = substitution)
predicted = torch.argmax(output, dim=1)

# Create a log directory if needed
log_dir = "adaptive_therapy_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "speech_error_predictions.csv")

# Write predictions to CSV
with open(log_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Sample Index", "Predicted Class"])
    timestamp = datetime.now().isoformat()
    for idx, label in enumerate(predicted.tolist()):
        writer.writerow([timestamp, idx, label])

print(f"✅ Predictions logged to {log_file}")
