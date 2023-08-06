from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from .document import Paragraph
from .document import Document
import uuid

import qdrant_client.models as models


class SentenceTransformerModel:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode_questions(self, text):
        assert isinstance(text, list), "Parameter must be a list"
        return self.model.encode(text, show_progress_bar=True)

    def encode_paragraphs(self, text):
        assert isinstance(text, list), "Parameter must be a list"
        return self.model.encode(text, show_progress_bar=True)


class Database:
    """
    Manages a database of similar document parts
    """

    class SearchResult:
        def __init__(self, score, collection, text):
            self.score = float(score)
            self.collection = str(collection)
            self.text = str(text)

    def __init__(self, path, model=SentenceTransformerModel()):
        # Load a pre-trained Sentence Transformer model
        self.model = model
        self.qdrant = QdrantClient(path=path)

    def index(self, collection, obj):
        if isinstance(obj, Document):
            self.index_documents(collection, [obj])

    def index_documents(self, collection_name, docs):
        texts = []
        raw = []
        for doc in docs:
            texts.extend([x.preprocessed for x in doc.paragraphs])
            raw.extend([x.raw for x in doc.paragraphs])

        embeddings = self.model.encode_paragraphs(texts)

        vector_dim = len(embeddings[0])
        created = self.qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=vector_dim, distance=models.Distance.COSINE),
        )

        if not created:
            print(f"Collection '{collection_name}' already exists.")

        # Create a list of records to store in Qdrant
        records = []
        for idx, embedding in enumerate(embeddings):
            record = models.PointStruct(
                id=uuid.uuid1().int, vector=embedding.tolist(), payload={"text": raw[idx]}
            )
            records.append(record)

        # Store the records in Qdrant
        self.qdrant.upsert(collection_name=collection_name, points=records)

    @property
    def collections(self):
        return set([c.name for c in self.qdrant.get_collections().collections])

    def has_collection(self, name):
        return name in self.collections

    def drop_collections(self, collections):
        for c in collections:
            self.qdrant.delete_collection(collection_name=c)

    def search(self, query_text, top_k=20):
        query_text = Paragraph(query_text).preprocessed
        query_vector = self.model.encode_questions([query_text])[0]
        search_results = []
        for c in self.qdrant.get_collections().collections:
            res = self.qdrant.search(
                collection_name=c.name, query_vector=query_vector, limit=top_k
            )
            res = [self.SearchResult(r.score, c.name, r.payload["text"]) for r in res]
            search_results.extend(res)
        search_results.sort(key=lambda x: x.score, reverse=True)
        return search_results
