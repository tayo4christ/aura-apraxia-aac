import torch
import torch.nn as nn


class error_classifier_model(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(error_classifier_model, self).__init__()
        self.conv1 = nn.Conv1d(
            in_channels=input_dim, out_channels=64, kernel_size=3, padding=1
        )
        self.relu = nn.ReLU()
        self.lstm = nn.LSTM(
            input_size=64, hidden_size=hidden_dim, batch_first=True, bidirectional=True
        )
        self.fc = nn.Linear(hidden_dim * 2, output_dim)

    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = x.permute(0, 2, 1)
        _, (hn, _) = self.lstm(x)
        out = torch.cat((hn[0], hn[1]), dim=1)
        return self.fc(out)

    # error_classifier_model.py


def get_model():
    model = error_classifier_model(input_dim=13, hidden_dim=32, output_dim=3)
    return model


def generate_dummy_input():
    return torch.randn(8, 13, 100)  # batch of 8, 13 MFCCs, 100 time frames


if __name__ == "__main__":
    model = error_classifier_model(input_dim=13, hidden_dim=32, output_dim=3)
    dummy_input = torch.randn(8, 13, 100)
    output = model(dummy_input)
    print("Output shape:", output.shape)
