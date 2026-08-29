import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import json

class VectorStore:
    def __init__(self, index_path="database/faiss_index.bin", metadata_path="database/metadata.json"):
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = self.model.get_sentence_embedding_dimension()
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        
        self.metadata = []
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            self.index = faiss.read_index(index_path)
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)

    def add_texts(self, texts: list[str], metadatas: list[dict]):
        if not texts:
            return
        
        embeddings = self.model.encode(texts)
        faiss.normalize_L2(embeddings)
        self.index.add(np.array(embeddings).astype("float32"))
        
        self.metadata.extend(metadatas)
        
        # Save
        faiss.write_index(self.index, self.index_path)
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f)

    def search(self, query: str, k: int = 3):
        if self.index.ntotal == 0:
            return []
            
        query_embedding = self.model.encode([query])
        faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(np.array(query_embedding).astype("float32"), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "content": self.metadata[idx].get("content", ""),
                    "source": self.metadata[idx].get("source", "unknown"),
                    "score": float(distances[0][i])
                })
        return results

vector_store = VectorStore()
