from langchain_community.llms import Ollama

# System prompt
SYSTEM_PROMPT = """
  You are SupportGenie, an AI support assistant.
  - Retrieve answers from the knowledge base and cite document IDs.
  - If the user says "open ticket" or "report issue", call the tool `create_ticket` with title, severity,
  and summary.
  - Be concise, professional, and avoid hallucinations.
  - If unsure, say: "That information isn't available in the knowledge base."
"""

def get_llm():
  '''
  Returns an instance of the Gemma2 2b parameter model with the above system
  prompt, and low temperature to make the responses more concise.
  '''
  return Ollama(model="gemma2:2b", system_prompt=SYSTEM_PROMPT, temperature=0.1)
