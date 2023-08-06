import numpy.random
from torch.utils.data import DataLoader, TensorDataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Random Procedure Indicator
from numpy import random as np_random  # code smell indicator
from torch import rand as torch_rand  # code smell indicator
from random import random as py_random  # code smell indicator

# Importing random libraries
import numpy as np  # code smell indicator
import torch  # code smell indicator
import random  # code smell indicator

# Test random generation
# test_py_random = py_random()
# test_random = np_random.random()
# test_torch = torch_rand()

test_numpy_rand = np.random.rand()  # code smell indicator
test_py_random = random.random()    # code smell indicator
test_torch = torch.rand()           # code smell indicator

# np.random.seed(42)      # Required to avoid code smell
# torch.manual_seed(42)   # Required to avoid code smell
# random.seed(42)         # Required to avoid code smell

# Generator manual seed setup
# g = torch.Generator.manual_seed(0)  # code smell if not set

# Create a simple train dataset using random tensor
train_data = torch.randn(100, 3, 32, 32)  # 100 samples with shape (3, 32, 32)
train_labels = torch.randint(0, 10, (100,))  # 100 random labels in the range [0, 10)
train_dataset = TensorDataset(train_data, train_labels)

# Set batch_size
batch_size = 4

# Initialize DataLoader with generator
# seeder = torch.Generator().manual_seed(42)  # Manual seed set (Not a code smell)
dataloader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    num_workers=0,
)  # Code smell

# dataloader = DataLoader(
#     train_dataset,
#     batch_size=batch_size,
#     num_workers=0,
#     generator=seeder,
#     worker_init_fn=numpy.random.random(1)
# )  # Not Code smell

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split the dataset into a training set and a test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Create a RandomForestClassifier with a specified random_state for reproducibility
# random_forest = RandomForestClassifier(n_estimators=100, random_state=42)  # Not a code smell
random_forest = RandomForestClassifier(n_estimators=100)  # Code smell
