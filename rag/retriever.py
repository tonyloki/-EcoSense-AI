# Retrieval-Augmented Generation (RAG) implementation with FAISS
import os
import numpy as np
from pathlib import Path
from logger_config import logger

class PolicyRetriever:
    """
    Retrieve sustainability policies and documents using embedding-based search
    Implements RAG for policy-grounded recommendations
    """
    
    def __init__(self, knowledge_base_path=None):
        """
        Initialize policy retriever
        
        Args:
            knowledge_base_path: Path to policy documents
        """
        if knowledge_base_path is None:
            knowledge_base_path = os.path.join(
                os.path.dirname(__file__), 
                "policy_docs.txt"
            )
        
        self.kb_path = knowledge_base_path
        self.documents = self._load_documents()
        self.document_chunks = self._chunk_documents()
        
        # Try to import FAISS, fallback to simple search if unavailable
        try:
            import faiss
            self.faiss_available = True
            self._initialize_faiss()
        except ImportError:
            logger.warning("FAISS not available, using keyword-based retrieval")
            self.faiss_available = False
    
    def _load_documents(self):
        """Load knowledge base documents"""
        try:
            if os.path.exists(self.kb_path):
                with open(self.kb_path, 'r') as f:
                    return f.read()
            else:
                logger.warning(f"Knowledge base not found at {self.kb_path}")
                return ""
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return ""
    
    def _chunk_documents(self, chunk_size=500):
        """
        Split documents into chunks for better retrieval
        
        Args:
            chunk_size: Approximate size of each chunk
            
        Returns:
            List of document chunks
        """
        if not self.documents:
            return []
        
        chunks = []
        current_chunk = ""
        
        for sentence in self.documents.split('.'):
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += sentence + "."
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + "."
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _initialize_faiss(self):
        """Initialize FAISS index"""
        try:
            import faiss
            from sentence_transformers import SentenceTransformer
            
            # Use a lightweight model for embeddings
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create embeddings
            embeddings = self.embedding_model.encode(
                self.document_chunks,
                convert_to_numpy=True
            )
            
            # Initialize FAISS index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            logger.info("FAISS index initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize FAISS: {e}")
            self.faiss_available = False
    
    def retrieve(self, query, top_k=3):
        """
        Retrieve relevant policy documents based on query
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if self.faiss_available:
            return self._retrieve_with_faiss(query, top_k)
        else:
            return self._retrieve_with_keywords(query, top_k)
    
    def _retrieve_with_faiss(self, query, top_k=3):
        """Retrieve using FAISS embeddings"""
        try:
            query_embedding = self.embedding_model.encode([query])[0].astype('float32')
            distances, indices = self.index.search(
                np.array([query_embedding]), 
                min(top_k, len(self.document_chunks))
            )
            
            results = []
            for idx in indices[0]:
                if idx < len(self.document_chunks):
                    results.append(self.document_chunks[idx])
            
            return results
        except Exception as e:
            logger.error(f"Error in FAISS retrieval: {e}")
            return self._retrieve_with_keywords(query, top_k)
    
    def _retrieve_with_keywords(self, query, top_k=3):
        """Fallback keyword-based retrieval"""
        query_terms = query.lower().split()
        chunk_scores = []
        
        for chunk in self.document_chunks:
            score = sum(1 for term in query_terms if term in chunk.lower())
            if score > 0:
                chunk_scores.append((chunk, score))
        
        # Sort by relevance
        chunk_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [chunk for chunk, _ in chunk_scores[:top_k]]
    
    def augment_prompt(self, user_prompt, query_for_retrieval=None):
        """
        Combine user prompt with retrieved context (RAG)
        
        Args:
            user_prompt: Original user prompt
            query_for_retrieval: Query to use for retrieval (if different from prompt)
            
        Returns:
            Augmented prompt with retrieved context
        """
        retrieval_query = query_for_retrieval or user_prompt
        retrieved_context = self.retrieve(retrieval_query, top_k=3)
        
        if not retrieved_context:
            return user_prompt
        
        context_section = "\nRELEVANT SUSTAINABILITY GUIDELINES:\n"
        context_section += "\n".join([f"- {ctx}" for ctx in retrieved_context])
        
        augmented = f"""{user_prompt}

{context_section}

Please consider the above guidelines when formulating your response."""
        
        return augmented
    
    def get_policy_context(self, topic):
        """
        Get relevant policy context for a topic
        
        Args:
            topic: Sustainability topic
            
        Returns:
            String with relevant policies
        """
        retrieved = self.retrieve(topic, top_k=5)
        
        if not retrieved:
            return f"No specific policies found for '{topic}'"
        
        return "\n\n".join(retrieved)
    
    def search_policies(self, keyword):
        """
        Search for policies containing specific keywords
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching policy sections
        """
        results = []
        keyword_lower = keyword.lower()
        
        for chunk in self.document_chunks:
            if keyword_lower in chunk.lower():
                results.append(chunk)
        
        return results[:10]  # Return top 10 results
    
    def get_all_policies(self):
        """Get all policy documents"""
        return self.documents

class RAGAnalyzer:
    """
    Combine RAG retrieval with analysis for grounded insights
    """
    
    def __init__(self, knowledge_base_path=None):
        """Initialize RAG analyzer"""
        self.retriever = PolicyRetriever(knowledge_base_path)
    
    def ground_analysis_in_policies(self, analysis_data, analysis_type):
        """
        Ground analysis in sustainability policies
        
        Args:
            analysis_data: Analysis results
            analysis_type: 'electricity' or 'water'
            
        Returns:
            Policy-grounded analysis
        """
        if analysis_type == "electricity":
            query = "electricity efficiency energy consumption optimization"
        elif analysis_type == "water":
            query = "water conservation usage efficiency waste"
        else:
            query = "sustainability efficiency"
        
        policies = self.retriever.get_policy_context(query)
        
        grounded_analysis = f"""
ANALYSIS RESULTS:
{analysis_data}

POLICY-BASED FRAMEWORK:
{policies}

This analysis is grounded in established sustainability frameworks and best practices.
"""
        return grounded_analysis
