# Scikit-Learn
from sklearn.cluster import KMeans
kmeans = KMeans() # Code smell
kmeans = KMeans(n_clusters=8, random_state=0) # No code smell

# PyTorch
from torch.optim import SGD
optimizer = SGD() # Code smell
optimizer = SGD(lr=0.01, momentum=0.9, weight_decay=0) # No code smell