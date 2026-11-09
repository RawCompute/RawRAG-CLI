import numpy as np
import os

class VectorMath:
    def __init__(self, index_path="rawrag_vectors.npy"):
        self.index_path = index_path
        # Load existing matrix from disk if it exists, otherwise start fresh
        if os.path.exists(self.index_path):
            self.matrix = np.load(self.index_path)
        else:
            self.matrix = None

    def add_vector(self, vector):
        if self.matrix is None:
            self.matrix = np.atleast_2d(vector)
        else:
            self.matrix = np.vstack([self.matrix, np.atleast_2d(vector)])
        return self.matrix.shape

    def search(self, query_vector, top_k=3):
        if self.matrix is None:
            return []
        
        q = np.array(query_vector)
        dot = np.dot(self.matrix, q)
        norm = np.linalg.norm(self.matrix, axis=1) * np.linalg.norm(q)
        
        # Avoid division by zero
        similarity = np.divide(dot, norm, out=np.zeros_like(dot), where=norm!=0)
        
        # Get top_k indices
        top_indices = np.argsort(similarity)[::-1][:top_k]
        return top_indices.tolist()

    def save_index(self):
        """Saves the NumPy matrix to disk."""
        if self.matrix is not None:
            np.save(self.index_path, self.matrix)