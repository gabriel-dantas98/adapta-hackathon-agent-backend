"""
Embedding service for generating and caching vector embeddings.
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from functools import lru_cache
from langchain_openai import OpenAIEmbeddings
from langchain_core.embeddings import Embeddings
from ..core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for managing embeddings with OpenAI."""
    
    def __init__(self):
        """Initialize the embedding service."""
        self.openai_embeddings = OpenAIEmbeddings(
            model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
            dimensions=settings.embedding_dimensions
        )
        self.dimensions = settings.embedding_dimensions
        
        logger.info(f"EmbeddingService initialized with model: {settings.openai_model}")
    
    @property
    def embeddings(self) -> Embeddings:
        """Get the underlying embeddings instance."""
        return self.openai_embeddings
    
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: The text to embed
            
        Returns:
            List of floats representing the embedding
        """
        if not text.strip():
            logger.warning("Empty text provided for embedding")
            return [0.0] * self.dimensions
        
        try:
            # Generate embedding
            embedding = await self.openai_embeddings.aembed_query(text)
            logger.debug(f"Generated embedding for text: {text[:50]}...")
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embeddings
        """
        if not texts:
            return []
        
        try:
            embeddings = await self.openai_embeddings.aembed_documents(texts)
            logger.debug(f"Generated embeddings for {len(texts)} texts")
            return embeddings
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score between -1 and 1
        """
        import numpy as np
        
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        # Calculate dot product
        dot_product = np.dot(vec1_np, vec2_np)
        
        # Calculate magnitudes
        magnitude1 = np.linalg.norm(vec1_np)
        magnitude2 = np.linalg.norm(vec2_np)
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        # Calculate cosine similarity
        similarity = dot_product / (magnitude1 * magnitude2)
        
        return float(similarity)
    
    @staticmethod
    def combine_embeddings(embeddings: List[List[float]], weights: Optional[List[float]] = None) -> List[float]:
        """
        Combine multiple embeddings into a single embedding.
        
        Args:
            embeddings: List of embeddings to combine
            weights: Optional weights for each embedding
            
        Returns:
            Combined embedding
        """
        if not embeddings:
            return []
        
        import numpy as np
        
        embeddings_np = np.array(embeddings)
        
        if weights is None:
            # Simple average
            combined = np.mean(embeddings_np, axis=0)
        else:
            # Weighted average
            weights_np = np.array(weights)
            combined = np.average(embeddings_np, axis=0, weights=weights_np)
        
        return combined.tolist()
    
    async def semantic_search(
        self, 
        query_embedding: List[float], 
        candidate_embeddings: List[List[float]], 
        top_k: int = 5
    ) -> List[tuple]:
        """
        Perform semantic search using cosine similarity.
        
        Args:
            query_embedding: The query embedding
            candidate_embeddings: List of candidate embeddings
            top_k: Number of top results to return
            
        Returns:
            List of (index, similarity_score) tuples
        """
        if not candidate_embeddings:
            return []
        
        # Calculate similarities
        similarities = []
        for i, candidate_embedding in enumerate(candidate_embeddings):
            similarity = self.cosine_similarity(query_embedding, candidate_embedding)
            similarities.append((i, similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results
        return similarities[:top_k]
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Check the health of the embedding service.
        
        Returns:
            Health status information
        """
        try:
            # Test with a simple embedding
            test_embedding = await self.embed_text("health check")
            
            return {
                "status": "healthy",
                "model": settings.openai_model,
                "dimensions": self.dimensions,
                "test_embedding_length": len(test_embedding)
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "model": settings.openai_model,
                "dimensions": self.dimensions
            }

# Global embedding service instance
embedding_service = EmbeddingService() 
