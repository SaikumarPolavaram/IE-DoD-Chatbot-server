from timings import time_it, logger
from openai import OpenAI
from settings import Settings
import tiktoken
import time

class BudgetAnalystAgent:
    def __init__(self):
        self.client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        self.model = "gpt-4o"
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 4096  # Adjust as needed

    def respond(self, query, context, memory):
        """
        Generate a response for budget analysis queries, providing data from DoD Military Personnel budget tables.
        """
        prompt = self._create_base_prompt(query, context, memory)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert budget analyst for DoD Military Personnel budget reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()

    def _create_base_prompt(self, query, context, memory):
        # Custom prompt for extracting data from budget tables accurately
        return f"""
        Budget report context and tables:
        {context}

        Current question: {query}

        Guidelines:
        1. Answer directly without introductory phrases like 'based on the context'.
        2. Provide a clear, precise answer with relevant budget details, data, or figures.
        3. Focus on tables and ensure accuracy in rows and columns matching.
        4. Respond as a budget analyst without any references to being an AI.

        Context and memory details:
        Previous memory: {memory.get_context()}
        """

# Responder Class

class Responder:
    def __init__(self):
        self.agent = BudgetAnalystAgent()

    @time_it
    def respond(self, query, context, memory):
        max_retries = 3
        retry_delay = 10  # seconds

        for attempt in range(max_retries):
            try:
                answer = self.agent.respond(query, context, memory)
                logger.info(f"Generated response for: '{query}'")
                return answer.strip()
            except Exception as e:
                if "rate_limit_exceeded" in str(e).lower():
                    logger.error(f"Rate limit exceeded. Retrying {attempt+1}/{max_retries}...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Error occurred: {e}")
                    raise e

        raise Exception("Max retries reached. Could not generate a response.")


