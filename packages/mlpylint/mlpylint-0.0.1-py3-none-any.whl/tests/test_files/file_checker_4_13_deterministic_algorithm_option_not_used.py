import torch
import torch.nn as nn
import torch.optim as optim

# Correct usage: Setting deterministic algorithms during development

# Uncomment the two lines below to trigger code-smell
torch.use_deterministic_algorithms(mode=False)  # CODE_SMELL
torch.use_deterministic_algorithms(mode=True)


# Model definition
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.layer1 = nn.Linear(10, 5)
        self.layer2 = nn.Linear(5, 2)

    def forward(self, x):
        x = torch.relu(self.layer1(x))
        x = self.layer2(x)
        return x


# Training loop
def train(model, data_loader, epochs, device):
    model.train()
    optimizer = optim.SGD(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(epochs):
        for batch_idx, (data, target) in enumerate(data_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()


# Incorrect usage: Not setting deterministic algorithms during development
# Uncomment the following line to see the warning from the checker
torch.use_deterministic_algorithms(False)  # CODE_SMELL (if uncommented)

# Other scenarios

# Scenario: Deterministic algorithms are enabled, then disabled
torch.use_deterministic_algorithms(True)
torch.use_deterministic_algorithms(False)  # CODE_SMELL (deterministic setting toggled)


# Scenario: Deterministic algorithms setting is changed within a function
def change_deterministic_setting():
    torch.use_deterministic_algorithms(True)


change_deterministic_setting()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleModel().to(device)
dummy_data_loader = [(torch.randn(1, 10), torch.tensor([1])) for _ in range(10)]
train(model, dummy_data_loader, 5, device)
