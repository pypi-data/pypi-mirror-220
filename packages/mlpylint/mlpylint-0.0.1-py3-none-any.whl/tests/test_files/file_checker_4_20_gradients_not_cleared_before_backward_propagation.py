import torch
import torch.nn as nn
import torch.optim as optim


class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.layer = nn.Linear(10, 1)

    def forward(self, x):
        return self.layer(x)


model = Model()
optimizer = optim.SGD(model.parameters(), lr=0.001)
loss_fn = nn.MSELoss()

inputs = torch.randn(10)
targets = torch.randn(1)

# Correct usage of gradient clearing
for _ in range(100):
    optimizer.zero_grad()  # Clear gradients
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    loss.backward()  # Backward propagation
    optimizer.step()  # Weight update

# Incorrect usage of gradient clearing - missing zero_grad()
for _ in range(100):
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    loss.backward()  # Backward propagation
    optimizer.step()  # Weight update

# Incorrect usage of gradient clearing - wrong order
for _ in range(100):
    optimizer.zero_grad()  # Clear gradients
    outputs = model(inputs)
    loss = loss_fn(outputs, targets)
    optimizer.step()  # Weight update
    loss.backward()  # Backward propagation
