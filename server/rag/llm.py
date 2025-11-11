from langchain_community.llms import Ollama

def get_llm():
  '''
  Returns an instance of the Gemma2 2b parameter model
  '''
  return Ollama(model="gemma2:2b")
