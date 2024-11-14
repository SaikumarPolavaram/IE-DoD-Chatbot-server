import uuid
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from settings import Settings
from timings import logger, time_it
import pickle
import os

# class DBManager:
#     def __init__(self, embedder, index_file_name):
#         self.embedder = embedder
#         self.db_file = os.path.join(Settings.DB_FOLDER, index_file_name)
#         self.db = self._load_or_create_db()

#     def _load_or_create_db(self):
#         if os.path.exists(self.db_file):
#             try:
#                 with open(self.db_file, "rb") as f:
#                     db = pickle.load(f)
#                 logger.info("Loaded existing DB")
#                 return db
#             except Exception as e:
#                 logger.error(f"Error loading DB: {str(e)}")
        
#         logger.info("Creating new DB")
#         return self._create_db()

#     def _create_db(self):
#         dummy_texts = ["Dummy text for init"]
#         db = FAISS.from_texts(dummy_texts, self.embedder)
#         logger.info("Created new DB")
#         self._save_db(db)
#         return db

#     @time_it
#     def add_docs(self, documents):
#         if not documents:
#             logger.warning("No docs to add")
#             return
        
#         try:
#             texts = [doc.page_content for doc in documents]
#             metadatas = [doc.metadata for doc in documents]
#             self.db.add_texts(texts, metadatas=metadatas)
#             self._save_db(self.db)
#             logger.info(f"Added {len(documents)} docs to DB")
#         except Exception as e:
#             logger.error(f"Error adding docs to DB: {str(e)}")
#             raise

#     @time_it
#     def search(self, query, role, k=2):
#         try:
#             role_access = {
#                 'public': ['public'],
#                 'private': ['private', 'public'],
#                 'individual': ['individual', 'private', 'public']
#             }
#             allowed_roles = role_access.get(role, ['public'])
#             results = self.db.similarity_search(
#                 query,
#                 k=k,
#                 filter_fn=lambda doc: doc.metadata['role'] in allowed_roles
#             )
#             logger.info(f"Searched for: '{query}' with {role} access level")
#             return results
        
#         except Exception as e:
#             logger.error(f"Error searching DB: {str(e)}")
#             return []
    
#     def _save_db(self, db):
#         os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
#         try:
#             with open(self.db_file, "wb") as f:
#                 pickle.dump(db, f)
#             logger.info("DB saved")
#         except Exception as e:
#             logger.error(f"Error saving DB: {str(e)}")
#             raise

# Bharath code
class DBManager:
    def __init__(self, embedder, collection_name):
        self.embedder = embedder
        self.collection_name = collection_name
        self.client = self._get_client()

        # Check if collection exists; if not, create it
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
            logger.info("Created new DB")
            
    def _get_client(self):
        client = QdrantClient(url=Settings.QDRANT_URL, api_key=Settings.QDRANT_API_KEY, timeout=30, prefer_grpc=True)
        return client
       
 
    @time_it
    def add_docs(self, documents):
        if not documents:
            logger.warning("No docs to add")
            return
       
        try:
            points = []
            for doc in documents:
                embedding = self.embedder.embed_query(doc.page_content)
                point_id = str(uuid.uuid4())
                payload = {**doc.metadata, 'page_content':doc.page_content}
                points.append(
                    PointStruct(id=point_id, vector=embedding, payload=payload)
                )
           
            self._save_db(points)
            logger.info(f"Added {len(documents)} docs to Qdrant")
        except Exception as e:
            logger.error(f"Error adding docs to DB: {str(e)}")
            raise
 
    @time_it
    def search(self, query, role, k=4):
        try:
            embedding = self.embedder.embed_query(query)
           
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding, 
                limit=k,
                # query_filter={
                #     "must": [
                #         {"key": "role", "match": {"value": role}}
                #     ]
                # }
            )
            documents = [
                Document(
                    page_content=result.payload.get('page_content'), 
                    metadata={'role': result.payload.get('role'), 'source' : result.payload.get('source')}
                    ) 
                for result in results
            ]
            return documents
       
        except Exception as e:
            logger.error(f"Error searching DB: {str(e)}")
            return []
   
    # @time_it
    # def search(self, query, role=None, k=2):
    #     try:
            
    #         embedding = self.embedder.embed_query(query)
    #         search_result = self.client.search(
    #             collection_name=self.collection_name,
    #             query_vector=embedding,
    #             limit=k,
    #             # filter={"must": [{"key": "role", "match": {"value": role}}]}
    #         )
    #         print(search_result, '*'*30)
    #         logger.info(f"Searched Qdrant for: '{query}'")
    #         return [hit.payload for hit in search_result]
    #     except Exception as e:
    #         logger.error(f"Error searching Qdrant: {str(e)}")
    #         return []


    def _save_db(self, points):
        try:
            self.client.upsert(collection_name=self.collection_name, points=points)
            logger.info("DB saved")
        except Exception as e:
            logger.error(f"Error saving DB: {str(e)}")
            raise
 
