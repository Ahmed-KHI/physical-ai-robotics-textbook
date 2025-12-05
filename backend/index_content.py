"""
Index book content to Qdrant vector database for RAG system.
Reads all markdown files from docs/, chunks them, and creates embeddings.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import re
from pydantic import SecretStr

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_openai import OpenAIEmbeddings
    from langchain_qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


class ContentIndexer:
    def __init__(
        self,
        openai_api_key: str,
        qdrant_url: str,
        qdrant_api_key: str,
        collection_name: str = "physical_ai_robotics_book"
    ):
        """Initialize the content indexer"""
        self.collection_name = collection_name
        self.qdrant_url = qdrant_url
        self.qdrant_api_key = qdrant_api_key
        
        # Initialize OpenAI embeddings
        self.embeddings = OpenAIEmbeddings(
            api_key=SecretStr(openai_api_key),
            model="text-embedding-3-large"
        )
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key
        )
        
        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n## ", "\n### ", "\n\n", "\n", " ", ""]
        )
    
    def read_markdown_files(self, docs_dir: str) -> List[Dict]:
        """Read all markdown files from docs directory"""
        docs_path = Path(docs_dir)
        documents = []
        
        for md_file in docs_path.rglob("*.md"):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract metadata from frontmatter
                metadata = self.extract_metadata(content)
                
                # Remove frontmatter from content
                content = self.remove_frontmatter(content)
                
                # Store document with metadata
                documents.append({
                    'content': content,
                    'metadata': {
                        **metadata,
                        'source': str(md_file.relative_to(docs_path.parent)),
                        'filename': md_file.name,
                        'module': self.extract_module(md_file)
                    }
                })
                
                print(f"✓ Read: {md_file.name}")
            
            except Exception as e:
                print(f"✗ Error reading {md_file}: {e}")
        
        return documents
    
    def extract_metadata(self, content: str) -> Dict:
        """Extract metadata from markdown frontmatter"""
        metadata = {}
        
        # Match YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            
            # Extract title
            title_match = re.search(r'title:\s*(.+)', frontmatter)
            if title_match:
                metadata['title'] = title_match.group(1).strip('"\'')
            
            # Extract sidebar_position
            pos_match = re.search(r'sidebar_position:\s*(\d+)', frontmatter)
            if pos_match:
                metadata['sidebar_position'] = int(pos_match.group(1))
        
        # Extract first heading as title if not in frontmatter
        if 'title' not in metadata:
            heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if heading_match:
                metadata['title'] = heading_match.group(1)
        
        return metadata
    
    def remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content"""
        return re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    def extract_module(self, file_path: Path) -> str:
        """Extract module name from file path"""
        parts = file_path.parts
        for part in parts:
            if part.startswith('module-'):
                return part
        
        if 'intro.md' in str(file_path):
            return 'introduction'
        elif 'hardware.md' in str(file_path):
            return 'hardware'
        elif 'setup.md' in str(file_path):
            return 'setup'
        elif 'faq.md' in str(file_path):
            return 'faq'
        
        return 'general'
    
    def create_collection(self):
        """Create Qdrant collection if it doesn't exist"""
        try:
            # Check if collection exists
            collections = self.qdrant_client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name in collection_names:
                print(f"Collection '{self.collection_name}' already exists. Deleting...")
                self.qdrant_client.delete_collection(self.collection_name)
            
            # Create new collection
            self.qdrant_client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=3072,  # text-embedding-3-large dimension
                    distance=Distance.COSINE
                )
            )
            print(f"✓ Created collection: {self.collection_name}")
        
        except Exception as e:
            print(f"✗ Error creating collection: {e}")
            raise
    
    def index_documents(self, documents: List[Dict]):
        """Chunk and index documents to Qdrant"""
        all_texts = []
        all_metadatas = []
        
        for doc in documents:
            # Split content into chunks
            chunks = self.text_splitter.split_text(doc['content'])
            
            for i, chunk in enumerate(chunks):
                all_texts.append(chunk)
                all_metadatas.append({
                    **doc['metadata'],
                    'chunk_id': i,
                    'total_chunks': len(chunks)
                })
        
        print(f"\n📊 Statistics:")
        print(f"  Documents: {len(documents)}")
        print(f"  Total chunks: {len(all_texts)}")
        print(f"  Avg chunks per doc: {len(all_texts) / len(documents):.1f}")
        
        # Create vector store and index
        print(f"\n🔄 Indexing to Qdrant...")
        try:
            vector_store = QdrantVectorStore.from_texts(
                texts=all_texts,
                embedding=self.embeddings,
                metadatas=all_metadatas,
                url=self.qdrant_url,
                api_key=self.qdrant_api_key,
                collection_name=self.collection_name,
                force_recreate=False
            )
            print(f"✓ Successfully indexed {len(all_texts)} chunks!")
            return vector_store
        
        except Exception as e:
            print(f"✗ Error indexing documents: {e}")
            raise
    
    def verify_index(self):
        """Verify that documents were indexed correctly"""
        try:
            collection_info = self.qdrant_client.get_collection(self.collection_name)
            point_count = collection_info.points_count
            print(f"\n✓ Verification: {point_count} points in collection")
            return point_count is not None and point_count > 0
        
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False


def main():
    """Main indexing function"""
    print("=" * 60)
    print("📚 Physical AI & Robotics Book - Content Indexer")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    # Validate
    if not all([openai_api_key, qdrant_url, qdrant_api_key]):
        print("\n❌ ERROR: Missing environment variables!")
        print("Required: OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY")
        print("\nPlease create backend/.env with these values.")
        sys.exit(1)
    
    # Type assertions after validation
    assert openai_api_key is not None
    assert qdrant_url is not None
    assert qdrant_api_key is not None
    
    # Initialize indexer
    indexer = ContentIndexer(
        openai_api_key=openai_api_key,
        qdrant_url=qdrant_url,
        qdrant_api_key=qdrant_api_key
    )
    
    # Get docs directory (parent of backend)
    backend_dir = Path(__file__).parent
    docs_dir = backend_dir.parent / "docs"
    
    if not docs_dir.exists():
        print(f"\n❌ ERROR: Docs directory not found: {docs_dir}")
        sys.exit(1)
    
    print(f"\n📂 Reading from: {docs_dir}")
    
    # Read documents
    documents = indexer.read_markdown_files(str(docs_dir))
    
    if not documents:
        print("\n❌ ERROR: No documents found!")
        sys.exit(1)
    
    # Create collection
    print(f"\n🗃️  Setting up Qdrant collection...")
    indexer.create_collection()
    
    # Index documents
    indexer.index_documents(documents)
    
    # Verify
    if indexer.verify_index():
        print("\n✅ SUCCESS! All content indexed.")
        print("\n📖 The chatbot can now answer questions about:")
        print("  • ROS 2 fundamentals")
        print("  • Gazebo & Unity simulation")
        print("  • NVIDIA Isaac platform")
        print("  • Vision-Language-Action models")
        print("  • Hardware requirements")
        print("  • Software setup")
    else:
        print("\n❌ Indexing verification failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
