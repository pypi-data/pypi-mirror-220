import torch
import torch.nn as nn


class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(10, 5),
            nn.ReLU(),
            nn.Linear(5, 2),
        )

    def forward_pass(self, x):
        # Code smell: using self.net.forward() instead of self.net()
        output = self.net.forward(x)
        return output


def main():
    model = SimpleNet()
    x = torch.randn(1, 10)
    output = model.forward_pass(x)
    print(output)


if __name__ == "__main__":
    main()
