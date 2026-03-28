from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):

    embeddings = model.encode(chunks)

    return embeddings
def build_vector_index(embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index
def retrieve_chunks(query, chunks, index, k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k)

    results = []

    for i in indices[0]:
        results.append(chunks[i])

    return results
