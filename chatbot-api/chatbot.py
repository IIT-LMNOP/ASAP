# rag_service.py
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
from contextlib import asynccontextmanager
from bson.objectid import ObjectId


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlumniRAGService:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AlumniRAGService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Configuration from environment variables
        self.mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('DB_NAME', 'alumni_db')
        self.collection_name = os.getenv('COLLECTION_NAME', 'alumni')
        self.model_name = os.getenv('OLLAMA_MODEL', 'llama3:8b')
        self.embeddings_model = os.getenv('EMBEDDINGS_MODEL', 'sentence-transformers/all-MiniLM-L6-v2')
        
        # Initialize components
        self._initialize_mongodb()
        self._initialize_llm_and_embeddings()
        self._initialize_vectorstore()
        self._setup_conversation_chain()
        
        # Session store for conversations
        self.conversation_store = {}
        self.last_update = datetime.min
        
        self._initialized = True
        logger.info("Alumni RAG Service initialized successfully")
    
    def _initialize_mongodb(self):
        """Initialize MongoDB connection"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            # Test connection
            self.client.admin.command('ping')
            logger.info("MongoDB connection established")
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def _initialize_llm_and_embeddings(self):
        """Initialize LLM and embeddings"""
        try:
            self.llm = ChatOllama(model=self.model_name, temperature=0.3)
            self.embeddings = HuggingFaceEmbeddings(model_name=self.embeddings_model)
            logger.info("LLM and embeddings initialized")
        except Exception as e:
            logger.error(f"Failed to initialize LLM/embeddings: {e}")
            raise
    
    def _initialize_vectorstore(self):
        """Initialize or load vector store"""
        self.vectorstore_path = f"vectorstore_{self.collection_name}"
        
        if self._vectorstore_exists():
            logger.info("Loading existing vector store...")
            self.vectorstore = self._load_vectorstore()
        else:
            logger.info("Creating new vector store...")
            self.vectorstore = self._create_new_vectorstore()
        
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
    
    def _vectorstore_exists(self) -> bool:
        """Check if vector store files exist"""
        return (os.path.exists(f"{self.vectorstore_path}.faiss") and 
                os.path.exists(f"{self.vectorstore_path}.pkl"))
    
    def _load_vectorstore(self):
        """Load existing FAISS vector store"""
        try:
            return FAISS.load_local(
                self.vectorstore_path, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as e:
            logger.warning(f"Failed to load existing vector store: {e}")
            return self._create_new_vectorstore()
    
    def _create_new_vectorstore(self):
        """Create new FAISS vector store from MongoDB data"""
        documents = self._fetch_all_documents()
        if not documents:
            documents = ["No alumni data available."]
        
        vectorstore = FAISS.from_texts(documents, self.embeddings)
        self._save_vectorstore(vectorstore)
        return vectorstore
    
    def _save_vectorstore(self, vectorstore):
        """Save FAISS vector store to disk"""
        try:
            vectorstore.save_local(self.vectorstore_path)
            logger.info("Vector store saved successfully")
        except Exception as e:
            logger.error(f"Failed to save vector store: {e}")
    
    def _fetch_all_documents(self) -> List[str]:
        """Fetch all documents from MongoDB"""
        try:
            cursor = self.collection.find({})
            documents = []
            
            for doc in cursor:
                text_doc = self._convert_doc_to_text(doc)
                documents.append(text_doc)
            
            logger.info(f"Fetched {len(documents)} documents from MongoDB")
            return documents
        
        except Exception as e:
            logger.error(f"Error fetching documents: {e}")
            return []
    
    def _convert_doc_to_text(self, doc: Dict[str, Any]) -> str:
        """Convert MongoDB document to searchable text"""
        doc_copy = {k: v for k, v in doc.items() if k != '_id'}
        text_parts = []
        
        # Handle common alumni fields
        field_mappings = {
            'name': 'Name',
            'profession': 'Profession',
            'job_title': 'Job Title',
            'company': 'Company',
            'graduation_year': 'Graduated',
            'degree': 'Degree',
            'department': 'Department',
            'email': 'Email',
            'location': 'Location',
            'phone': 'Phone'
        }
        
        for field, label in field_mappings.items():
            if field in doc_copy:
                text_parts.append(f"{label}: {doc_copy[field]}")
        
        # Handle skills array
        if 'skills' in doc_copy:
            skills = doc_copy['skills']
            if isinstance(skills, list):
                skills = ', '.join(skills)
            text_parts.append(f"Skills: {skills}")
        
        # Handle any remaining fields
        handled_fields = set(field_mappings.keys()) | {'skills'}
        for key, value in doc_copy.items():
            if key not in handled_fields and not key.startswith('_'):
                text_parts.append(f"{key.replace('_', ' ').title()}: {value}")
        
        return ", ".join(text_parts)
    
    def _setup_conversation_chain(self):
        """Set up the conversational RAG chain"""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant for an Alumni Management System. 
            You help answer questions about alumni based on the available data.
            
            Guidelines:
            - Provide accurate information based only on the provided alumni data
            - Be helpful and conversational
            - If information is not available, clearly state that
            - Format responses in a clear and readable manner
            - When listing multiple alumni, organize the information clearly
            """),
            ("human", """
            Question: {question}
            
            Alumni Data:
            {data}
            
            Please answer the question based on the alumni data provided above.
            """)
        ])
        
        document_chain = create_stuff_documents_chain(
            self.llm,
            prompt,
            document_variable_name="data"
        )
        
        self.rag_chain = (
            {"question": lambda x: x["input"], "data": lambda x: self.retriever.invoke(x["input"])}
            | document_chain
        )
        
        self.conversational_chain = RunnableWithMessageHistory(
            self.rag_chain,
            self._get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )
    
    def _get_session_history(self, session_id: str):
        """Get or create session history"""
        if session_id not in self.conversation_store:
            self.conversation_store[session_id] = InMemoryChatMessageHistory()
        return self.conversation_store[session_id]
    
    def check_for_updates(self) -> bool:
        """Check if vector store needs updating"""
        # ... inside check_for_updates()
        try:
            latest_doc = list(self.collection.find().sort([
                ("updated_at", -1), ("created_at", -1), ("_id", -1)
            ]).limit(1))

            if not latest_doc:
                return False

            doc = latest_doc[0]
            
            # Try updated_at first, then created_at, then ObjectId generation_time
            current_timestamp = doc.get("updated_at")
            if not current_timestamp:
                current_timestamp = doc.get("created_at")
            if not current_timestamp and isinstance(doc["_id"], ObjectId):
                current_timestamp = doc["_id"].generation_time
            if not current_timestamp:
                logger.warning("No valid timestamp found in latest document")
                return False  # Can't determine update status

            if current_timestamp > self.last_update:
                self.last_update = current_timestamp
                return True

            return False

        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return False
        
    def update_vectorstore(self):
        try:
            logger.info("Updating vector store with latest data...")
            documents = self._fetch_all_documents()

            if not documents:
                logger.warning("No documents to index!")
                return False

            # Create new vectorstore safely
            new_vectorstore = FAISS.from_texts(documents, self.embeddings)
            temp_path = f"{self.vectorstore_path}_temp"

            # Save to temp path first
            new_vectorstore.save_local(temp_path)

            # Atomically replace
            if os.path.exists(f"{self.vectorstore_path}.faiss"):
                os.rename(f"{self.vectorstore_path}.faiss", f"{self.vectorstore_path}.faiss.bak")
            if os.path.exists(f"{self.vectorstore_path}.pkl"):
                os.rename(f"{self.vectorstore_path}.pkl", f"{self.vectorstore_path}.pkl.bak")

            os.rename(f"{temp_path}.faiss", f"{self.vectorstore_path}.faiss")
            os.rename(f"{temp_path}.pkl", f"{self.vectorstore_path}.pkl")

            # Update in-memory
            self.vectorstore = new_vectorstore
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
            self.last_update = datetime.now()  # Mark as updated

            logger.info("Vector store updated successfully")
            return True

        except Exception as e:
            logger.error(f"Error updating vector store: {e}")
            return False
        
    def add_alumni_and_embed(self, alumni_data: Dict[str, Any]) -> str:
        try:
            alumni_data['created_at'] = datetime.now()
            result = self.collection.insert_one(alumni_data)
            logger.info(f"Added alumni with ID: {result.inserted_id}")

            text_doc = self._convert_doc_to_text(alumni_data)
            self.vectorstore.add_texts([text_doc])

            # 🔥 CRITICAL: Rebuild retriever after adding texts!
            self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

            self._save_vectorstore(self.vectorstore)
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"Error adding alumni: {e}")
            raise
    
    def query_alumni(self, question: str, session_id: str = "default") -> Dict[str, Any]:
        try:
            if self.check_for_updates():
                self.update_vectorstore()

            response = self.conversational_chain.invoke(
                {
                    "input": question,
                    "chat_history": []  # ← This triggers the history system to record
                },
                config={"configurable": {"session_id": session_id}}
            )

            return {
                "success": True,
                "answer": str(response),
                "session_id": session_id
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "error": str(e),
                "answer": "Sorry, I encountered an error processing your question."
            }
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        try:
            if session_id not in self.conversation_store:
                return []
            
            history = self.conversation_store[session_id]
            messages = []
            
            for message in history.messages:
                content = message.content
                if not isinstance(content, str):
                    content = json.dumps(content, ensure_ascii=False)  # fallback
                messages.append({
                    "type": message.type,
                    "content": content
                })
            
            return messages
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
        
    def clear_conversation(self, session_id: str) -> bool:
        """Clear conversation history for a session"""
        try:
            if session_id in self.conversation_store:
                del self.conversation_store[session_id]
                logger.info(f"Cleared conversation for session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            return False
    
    def health_check(self) -> Dict[str, Any]:
        """Check if all services are healthy"""
        try:
            # Test MongoDB
            self.client.admin.command('ping')
            mongo_status = "healthy"
        except:
            mongo_status = "unhealthy"
        
        try:
            # Test vector store
            test_results = self.retriever.invoke("test")
            vectorstore_status = "healthy"
        except:
            vectorstore_status = "unhealthy"
        
        return {
            "mongodb": mongo_status,
            "vectorstore": vectorstore_status,
            "total_documents": self.collection.count_documents({}),
            "active_sessions": len(self.conversation_store)
        }

# Global service instance
rag_service = AlumniRAGService()