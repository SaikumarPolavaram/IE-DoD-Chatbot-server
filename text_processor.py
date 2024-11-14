import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.document_loaders import CSVLoader
from PyPDF2 import PdfReader
from settings import Settings
from timings import time_it, logger

class TextProcessor:
    @staticmethod
    @time_it
    def process_text(file_path : str, role):
        try:
            csv = False
            if file_path.endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
            elif file_path.endswith('.pdf'):
                reader = PdfReader(file_path)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
            elif file_path.endswith('.csv'):
                loader = CSVLoader(file_path=file_path, encoding='utf-8')
                text = loader.load()
                csv = True
                
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=Settings.CHUNK_SIZE,
                chunk_overlap=Settings.CHUNK_OVERLAP,
                length_function=len,
            )

            if csv:
                documents = splitter.split_documents(text)
                for doc in documents:
                    doc.metadata.update({
                    "source": file_path,
                    "role": role
                    })
            else:
                chunks = splitter.split_text(text)
                documents = [Document(page_content=chunk, metadata={"source": file_path, 'role': role}) for chunk in chunks]
            
            logger.info(f"Processed {file_path} into {len(documents)} chunks")
            return documents
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return []
        

class FolderProcessor:
    @staticmethod
    @time_it
    def process_folder(folder_path, role):
        all_documents = []
        processed_files_path = os.path.join(folder_path, 'processed_files.txt')
        
        try:
            # Load processed files
            processed_files = set()
            if os.path.exists(processed_files_path):
                with open(processed_files_path, 'r') as f:
                    processed_files = set(f.read().splitlines())
            
            # Process new files
            new_files_processed = False
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                
                with open(processed_files_path, 'a') as f:
                    if filename.endswith('.txt') and filename != 'processed_files.txt' and file_path not in processed_files:
                        logger.info(f"Processing new file: {filename}")
                        documents = TextProcessor.process_text(file_path, role)
                        all_documents.extend(documents)
                        
                        # Mark file as processed
                        f.write(f"{file_path}\n")
                        new_files_processed = True

                    elif filename.endswith('.pdf') and filename != 'processed_files.txt' and file_path not in processed_files:
                        logger.info(f"Processing new file: {filename}")
                        documents = TextProcessor.process_text(file_path, role)
                        all_documents.extend(documents)
                        
                        # Mark file as processed
                        f.write(f"{file_path}\n")
                        new_files_processed = True
                    
                    elif filename.endswith('.csv') and filename != 'processed_files.txt' and file_path not in processed_files:
                        logger.info(f"Processing new file: {filename}")
                        documents = TextProcessor.process_text(file_path, role)
                        all_documents.extend(documents)
                        
                        # Mark file as processed
                        f.write(f"{file_path}\n")
                        new_files_processed = True

            if new_files_processed:
                logger.info(f"Processed new files in {folder_path}. Total new documents: {len(all_documents)}")

            return all_documents
        except Exception as e:
            logger.error(f"Error processing folder {folder_path}: {str(e)}")
            return []
        
