from timings import time_it, logger

class QueryHandler:
    def __init__(self, db_manager):
        self.db = db_manager

    @time_it
    def handle(self, query, role, memory=None):
        try:
            role_access = {
                'public': ['public'],
                'private': ['public', 'private'],
                'individual': ['public', 'private', 'individual']
            }
            allowed_roles = role_access.get(role, ['public'])

            docs = self.db.search(query, role)
            print("documents:", docs)
            if not docs:
                return "Access Denied"
            
            # Filter documents based on access level
            filtered_docs = []
            for doc in docs:
                doc_role = doc.metadata.get('role', 'public')
                if doc_role in allowed_roles:
                    filtered_docs.append(doc)
            
            # if not filtered_docs:
            #     return self._get_access_denied_message(role)

            context = self._format_context(filtered_docs)
            
            # If memory is provided and has current_context, include it in the search
            if memory and hasattr(memory, 'current_context') and memory.current_context:
                context_docs = self.db.search(memory.current_context, role)
                filtered_memory_docs = [
                    doc for doc in context_docs 
                    if doc.metadata.get('role', 'public') in allowed_roles
                ]
                if filtered_memory_docs:
                    context += "\n\n" + self._format_context(filtered_memory_docs)
            
            logger.info(f"Handled query: '{query}' with {len(filtered_docs)} relevant docs")
            return context
        
        except Exception as e:
            logger.error(f"Error handling query: {str(e)}")
            return "An error occurred while processing your query."

    def _format_context(self, documents):
        context = []
        for doc in documents:
            context.append(f"Text: {doc.page_content}")
        return "\n\n".join(context)