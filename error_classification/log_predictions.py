import torch
import csv
import os
from datetime import datetime
from error_classifier_model import get_model, generate_dummy_input

# Load model and simulate input
model = get_model()
input_tensor = generate_dummy_input()
output = model(input_tensor)
predicted = torch.argmax(output, dim=1)

# Write predictions to CSV
log_dir = "adaptive_therapy_logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "speech_error_predictions.csv")

with open(log_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Sample Index", "Predicted Class"])
    timestamp = datetime.now().isoformat()
    for i, label in enumerate(predicted.tolist()):
        writer.writerow([timestamp, i, label])

print(f"✅ Predictions logged to {log_file}")
