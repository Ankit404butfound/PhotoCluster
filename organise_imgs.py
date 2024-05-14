import os
import json

IMAGE_DIR = "/mnt/sda1/Documents/backup/my_phone/Camera"

clusters = json.load(open("cluster.json"))
for cluster, images in clusters.items():
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