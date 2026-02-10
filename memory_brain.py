import os
import chromadb
import logging
import uuid
from datetime import datetime
from chromadb.utils import embedding_functions

# Configure Logger
logger = logging.getLogger("memory-brain")
logger.setLevel(logging.INFO)

class MemoryBrain:
    """
    Bankoo's Long-Term Vector Memory using ChromaDB.
    Stores and retrieves semantic context from conversations and documents.
    """

    def __init__(self, db_path="bankoo_vector_db"):
        self.db_path = db_path
        
        try:
            # Initialize Persistent Chroma Client
            self.client = chromadb.PersistentClient(path=db_path)
            
            # Use Default Embedding Function (all-MiniLM-L6-v2 is standard and efficient)
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
            # Get or Create Collection
            self.collection = self.client.get_or_create_collection(
                name="bankoo_knowledge",
                embedding_function=self.embedding_fn
            )
            logger.info(f"🧠 Memory Brain initialized at {db_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {e}")
            self.client = None
            self.collection = None

    def add_memory(self, text, source="chat", metadata=None):
        """
        Stores a piece of information in the vector database.
        
        Args:
            text (str): The content to remember.
            source (str): Where it came from (chat, pdf, system).
            metadata (dict): Additional info (timestamp, user, etc).
        """
        if not self.collection:
            return False

        try:
            if metadata is None:
                metadata = {}
            
            # Enrich metadata
            metadata["source"] = source
            metadata["timestamp"] = datetime.now().isoformat()
            
            # Generate unique ID
            mem_id = str(uuid.uuid4())
            
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[mem_id]
            )
            logger.info(f"💾 Memory stored: {text[:30]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to add memory: {e}")
            return False

    def search_memory(self, query, n_results=3):
        """
        Retrieves semantically relevant memories.
        
        Args:
            query (str): The user's question or context.
            n_results (int): How many memories to retrieve.
            
        Returns:
            list: List of relevant text strings.
        """
        if not self.collection:
            return []

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Chroma returns dictionary with lists, we just want the documents
            if results and results['documents']:
                # Flatten the list of lists
                memories = results['documents'][0]
                logger.info(f"🔍 Found {len(memories)} relevant memories for '{query}'")
                return memories
            
            return []
            
        except Exception as e:
            logger.error(f"❌ Memory search failed: {e}")
            return []

    def count_memories(self):
        """Returns total number of memories stored."""
        if self.collection:
            return self.collection.count()
        return 0

# Global Instance
brain = MemoryBrain()
