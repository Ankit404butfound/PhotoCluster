from PIL import Image
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_openapi_client.models import VectorParams, Distance, Batch

import os
import secrets


IMAGE_DIR = "/mnt/sda1/Documents/backup/my_phone/Camera"
COLLECTION = "photo_cluster"

client = QdrantClient(url="http://localhost:6333")
model = SentenceTransformer("clip-ViT-B-32")

if not client.collection_exists(COLLECTION):
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )
else:
    print(client.scroll(
    collection_name=COLLECTION, 
    limit=10,
    with_payload=False, # change to True to see the payload
    with_vectors=False  # change to True to see the vectors
))
    client.delete_collection(COLLECTION)
    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )

images = os.listdir(IMAGE_DIR)
id_arr = []
vector_arr = []
payloads = []
counter = 1
for image in images:
    image_path = os.path.join(IMAGE_DIR, image)
    with Image.open(image_path) as img:
        vector = model.encode(img)
        id_arr.append(counter)
        vector_arr.append(vector)
        payloads.append(
            {
                "img_name": image,
                "hex": secrets.token_hex(16),
                "path": image_path,
            }
        )
        

        counter += 1
    if counter % 10 == 0:
        client.upsert(
            collection_name=COLLECTION,
            points=Batch(
                ids=id_arr,
                vectors=vector_arr,
                payloads=payloads
            )
        )
        id_arr = []
        vector_arr = []
        payloads = []
        print(f"Inserted {counter} out of {len(images)}")
        

