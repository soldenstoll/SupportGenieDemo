from langchain_ollama import OllamaLLM

def get_llm():
  '''
  Returns an instance of the Gemma2 2b parameter model with low temperature to 
  make the responses more concise.
  '''
  return OllamaLLM(model="gemma2:2b", temperature=0.1)
