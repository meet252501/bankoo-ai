import chromadb
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryVault:
    """
    Zenith v19: Local Vector Memory Vault.
    Uses ChromaDB to store and retrieve memories semanticly.
    100% Free & Local.
    """
    def __init__(self, db_dir="moltbot_memory"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.persist_directory = os.path.join(self.base_dir, db_dir)
        
        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory)

        # Initialize ChromaDB Local Client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Get or Create Collection
        self.collection = self.client.get_or_create_collection(
            name="bankoo_memories",
            metadata={"hnsw:space": "cosine"} # Use cosine similarity for semantic matching
        )
        logger.info(f"💾 [MEMORY-VAULT] Local Vault Active at {self.persist_directory}")

    def store_memory(self, text, metadata=None):
        """Stores a new memory chunk with metadata."""
        if not text: return
        
        timestamp = datetime.now().isoformat()
        if metadata is None:
            metadata = {}
        
        metadata["timestamp"] = timestamp
        
        # We use the text as ID if it's small, otherwise generate a unique one
        import hashlib
        mem_id = hashlib.md5(text.encode()).hexdigest()
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[mem_id]
        )
        logger.debug(f"💾 [MEMORY-VAULT] Memory Saved: {text[:50]}...")

    def retrieve_memories(self, query, top_k=3):
        """Retrieves top K most relevant memories for a query."""
        if not query: return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k
            )
            
            # Format results
            memories = []
            if results and results['documents']:
                for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                    memories.append({
                        "text": doc,
                        "timestamp": meta.get("timestamp", "Unknown")
                    })
            return memories
        except Exception as e:
            logger.error(f"💾 [MEMORY-VAULT] Retrieval failed: {e}")
            return []

# Singleton Instance
vault = MemoryVault()
