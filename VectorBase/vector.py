import re
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorDatabase:
    def __init__(self, model_name='all-MiniLM-L6-v2', index_path='vector_store.index', doc_path='documents.txt'):
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.doc_path = doc_path
        self.faiss_index = None
        self.documents = []

    def split_text_by_number(self, text):
        """将文本按数字分割成多个部分"""
        pattern = re.compile(r"\d{2}")
        sections = pattern.split(text)
        sections = sections[1:]  # 第一个元素是空的，因为它在第一个分隔符之前
        return sections

    def generate_vector_database(self, file_path):
        """生成向量数据库"""
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        texts = self.split_text_by_number(text)
        assert len(texts) == 64, f"Expected 64 sections, but got {len(texts)}"

        embeddings = self.model.encode(texts)

        dimension = embeddings.shape[1]
        self.faiss_index = faiss.IndexFlatL2(dimension)
        self.faiss_index.add(embeddings)

        # 保存FAISS索引
        faiss.write_index(self.faiss_index, self.index_path)

        # 保存分割后的文本数据
        with open(self.doc_path, "w", encoding='utf-8') as f:
            f.write("<seg>".join(texts))

    def load_vector_database(self):
        """读取向量数据库"""
        self.faiss_index = faiss.read_index(self.index_path)

        with open(self.doc_path, "r", encoding='utf-8') as f:
            self.documents = f.read().split("<seg>")

        assert len(self.documents) == 64, f"Expected 64 sections, but got {len(self.documents)}"

    def query(self, text, k=5):
        """查询相似文本块"""
        query_embedding = self.model.encode([text])
        distances, indices = self.faiss_index.search(query_embedding, k)
        results = [self.documents[idx] for idx in indices[0]]
        return results