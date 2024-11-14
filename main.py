from settings import Settings
from text_processor import FolderProcessor
from embedder import Embedder
from db_manager import DBManager
from query_handler import QueryHandler
from responder import Responder
from db_operations import DatabaseManager
from timings import logger
import time

class MemoryContext:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history
        self.current_context = None

    def add(self, question, answer):
        self.history.append((question, answer))
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def set_current_context(self, context):
        self.current_context = context

    def get_context(self):
        context = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])
        if self.current_context:
            context += f"\n\nCurrent context: {self.current_context}"
        return context

def setup():
    try:
        Settings.check()
        
        embedder = Embedder()
        public_db = DBManager(embedder,'dod_public')
        
        # Process new text files for public data
        new_documents_public = FolderProcessor.process_folder(Settings.PUBLIC_TEXT_FILES_FOLDER, 'public')
        if new_documents_public:
            public_db.add_docs(new_documents_public)
        else:
            logger.info("No new files to process.")

        public_query_handler = QueryHandler(public_db)
        
        
        # Process new text files for private data   
        private_db = DBManager(embedder,'dod_team')
        new_documents_private = FolderProcessor.process_folder(Settings.PRIVATE_TEXT_FILES_FOLDER, 'private')
        if new_documents_private:
            private_db.add_docs(new_documents_private)
        else:
            logger.info("No new files to process.")

        private_query_handler = QueryHandler(private_db)


        # Process new text files for individual data   
        individual_db = DBManager(embedder,'dod_personal')
        new_documents_individual = FolderProcessor.process_folder(Settings.INDIVIDUAL_TEXT_FILES_FOLDER, 'individual')
        if new_documents_individual:
            individual_db.add_docs(new_documents_individual)
        else:
            logger.info("No new files to process.")

        individual_query_handler = QueryHandler(individual_db)


        responder = Responder()
        memory = MemoryContext()
        
        # Initialize database
        db_manager = DatabaseManager()
        DatabaseManager.create_tables(db_manager.connection)
        DatabaseManager.update_knowledge_graphs(db_manager.connection)
        DatabaseManager.userproflie_list(db_manager.connection)
        logger.info("Setup complete")
        return public_query_handler, private_query_handler, individual_query_handler, responder, memory, db_manager
    
    except Exception as e:
        logger.error(f"Setup error: {str(e)}")
        raise

def run():
    try:
        public_query_handler, private_query_handler, individual_query_handler, responder, memory, db_manager = setup()
        
        while True:
            query = input("Ask a question (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            context = public_query_handler.handle(query, memory)
            
            answer = responder.respond(query, context, memory)
            print(f"Answer: {answer}")
            
            if "technical difficulties" not in answer and "unable to provide an answer" not in answer:
                memory.add(query, answer)
                memory.set_current_context(f"{query} - {answer[:100]}...")
                # Save chat history and update FAQ count
                db_manager.save_chat_history('console_user', query, answer)
                db_manager.update_faq_count(query, answer, 'console_user')
            else:
                print("Apologies for the inconvenience. Please wait a moment before asking another question.")
                time.sleep(10)  
    except Exception as e:
        logger.error(f"Runtime error: {str(e)}")
    finally:
        if db_manager:
            db_manager.close_connection()

if __name__ == "__main__":
    run()