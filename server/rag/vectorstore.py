from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.documents import Document
import json

# Persistent ChromaDB folder
CHROMA_DIR = "./db"

# Data location
DOCS_PATH = "./data/kb_seed/support_kb.json"

_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=_embeddings)

def query_db(query):
  '''
  Queries the db to retrieve top 3 most similar documents to the given query.
  Returns a list of the top 3 queries (sorted from most to least similar) in 
  a tuple of the form
  ({
    "id": id,
    "title": title,
    "content": content
  }, score)
  '''
  top3 = []
  results = _db.similarity_search_with_score(query, k=3)
  for doc, score in results:
      top3.append(({
        "id": doc.metadata["id"],
        "title": doc.metadata["title"],
        "content": doc.page_content
      }, score))

  return top3

def init_db():
  # Load data into db
  try:
    with open(DOCS_PATH, 'r') as f:
      data = json.load(f)

    # Parse data into docs
    docs = []
    for faq in data:
      doc = Document(
        page_content=faq["content"],
        metadata={
            "id": faq["id"],
            "title": faq["title"]
        }
      )

      docs.append(doc)

    # Add docs to our db
    _db.add_texts(docs)

  except FileNotFoundError:
    print(f"Error: The file '{DOCS_PATH}' was not found.")
  except json.JSONDecodeError:
      print(f"Error: Could not decode JSON from '{DOCS_PATH}'. Check if the file contains valid JSON.")
  except Exception as e:
      print(f"An unexpected error occurred: {e}")
