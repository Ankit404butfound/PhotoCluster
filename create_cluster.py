import os
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from qdrant_client import QdrantClient

IMAGE_DIR = "/mnt/sda1/Documents/backup/my_phone/Camera"
COLLECTION = "photo_cluster"

client = QdrantClient(url="http://localhost:6333")

s = client.scroll(COLLECTION, limit=2000, with_vectors=True)

feat = []
img = []
for i in s[0]:
    feat.append(i.vector)
    img.append(i.payload["img_name"])


features = np.array(feat)

kmeans = KMeans(n_clusters=50)
normalized_features = normalize(features)
kmeans.fit(normalized_features)

groups = {}

for name, label in zip(img, kmeans.labels_.tolist()):
    if label not in groups:
        groups[label] = []
    groups[label].append(name)

for cluster, images in groups.items():
    cluster_dir = f"cluster_{cluster}"
    os.makedirs(cluster_dir, exist_ok=True)
    for image in images:
        try:
            os.symlink(
                os.path.join(IMAGE_DIR, image),
                os.path.join(cluster_dir, image),
            )
        except FileExistsError:
            pass

    
