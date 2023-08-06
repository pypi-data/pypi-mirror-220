import torch
import torch.nn as nn


def train(model, data, labels):
    # Training code here...
    pass


def evaluate(model, data, labels):
    # Evaluation code here...
    pass


if __name__ == "__main__":
    # Use a built-in model from PyTorch
    model = nn.Sequential(
        nn.Linear(10, 5),
        nn.ReLU(),
        nn.Linear(5, 2)
    )

    # Train the model
    train_data = torch.randn(100, 10)
    train_labels = torch.randint(0, 2, (100,))
    model.train()  # Training mode
    train(model, train_data, train_labels)

    # Evaluate the model
    eval_data = torch.randn(50, 10)
    eval_labels = torch.randint(0, 2, (50,))
    model.eval()  # Evaluation mode
    evaluate(model, eval_data, eval_labels)

    # Forgot to toggle back to training mode
    train_data = torch.randn(100, 10)
    train_labels = torch.randint(0, 2, (100,))
    train(model, train_data, train_labels)  # Code smell: training without toggling back to training mode
