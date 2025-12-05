"""
RAG (Retrieval-Augmented Generation) Implementation
Uses OpenAI for embeddings and chat, Qdrant for vector storage
"""

from typing import List, Dict, Optional, Any
from pydantic import SecretStr
try:
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI  # type: ignore
    from langchain_qdrant import QdrantVectorStore  # type: ignore
    from langchain.text_splitter import RecursiveCharacterTextSplitter  # type: ignore
    from langchain.chains import ConversationalRetrievalChain  # type: ignore
    from langchain.memory import ConversationBufferMemory  # type: ignore
    from qdrant_client import QdrantClient  # type: ignore
    from qdrant_client.models import Distance, VectorParams  # type: ignore
except ImportError as e:
    print(f"Warning: Some dependencies not installed: {e}")
    print("Run: pip install -r requirements.txt")
import os


class RAGSystem:
    """
    Retrieval-Augmented Generation system for the textbook chatbot
    """
    
    def __init__(self):
        """Initialize RAG components"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            model=os.getenv("EMBEDDING_MODEL", "text-embedding-3-large"),
            api_key=SecretStr(self.openai_api_key) if self.openai_api_key else None
        )
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=self.qdrant_url,
            api_key=self.qdrant_api_key,
        )
        
        # Collection name for the book content
        self.collection_name = "physical_ai_robotics_book"
        
        # Initialize LLM for chat (using GPT-3.5-turbo for cost efficiency)
        self.llm = ChatOpenAI(
            model=os.getenv("CHAT_MODEL", "gpt-3.5-turbo"),
            temperature=0.7,
            api_key=SecretStr(self.openai_api_key) if self.openai_api_key else None
        )
        
        self.vector_store = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_names = [col.name for col in collections]
            
            if self.collection_name not in collection_names:
                # Create collection with proper vector configuration
                self.qdrant_client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=3072,  # text-embedding-3-large dimension
                        distance=Distance.COSINE
                    )
                )
                print(f"Created Qdrant collection: {self.collection_name}")
            
            # Initialize vector store
            self.vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.collection_name,
                embedding=self.embeddings
            )
            
        except Exception as e:
            print(f"Error initializing Qdrant collection: {e}")
    
    def index_documents(self, documents: List[Dict[str, str]]) -> int:
        """
        Index book chapters into vector database
        
        Args:
            documents: List of dicts with 'content', 'chapter', 'module' keys
            
        Returns:
            Number of documents indexed
        """
        if not self.vector_store:
            raise Exception("Vector store not initialized")
        
        # Text splitter for chunking
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            # Split document into chunks
            chunks = text_splitter.split_text(doc['content'])
            
            # Create metadata for each chunk
            for chunk in chunks:
                all_chunks.append(chunk)
                all_metadata.append({
                    'chapter': doc.get('chapter', 'Unknown'),
                    'module': doc.get('module', 'Unknown'),
                    'title': doc.get('title', '')
                })
        
        # Add to vector store
        self.vector_store.add_texts(
            texts=all_chunks,
            metadatas=all_metadata
        )
        
        return len(all_chunks)
    
    def query(
        self,
        question: str,
        context: Optional[str] = None,
        k: int = 4
    ) -> Dict[str, Any]:
        """
        Query the RAG system
        
        Args:
            question: User's question
            context: Optional selected text context
            k: Number of relevant chunks to retrieve
            
        Returns:
            Dict with answer and sources
        """
        if not self.vector_store:
            raise Exception("Vector store not initialized")
        
        # If user provided context (selected text), include it in the query
        enhanced_question = question
        if context:
            enhanced_question = f"Based on this context: '{context}'\n\nQuestion: {question}"
        
        # Retrieve relevant documents
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": k}
        )
        
        # Create conversational chain
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"  # Specify which output to save in memory
        )
        
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,  # type: ignore
            retriever=retriever,  # type: ignore
            memory=memory,
            return_source_documents=True
        )
        
        # Get answer
        result = qa_chain({"question": enhanced_question})
        
        # Extract source information
        sources = []
        for doc in result.get('source_documents', []):
            sources.append({
                'chapter': doc.metadata.get('chapter', 'Unknown'),
                'module': doc.metadata.get('module', 'Unknown'),
                'content_preview': doc.page_content[:200] + "..."
            })
        
        return {
            'answer': result['answer'],
            'sources': sources,
            'context_used': context is not None
        }
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the indexed content"""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            return {
                'total_documents': collection_info.points_count,
                'collection_name': self.collection_name,
                'status': 'ready'
            }
        except Exception as e:
            return {
                'total_documents': 0,
                'collection_name': self.collection_name,
                'status': 'error',
                'error': str(e)
            }


# Singleton instance
_rag_instance = None

def get_rag_system() -> RAGSystem:
    """Get or create RAG system singleton"""
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = RAGSystem()
    return _rag_instance
